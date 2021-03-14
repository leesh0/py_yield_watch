from .module import Module
import requests as rq
from pyjson5 import decode
from datetime import datetime
from functools import partial
import asyncio


class ModuleBeefy(Module):
    class Config:
        name = 'beefy'
        pool_urls = [
            'https://raw.githubusercontent.com/beefyfinance/beefy-app/prod/src/features/configure/bsc_pools.js']
        logo_base = "https://github.com/beefyfinance/beefy-app/blob/master/src/images/"
        abi = """[{"inputs":[{"internalType":"address","name":"_token","type":"address"},{"internalType":"address","name":"_strategy","type":"address"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint256","name":"_approvalDelay","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"implementation","type":"address"}],"name":"NewStratCandidate","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"implementation","type":"address"}],"name":"UpgradeStrat","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"approvalDelay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"available","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"balance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"depositAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"earn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getPricePerFullShare","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_implementation","type":"address"}],"name":"proposeStrat","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"stratCandidate","outputs":[{"internalType":"address","name":"implementation","type":"address"},{"internalType":"uint256","name":"proposedTime","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"strategy","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"token","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"upgradeStrat","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_shares","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"withdrawAll","outputs":[],"stateMutability":"nonpayable","type":"function"}]"""

    async def read_history(self, history: dict, with_current=True, with_history=True):
        wallet = self.wallet

        async def set_current(block):
            if block['moo'] > 0:
                crnt = await self.get_moo_current(block['contract'], block['moo'])
            else:
                crnt = 0
            block['current'] = crnt
            return block

        for k, v in history.items():
            hp = self.history_parser(v)
            history[k] = {'name': self.pools[k]['name'], 'contract': k, 'deposit': hp['deposit'] / 1e18,
                          'moo': hp['moo']}
            if with_history:
                history[k]['history'] = v
        if with_current:
            coros = [set_current(block) for block in history.values()]
            return await asyncio.gather(*coros)
        else:
            return [v for v in history.values()]

    async def get_moo_current(self, contract_address: str, moo):
        wallet = self.wallet
        loop = asyncio.get_event_loop()
        contract_address = self.w3.toChecksumAddress(contract_address)
        abi = self.Config.abi
        contract_params = {
            'address': contract_address,
            'abi': str(abi)
        }
        contract = self.w3.eth.contract(**contract_params)
        ppf = await loop.run_in_executor(None, contract.functions.getPricePerFullShare().call)
        return ppf * moo / 1e36

    @staticmethod
    def history_parser(partial_history):
        depo = 0
        moo = 0
        mood = 0
        for hist in partial_history:
            if hist['action'] == "IN":
                depo += hist['value']
                moo += hist['moo']
                mood = depo / moo
            else:
                depo += hist['moo'] * mood
                if abs(moo) == abs(hist['moo']):
                    depo = 0
                moo += hist['moo']
        return {
            'deposit': depo,
            'moo': moo,
        }

    async def get_history(self) -> dict:
        logs = self.log
        wallet = self.wallet
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

    async def get_yields_with_history(self) -> list:
        history = await self.get_history()
        return await self.read_history(history)

    async def get_yields(self) -> list:
        history = await self.get_history()
        return  await self.read_history(history, with_history=False)

    async def update_pools(self):
        loop = asyncio.get_event_loop()
        data = ""
        for url in self.Config.pool_urls:
            recv = await loop.run_in_executor(None, partial(rq.get, url))
            data += recv.text.split("=")[1][:-2]
        tokens = decode(data)
        for v in tokens:
            v['logo'] = self.Config.logo_base + v['logo'] + "?raw=true"
        self.pools = {x['earnContractAddress'].lower(): x for x in tokens}
        return self.pools
