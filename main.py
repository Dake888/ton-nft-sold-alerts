import requests
import asyncio

from pathlib import Path
from pytonlib import TonlibClient

from config import current_path, ton_config_url, royalty_addresses, get_methods, trs_limit, collections_list
from functions import parse_sale_stack
from nftData import get_nft_data, get_collection_floor
from tgMessage import tg_message


async def get_client():
    config = requests.get(ton_config_url).json()
    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True,
                             exist_ok=True)

    client = TonlibClient(ls_index=2,
                          config=config,
                          keystore=keystore_dir,
                          tonlib_timeout=10)
    await client.init()

    return client


async def royalty_trs(royalty_address):
    utimes = list()
    last_utime = int(open(f'{current_path}/lastUtime', 'r').read())

    client = await get_client()

    try:
        trs = await client.get_transactions(account=royalty_address,
                                            limit=trs_limit)

    except Exception as e:
        print(f'Get Request for ({royalty_address}) address Failed! Check the logs\n{e}\n\n')

    if trs is not None:
        for tr in trs[::-1]:
            sc_address = tr['in_msg']['source']

            if tr['utime'] <= last_utime or tr['in_msg']['source'] == '':
                continue

            for method in get_methods:

                try:
                    response = await client.raw_run_method(address=sc_address,
                                                           method=method,
                                                           stack_data=[])

                except Exception as e:
                    print(
                        f'Error in raw run ({method}) method. Some problems with ({sc_address}) NFT sale contract. Check the logs:\n{e}')

                if response is not None and response['exit_code'] == 0:
                    sale_contract_data = parse_sale_stack(response['stack'])

                    if sale_contract_data is not None and sale_contract_data[1]:
                        sale_nft_data = await get_nft_data(client, sale_contract_data[4])

                        if sale_nft_data is not None and sale_nft_data[1] in collections_list and sale_nft_data[0]:
                            collection_floor_data = get_collection_floor(sale_nft_data[1])

                            if sale_contract_data[0] == 'SaleFixPrice':
                                tg_message(sale_contract_data[0], sale_contract_data[3], sale_contract_data[4],
                                           sale_contract_data[5], sale_nft_data[2], sale_contract_data[6],
                                           sale_nft_data[3], sale_nft_data[4], collection_floor_data[0],
                                           collection_floor_data[1])

                            elif sale_contract_data[0] == 'SaleAuction':
                                tg_message(sale_contract_data[0], sale_contract_data[3], sale_contract_data[4],
                                           sale_contract_data[5], sale_nft_data[2], sale_contract_data[11],
                                           sale_nft_data[3], sale_nft_data[4], collection_floor_data[0],
                                           collection_floor_data[1])

                            elif sale_contract_data[0] == 'SaleOffer':
                                tg_message(sale_contract_data[0], sale_contract_data[3], sale_contract_data[4],
                                           sale_contract_data[5], sale_nft_data[2], sale_contract_data[6],
                                           sale_nft_data[3], sale_nft_data[4], collection_floor_data[0],
                                           collection_floor_data[1])

                            utimes.append(tr['utime'])

    await client.close()

    try:
        return utimes[-1]
    except:
        pass


async def scheduler():
    while True:
        utimes = await asyncio.gather(*map(royalty_trs, royalty_addresses))
        utimes = list(filter(None, utimes))
        try:
            if len(utimes) > 0:
                open(f'{current_path}/lastUtime', 'w').write(str(max(utimes)))
        except:
            pass

        await asyncio.sleep(15)


if __name__ == '__main__':
    asyncio.run(scheduler())
