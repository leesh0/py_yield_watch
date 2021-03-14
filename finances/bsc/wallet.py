from .bsc_config import *
from .dex import Module, ModuleBeefy
import asyncio

class Connector:
    def __init__(self, logs, wallet, fins: dict):
        self.logs = logs
        self.wallet = wallet
        self.fins = fins

    def history(self):
        async def get_history():
            coros = [fin.new(self.logs, self.wallet).get_history() for fin in self.fins.values()]
            result = await asyncio.gather(*coros)
            return [{fin_name: v} for fin_name, v in zip(self.fins.keys(), result)]

        if not (self.wallet and self.logs):
            raise AttributeError("pls init wallet")
        return asyncio.run(get_history())

    def yields(self):
        async def get_yields():
            coros = [fin.new(self.logs, self.wallet).get_yields() for fin in self.fins.values()]
            result = await asyncio.gather(*coros)
            return [{fin_name: v} for fin_name, v in zip(self.fins.keys(), result)]

        if not (self.wallet and self.logs):
            raise AttributeError("pls init wallet")
        return asyncio.run(get_yields())

    def yields_with_history(self):
        async def get_yields_history():
            coros = [fin.new(self.logs, self.wallet).get_yields_with_history() for fin in self.fins.values()]
            result = await asyncio.gather(*coros)
            return [{fin_name: v} for fin_name, v in zip(self.fins.keys(), result)]

        if not (self.wallet and self.logs):
            raise AttributeError("pls init wallet")
        return asyncio.run(get_yields_history())


class Wallet:
    fins = {
        'beefy': ModuleBeefy()
    }

    def __init__(self):
        self.wallet = None
        self.logs = None
        self.update_modules()

    def update_modules(self):
        async def init_modules():
            coros = [fin.update_pools() for fin in self.fins.values()]
            await asyncio.gather(*coros)
            return
        asyncio.run(init_modules())

    def add_module(self, module):
        self.fins[module.__name__.lower()] = module
        return self

    def __call__(self, wallet: str):
        self.wallet = wallet
        self.logs = bs.get_bep20_token_transfer_events_by_address(wallet, startblock=None,
                                                                  endblock=None, sort="asc")
        return Connector(self.logs, self.wallet, self.fins)
