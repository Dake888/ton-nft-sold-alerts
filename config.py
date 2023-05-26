import telepot
import pathlib

from secretData import *

bot = telepot.Bot(bot_token)
current_path = pathlib.Path(__file__).parent.resolve()

trs_limit = 50

royalty_addresses = [#'EQAA4W2tr6JdJsyej6Ix5tckcwsiRwWmLuI67Tznj1JlaP4X',  # Toned Ape Club!
                     #'EQCgRvXbOJeFSRKnEg1D-i0SqDMlaNVGvpSSKCzDQU_wDAR4',  # Tonex
                     ]

collections_list = [#'EQCzuSjkgUND61l7gIH3NvVWNtZ0RX1hxz1rWnmJqGPmZh7S',  # Toned Ape Club!
                    ]

ton_config_url = 'https://ton.org/global-config.json'
tonorg_price_url = 'https://ton.org/getpriceg/'
tonapi_url = 'https://tonapi.io/v1/'
getgems_api_url = 'https://api.getgems.io/graphql'
getgems_user_url = 'https://getgems.io/user/'
cmc_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

get_methods = ['get_sale_data',
               'get_offer_data']

markets = {
           'EQBYTuYbLf8INxFtD8tQeNk5ZLy-nAX9ahQbG_yl1qQ-GEMS': 'Getgems',
           'EQCjc483caXMwWw2kwl2afFquAPO0LX1VyZbnZUs3toMYkk9': 'Getgems',
           'EQCgRvXbOJeFSRKnEg1D-i0SqDMlaNVGvpSSKCzDQU_wDAR4': 'Tonex',
           'EQDrLq-X6jKZNHAScgghh0h1iog3StK71zn8dcmrOj8jPWRA': 'Disintar',
           'EQAezbdnLVsLSq8tnVVzaHxxkKpoSYBNnn1673GXWsA-Lu_w': 'Diamonds',
          }

markets_links = {
                 'Getgems': 'https://getgems.io/nft/',
                 'Tonex': 'https://tonex.app/nft/market/nfts/',
                 'Disintar': 'https://beta.disintar.io/object/',
                 'Diamonds': 'https://ton.diamonds/explorer/',
                }

getgems_query = "query nftSearch($count: Int!, $cursor: String, $query: String, $sort: String) " \
                "{\n  alphaNftItemSearch(first: $count, after: $cursor, query: $query, sort: $sort) " \
                "{\n    edges {\n      node {\n        ...nftPreview\n        __typename\n      }" \
                "\n      cursor\n      __typename\n    }\n    info {\n      hasNextPage\n      __typename\n    }" \
                "\n    __typename\n  }\n}\n\nfragment nftPreview on NftItem {\n  name\n  previewImage: content " \
                "{\n    ... on NftContentImage {\n      image {\n        sized(width: 500, height: 500)" \
                "\n        __typename\n      }\n      __typename\n    }\n    ... on NftContentLottie " \
                "{\n      lottie\n      fallbackImage: image {\n        sized(width: 500, height: 500)" \
                "\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  address\n  collection " \
                "{\n    name\n    address\n    __typename\n  }\n  sale {\n    ... on NftSaleFixPrice " \
                "{\n      fullPrice\n      __typename\n    }\n    __typename\n  }\n  __typename\n}"

cmc_params = {'slug': 'toncoin',
              'convert': 'USD'}

cmc_headers = {'Accepts': 'application/json',
               'X-CMC_PRO_API_KEY': cmc_token}
