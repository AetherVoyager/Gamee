from requests import post, get
from urllib.parse import unquote
from colorama import Fore
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
    [1] - `Получение информации о текущем майнинг ивенте`
    
    [2] - `Разблокировка майнинга при его блокировке`
    
    [3] - `Сбор WP при разблокированном майнинге`
    
    [4] - `Попытка апгрейда для майнинга WP`
    
    [5] - `Получение информации о наличии спинов`
    
    [6] - `Прокрутка всех доступных спинов`
    
    [7] - `Ожидание от 30 до 60 минут`
    
    [8] - `Повторение действий через 30-60 минут`
    '''



    def __init__(self, Name: str, URL: str, Proxy: dict = None) -> None:
        self.Name = Name                         # Ник аккаунта
        self.URL = self.URL_Clean(URL)           # Уникальная ссылка для авторизации в mini app
        self.Proxy = Proxy                       # Прокси (при наличии)
        self.UA = HPV_User_Agent()               # Генерация уникального User Agent
        self.Domain = 'https://api.gamee.com/'   # Домен игры
        self.Token = self.Authentication()       # Токен аккаунта



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



    def Authentication(self) -> str:
        '''Аутентификация аккаунта'''

        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9', 'client-language': 'en', 'content-type': 'text/plain;charset=UTF-8', 'origin': 'https://prizes.gamee.com', 'priority': 'u=1, i', 'referer': 'https://prizes.gamee.com/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-install-uuid': 'a5658ae5-54e4-447c-a8cc-d1859be596ea'}
        Data = '{"jsonrpc":"2.0","id":"user.authentication.loginUsingTelegram","method":"user.authentication.loginUsingTelegram","params":{"initData":"' + self.URL + '"}}'

        try:
            Token = post(self.Domain, headers=Headers, data=Data, proxies=self.Proxy).json()['result']['tokens']['authenticate']
            self.Logging('Success', self.Name, '🟢', 'Инициализация успешна!')
            return Token
        except:
            self.Logging('Error', self.Name, '🔴', 'Ошибка инициализации!')
            return ''



    def ReAuthentication(self) -> None:
        '''Повторная аутентификация аккаунта'''

        self.Token = self.Authentication()



    def Get_EventID(self) -> dict:
        '''Получение информации о текущем майнинг ивенте'''

        URL = 'https://raw.githubusercontent.com/A-KTO-Tbl/Gamee/main/Core/Config/HPV_Events_Info.json'

        try:
            HPV = get(URL).json()

            ID = HPV['id'] # ID ивента
            PASS = HPV['pass'] # Пароль для разблокировки ивента

            return {'Status': True, 'ID': ID, 'PASS': PASS}
        except:
            return {'Status': False}



    def Get_Info(self, ID: str) -> dict:
        '''Получение информации о балансе и окончания майнинга'''

        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9', 'authorization': f'Bearer {self.Token}', 'client-language': 'en', 'content-type': 'text/plain;charset=UTF-8', 'origin': 'https://prizes.gamee.com', 'priority': 'u=1, i', 'referer': 'https://prizes.gamee.com/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-install-uuid': 'a5658ae5-54e4-447c-a8cc-d1859be596ea'}
        Data = '{"jsonrpc":"2.0","id":"miningEvent.get","method":"miningEvent.get","params":{"miningEventId":' + ID + '}}'

        try:
            HPV = post(self.Domain, headers=Headers, data=Data, proxies=self.Proxy).json()


            USER_INFO = HPV['user'] # Информация о балансе билетов и долларов
            Tickets = USER_INFO['tickets']['count'] # Баланс билетов
            try:
                Dollars = USER_INFO['money']['usdCents'] / 100 # Баланс долларов
            except:
                Dollars = USER_INFO['money']['usdCents']


            WP_INFO = HPV['result']['miningEvent']['miningUser'] # Информация о майнинге WP
            if WP_INFO:
                Improvement_Level = WP_INFO['countOfStorageImprovements'] + 1 # Уровень улучшения майнинга
                Max_Storage = f'{WP_INFO["currentSessionMicroToken"] / 1_000_000:,.0f}' # Максимальное кол-во токеном, которое можно получить за один период майминга
                Received = f'{WP_INFO["currentSessionMicroTokenMined"] / 1_000_000:,.2f}' # Намайнено в данный момент
                Mining_Speed = f'{WP_INFO["currentSpeedMicroToken"] / 1_000_000:,.2f}' # Скорость майнинга
                Mining_Over = WP_INFO['miningSessionEnded'] # Завершился ли цикл майнинга [True или False]
                try:
                    WPs = f'{WP_INFO["cumulativeMicroTokenMined"] / 1_000_000:,.2f}' # Баланс WP
                except:
                    WPs = f'{WP_INFO["cumulativeMicroTokenMined"]:,.2f}'

                return {'Improvement_Level': Improvement_Level, 'Max_Storage': Max_Storage, 'Received': Received, 'Mining_Speed': Mining_Speed, 'Mining_Over': Mining_Over, 'WPs': WPs, 'Tickets': f'{Tickets:,}', 'Dollars': Dollars, 'WP_INFO': True}

            return {'Tickets': f'{Tickets:,}', 'Dollars': Dollars, 'WP_INFO': False}
        except:
            return None



    def Get_Info_Spin(self) -> int:
        '''Получение информации о наличии спинов'''

        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9', 'authorization': f'Bearer {self.Token}', 'client-language': 'en', 'content-type': 'text/plain;charset=UTF-8', 'origin': 'https://prizes.gamee.com', 'priority': 'u=1, i', 'referer': 'https://prizes.gamee.com/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-install-uuid': 'a5658ae5-54e4-447c-a8cc-d1859be596ea'}
        Data = '{"jsonrpc":"2.0","id":"dailyReward.getPrizes","method":"dailyReward.getPrizes","params":{}}'

        try:
            return post(self.Domain, headers=Headers, data=Data, proxies=self.Proxy).json()['result']['dailyReward']['spinsCountAvailable']
        except:
            return None



    def Claim_WP(self, ID: str) -> bool:
        '''Сбор WP'''

        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'authorization': f'Bearer {self.Token}', 'client-language': 'en', 'content-type': 'text/plain;charset=UTF-8', 'origin': 'https://prizes.gamee.com', 'priority': 'u=1, i', 'referer': 'https://prizes.gamee.com/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-install-uuid': '7a971f19-6698-482e-8083-63882c87ee36'}
        Data = '{"jsonrpc":"2.0","id":"miningEvent.startSession","method":"miningEvent.startSession","params":{"miningEventId":' + ID + '}}'

        try:
            post(self.Domain, headers=Headers, data=Data, proxies=self.Proxy).json()['result']
            self.Logging('Success', self.Name, '🟢', 'Монеты собраны!')
            return True
        except:
            self.Logging('Error', self.Name, '🔴', 'Монеты не собраны!')
            return False



    def WP_Mining_Update(self, ID: str) -> bool:
        '''Апгрейд для майнинга WP'''

        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9', 'authorization': f'Bearer {self.Token}', 'client-language': 'en', 'content-type': 'text/plain;charset=UTF-8', 'origin': 'https://prizes.gamee.com', 'priority': 'u=1, i', 'referer': 'https://prizes.gamee.com/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-install-uuid': 'a5658ae5-54e4-447c-a8cc-d1859be596ea'}
        Data = '{"jsonrpc":"2.0","id":"miningEvent.upgrade","method":"miningEvent.upgrade","params":{"miningEventId":' + ID + ',"upgrade":"storage"}}'

        try:
            post(self.Domain, headers=Headers, data=Data, proxies=self.Proxy).json()['result']
            return True
        except:
            return False



    def Spin(self) -> None:
        '''Прокрутка всех доступных спинов'''

        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9', 'authorization': f'Bearer {self.Token}', 'client-language': 'en', 'content-type': 'text/plain;charset=UTF-8', 'origin': 'https://prizes.gamee.com', 'priority': 'u=1, i', 'referer': 'https://prizes.gamee.com/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-install-uuid': 'a5658ae5-54e4-447c-a8cc-d1859be596ea'}
        Data = '[{"jsonrpc":"2.0","id":"dailyReward.claimPrize","method":"dailyReward.claimPrize","params":{}},{"jsonrpc":"2.0","id":"dailyReward.getPrizes","method":"dailyReward.getPrizes","params":{}}]'

        try:
            HPV = post(self.Domain, headers=Headers, data=Data, proxies=self.Proxy).json()[0]['result']['reward']

            Prize = ''
            if HPV['type'] == 'money':
                Prize = f'{HPV["usdCents"] / 100:,.2f}$'
            else:
                Prize = f'{HPV["tickets"]} билетов'

            self.Logging('Success', self.Name, '🟢', f'Вращение произведено! Получено: {Prize}')
        except:
            self.Logging('Error', self.Name, '🔴', 'Вращение не произведено!')



    def Unblock(self, ID: str, PASS: str) -> bool:
        '''Ввод пароля для разблокировки фарма WP'''

        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'authorization': f'Bearer {self.Token}', 'client-language': 'en', 'content-type': 'text/plain;charset=UTF-8', 'origin': 'https://prizes.gamee.com', 'priority': 'u=1, i', 'referer': 'https://prizes.gamee.com/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-install-uuid': '7a971f19-6698-482e-8083-63882c87ee36'}
        Data = '{"jsonrpc":"2.0","id":"miningEvent.startSession","method":"miningEvent.startSession","params":{"miningEventId":' + ID + ',"code":"' + PASS + '"}}'

        try:
            post(self.Domain, headers=Headers, data=Data, proxies=self.Proxy).json()['result']
            return True
        except:
            return False



    def Run(self) -> None:
        '''Активация бота'''

        while True:
            try:
                if self.Token: # Если аутентификация успешна

                    Event_INFO = self.Get_EventID() # Получение информации о текущем майнинг ивенте
                    if Event_INFO['Status']: # Если ID и пароль ивента получены
                        ID, PASS = Event_INFO['ID'], Event_INFO['PASS']
                        INFO = self.Get_Info(ID)

                        if INFO['WP_INFO']: # Если майнинг разблокирован
                            self.Logging('Success', self.Name, '💰', f'Текущий баланс: {self.Get_Info(ID)["Dollars"]}$, {self.Get_Info(ID)["WPs"]} WP и {self.Get_Info(ID)["Tickets"]} билетов')

                            if INFO['Mining_Over']: # Проверка окончания майнинга WP, и дальнейший его запуск
                                if self.Claim_WP(ID):
                                    self.Logging('Success', self.Name, '💰', f'Баланс после сбора WP: {self.Get_Info(ID)["Dollars"]}$, {self.Get_Info(ID)["WPs"]} WP и {self.Get_Info(ID)["Tickets"]} билетов')
                                    sleep(randint(33, 103)) # Промежуточное ожидание

                        else: # Если майнинг заблокирован
                            if self.Unblock(ID, PASS): # Ввод пароля, в случае блокировки
                                self.Logging('Success', self.Name, '🟢', 'Фарминг разблокирован!')
                                sleep(randint(33, 103)) # Промежуточное ожидание

                        if UPDATE: # Попытка апгрейда для майнинга WP
                            if self.WP_Mining_Update(ID):
                                self.Logging('Success', self.Name, '🟢', 'Апгрейд майнинга успешен!')
                                sleep(randint(33, 103)) # Промежуточное ожидание

                    else: # Если не удалось получить ID и пароль ивента
                        self.Logging('Warning', self.Name, '🔴', 'Не удалось получить информацию об ивенте!')


                    # Получение кол-ва доступных спинов и запуск их прокрутки
                    Get_Spins = self.Get_Info_Spin()
                    if Get_Spins > 0:
                        self.Logging('Success', self.Name, '🎮', f'Спинов доступно: {Get_Spins}!')
                        for _ in range(Get_Spins):
                            self.Spin()
                            sleep(randint(12, 23))

                        INFO = self.Get_Info(ID)
                        self.Logging('Success', self.Name, '💰', f'Баланс после игр: {INFO["Dollars"]}$, {INFO["WPs"]} WP и {INFO["Tickets"]} билетов')


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

    for Account, URL in HPV_Get_Accounts().items():
        if Proxy:
            Proxy = cycle(Proxy)
            Thread(target=Start_Thread, args=(Account, URL, next(Proxy),)).start()
        else:
            Thread(target=Start_Thread, args=(Account, URL,)).start()


