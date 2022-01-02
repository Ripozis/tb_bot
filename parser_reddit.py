# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from auth_date import username, password, redit
import time
import random
from sql import create_tbl, recordingDateJson, cur, url_fot_tbl, sql_update, remov, delite_post
from bs4 import BeautifulSoup
import json
from datetime import datetime
import requests
import os
from deep_translator import (GoogleTranslator)
import threading
import schedule

"""test browser"""
# # options
# options = webdriver.ChromeOptions()
# options.add_argument("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36") # Прописываем user agent
# options.add_argument("--disable-blink-features=AutomationControlled") # Отключаем режим веб драйвера
# options.headless = True # Запускаем браузер в фоновом режиме
# s = Service('/home/ily/tb_bot/webdriver/chromedriver')
# browser = webdriver.Chrome(service=s, options=options)
# browser.get("https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html")

# time.sleep(10)
# browser.close()
# browser.quit()

def search_reddit():
    def redit_login(username, password, redit):
        # browser = webdriver.Firefox('/home/ily/tb_bot/webdriver/geckodriver')
        for row in redit:
            redit = row
            options = webdriver.ChromeOptions()
            options.add_argument("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36") # Прописываем user agent
            options.add_argument("--disable-blink-features=AutomationControlled") # Отключаем режим веб драйвера
            options.headless = True # Запускаем браузер в фоновом режиме
            s = Service('/home/ily/tb_bot/webdriver/chromedriver')
            browser = webdriver.Chrome(service=s, options=options)
            # browser = webdriver.Firefox(service=s)
            # browser = webdriver.Chrome(executable_path=r"C:\\Users\\Илья\\Desktop\\tb_bot\\tb_bot\webdriver\\chromedriver.exe") # Указываем путь до веб драйвера
            try: #- это обработчик ошибок
            #Заходим на страницу авторизации
                browser.get('https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2F')
                time.sleep(random.randrange(4, 7))
            #Передаем данные username из файла auth_date
                username_input = browser.find_element_by_name('username')
                username_input.clear()
                username_input.send_keys(username)
                time.sleep(3)
            # Передаем данные password из файла auth_date
                password_input = browser.find_element_by_name('password')
                password_input.clear()
                password_input.send_keys(password)
                password_input.send_keys(Keys.ENTER)
                time.sleep(10)
            #переход по ссылке
                print (redit)
                try:
                    browser.get(f'https://www.reddit.com/r/{redit}.json') #в redit передается значение
                # time.sleep(10)
                # Получает источник текущей страницы html на странице и записываем в переменную
                    html = browser.page_source
                # time.sleep(10)
                # # сохраняем страницу в файл
                    with open('data.html', 'w', encoding='utf=8') as file:
                        file.write(html)
                    browser.close()
                    browser.quit()
                except Exception as ex:
                    print(ex)
                    browser.close()
                    browser.quit()

            except Exception as ex: #При возникновении ошибки, в принте она появиться
                print(ex)
                browser.close()
                browser.quit()
         #подставляет занчение в место {redit}
            with open("data.html") as file:
                src = file.read()
            soup = BeautifulSoup(src, "lxml")
            js = soup.get_text()# выниваем данне json из html

            #####_Создаем data.json по данным из html
            with open("data.json", "w") as file:
                file.write(js)
                dictData = json.loads(js)

            # #####_Вынимаем необходмые данне из data.json 
            with open("data.json") as file:
                datJs = file.read()
            data = json.loads(datJs)
            dictChildren = data['data']
            dist = dictChildren['children']

            # #####_Создаем БД SQL
            create_tbl()
            print("Начинаем писать в БД из паблика " + redit)

            #Читаем данные из переменой dist и пишем их в таблицу
            for item in dist:
                postOffice = item['data']
                # print(postOffice)
                # print(postOffice.keys())
                created = (postOffice['created']) # дата создания поста
                creadat = (datetime.utcfromtimestamp(created).strftime('%Y-%m-%d %H:%M:%S'))
                title = (postOffice['title'])
                title_ru = GoogleTranslator ( source = 'auto' , target = 'ru' ).translate(title)
                url = (postOffice['url'])
                likes = (postOffice['score']) # Лайки 
                format_cont = postOffice.get("post_hint") # Формат медиа
                preview = postOffice.get("preview")
                # Цикл для исключения пустых результатов
                if preview is not None:
                    reddit_video_preview = preview.get("reddit_video_preview")
                    if reddit_video_preview is not None:
                        url = reddit_video_preview.get("fallback_url")
                secure_media = postOffice.get("secure_media")
                if secure_media is not None:
                    reddit_video = secure_media.get("reddit_video")
                    if reddit_video is not None:
                        fallback_url = reddit_video.get("fallback_url")
                        url=fallback_url.replace("?source=fallback", "")
                        # print(url + " " + title) # Cсылка на видео
                #####_Записываем таблицу SQL parser значения из переменных (title, url)
                recordingDateJson(title, url, creadat, title_ru,format_cont,likes)
            print("Закончили писать в БД из паблика " + redit)
            # Удаление файлов из БД помеченных на удаление 
            print("Удаление файлов из БД помеченных на удаление")
            r = remov()
            for row in r:
                path_file = (row[0])
                id_post = (row[1])
                try:
                    if 'None' in path_file:
                        print("Нет пути к файлу" + path_file)
                    else:
                        print("Файл на удаление" + path_file)
                        os.remove(r'/home/ily/tb_bot/images' + path_file) # удаление файла
                        print("Файл удален")
                        delite_post(id_post)
                except Exception as ex:
                    print(ex)

    redit_login(username, password, redit)
# search_reddit()