from finances.bsc import Wallet
from time import time
from pprint import pp

w = Wallet()

start = time()
a = w("0xb732a5B907FC38eD71A9B18eBd77dDa3F2771103").yields_with_history()
pp(a)
print(time()-start, 'seconds')
