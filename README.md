# ton-nft-sold-alerts
A simple bot for tracking sold NFTs from the collections you are interested in on the TON blockchain, which works not only on the principle of scanning collections royalty wallets, but also on commission-free marketplaces (for example, Tonex).

_**The bot will be useful for those who want to set up monitoring of NFTs that have been sold in the collections you are interested in recently, by any possible means: simple sale, auction sale, order sale, sale on the commission-free marketplace.
Information about sold NFTs will be sent to your Telegram group.
Continue to improve the user experience of your NFT project by adding a sell-alerts tracking bot using code available at the [link](https://github.com/Dake888/ton-nft-sell-alerts)!**_

The part responsible for scanning the addresses of collections royalty and addresses of commission-free marketplaces works asynchronously, which allows you to receive notifications very quickly.

The code uses public modules for TON: [pytonlib by toncenter](https://github.com/toncenter/pytonlib), [pytonlib by psylopunk](https://github.com/psylopunk/pytonlib), [tonsdk](https://github.com/tonfactory/tonsdk).
The code works without using public api to get information about NFT.

## Quick start

Before you start working with the bot, you should make sure that all modules from **requirements.txt** installed in your environment.
An easy way to quickly install all requirements: `pip install -r /path/to/requirements.txt`

You will also need to fill out a **secretData.py** with your token data.
```
bot_token = ''
cmc_token = ''
notify_chat = ''
```

### Configure your parameters in the config.py:
1. **Select the royalty addresses of NFT collections and commission-free NFT marketplaces to track by changing the royalty_addresses list.** You can also add several commission-free NFT marketplaces for scanning (if any appear in TON) if it receives a transaction from the NFT sale contract of the collection you are interested in upon successful sale of NFT.
2. **Select the addresses of NFT collections to track by changing the collections_list list.**
3. **Select the transaction limit to get from the get_transactions method by changing the trs_limit variable (optional).** Can be increased if your code doesn't run very often.
4. **Select the get methods to get data from sale contacts to calculate by changing the get_methods list (optional).** Can be increased if your code doesn't run very often. For example, if you do not want to receive information from sales contracts through an auction.

_Was the bot helpful to you? I am very happy, if it is ^^_

_For donations - EQC7QQ4yZGuNr-qJYOcg-w8hP7EdF29rok-d84fXTKRuUq0-_