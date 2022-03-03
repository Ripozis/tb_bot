# -*- coding: utf-8 -*-
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message,\
    InlineKeyboardButton, InlineKeyboardMarkup, user
from aiogram.utils.callback_data import CallbackData
from sql import read_tbl,moder_msgid,publication_attribute_update,to_remove,content_error_update,sql_update, post_on_publik_all,for_editing
import os
import time
from pyrogram import Client, filters
import requests
from loguru import logger
from auth_date import token
import subprocess

logger.add("logger/bot_log.log", format="{time:YYYY-MM-DD at HH:mm:ss}|{level}|{message}", rotation="100 MB", compression="zip")
bot = Bot(token=token)
dp =Dispatcher(bot)


@logger.catch
@dp.message_handler(commands="start")
async def start(message: types.Message):
    ### Объединение кнопок в список
    userid = int(message.from_user.id)

    if 467601941 == userid:
        logger.debug("Запуск бота под админом")
        start_buttons = ["Пост на одобрение", "Все посты на публикацию"]
        keyboard =types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)
        await message.answer("Бот готов к работе 👍", reply_markup=keyboard)
    else:
        await message.answer("Уходи))")


#Вывод клавы
@logger.catch
@dp.message_handler(Text(equals="Пост на одобрение"))
async def test_message(message: types.Message):
    # await message.answer('Тут должен быть текст поста', reply_markup=lnkb)
    re = read_tbl() 
    #row = len(re) # Считаем количество количество элементов в списке
    #print(row) 
    # Проходим в цикле по всем элементам списка для публикации в модерку
    logger.debug("Получены данные из БД:" + str(re))
    for row in re:
        title = (row[0]) # из списка выбераем 1е значенеие - title
        url_link = (row[1]) # из списка выбераем 2е значенеие - url
        id_post = str((row[3]))
        # Выполняем скачивание файла
        # Сделать проверку на наличеее в ссылке .jpeg, .png, .jpg или .mp4. Возможно в самом парсере (?)
        lin = url_link.split('/')[-1] #выявляет по слешу название файла
        lin = str(id_post) + lin # добавляем id в название файла
        path_file = str(lin)
        logger.debug("Файл на загрузку: " + str(path_file))
        
        def content_upload_img(url_link,lin,path_file):
            """Функция загрузки контента кроме видео"""
            r = requests.get(url_link, allow_redirects=True)
            # os.chdir(r'C:\\Users\\Илья\\Desktop\\tb_bot\\tb_bot\\images') # для винды
            os.chdir(r'/home/ripo/tb_bot/images') # для сервера
            open(lin, 'wb').write(r.content)
            sql_update(url_link, path_file)
        
        def content_upload_video(url_link,id_post):
            """Функция загрузки видео и склейки с аудио"""
            # os.chdir(r'C:\\Users\\Илья\\Desktop\\tb_bot\\tb_bot\\images') # для винды
            os.chdir(r'/home/ripo/tb_bot/images') # для сервера
            #print(lin)
            #open(lin, 'wb').write(r.content)
            print(url_link)
            dash_url = url_link
            #headers = {'User-Agent':'Mozilla/5.0'}
            title = 'video'
            dash_url = url_link[:int(dash_url.find('DASH')) + 4]
            print("Наполнение dash_url: " + dash_url)
            video_url = f'{url_link}'    # this URL will be used to download the video
            print(video_url)
            audio_url = f'{dash_url}_audio.mp4'    # this URL will be used to download the      audio part
            print(audio_url)
            # path_video = r'C:\\Users\\Илья\\Desktop\\tb_bot\\tb_bot\\images\\' + f'{id_post}_video.mp4' # для винды 
            path_video = r'/home/ripo/tb_bot/images/' + f'{id_post}_video.mp4' # для сервера
            if os.path.exists(path_video):
                print("файл был ранее скачан")
            else:    
                with open(f'{id_post}_{title}_video.mp4','wb') as file:
                        print('Downloading Video...',end='',flush = True)
                        response = requests.get(video_url,allow_redirects=True)
                        if(response.status_code == 200):
                            file.write(response.content)
                            print('\rVideo Downloaded...!')
                        else:
                            print('\rVideo Download Failed..!')
                            logger.exception("rVideo Download Failed")
                            content_error_update(id_post)
                with open(f'{id_post}_{title}_audio.mp4','wb') as file:
                        print('Downloading Audio...',end = '',flush = True)
                        response = requests.get(audio_url,allow_redirects=True)
                        if(response.status_code == 200):
                            file.write(response.content)
                            print('\rAudio Downloaded...!')
                            print("Идет склейка ")
                            subprocess.call(['ffmpeg','-i',f'{id_post}_{title}_video.mp4','-i',f'{id_post}_{title}_audio.mp4','-map','0:v', '-map','1:a','-c:v','copy',f'{id_post}_{title}.mp4'])
                            path_file = f'{id_post}_{title}.mp4'
                            sql_update(url_link, path_file)
                        else:
                            print('\rAudio Download Failed..!')
                            time.sleep(5)
                            logger.exception("Audio Download Failed")
                            # os.rename(r'C:\\Users\\Илья\\Desktop\\tb_bot\\tb_bot\\images\\' + f'{id_post}_{title}_video.mp4',r'C:\\Users\\Илья\\Desktop\\tb_bot\\tb_bot\\images\\' +  f'{id_post}_{title}.mp4') # для винды 
                            os.rename(r'/home/ripo/tb_bot/images/' + f'{id_post}_{title}_video.mp4',r'/home/ripo/tb_bot/images/' +  f'{id_post}_{title}.mp4') # для сервера
                            path_file = f'{id_post}_{title}.mp4'
                            sql_update(url_link, path_file)
        
            # file_path_video = r'C:\\Users\\Илья\\Desktop\\tb_bot\\tb_bot\\images\\' + f'{id_post}_{title}_video.mp4' # для винды 
            file_path_video = r'/home/ripo/tb_bot/images/' + f'{id_post}_{title}_video.mp4' # для сервера
            # file_path_audio = r'C:\\Users\\Илья\\Desktop\\tb_bot\\tb_bot\\images\\' + f'{id_post}_{title}_audio.mp4' # для винды 
            file_path_audio = r'/home/ripo/tb_bot/images/' + f'{id_post}_{title}__audio.mp4' # для сервера
            if os.path.exists(file_path_video):
                    print("Файл существует")
                    # os.remove(r'C:\\Users\\Илья\\Desktop\\tb_bot\\tb_bot\\images\\' + f'{id_post}_{title}_video.mp4') # для винды удаляем видео файл
                    os.remove(r'/home/ripo/tb_bot/images/' + f'{id_post}_{title}_video.mp4') # для сервера      
            else:
                print("Файл не существует")
            
            if os.path.exists(file_path_audio):
                # os.remove(r'C:\\Users\\Илья\\Desktop\\tb_bot\\tb_bot\\images\\' + f'{id_post}_{title}_audio.mp4') # для винды
                os.remove(r'/home/ripo/tb_bot/images/' + f'{id_post}_{title}_audio.mp4') # для сервера
            else:
                print("Файл не существует")

            path_file = f'{id_post}_{title}.mp4'
            print(path_file)
            sql_update(url_link, path_file)
            return path_file

        #Проверка контента перед скачиванием 
        logger.info("Проверка контента перед скачиванием: " + str(path_file))
        if '.jpg' in path_file or '.png' in path_file or '.jpeg' in path_file or '. gif' in path_file:
            logger.debug("Подходящий файл для скачивания " + str(path_file))
            content_upload_img(url_link,lin,path_file)
            # path_fi = open('C:/Users/Илья/Desktop/tb_bot/tb_bot/images/' + path_file, 'rb') # для винды
            path_fi = open('/home/ripo/tb_bot/images/' + path_file, 'rb') # для сервера
            logger.debug("Путь файла на загрузку: " + str(path_fi))
            
            if '.gif' in path_file:
                logger.debug("Отправка анимации: " + str(path_file))
                try: 
                    await bot.send_animation(chat_id=message.from_user.id, animation=path_fi, reply_markup=lnkb, caption=title)
                    moder_id = message.message_id + 1
                    moder_msgid(moder_id, id_post)
                    logger.success("В БД отправлен id сообщения: " + str(moder_id))
                except Exception as ex:
                    logger.exception("Ошибка с анимацией для DEV"  + str(path_file))
                    # print("Ошибка с анимацией для DEV" + path_file)
                    # print(ex)
                    content_error_update(id_post) #Помечаем пост с ошибкой в контенте
            elif '.jpg' in path_file or '.png' in path_file or '.jpeg' in url_link:
                logger.debug("Отправка изображения: " + str(path_file))
                try:
                    await bot.send_photo(chat_id=message.from_user.id, photo=path_fi, reply_markup=lnkb, caption=title)
                    moder_id = message.message_id + 1
                    moder_msgid(moder_id, id_post)
                    logger.success("В БД отправлен id сообщения: " + str(moder_id))
                except Exception as ex:
                    logger.exception("Ошибка с картинкой для DEV " + str(path_file))
                    # print("Ошибка с картинкой для DEV" + path_file)
                    # print(ex)
                    content_error_update(id_post) #Помечаем пост с ошибкой в контенте
        elif '.mp4' in path_file:
            path_file = content_upload_video(url_link,id_post)
            print(path_file)
            # path = open('C:/Users/Илья/Desktop/tb_bot/tb_bot/images/' + content_upload_video(url_link,id_post), 'rb') # для винды
            path = open('/home/ripo/tb_bot/images/' + content_upload_video(url_link,id_post), 'rb') # для сервера
            logger.debug("Отправка видео " + str(path_file))

            # print("Отправка видео")
            try:
                await bot.send_video(chat_id=message.from_user.id, video=path, reply_markup=lnkb, caption=title)
                moder_id = message.message_id + 1
                moder_msgid(moder_id, id_post)
                logger.success("В БД отправлен id сообщения: " + str(moder_id))
            except Exception as ex:
                logger.exception("Ошибка с видео для DEV" + str(path_file))
                # print("Ошибка с видео для DEV" + path_file)
                # print(ex)
                content_error_update(id_post) #Помечаем пост с ошибкой в контенте        
        else:
            logger.debug("Неподходящий файл для скачивания " + str(path_file) + str (id_post))
            content_error_update(id_post)

@logger.catch      
@dp.message_handler(Text(equals="Все посты на публикацию"))
async def test_message(message: types.Message):
    post_on_publ_all = post_on_publik_all()
    for row in post_on_publ_all:
        post_on_publ_all = str(row[0])
        logger.success("Получены кол-во постов на публикацию")
        # print(post_on_publ_all)
        await message.answer('Всего постов на публикацию: ' + post_on_publ_all)

## Описание клавиатуры
lnkb = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Опубликовать', callback_data='pudlik'),\
                            InlineKeyboardButton(text='Удалить', callback_data='del'),  InlineKeyboardButton(text='Редактировать', callback_data='editing'))

##действие кнопки при нажатии 'Опубликовать'
@logger.catch
@dp.callback_query_handler(text='pudlik')
async def public_priz(calback : types.CallbackQuery):
    moder_id = calback.message.message_id
    publication_attribute_update(moder_id) # Сделать поиск по полученному id и обновить признак публикации на "1"
    logger.debug("id Сообщения на публикацию: " + str(moder_id))
    # print(moder_id) # id Сообщения на публикацию
    logger.success('Сработала кнопка "Опубликовать"')
    # print('Сработала кнопка "Опубликовать"')
    await calback.answer('Пост принят на публикацию')
    await calback.message.answer('Пост принят на публикацию')

##действие кнопки при нажатии 'Удалить'
@logger.catch
@dp.callback_query_handler(text='del')
async def public_priz(calback : types.CallbackQuery,):
    moder_id = calback.message.message_id
    to_remove(moder_id)
    logger.debug("Пост помечен на удаление: " + str(moder_id))
    # id Сообщения на удаление 
    logger.success('Сработала кнопка "Удалить"')
    # print('Сработала кнопка "Удалить"')
    await calback.answer("Пост помечен на удаление")
    await calback.message.answer('Пост помечен на удаление')

##действие кнопки при нажатии 'Редактировать'
@logger.catch
@dp.callback_query_handler(text='editing')
async def editing(calback : types.CallbackQuery,):
    moder_id = calback.message.message_id
    for_editing(moder_id)
    logger.debug("Пост помечен на редактирование: " + str(moder_id))
    # id Сообщения на удаление 
    logger.success('Сработала кнопка "Редактировать"')
    # print('Сработала кнопка "Удалить"')
    await calback.answer("Пост помечен на редактирование")
    await calback.message.answer('Пост помечен на редактирование')

#----------------
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

#----------------