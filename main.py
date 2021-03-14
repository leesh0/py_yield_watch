from finances.bsc import Wallet
from time import time
from pprint import pp

w = Wallet()

start = time()
a = w('').yields_with_history()
pp(a)
print(time()-start, 'seconds')
