# PY_YIELD_WATCH

> defi vaults & finance yield reader by Python.(py-web3)
>
> Powered by. [BscScan](https://bscscan.com/)

## Support

Now Only Support BSC(Binance Smart Chain)
- [Beefy](http://beefy.finance)

## Quick Start
```python
from finances.bsc import Wallet
from time import time
w = Wallet()

start = time()
a = w(YOUR_BSC_WALLET_ADDRESS).yields()
print(a)
print(time()-start, 'seconds')
```
