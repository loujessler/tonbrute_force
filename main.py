import asyncio
# import multiprocessing
import logging
import os
import random
import time
from datetime import datetime

import requests
from ton import TonlibClient

from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from dotenv import load_dotenv

# cdll_path = './ton-venv/lib/python3.10/site-packages/ton/distlib/linux/libtonlibjson.x86_64.so'

load_dotenv()  # take environment variables from .env.

TOKEN = str(os.environ.get("API_TOKEN"))
logging.basicConfig(format='%(asctime)s %(module)-15s %(message)s',
                    level=logging.INFO)
logging.basicConfig(filename='ton_logs.log', filemode='w',
                    format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    # level=logging.INFO,
                    level=logging.DEBUG,
                    )

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


ADMINS = [
    6405640,
    # 118218714,
]


def dictionary(file):
    d = {}
    for i, line in enumerate(open(file, 'r')):
        line = line.strip()
        a = line
        d[i] = a
    return d


async def check_address_in_network(seed, client):
    wallet = await client.import_wallet(' '.join(x for x in seed))
    balance = await wallet.get_balance()
    if balance != -1:
        f = open("finder.txt", "a")
        f.write('ADDReSS: ' + str(wallet.account_address.account_address))
        f.write('Balance: ' + str(balance))
        f.write('\nSEED: ' + str(' '.join(x for x in seed)))
        f.write('\n------------------------\n')
        f.close()
        for admin in ADMINS:
            try:
                await dp.bot.send_message(chat_id=admin,
                                          text=f'Find\n'
                                               f'Address: {str(wallet.account_address.account_address)}\n'
                                               f'Balance: {str(balance)}\n'
                                               f'Seed: {str(" ".join(x for x in seed))}')
            except Exception:
                pass


async def new_ton_lib():
    # client = TonlibClient()
    # client.enable_unaudited_binaries()

    client = TonlibClient(keystore=None,
                          config='https://newton-blockchain.github.io/global.config.json',
                          ls_index=0)
    client.enable_unaudited_binaries()
    print('Start')
    try:
        await client.init_tonlib()
    except TypeError as ex:
        print(ex)

    for admin in ADMINS:
        try:
            await dp.bot.send_message(chat_id=admin, text="Script is running!!!!!")
        except TypeError:
            pass

    n = 0
    start_timer = time.time()

    d = dictionary('english.txt')

    # while seed is 'blast cave virus nation roof notice walnut circle stadium december defy execute game wear helmet':
    while True:
        n += 1
        seed = 'blast cave virus nation roof notice walnut round stadium december defy execute game wear helmet'

        seed = seed.split(' ')
        while len(seed) != 24:
            word = d[random.randint(0, 2047)]
            seed.append(word)
        try:
            await check_address_in_network(seed, client)
        except:
            pass
        try:
            seed[7] = 'range'
            await check_address_in_network(seed, client)
        except:
            pass
        try:
            seed[12] = 'play'
            await check_address_in_network(seed, client)
        except:
            pass
        try:
            seed[7] = 'round'
            await check_address_in_network(seed, client)
        except:
            pass
        # ____________________________Counter
        if n % 1000 == 0:
            end_timer = time.time()
            print(f'Counted {n} times')
            print(
                f'For 1 iteration  {round((end_timer - start_timer) / 4000, 5)} sec. {round(4000 / (end_timer - start_timer), 5)} iterations per second')
            f = open("logs.txt", "a")
            f.write(f'Counted {n} times {str(datetime.now())}')
            f.write(
                f'\nFor 1 iteration {round((end_timer - start_timer) / 4000, 5)}c. {round(4000 / (end_timer - start_timer), 5)} iterations per second')
            f.write('\n------------------------\n')
            f.close()
            start_timer = time.time()
        if n % 500000 == 0:
            f = open("logs.txt", "w")
            f.truncate()
            f.close()


if __name__ == '__main__':
    # asyncio.run(new_ton_lib())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(new_ton_lib())

# if __name__ == '__main__':
#
#     for cpu in range(multiprocessing.cpu_count()):
#         loop = asyncio.get_event_loop()
#         print('start')
#         loop.run_until_complete(new_ton_lib())
#         # multiprocessing.Process(target=new_ton_lib).start()
