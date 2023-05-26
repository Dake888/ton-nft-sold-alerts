import requests
import json
import re

from tonsdk.utils import b64str_to_bytes, from_nano
from tonsdk.boc import Cell
from ton.utils import read_address

from config import getgems_api_url, getgems_query


async def get_nft_data(client, nft_address):
    try:
        response = await client.raw_run_method(address=nft_address,
                                               method='get_nft_data',
                                               stack_data=[])

        if response['exit_code'] == 0:
            init = bool(int(response['stack'][0][1], 16))
            index = int(response['stack'][1][1], 16)
            collection_address = read_address(Cell.one_from_boc(b64str_to_bytes(response['stack'][2][1]['bytes']))).to_string(True, True, True)
            owner_address = read_address(Cell.one_from_boc(b64str_to_bytes(response['stack'][3][1]['bytes']))).to_string(True, True, True)
            nft_content = Cell.one_from_boc(b64str_to_bytes(response['stack'][4][1]['bytes'])).bits.get_top_upped_array().decode().split('\x01')[-1]

            if nft_content == '':
                nft_content = b64str_to_bytes(response['stack'][4][1]['object']['refs'][-1]['data']['b64']).decode('utf-8')

            request_stack = [
                ["number", index],
                ["tvm.Cell", response['stack'][4][1]['bytes']]
            ]

            try:
                response = await client.raw_run_method(address=collection_address,
                                                       method='get_nft_content',
                                                       stack_data=request_stack)

                content = Cell.one_from_boc(b64str_to_bytes(response['stack'][0][1]['bytes'])).bits.get_top_upped_array().decode().split('\x01')[-1]
                content += nft_content

                if re.match(r'^ipfs', content):
                    metadata = requests.get(f'https://ipfs.io/ipfs/{content.split("ipfs://")[-1]}').json()
                else:
                    metadata = requests.get(f'{content}').json()

                nft_name = metadata['name']
                nft_image = metadata['image']

                return init, collection_address, owner_address, nft_name, nft_image

            except Exception as e:
                print(f'Error in Get NFT content method. Some problems with ({collection_address}) NFT collection. Check the logs:\n{e}')

    except Exception as e:
        print(f'Error in Get NFT data method. Some problems with ({nft_address}) NFT. Check the logs:\n{e}')


def get_collection_floor(col_address):
    try:
        json_data = {'operationName': 'nftSearch',
                     'query': getgems_query,
                     'variables': {
                         'count': 30,
                         'query': '{"$and":[{"collectionAddress":"' + col_address + '"}]}',
                         'sort': '[{"isOnSale":{"order":"desc"}},{"price":{"order":"asc"}},{"index":{"order":"asc"}}]'}
                     }

        data = json.loads(requests.post(getgems_api_url,
                                        json=json_data).text)['data']['alphaNftItemSearch']['edges']

        for item in data:
            if 'fullPrice' not in item['node']['sale']:
                continue

            floor_price = from_nano(int(item['node']['sale']['fullPrice']), 'ton')
            floor_link = item['node']['address']

            return floor_price, floor_link

    except Exception as e:
        print(f'Error in Get collection floor method. Some problems with ({col_address}) NFT collection. Check the logs:\n{e}')
