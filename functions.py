import requests
import json

from tonsdk.utils import from_nano, b64str_to_bytes
from ton.utils import read_address
from tonsdk.boc import Cell

from config import tonorg_price_url, cmc_url, cmc_params, cmc_headers


def parse_sale_stack(stack):
    try:
        if stack[0][1] == '0x415543':
            return parse_auction_stack(stack)
        if stack[0][1] == '0x4f46464552':
            return parse_offer_stack(stack)
        action = 'SaleFixPrice'
        is_complete = bool(int(stack[1][1], 16))
        created_at = int(stack[2][1], 16)
        marketplace_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[3][1]['bytes']))).to_string(True, True, True)
        nft_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[4][1]['bytes']))).to_string(True, True, True)
        try:
            nft_owner_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[5][1]['bytes']))).to_string(True, True, True)
        except:
            nft_owner_address = None
        full_price = from_nano(int(stack[6][1], 16), 'ton')

        return action, is_complete, created_at, marketplace_address, nft_address, nft_owner_address, full_price

    except:
        print(f'Some problem has been found in the stack of the get contract method.'
              f'\nStart the method of parsing a brock stack...')
        return parse_broke_stack(stack)


def parse_auction_stack(stack):
    action = 'SaleAuction'
    is_end = bool(int(stack[1][1], 16))
    created_at = int(stack[17][1], 16)
    marketplace_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[3][1]['bytes']))).to_string(True, True, True)
    nft_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[4][1]['bytes']))).to_string(True, True, True)
    nft_owner_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[5][1]['bytes']))).to_string(True, True, True)
    min_bid = from_nano(int(stack[16][1], 16), 'ton')
    max_bid = from_nano(int(stack[15][1], 16), 'ton')
    min_step = from_nano(int(stack[8][1], 16), 'ton')
    last_bid_at = int(stack[18][1], 16)
    last_member = read_address(Cell.one_from_boc(b64str_to_bytes(stack[7][1]['bytes'])))
    if last_member is not None:
        last_member = last_member.to_string(True, True, True)
    last_bid = from_nano(int(stack[6][1], 16), 'ton')
    is_canceled = bool(int(stack[19][1], 16))
    end_time = int(stack[2][1], 16)

    return action, is_end, created_at, marketplace_address, nft_address, nft_owner_address, min_bid, max_bid, \
        min_step, last_bid_at, last_member, last_bid, is_canceled, end_time


def parse_offer_stack(stack):
    action = 'SaleOffer'
    is_complete = bool(int(stack[1][1], 16))
    created_at = int(stack[2][1], 16)
    marketplace_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[4][1]['bytes']))).to_string(True, True, True)
    nft_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[5][1]['bytes']))).to_string(True, True, True)
    offer_owner_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[6][1]['bytes']))).to_string(True, True, True)
    full_price = from_nano(int(stack[7][1], 16), 'ton')

    return action, is_complete, created_at, marketplace_address, nft_address, offer_owner_address, full_price


def parse_broke_stack(stack):
    try:
        action = 'SaleFixPrice'
        marketplace_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[0][1]['bytes']))).to_string(True, True, True)
        nft_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[1][1]['bytes']))).to_string(True, True, True)
        nft_owner_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[2][1]['bytes']))).to_string(True, True, True)
        full_price = from_nano(int(stack[3][1], 16), 'ton')

        return action, True, None, marketplace_address, nft_address, nft_owner_address, full_price

    except Exception as e:
        print(f'Broke stack parsing Failed.'
              f'Check the logs!\n\nError: {e}\n')


def convert_ton_to_usd_old(ton):
    try:
        usd = json.loads(requests.get(tonorg_price_url).text)['the-open-network']['usd']
        usd_price = round(float(ton) * usd, 2)
        return usd_price

    except Exception as e:
        print(f'Error in Convert ton to usd (old) method. Check the logs:\n{e}')


def convert_ton_to_usd(ton):
    try:
        session = requests.Session()
        session.headers.update(cmc_headers)

        usd = json.loads(session.get(cmc_url, params=cmc_params).text)['data']['11419']['quote']['USD']['price']
        usd_price = round(float(ton) * usd, 2)

        return usd_price

    except Exception as e:
        print(f'Error in Convert ton to usd method. Check the logs:\n{e}')
        print(f'Try to convert with old method...')
        convert_ton_to_usd_old(ton)
