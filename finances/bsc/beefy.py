import requests as rq
from pyjson5 import decode
from datetime import datetime
from .bsc_config import *
import asyncio


class Beefy:
    urls = {
        'pools': ['https://raw.githubusercontent.com/beefyfinance/beefy-app/prod/src/features/configure/bsc_pools.js'],
        'logo_base': 'https://github.com/beefyfinance/beefy-app/blob/master/src/images/'
    }

    def __init__(self):
        self.pools = self.update_pools()

    def update_pools(self):
        data = ""
        for url in self.urls['pools']:
            data += rq.get(url).text.split("=")[1][:-2]
        tokens = decode(data)
        for v in tokens:
            v['logo'] = self.urls['logo_base'] + v['logo'] + "?raw=true"
        self.pools = {x['earnContractAddress'].lower(): x for x in tokens}
        return self.pools

    def get_user_history(self, wallet):
        logs = bs.get_bep20_token_transfer_events_by_address(wallet, startblock=None,
                                                             endblock=None, sort="asc")
        my_tokens = {}
        zaddr = "0x0000000000000000000000000000000000000000"
        for tr in logs:
            if self.pools.get(tr['from']) or self.pools.get(tr['to']):
                if tr['from'] == wallet.lower():
                    action, token_id = "IN", tr['to']
                else:
                    action, token_id = "OUT", tr['from']
                if not my_tokens.get(token_id):
                    my_tokens[token_id] = []
                my_tokens[token_id].append({
                    'action': action,
                    'token': token_id,
                    'time': datetime.fromtimestamp(int(tr['timeStamp'])).isoformat(),
                    'moo': my_tokens[token_id][-1]['omoo'] if len(my_tokens[token_id]) > 0 and my_tokens[token_id][
                        -1].get(
                        'omoo') else 0,
                    'value': int(tr['value']) if action == "IN" else -int(tr['value']),
                })
                if len(my_tokens[token_id]) > 1 and my_tokens[token_id][-2].get('omoo'):
                    del my_tokens[token_id][-2]['omoo']
            if tr['from'] == wallet.lower() and tr['to'] == zaddr and my_tokens.get(tr['contractAddress']):
                my_tokens[tr['contractAddress']][-1]['omoo'] = -int(tr['value'])
            elif tr['to'] == wallet.lower() and tr['from'] == zaddr and my_tokens.get(tr['contractAddress']):
                my_tokens[tr['contractAddress']][-1]['moo'] += int(tr['value'])
        return my_tokens

    async def read_history(self, history: dict, with_current=True):
        async def set_current(block):
            if block['moo'] > 0:
                crnt = await self.get_moo_current(block['contract'], block['moo'])
            else:
                crnt = 0
            block['current'] = crnt
            block['name'] = self.pools[block['contract']]['name']
            return block

        for k, v in history.items():
            deposit = sum([x['value'] for x in v])
            moo = sum([x['moo'] for x in v])
            history[k] = {'contract': k, 'deposit': deposit / 1e18, 'moo': moo, 'history': v}
        if with_current:
            coros = [set_current(block) for block in history.values()]
            return await asyncio.gather(*coros)
        else:
            return [v for v in history.values()]

    async def get_moo_current(self, contract_address, moo):
        loop = asyncio.get_event_loop()
        abi = beefy_abi
        contract_params = {
            'address': w3.toChecksumAddress(contract_address),
            'abi': str(abi)
        }
        contract = w3.eth.contract(**contract_params)
        ppf = await loop.run_in_executor(None, contract.functions.getPricePerFullShare().call)
        return ppf * moo / 1e36

    def user_deposits(self, wallet):
        user_history = self.get_user_history(wallet)
        return asyncio.run(self.read_history(user_history, with_current=True))

