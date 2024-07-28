from requests import post
from urllib.parse import unquote
from colorama import Fore
from hashlib import md5
from datetime import datetime, timedelta
from threading import Thread, Lock
from typing import Literal
from random import randint
from os import system as sys
from platform import system as s_name
from time import sleep
from itertools import cycle

from Core.Tools.HPV_Getting_File_Paths import HPV_Get_Accounts
from Core.Tools.HPV_Proxy import HPV_Proxy_Checker
from Core.Tools.HPV_User_Agent import HPV_User_Agent

from Core.Config.HPV_Config import *







class HPV_Gamee:
    '''
    AutoBot Ferma /// HPV
    ---------------------
    [1] - `Разблокировка майнинга при его блокировке`
    
    [2] - `Сбор WP при разблокированном майнинге`
    
    [3] - `Попытка апгрейда для майнинга WP`
    
    [4] - `Получение информации о наличии спинов`
    
    [5] - `Прокрутка всех доступных спинов`
    
    [6] - `Получение информации о наличии игр`
    
    [7] - `Прохождение всех доступных игр`
    
    [8] - `Ожидание от 30 до 60 минут`
    
    [9] - `Повторение действий через 30-60 минут`
    '''



    def __init__(self, Name: str, URL: str, Proxy: dict = None) -> None:
        self.Name = Name                         # Ник аккаунта
        self.URL = self.URL_Clean(URL)           # Уникальная ссылка для авторизации в mini app
        self.Proxy = Proxy                       # Прокси (при наличии)
        self.UA = HPV_User_Agent()               # Генерация уникального User Agent
        self.Domain = 'https://api.gamee.com/'   # Домен игры
        INFO = self.Authentication()
        self.Token = INFO['Token']               # Токен аккаунта
        self.Games = str(INFO['Games'] + 1)      # Кол-во сыгранных игр



    def URL_Clean(self, URL: str) -> str:
        '''Очистка уникальной ссылки от лишних элементов'''

        try:
            return unquote(URL.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        except:
            return ''



    def Current_Time(self) -> str:
        '''Текущее время'''

        return Fore.BLUE + f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'



    def Logging(self, Type: Literal['Success', 'Warning', 'Error'], Name: str, Smile: str, Text: str) -> None:
        '''Логирование'''

        with Console_Lock:
            COLOR = Fore.GREEN if Type == 'Success' else Fore.YELLOW if Type == 'Warning' else Fore.RED # Цвет текста
            DIVIDER = Fore.BLACK + ' | '   # Разделитель

            Time = self.Current_Time()     # Текущее время
            Name = Fore.MAGENTA + Name     # Ник аккаунта
            Smile = COLOR + str(Smile)     # Смайлик
            Text = COLOR + Text            # Текст лога

            print(Time + DIVIDER + Smile + DIVIDER + Text + DIVIDER + Name)



    def Authentication(self) -> dict:
        '''Аутентификация аккаунта'''

        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9', 'client-language': 'en', 'content-type': 'text/plain;charset=UTF-8', 'origin': 'https://prizes.gamee.com', 'priority': 'u=1, i', 'referer': 'https://prizes.gamee.com/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-install-uuid': 'a5658ae5-54e4-447c-a8cc-d1859be596ea'}
        Data = '{"jsonrpc":"2.0","id":"user.authentication.loginUsingTelegram","method":"user.authentication.loginUsingTelegram","params":{"initData":"' + self.URL + '"}}'

        try:
            HPV = post(self.Domain, headers=Headers, data=Data, proxies=self.Proxy).json()['result']

            Token = HPV['tokens']['authenticate'] # Токен аккаунта
            Games = HPV['user']['gamee']['gameplays'] # Кол-во сыгранных игр

            self.Logging('Success', self.Name, '🟢', 'Инициализация успешна!')
            return {'Token': Token, 'Games': Games}
        except:
            self.Logging('Error', self.Name, '🔴', 'Ошибка инициализации!')
            return {'Token': '', 'Games': 0}



    def ReAuthentication(self) -> None:
        '''Повторная аутентификация аккаунта'''

        INFO = self.Authentication()
        self.Token = INFO['Token']               # Токен аккаунта
        self.Games = str(INFO['Games'] + 1)      # Кол-во сыгранных игр



    def Get_Info(self) -> dict:
        '''Получение информации о балансе и окончания майнинга'''

        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'authorization': f'Bearer {self.Token}', 'client-language': 'en', 'content-type': 'text/plain;charset=UTF-8', 'origin': 'https://prizes.gamee.com', 'priority': 'u=1, i', 'referer': 'https://prizes.gamee.com/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-install-uuid': '927fcdde-8b83-4e37-9862-24e9611fb9c2'}
        Data = '{"jsonrpc":"2.0","id":"miningEvent.getAll","method":"miningEvent.getAll","params":{"pagination":{"offset":0,"limit":10}}}'

        try:
            HPV = post(self.Domain, headers=Headers, data=Data, proxies=self.Proxy).json()

            USER_INFO = HPV['user'] # Информация о балансе билетов и долларов
            Tickets = USER_INFO['tickets']['count'] # Баланс билетов
            WP = '' # Баланс WP
            COIN = '' # Баланс COIN

            try:Dollars = USER_INFO['money']['usdCents'] / 100 # Баланс долларов
            except:Dollars = USER_INFO['money']['usdCents']

            for Token in USER_INFO['assets']:
                if Token['currency']['ticker'] == 'WP':
                    WP = f"{Token['amountMicroToken'] / 1_000_000:,.2f}"
                elif Token['currency']['ticker'] == 'COIN':
                    COIN = f"{Token['amountMicroToken'] / 1_000_000:,.0f}"

            WP_INFO = HPV['result']['miningEvents'] # Информация о майнинге WP
            for WP_Mining in WP_INFO:
                try:Mining_Over = WP_Mining['miningUser']['miningSessionEnded'] # Завершился ли цикл майнинга [True или False]
                except:pass

            return {'Tickets': f'{Tickets:,}', 'WP': WP, 'COIN': COIN, 'Dollars': Dollars, 'Mining_Over': Mining_Over}
        except:
            return {'Tickets': None, 'WP': None, 'COIN': None, 'Dollars': None, 'Mining_Over': None}



    def Get_Info_Spin(self) -> int:
        '''Получение информации о наличии спинов'''

        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9', 'authorization': f'Bearer {self.Token}', 'client-language': 'en', 'content-type': 'text/plain;charset=UTF-8', 'origin': 'https://prizes.gamee.com', 'priority': 'u=1, i', 'referer': 'https://prizes.gamee.com/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-install-uuid': 'a5658ae5-54e4-447c-a8cc-d1859be596ea'}
        Data = '{"jsonrpc":"2.0","id":"dailyReward.getPrizes","method":"dailyReward.getPrizes","params":{}}'

        try:
            HPV = post(self.Domain, headers=Headers, data=Data, proxies=self.Proxy).json()['result']['dailyReward']

            Spins = HPV['spinsCountAvailable'] # Обычные спины
            Gold_Spins = HPV['wheelOfCashSpinsCountAvailable'] # Спины за призы в $

            return Spins + Gold_Spins
        except:
            return 0



    def Claim_WP(self) -> bool:
        '''Сбор WP'''

        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'authorization': f'Bearer {self.Token}', 'client-language': 'en', 'content-type': 'text/plain;charset=UTF-8', 'origin': 'https://prizes.gamee.com', 'priority': 'u=1, i', 'referer': 'https://prizes.gamee.com/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-install-uuid': '927fcdde-8b83-4e37-9862-24e9611fb9c2'}
        Data1 = '{"jsonrpc":"2.0","id":"miningEvent.claim","method":"miningEvent.claim","params":{"miningEventId":26}}'
        Data2 = '{"jsonrpc":"2.0","id":"miningEvent.startSession","method":"miningEvent.startSession","params":{"miningEventId":26}}'

        try:
            post(self.Domain, headers=Headers, data=Data1, proxies=self.Proxy).json()['result'] # Claim
            post(self.Domain, headers=Headers, data=Data2, proxies=self.Proxy).json()['result'] # Start Session
            self.Logging('Success', self.Name, '🟢', 'Монеты собраны!')
            return True
        except:
            self.Logging('Error', self.Name, '🔴', 'Монеты не собраны!')
            return False



    def WP_Mining_Update(self) -> bool:
        '''Апгрейд для майнинга WP'''

        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'authorization': f'Bearer {self.Token}', 'client-language': 'en', 'content-type': 'text/plain;charset=UTF-8', 'origin': 'https://prizes.gamee.com', 'priority': 'u=1, i', 'referer': 'https://prizes.gamee.com/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-install-uuid': '927fcdde-8b83-4e37-9862-24e9611fb9c2'}
        Data = '{"jsonrpc":"2.0","id":"miningEvent.upgrade","method":"miningEvent.upgrade","params":{"miningEventId":26,"upgrade":"storage"}}'

        try:
            post(self.Domain, headers=Headers, data=Data, proxies=self.Proxy).json()['result']
            return True
        except:
            return False



    def Spin(self) -> None:
        '''Прокрутка всех доступных спинов'''

        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'authorization': f'Bearer {self.Token}', 'client-language': 'en', 'content-type': 'text/plain;charset=UTF-8', 'origin': 'https://prizes.gamee.com', 'priority': 'u=1, i', 'referer': 'https://prizes.gamee.com/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-install-uuid': '927fcdde-8b83-4e37-9862-24e9611fb9c2'}
        Data = '[{"jsonrpc":"2.0","id":"dailyReward.claimPrize","method":"dailyReward.claimPrize","params":{}},{"jsonrpc":"2.0","id":"dailyReward.getPrizes","method":"dailyReward.getPrizes","params":{}}]'

        try:
            HPV = post(self.Domain, headers=Headers, data=Data, proxies=self.Proxy).json()[0]['result']['reward']

            Prize = ''
            if HPV['type'] == 'money' or HPV['type'] == 'wheelOfCash':
                Prize = f'{HPV["usdCents"] / 100:,.2f}$'
            else:
                Prize = f'{HPV["tickets"]} билетов'

            self.Logging('Success', self.Name, '🟢', f'Вращение произведено! Получено: {Prize}')
        except:
            self.Logging('Error', self.Name, '🔴', 'Вращение не произведено!')



    def Get_Plays(self) -> int:
        '''Получение кол-ва доступных игр'''

        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'authorization': f'Bearer {self.Token}', 'client-language': 'en', 'content-type': 'text/plain;charset=UTF-8', 'origin': 'https://prizes.gamee.com', 'priority': 'u=1, i', 'referer': 'https://prizes.gamee.com/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-install-uuid': '927fcdde-8b83-4e37-9862-24e9611fb9c2'}
        Data = '{"jsonrpc":"2.0","id":"telegram.getGameAndLives","method":"telegram.getGameAndLives","params":{"gameId":null}}'

        try:
            return int(post(self.Domain, headers=Headers, data=Data, proxies=self.Proxy).json()['result']['lives']['numberOfLives'] / 30)
        except:
            return 0



    def Play(self) -> None:
        '''Воспроизведение игры в машинку'''

        def Checksum_Generation(WP, COIN):
            gameStateData = '{"usedLives":30,"reward":{"WP":'+WP+',"COIN":'+COIN+'}}'
            return md5(f'0:32::{gameStateData}:crmjbjm3lczhlgnek9uaxz2l9svlfjw14npauhen'.encode()).hexdigest()

        WP, COIN = str(randint(WPs[0], WPs[1])), str(randint(COINs[0], COINs[1]))
        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'authorization': f'Bearer {self.Token}', 'client-language': 'en', 'content-type': 'text/plain;charset=UTF-8', 'origin': 'https://prizes.gamee.com', 'priority': 'u=1, i', 'referer': 'https://prizes.gamee.com/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-install-uuid': '927fcdde-8b83-4e37-9862-24e9611fb9c2'}
        Data = '{"jsonrpc":"2.0","id":"game.saveTelegramMainGameplay","method":"game.saveTelegramMainGameplay","params":{"gameplayData":{"gameId":294,"score":0,"playTime":32,"releaseNumber":4,"createdTime":"2024-07-28T16:05:36+05:00","metadata":{"gameplayId":' + self.Games + '},"checksum":"' + Checksum_Generation(WP, COIN) + '","gameStateData":"{\\"usedLives\\":30,\\"reward\\":{\\"WP\\":'+WP+',\\"COIN\\":'+COIN+'}}","replayData":"AgAAABIAHnkD5cwAbgBvBQAe","replayVariant":null,"replayDataChecksum":null}}}'

        try:
            HPV = post(self.Domain, headers=Headers, data=Data, proxies=self.Proxy).json()['result']['rewardVirtualTokens']

            WP = ''
            COIN = ''

            for Token in HPV:
                if Token['currency']['ticker'] == 'WP':
                    WP = int(Token['amountMicroToken'] / 1_000_000)
                if Token['currency']['ticker'] == 'COIN':
                    COIN = int(Token['amountMicroToken'] / 1_000_000)

            self.Logging('Success', self.Name, '🟢', f'Игра сыграна! Получено: +{WP} WP и +{COIN} COIN')
        except:
            self.Logging('Error', self.Name, '🔴', 'Игра не сыграна!')



    def Run(self) -> None:
        '''Активация бота'''

        while True:
            try:
                if self.Token: # Если аутентификация успешна
                    INFO = self.Get_Info()


                    Tickets = INFO['Tickets'] # Баланс билетов
                    WP = INFO['WP'] # Баланс WP
                    COIN = INFO['COIN'] # Баланс COIN
                    Dollars = INFO['Dollars'] # Баланс долларов
                    Mining_Over = INFO['Mining_Over'] # Завершился ли цикл майнинга [True или False]


                    self.Logging('Success', self.Name, '💰', f'Текущий баланс: {Dollars}$, {Tickets} билетов, {WP} WP и {COIN} COIN')


                    # Проверка окончания майнинга WP, и дальнейший его запуск
                    try: # Если майнинг разблокирован
                        if Mining_Over:
                            if self.Claim_WP():
                                INFO = self.Get_Info()
                                Tickets, WP, COIN, Dollars = INFO['Tickets'], INFO['WP'], INFO['COIN'], INFO['Dollars']
                                self.Logging('Success', self.Name, '💰', f'Текущий баланс: {Dollars}$, {Tickets} билетов, {WP} WP и {COIN} COIN')
                                sleep(randint(33, 103)) # Промежуточное ожидание
                    except: # Если майнинг заблокирован
                        self.Claim_WP() # Разблокировка майнинга
                        sleep(randint(33, 103)) # Промежуточное ожидание


                    # Попытка апгрейда для майнинга WP
                    if UPDATE:
                        if self.WP_Mining_Update():
                            self.Logging('Success', self.Name, '🟢', 'Апгрейд майнинга успешен!')
                            INFO = self.Get_Info()
                            Tickets, WP, COIN, Dollars = INFO['Tickets'], INFO['WP'], INFO['COIN'], INFO['Dollars']
                            self.Logging('Success', self.Name, '💰', f'Текущий баланс: {Dollars}$, {Tickets} билетов, {WP} WP и {COIN} COIN')
                            sleep(randint(33, 103)) # Промежуточное ожидание


                    # Получение кол-ва доступных спинов и запуск их прокрутки
                    Get_Spins = self.Get_Info_Spin()
                    if Get_Spins > 0:
                        self.Logging('Success', self.Name, '🎮', f'Спинов доступно: {Get_Spins}!')
                        for _ in range(Get_Spins):
                            self.Spin()
                            sleep(randint(12, 23))

                            INFO = self.Get_Info()
                            Tickets, WP, COIN, Dollars = INFO['Tickets'], INFO['WP'], INFO['COIN'], INFO['Dollars']
                            self.Logging('Success', self.Name, '💰', f'Текущий баланс: {Dollars}$, {Tickets} билетов, {WP} WP и {COIN} COIN')


                    # Получение кол-ва доступных игр и запуск их прохождения
                    Get_Plays = self.Get_Plays()
                    if Get_Plays > 0:
                        self.Logging('Success', self.Name, '🎮', f'Игр доступно: {Get_Spins}!')
                        for _ in range(Get_Spins):
                            self.Play()
                            sleep(randint(12, 23))

                            INFO = self.Get_Info()
                            Tickets, WP, COIN, Dollars = INFO['Tickets'], INFO['WP'], INFO['COIN'], INFO['Dollars']
                            self.Logging('Success', self.Name, '💰', f'Текущий баланс: {Dollars}$, {Tickets} билетов, {WP} WP и {COIN} COIN')


                    Waiting = randint(1_800, 3_600) # Значение времени в секундах для ожидания
                    Waiting_STR = (datetime.now() + timedelta(seconds=Waiting)).strftime('%Y-%m-%d %H:%M:%S') # Значение времени в читаемом виде

                    self.Logging('Warning', self.Name, '⏳', f'Следующая проверка спинов: {Waiting_STR}!')

                    sleep(Waiting) # Ожидание от 30 до 60 минут
                    self.ReAuthentication() # Повторная аутентификация аккаунта

                else: # Если аутентификация не успешна
                    sleep(randint(33, 66)) # Ожидание от 33 до 66 секунд
                    self.ReAuthentication() # Повторная аутентификация аккаунта
            except:
                pass







if __name__ == '__main__':
    sys('cls') if s_name() == 'Windows' else sys('clear')

    Console_Lock = Lock()
    Proxy = HPV_Proxy_Checker()

    def Start_Thread(Account, URL, Proxy = None):
        Gamee = HPV_Gamee(Account, URL, Proxy)
        Gamee.Run()

    if Proxy:
        DIVIDER = Fore.BLACK + ' | '
        Time = Fore.BLUE + f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        Text = Fore.GREEN + f'Проверка прокси окончена! Работоспособные: {len(Proxy)}'
        print(Time + DIVIDER + '🌐' + DIVIDER + Text)
        sleep(5)

    try:
        for Account, URL in HPV_Get_Accounts().items():
            if Proxy:
                Proxy = cycle(Proxy)
                Thread(target=Start_Thread, args=(Account, URL, next(Proxy),)).start()
            else:
                Thread(target=Start_Thread, args=(Account, URL,)).start()
    except:
        print(Fore.RED + '\n\tОшибка чтения `HPV_Account.json`, ссылки указаны некорректно!')


