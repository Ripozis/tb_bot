# -*- coding: utf-8 -*-
import json
import os
import random
import sqlite3 as sq
import time
from datetime import datetime, timedelta
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
from loguru import logger

logger.add("logger/main_log.log", format="{time:YYYY-MM-DD at HH:mm:ss}|{level}|{message}", rotation="100 MB", compression="zip")
# ----------------
# Функция запуска парсера
# search_reddit()
# ----------------

pbl_path_img = r'/root/tb_bot/images'

# ----------------
# Имя сессии pyrogram
app = Client("my_account")
app.start()

# ----------------
# функция Отправки на dev поста с пометкой
@logger.catch
def send_post_dev(app):
    post_on_pub = post_on_publik()
    logger.info("Получаем посты для публикации")
    # post_on_pub = post_on_pub[0]
    row = len(post_on_pub)
    def on_publik (app,row, post_on_pub):
            for row in post_on_pub:
                title = (row[0]) # из списка выбераем 1е значенеие - title
                path_file = str(row[1])
                id_post = int((row[2]))

                # Отправка анимации 
                print(id_post)
                os.chdir(pbl_path_img)
                if '.gif' in path_file:
                    logger.success("Будем отправлять анимацию " + str(path_file))
                    print("анимация и пнг")
                    try: 
                        logger.debug("Формируем собщение поста с id: " + str(id_post))
                        app.send_animation("Testyfakt", path_file, title)
                        logger.success("Собщение сформировано")
                        attr_dev(id_post)
                        os.remove(pbl_path_img + '/' + path_file) # удаление файла
                        logger.success("Файл " + str(path_file) + " удален с диска")
                    except Exception as ex:
                        logger.exception("Ошибка с анимацией для DEV" +  str(path_file) + " id: " + str(id_post))
                        print("Ошибка с анимацией для DEV" + path_file)
                        print(ex)
                        content_error_update(id_post) #Помечаем пост с ошибкой в контенте

                elif '.jpg' in path_file or '.png' in path_file or '.jpeg' in path_file:
                    logger.success("Будем отправлять изображение " + str(path_file))
                    try:
                        logger.debug("Формируем собщение поста с id: " + str(id_post))
                        
                        app.send_photo("Testyfakt", path_file, title)
                        logger.success("Собщение сформировано")
                        attr_dev(id_post)
                        os.remove(pbl_path_img + '/' + path_file) # удаление файла
                        logger.success("Файл " + str(path_file) + " удален с диска")
                    except Exception as ex:
                        logger.exception("Ошибка с картинкой для DEV" +  str(path_file) + " id: " + str(id_post))
                        print("Ошибка с картинкой для DEV" + path_file)
                        print(ex)
                        content_error_update(id_post) #Помечаем пост с ошибкой в контенте

                elif '.mp4' in path_file:
                    logger.success("Будем отправлять видео" + str(path_file))
                    print("Отправка видео")
                    try:
                        logger.debug("Формируем собщение поста с id: " + str(id_post))
                        
                        app.send_video("Testyfakt", video=path_file, caption=title)
                        logger.success("Собщение сформировано")
                        attr_dev(id_post)
                        os.remove(pbl_path_img + '/' + path_file) # удаление файла
                        logger.success("Файл " + str(path_file) + " удален с диска")
                    except Exception as ex:
                        logger.exception("Ошибка с видео для DEV" +  str(path_file) + " id: " + str(id_post))
                        print("Ошибка с видео для DEV" + path_file)
                        print(ex)
                        content_error_update(id_post) #Помечаем пост с ошибкой в контенте
                
    on_publik (app, row, post_on_pub)

# # # ----------------

# # # ----------------
# # #запуск функции на отправку постаста кажды ... минут (https://tirinox.ru/schedule-cron-python/)
# # schedule.every().hour.do(send_post_dev, app) #Отправки на dev поста с пометкой ~каждый час

# # # -----------Расписание работы 
# schedule.every(1).minutes.do(publication_attr, app) #Запуск функц установки признака публикации ~каждые 30мин час
# schedule.every(2).minutes.do(moder_post) #Публикация в моджерку

 # Функция для создания потоков на расписание 
# def run_threaded(job_func):
#     job_thread = threading.Thread(target=job_func, args=(app,))
#     job_thread.start()

#  # Функция для создания потоков на парсинг
# def run_threaded_pars(job_func1):
#     job_thread = threading.Thread(target=job_func1)
#     job_thread.start()

#При многопотоке появляеться ошибка
#in _wait_for_tstate_lock     elif lock.acquire(block, timeout):

#Отправки на dev поста с пометкой ~каждый час
# # schedule.every().hour.do(send_post_dev, app) #Отправки на dev поста с пометкой ~каждый час
#schedule.every(1).minutes.do(send_post_dev, app)

schedule.every().day.at("02:30").do(search_reddit)
schedule.every().day.at("06:30").do(search_reddit)
schedule.every().day.at("07:30").do(send_post_dev, app)
schedule.every().day.at("08:00").do(send_post_dev, app)
schedule.every().day.at("09:00").do(send_post_dev, app)
schedule.every().day.at("09:30").do(search_reddit)
schedule.every().day.at("10:00").do(send_post_dev, app)
schedule.every().day.at("11:00").do(send_post_dev, app)
schedule.every().day.at("12:00").do(send_post_dev, app)
schedule.every().day.at("13:00").do(send_post_dev, app)
schedule.every().day.at("13:30").do(search_reddit)
schedule.every().day.at("14:00").do(send_post_dev, app)
schedule.every().day.at("15:00").do(send_post_dev, app)
schedule.every().day.at("16:00").do(send_post_dev, app)
schedule.every().day.at("16:30").do(search_reddit)
schedule.every().day.at("17:00").do(send_post_dev, app)
schedule.every().day.at("18:00").do(send_post_dev, app)
schedule.every().day.at("19:00").do(send_post_dev, app)
schedule.every().day.at("19:30").do(search_reddit)
schedule.every().day.at("20:00").do(send_post_dev, app)
schedule.every().day.at("21:00").do(send_post_dev, app)
schedule.every().day.at("22:00").do(send_post_dev, app)
schedule.every().day.at("23:00").do(send_post_dev, app)
schedule.every().day.at("00:30").do(search_reddit)

#schedule.every(3).minutes.do(search_reddit) #Запуск парсера ~каждые 30 мин

while True:
    schedule.run_pending()
    time.sleep(4)
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
