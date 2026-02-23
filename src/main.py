import asyncio
from asyncio import sleep
from scripts.load_data import load_data

if __name__ == '__main__':
    asyncio.run(load_data())
    asyncio.run(sleep(10000))
