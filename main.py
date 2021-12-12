# -*- coding: utf-8 -*-
import json
import os
import random
import sqlite3 as sq
import time
from datetime import datetime, timedelta
# import datetime as DT
# import requests
# from bs4 import BeautifulSoup
from pyrogram import Client
from pyrogram.types import InputMediaPhoto, InputMediaVideo
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import schedule
from auth_date import password, username
from parser_reddit import search_reddit
from sql import (attr_dev, create_tbl, cur, last_post, post_on_publik,
                 publication_attribute_update, read_tbl, recordingDateJson,
                 sql_update, url_fot_tbl,content_error_update,for_editing,to_remove)
import threading
from queue import Queue
# ----------------
# Функция запуска парсера
# search_reddit()
# ----------------


# ----------------
# # #имя сессии pyrogram
app = Client("my_account")
app.start()
# ----------------


# ----------------
# Функция для публикации поста в модерку
# def moder_post():
#     re = read_tbl() 
#     row = len(re) # Считаем количество количество элементов в списке
#     print(row) 
#     # Проходим в цикле по всем элементам списка для публикации в модерку
#     for row in re:
#         title = (row[0]) # из списка выбераем 1е значенеие - title
#         url = (row[1])  # из списка выбераем 2е значенеие - url
#         path_file = (row[2])
#         id_post = str((row[3]))
#         os.chdir(r'C:\bottelegramm\images')
#         print(path_file)

#         # Отправка анимации 
#         if '.gif' in path_file:
#             print("анимация и пнг")
#             try: 
#                 app.send_animation("scrapitir_bot", path_file, title + '\n' + 'Post№: ' + id_post)
#             except Exception as ex:
#                 print("Ошибка с анимацией для модерки" + path_file)
#                 print(ex)
#                 content_error_update(id_post) #Помечаем пост с ошибкой в контенте

#         elif '.jpg' in path_file or '.png' in path_file or '.jpeg' in path_file:
#             try:
#                 app.send_photo("scrapitir_bot", path_file, title + '\n' + 'Post№: ' + id_post)
#             except Exception as ex:
#                 print("Ошибка с картинкой для модерки" + path_file)
#                 print(ex)
#                 content_error_update(id_post) #Помечаем пост с ошибкой в контенте

#         elif '.mp4' in path_file:
#             print("Отправка видео")
#             try:
#                 app.send_video("scrapitir_bot", video=path_file, caption=title + '\n' + 'Post№: ' + id_post)
#             except Exception as ex:
#                 print("Ошибка с видео для модерки" + path_file)
#                 print(ex)
#                 content_error_update(id_post) #Помечаем пост с ошибкой в контенте
# # ----------------

# # ----------------
# # функция установки признака публикации 
# # цикл для прослушки чата по id/
# def publication_attr(app):
#         # while last_post() > 0: # Проверяем признак публикации у последнего поста
#     # for i in range(6):
#     for message in app.search_messages("me",query="id/", limit=5):
#         search_id =(message.text)
#         id_post = search_id.split('/')[-1]  # Вынемаем id поста
#         print("Пост на публикацию - " + id_post) # Сделать поиск по полученному id и обновить признак публикации на "1"
#         publication_attribute_update(id_post)
    
#     for message in app.search_messages("me",query="ed/", limit=5):
#         search_id =(message.text)
#         id_post_ed = search_id.split('/')[-1]  # Вынемаем id поста
#         print("Пост на редактирование - " + id_post_ed)
#         for_editing(id_post_ed)
    
#     for message in app.search_messages("me",query="del/", limit=5):
#         search_id =(message.text)
#         id_post_del = search_id.split('/')[-1]  # Вынемаем id поста
#         print("Пост на удаление - " + id_post_del)
#         to_remove(id_post_del)
# ----------------


# ----------------
# функция Отправки на dev поста с пометкой 
def send_post_dev(app):
    post_on_pub = post_on_publik()
    # post_on_pub = post_on_pub[0]
    row = len(post_on_pub)
    def on_publik (app,row, post_on_pub):
            for row in post_on_pub:
                title = (row[0]) # из списка выбераем 1е значенеие - title
                path_file = (row[1])
                id_post = int((row[2]))

                
                # try:
                #     print('Блок отправка сообщений в ДЕВ')
                #     attr_dev(id_post)
                #     app.send_photo("Testyfakt", path_file, title)
                # except:
                #     print("Ошибка при публикации " + path_file)
                        # Отправка анимации 
                print(id_post)
                os.chdir(r'/home/ily/tb_bot/images')
                if '.gif' in path_file:
                    print("анимация и пнг")
                    try: 
                        attr_dev(id_post)
                        app.send_animation("Testyfakt", path_file, title)
                        os.remove('/home/ily/tb_bot/images/'+ path_file) # удаление файла
                    except Exception as ex:
                        print("Ошибка с анимацией для DEV" + path_file)
                        print(ex)
                        content_error_update(id_post) #Помечаем пост с ошибкой в контенте

                elif '.jpg' in path_file or '.png' in path_file or '.jpeg' in path_file:
                    try:
                        attr_dev(id_post)
                        app.send_photo("Testyfakt", path_file, title)
                        os.remove('/home/ily/tb_bot/images/'+ path_file) # удаление файла
                    except Exception as ex:
                        print("Ошибка с картинкой для DEV" + path_file)
                        print(ex)
                        content_error_update(id_post) #Помечаем пост с ошибкой в контенте

                elif '.mp4' in path_file:
                    print("Отправка видео")
                    try:
                        attr_dev(id_post)
                        app.send_video("Testyfakt", video=path_file, caption=title)
                        os.remove('/home/ily/tb_bot/images/'+ path_file) # удаление файла
                    except Exception as ex:
                        print("Ошибка с видео для DEV" + path_file)
                        print(ex)
                        content_error_update(id_post) #Помечаем пост с ошибкой в контенте
                
    on_publik (app,row, post_on_pub)

# # # ----------------

# # # ----------------
# # #запуск функции на отправку постаста кажды ... минут (https://tirinox.ru/schedule-cron-python/)
# # schedule.every().hour.do(send_post_dev, app) #Отправки на dev поста с пометкой ~каждый час

# # # -----------Расписание работы 
# schedule.every(1).minutes.do(publication_attr, app) #Запуск функц установки признака публикации ~каждые 30мин час
# schedule.every(2).minutes.do(moder_post) #Публикация в моджерку

schedule.every(2).minutes.do(send_post_dev, app) #Отправки на dev поста с пометкой ~каждый час
schedule.every(3).minutes.do(search_reddit) #Запуск парсера ~каждые 40 мин

while True:
    schedule.run_pending()
    time.sleep(3)
# # ----------------

# Склеить это пиример https://russianblogs.com/article/21691175263/ с ПРИМЕР 30 https://python.hotexamples.com/ru/examples/schedule/-/run_pending/python-run_pending-function-examples.html

#---------реализация с потоками 
# def run_threaded(job_func):
#     job_thread = threading.Thread(target=job_func)
#     job_thread.start()


# schedule.every(1).minutes.do(run_threaded, search_reddit)
# #---------реализация с потоками 

# def worker_main():
#     while 1:
#         job_func = jobqueue.get()
#         job_func()
#         jobqueue.task_done()
 
# jobqueue = Queue()
 

# # schedule.every(1).minutes.do(jobqueue.put, test) 

# schedule.every(1).minutes.do(jobqueue.put, moder_post()) #Публикация в моджерку
# schedule.every(2).minutes.do(jobqueue.put, publication_attr(app)) #Запуск функц установки признака публикации ~каждые 30мин час
# schedule.every(3).minutes.do(jobqueue.put, send_post_dev(app)) #Отправки на dev поста с пометкой ~каждый час
# schedule.every(1).minutes.do(jobqueue.put, search_reddit()) #Запуск парсера ~каждые 40 мин


# worker_thread = threading.Thread(target=worker_main)
# worker_thread.start()
