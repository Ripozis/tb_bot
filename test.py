
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from auth_date import username, password, redit
import time
import random
from sql import create_tbl, recordingDateJson, cur, url_fot_tbl, sql_update, remov, delite_post
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
from deep_translator import (GoogleTranslator)
from loguru import logger

# Тест парсера
logger.add("/root/tb_bot/logger/parser_log.log", format="{time:YYYY-MM-DD at HH:mm:ss}|{level}|{message}", rotation="100 MB", compression="zip")

# prs_path_img = r'/root/tb_bot/images/'
# prs_path_driver = str(r'/root/tb_bot/webdriver/chromedriver')
# prs_path_html = r'/root/tb_bot/logger/data.html'
# prs_path_json = r'/root/tb_bot/logger/data.json'

prs_path_img = str(r'C:\\Users\\Илья\\Desktop\\tb_bot\\tb_bot\\images\\')
prs_path_driver = str(r'C:\\Users\\Илья\\Desktop\\tb_bot\\tb_bot\\chromedriver')
prs_path_html = str(r'C:\\Users\\Илья\\Desktop\\tb_bot\\tb_bot\\logger\\data.html')
prs_path_json = str(r'C:\\Users\\Илья\\Desktop\\tb_bot\\tb_bot\\logger\\data.json')


@logger.catch
def search_reddit():
    def redit_login(username, password, redit):
        # browser = webdriver.Firefox('/home/ripo/tb_bot/webdriver/geckodriver')
        options = webdriver.ChromeOptions()
        options.add_argument("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36") # Прописываем user agent
        options.add_argument("--disable-blink-features=AutomationControlled") # Отключаем режим веб драйвера
        # options.add_argument("--no-sandbox")
        # options.headless = True # Запускаем браузер в фоновом режиме
        s = Service(prs_path_driver)
        # browser = webdriver.Chrome(service=s, options=options)
        logger.success("Определены настройки веб драйвера")
        # browser = webdriver.Firefox(service=s)
        browser = webdriver.Chrome(executable_path=r"C:\\Users\\Илья\\Desktop\\tb_bot\\tb_bot\webdriver\\chromedriver.exe", options=options) # Указываем путь до веб драйвера
        #Заходим на страницу авторизации
        logger.debug("Логинимся на reddit")
        browser.get('https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2F')
        time.sleep(random.randrange(4, 7))
        #Передаем данные username из файла auth_date
        username_input = browser.find_element(By.NAME,'username')
        username_input.clear()
        username_input.send_keys(username)
        time.sleep(3)
        # Передаем данные password из файла auth_date
        password_input = browser.find_element(By.NAME,'password')
        password_input.clear()
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(random.randrange(4, 10))
        logger.success("Учпешно залогинились")
        for row in redit:
            redit = row
            logger.info("Получен список каналов")
            try: #- это обработчик ошибок
            #переход по ссылке
                logger.debug("Переходим в канал " + str(redit))
                # print (redit)
                try:
                    browser.get(f'https://www.reddit.com/r/{redit}.json') #в redit передается значение
                    logger.success("Зашли в канал " + str(redit) + " и сформировали json")
                    time.sleep(3)
                # Получает источник текущей страницы html на странице и записываем в переменную
                    html = browser.page_source
                    # browser.close()
                    # browser.quit()
                # time.sleep(10)
                # # сохраняем страницу в файл
                    with open(prs_path_html, 'w', encoding='utf=8') as file:
                        file.write(html)
                    logger.success("Завершили скачивание из канала " + str(redit))
                except Exception as ex:
                    logger.exception("Ошибка при формировани файла data.html")
                    print(ex)
                    # browser.close()
                    # browser.quit()

            except Exception as ex: #При возникновении ошибки, в принте она появиться авторизации
                logger.exception("Ошибка при авторизации")
                print(ex)
                browser.close()
                browser.quit()

            logger.info("Вынимаем данне json из html")
            with open(prs_path_html) as file:
                src = file.read()
            soup = BeautifulSoup(src, "lxml")
            js = soup.get_text()# выниваем данне json из html

            #####_Создаем data.json по данным из html
            with open(prs_path_json, "w") as file:
                file.write(js)
                dictData = json.loads(js)

            # #####_Вынимаем необходмые данне из data.json 
            with open(prs_path_json) as file:
                datJs = file.read()
            data = json.loads(datJs)
            dictChildren = data['data']
            dist = dictChildren['children']
            logger.success("Завершили формирование Json")
            # #####_Создаем БД SQL
            #create_tbl()
            # print("Начинаем писать в БД из паблика " + redit)
            logger.info("Начинаем писать в БД из паблика " + str(redit))
            #Читаем данные из переменой dist и пишем их в таблицу
            for item in dist:
                postOffice = item['data']
                logger.info("Пполучили из паблика" + str(redit))
                # print(postOffice)
                print(postOffice.keys())
            #     created = (postOffice['created']) # дата создания поста
            #     creadat = (datetime.utcfromtimestamp(created).strftime('%Y-%m-%d %H:%M:%S'))
            #     date_publication = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #     title = (postOffice['title'])
            #     title_ru = GoogleTranslator ( source = 'auto' , target = 'ru' ).translate(title)
            #     url = (postOffice['url'])
            #     likes = (postOffice['score']) # Лайки 
            #     format_cont = postOffice.get("post_hint") # Формат медиа
            #     preview = postOffice.get("preview")
            #     tred_red = redit
            #     # Цикл для исключения пустых результатов None
            #     if preview is not None:
            #         reddit_video_preview = preview.get("reddit_video_preview")
            #         if reddit_video_preview is not None:
            #             url = reddit_video_preview.get("fallback_url")
            #     secure_media = postOffice.get("secure_media")
            #     if secure_media is not None:
            #         reddit_video = secure_media.get("reddit_video")
            #         if reddit_video is not None:
            #             fallback_url = reddit_video.get("fallback_url")
            #             url=fallback_url.replace("?source=fallback", "")
            #             # print(url + " " + title) # Cсылка на видео
            #     #####_Записываем таблицу SQL parser значения из переменных (title, url)
            #     recordingDateJson(title, url, creadat, date_publication, title_ru, format_cont, likes, tred_red)
            logger.success("Закончили писать в БД из паблика " + str(redit))
        browser.close()
        browser.quit()
    redit_login(username, password, redit)
search_reddit()