<div align="center">

![Screenshot_1](https://telegra.ph/file/894d3309c99cfcf28ceaa.png)

# 🟣 Gamee AutoBot /// HPV /// V1.07 🟣

| **Возможности**                                                    | **Поддерживается**  |
|----------------------------------------------------------------|:---------------:|
| **Многофункциональный** — *выполняет все те же действия, что вы делали бы руками:*<br>**—** *Разблокировка майнинга при его блокировке*;<br>**—** *Сбор WP при разблокированном майнинге*;<br>**—** *Попытка апгрейда для майнинга WP*;<br>**—** *Получение информации о наличии спинов*;<br>**—** *Прокрутка всех доступных спинов*;<br>**—** *Получение информации о наличии игр*🆕;<br>**—** *Прохождение всех доступных игр*🆕;<br>**—** *Ожидание от 30 до 60 минут*;<br>**—** *Повторение действий через 30-60 минут*. |✅|
| **Кроссплатформенный** — *скрипт можно запускать на любой платформе, будь то Windows, Linux или Android. Это также позволяет удобно установить его на сервер и просто наблюдать за процессом фарма* |✅|
| **Многопоточный** — *благодаря использованию технологии потоков, скрипт позволяет одновременно фармить на нескольких аккаунтах. Ограничений по количеству добавленных аккаунтов нет* |✅|
| **Proxy** — *скрипт поддерживает добавление неограниченного количества прокси-серверов. Даже если количество прокси меньше, чем количество аккаунтов, они будут равномерно распределены между всеми аккаунтами после проверки на валидность. Хотя использование прокси не является обязательным, настоятельно рекомендуется их использование для предотвращения блокировки в Gamee (не в Telegram)* |✅|
| **Точечная настройка** — *скрипт позволяет включать или отключать автообновление для майнинга WP. По умолчанию установлено значение True, что означает включение автообновления. Однако вы можете отключить его, установив в конфигурации значение False. Также можно настроить желаемое количество монет, получаемых за одну игру. В конфигурации можно указать диапазон чисел, в пределах которого будут начисляться WP и COIN поинты. По умолчанию установлено значение от 159 до 357. Увеличивать максимальное значение выше 550 не рекомендуется! В лучшем случае монеты не будут засчитаны на баланс, в худшем — ваш аккаунт может быть заблокирован в Gamee (не в Telegram)* |✅|
| **Добавление аккаунтов** — *благодаря моей уникальной технологии, в отличие от других подобных скриптов, вам не нужно возиться с API_ID и API_HASH для каждого аккаунта. Это значительно снижает порог входа, защищает ваш Telegram аккаунт от бана и позволяет сэкономить драгоценное время. Чтобы добавить аккаунт, достаточно указать специальную ссылку, полученную от бота. Подробная инструкция приведена ниже* |✅|
| **Защита сибилла (ботовода)** — *в мире, где проекты вроде Gamee стремятся блокировать всех ботоводов, моя забота о вашей безопасности не осталась незамеченной. Реализованный с использованием всей мощи Python, скрипт разработан таким образом, чтобы минимизировать риск блокировки фермы аккаунтов. Каждый аккаунт после инициализации получает уникальный User-Agent, делая его невозможным для идентификации как бота. Дополнительно, скрипт случайным образом варьирует время выполнения каждого действия, чтобы симулировать натуральное поведение. И, конечно, есть поддержка прокси для максимальной анонимности и защиты. Вы можете не использовать их, но я настоятельно рекомендую это для вашей безопасности* |✅|

**<br>Данный скрипт предназначен исключительно для образовательных целей. Пользуйтесь им ответственно и избегайте злоупотреблений. Вы полностью несете ответственность за всевозможные последствия его использования, включая риск блокировки аккаунта в боте Gamee (не в Telegram)!**
***
</div>

# <br><br>🟡 Обновлено — 31.07.2024 🟡
- **Исправлен баг с прохождением игр. Теперь игры проигрываются на 100%.<br><br>**
- **Обновление за 28.07.2024:**
- - ***Удалён конфиг с ID эвента;<br>***
- - ***Обновлены все запросы;<br>***
- - ***Обновлён прокрут спина и исправлен баг;<br>***
- - ***Обновлён клейм WP;<br>***
- - ***Обновлён апгрейд майнера WP;<br>***
- - ***Изменена аутентификация;<br>***
- - ***Добавлено прохождение игры;<br>***
- - ***Другие мелкие но немаловажные изменения.***<br><br>
- **Обновление за 23.07.2024:**
- - ***Добавлен вывод ошибки о том, что ссылки в конфиге указаны не верно;<br>***
- - ***Добавлено 7,500 User Agent.<br>***

# <br><br>🧬 Предварительная настройка
- **Linux**
  - ```
    apt update && apt upgrade -y
    ```
  - ```
    apt install -y python3 git
    ```
  - ```
    git clone https://github.com/A-KTO-Tbl/Gamee
    ```
  - ```
    pip3 install -r Gamee\Core\Tools\requirements.txt
    ```
- **Windows**
  - Для начала нужно установить [Python](https://www.python.org/downloads/release/python-3103/) (не рекомендуется версию выше 3.10.3) и [Git](https://git-scm.com/download/win);
  - Создаём папку в любом месте, например на рабочем столе. После чего открываем её;
  - В верхней части проводника жмём по пути ***([СКРИНШОТ](https://telegra.ph/file/f4695bbc6a7c4e142c758.jpg))***, и вписываем "*CMD*";
  - Запустится CMD в текущей директории. Далее просто вводим следующие команды:
    - ```
      git clone https://github.com/A-KTO-Tbl/Gamee
      ```
    - ```
      pip install -r Gamee\Core\Tools\requirements.txt
      ```
- **Android**
  - Для вашего удобства рекомендуется выполнить первоначальную настройку скрипта на ПК. После этого загрузите настроенную версию скрипта на GitHub и клонируйте её в [Termux](https://github.com/termux/termux-app/releases). Затем просто запустите скрипт командой:
    - ```
      python HPV_Gamee.py
      ```

# <br>🌐 Настройка Proxy
- Чтобы добавить прокси, перейдите в раздел ***Core* > *Proxy*** и откройте файл ***HPV_Proxy.txt***. Далее просто введите свои прокси в формате одна строка — один прокси. Поддерживаются протоколы SOCKS5 и HTTPS. Пример добавления прокси можно найти в той же папке ***([СКРИНШОТ](https://telegra.ph/file/828b1caf4e50e522ffb9e.jpg))***.

# <br>⚙️ Настройка конфига
- Вы можете включить или выключить апгрейд майнинга WP. Для изменения конфигурации перейдите в ***Core > Config*** и откройте ***HPV_Config.py***. Найдите переменную ***UPDATE*** ***([СКРИНШОТ](https://telegra.ph/file/249c22f89dde8b13867c8.png))***. По умолчанию установлено значение ***True***, что является оптимальным решением. Если хотите, вы можете изменить значение на ***False***, чтобы отключить обновления майнинга.
- Помимо этого, вы можете настроить желаемое количество монет, получаемых за игру, указав диапазон чисел в конфигурационном файле. Для этого перейдите в ***Core > Config*** и откройте ***HPV_Config.py***. Найдите две переменные: ***WPs*** и ***COINs***. Первая отвечает за желаемое количество получаемых WP за одну игру, вторая — за желаемое количество получаемых COIN за одну игру. По умолчанию установлено значение ***от 159 до 357***, что является оптимальным. Вы можете изменить этот диапазон, но увеличивать максимальное значение выше 550 не рекомендуется. В лучшем случае монеты не будут засчитаны на баланс, в худшем — ваш аккаунт может быть заблокирован в Gamee (не в Telegram).

# <br>🔰 Добавление аккаунтов
Как упоминалось ранее, для добавления аккаунтов не нужно возиться с **API_ID** и **API_HASH** для каждого из них, что значительно снижает порог входа и экономит ваше время. Всё, что требуется, — это добавить в конфиг специальную ссылку, полученную от бота. Однако, этот процесс доступен только на устройствах Android. Обладателям iPhone придется найти Android-устройство для получения ссылки. **Android - One Love!** Теперь перейдём к делу.

- **Инструкция по получению уникальной ссылки:**
  ***
  **1)** *Перейдите в [бота](https://t.me/gamee/start?startapp=ref_1295320967);*<br>
  **2)** *Введите команду **/start**;*<br>
  **3)** *Нажмите на кнопку **"Крутить"***;<br>
  **4)** *Как только нажали на кнопку, сразу отключите интернет, чтобы mini app запустился, но не успел прогрузиться;*<br>
  **5)** *В результате появится ошибка с заветной ссылкой. Если ссылка не отобразилась, попробуйте без интернета нажать на три точки вверху и выбрать **"Перезагрузить"**. Если ссылка все равно не появилась, повторите этот шаг заново. Важно, чтобы ссылка была очень длинной;*<br>
  **6)** *Скопируйте весь текст ошибки, затем вставьте его в любом чате, и в тексте ошибки найдите нужную ссылку;*<br>
  **7)** *Далее перейдите в **Core > Config** и откройте **HPV_Account.json**;*<br>
  **8)** *В первом ключе введите желаемое имя аккаунта, которое будет отображаться в логах (оптимально использовать юзернейм аккаунта). Желательно писать не более одного слова и на английском языке **([СКРИНШОТ](https://telegra.ph/file/9fea159d1ec26acd6778a.jpg))**;*<br>
  **9)** *Напротив ключа введите полученную ранее ссылку **([СКРИНШОТ](https://telegra.ph/file/e35b6a41d26d55c357a5e.jpg))**;*<br>
  **10)** *Таким образом добавляйте ферму аккаунтов;*<br>
  **11)** *Важно отметить: **ставьте запятые после каждого предпоследнего элемента словаря (т.е. аккаунта), а на последнем элементе запятую ставить не нужно.** В конфиге показан явный пример **([СКРИНШОТ](https://telegra.ph/file/cf351db4e17e353fe6fc9.jpg))**.*
  ***
- **Видео инструкция по получению уникальной ссылки: [СМОТРЕТЬ](https://telegra.ph/file/f8567f9c842ec2f656944.mp4)**

# <br>⚡️ Запуск
- **Linux**
  - ```
    cd Gamee && python3 HPV_Gamee.py
    ```
- **Windows**
  - Запустите ***"[HPV] Start on Windows.bat"***
- **Android**
  - После подготовки скрипта на ПК и клонирования загруженного репозитория с GitHub в [Termux](https://github.com/termux/termux-app/releases), запустите скрипт следующей командой:
    - ```
      cd Gamee && python HPV_Gamee.py
      ```

# <br><br>💎 Дополнительно
- **[Telegram канал](https://t.me/+nXUk0aZ0valjYmFi). Подписка на наш канал — это лучшая поддержка и мотивация для продолжения этого и других проектов! 💜**
- **[Владелец](https://t.me/A_KTO_Tbl)**
- **TON:** ```UQChditl95Hy_kMektYwzpW7Os9OCmyriJaAD0YMdxJREp1s```
- **Base /// BNB Chain /// ETH (EVM):** ```0x4E7Fecf762295CB696e862F4c3a30Ffc586DeDb2```
- **NEAR:** ```a_kto_tbl.near```
- **Tron:** ```TSGP8XnjJ9wFNamYs3k17bN13Vg8WZE55s```
- **Solana:** ```wWMvNzKZFPTr96eGz5hi6aymYsycwvWWrWgHwdXNYPQ```
