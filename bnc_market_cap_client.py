import requests
import json
import csv
from datetime import date

BNC_AUTH_URL = 'https://api.bravenewcoin.com/v3/oauth/token'
BNC_MARKET_CAP_URL = 'https://api.bravenewcoin.com/v3/market-cap'
BNC_ASSET_URL = 'https://api.bravenewcoin.com/v3/asset'

bnc_id_symbol_map = {}
asset_res = requests.get(url=BNC_ASSET_URL)
for asset in json.loads(asset_res.content).get('content'):
    bnc_id_symbol_map[asset.get('id')] = (asset.get('symbol'), asset.get('name'))

# Get access token from BNC AUTH API
auto_req_body = {
    "grant_type": "client_credentials",
    "client_id": "<YOUR_AUTH_CLIENT_ID>",
    "client_secret": "<YOUR_AUTH_CLIENT_SECRET>",
    "audience": "https://api.bravenewcoin.com"
}

auth_res = requests.post(url=BNC_AUTH_URL, json=auto_req_body, headers={'content-type': 'application/json'})
access_token = json.loads(auth_res.content).get('access_token')

market_cap_list = [('id', 'assetId', 'symbol', 'name', 'timestamp', 'marketCapRank', 'volumeRank', 'price', 'volume',
                    'totalSupply', 'freeFloatSupply', 'marketCap', 'totalMarketCap')]
if access_token is not None:
    market_cap_rep = requests.get(url=BNC_MARKET_CAP_URL, headers={'Authorization': 'Bearer ' + access_token})
    bnc_supplies = json.loads(market_cap_rep.content).get('content')
    for bnc_supply in bnc_supplies:
        market_cap_list.append((bnc_supply.get('id'), bnc_supply.get('assetId'),
                                bnc_id_symbol_map.get(bnc_supply.get('assetId'))[0],
                                bnc_id_symbol_map.get(bnc_supply.get('assetId'))[1], bnc_supply.get('timestamp'),
                                bnc_supply.get('marketCapRank'), bnc_supply.get('volumeRank'), bnc_supply.get('price'),
                                bnc_supply.get('volume'), bnc_supply.get('totalSupply'),
                                bnc_supply.get('freeFloatSupply'), bnc_supply.get('marketCap'),
                                bnc_supply.get('totalMarketCap')))

with open('bnc-market-cap-ranking-date.csv'.replace('date', date.today().strftime("%Y-%m-%d")),
          mode='w') as bnc_market_cap_ranking_file:
    wr = csv.writer(bnc_market_cap_ranking_file, dialect='excel')
    wr.writerows(market_cap_list)

bnc_market_cap_ranking_file.close()
