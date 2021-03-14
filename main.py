from finances.bsc import Beefy
#
#
if __name__ == "__main__":
    b = Beefy()
    print(b.user_deposits("0xb732a5B907FC38eD71A9B18eBd77dDa3F2771103"))
# def sleep(delay):
#     time.sleep(delay)
#     return 'a'
#
#
# async def f1():
#     loop = asyncio.get_event_loop()
#     f = loop.run_in_executor(None, sleep, 1)
#     resp = await f
#     return resp
#
#
# def main():
#     async def iters():
#         data = {
#             'f1': await f1()
#         }
#         return data
#
#     cs = [iters() for _ in range(10)]
#     a = await asyncio.gather(*cs)
#     print(a)
#
#
# main()
