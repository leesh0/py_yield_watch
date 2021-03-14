from ..bsc_config import bs, w3


class Module:
    class Config:
        pool_urls = []
        pools = {}
        name = None

    def __init__(self):
        self.bs = bs  # BscScan
        self.w3 = w3  # pyWeb3
        self.pools = None  # x Finance Pools
        self.log = None
        self.wallet = None

    def new(self, log, wallet):
        self.log = log
        self.wallet = wallet
        return self

    async def get_history(self) -> dict:
        pass

    async def get_yields(self) -> list:
        pass

    async def get_yields_with_history(self) -> list:
        pass

    async def update_pools(self) -> None:
        pass
