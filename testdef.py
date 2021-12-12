# -*- coding: utf-8 -*-
# from sql import create_tbl, recordingDateJson, cur,read_tbl

# title = "title1112"
# url = "url112"

# create_tbl()

# recordingDateJson(title, url)

# re = read_tbl() # Вынемаем значения из функции 
# row = len(re) # Считаем количество количество элементов в списке
# print(row) 
# # Проходим в цикле по всем элементам списка  
# for row in re:
#     print(row[0])
#     print(row[1])

# import requests
# import os
# # print(os.listdir("images"))
# # функция для скачивания файла
# def save_file_from_www(link):
#     filename = link.split('/')[-1] #выявляет по слешу название файла
#     print(filename)
#     r = requests.get(link, allow_redirects=True)
#     os.chdir(r'C:\Users\Илья\Desktop\1\parsss\images') # Определяем директорию
#     open(filename, 'wb').write(r.content)

# ######################### функция для скачивания файла #########################

# link1 = "https://v.redd.it/y15ku80z7ar71/DASH_720.mp4"

# save_file_from_www(link1)



# # https://imgur.com/QrTI36g.jpeg

# from datetime import timedelta, datetime, timezone

# offset = timezone(timedelta(hours=3))  # Московское время
# now = datetime.now(offset).strftime('%H:%M')  # Текущая дата

# date1 = '19:36'
# date2 = '19:47'
# date3 = '19:47'

# # print(now)
# if now == date1:

# elif now == date2:

# elif now == date3:

# else:
#     print('Совпадений нет')
# import datetime as DT
# from time import time
# from sql import post_on_publik
# from datetime import datetime, timedelta, timezone
# from pyrogram import Client, filters
# from pyrogram.types import InputMediaPhoto, InputMediaVideo
# import os
# # post_on_pub = post_on_publik()  #'list'
# # print(type(post_on_pub))
# app = Client("my_account")
# app.start()
# # time_post -

# # def date_time_post(): 
# #     for row in post_on_pub
# os.chdir(r'C:\bottelegramm\images')
# offset = timezone(timedelta(hours=3))  # Московское время
# now_h = datetime.now(offset).strftime('%H:%M:')  # Текущая дата
# now_date = datetime.now(offset).strftime('%Y-%m-%d')

# date1 = '20:35'
# date2 = '20:18'
# # date3 = '20:45'
# dt =(now_date + ' ' + date1)
# dt = DT.datetime.strptime(dt, '%Y-%m-%d %H:%M')
# date_ux = int((dt.timestamp()))
# print(date_ux)
# path_file =  '6id02di9r2r71.jpg'
# title = 'jsdfhgklhjsdfklgh'

# app.send_photo("Testyfakt", path_file, title, schedule_date=date_ux)


# dt1 = DT.datetime.strptime(dt1, '%Y-%m-%d %H:%M:')
# date_ux2 = (dt1.timestamp())# from datetime import datetime, timedelta, timezone



# temee = '2019-12-24 04:00:00'
# offset = timezone(timedelta(hours=3))  # Московское время
# now_h = datetime.now(offset).strftime('%H:%M:')  #Текущая дата
# now_date = datetime.now(offset).strftime('%Y-%m-%d')
# dt =(now_date + ' ' + now_h)
# dt = DT.datetime.strptime(dt, '%Y-%m-%d %H:%M:')
# print(dt)
# date_ux = (dt.timestamp())
# print(date_ux)

# dt = DT.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
# print(dt)
# print(dt.timestamp())
# print()




#Переводчик
# from deep_translator import (GoogleTranslator)
# word = "Rules of the Subreddit. If these are broken, your comment/post will be removed and you could be banned. You should read this before posting."

# translate = GoogleTranslator ( source = 'en' , target = 'ru' ).translate(word)

# print(translate)


#Исходник парсера. Удален из дев  обработчик ошибок т.к. он мешал работать либе расписания
# def search_reddit():
#     def redit_login(username, password, redit):
#         browser = webdriver.Chrome('chromedriver.exe') # Указываем путь до веб драйвера
#         try: #- это обработчик ошибок
#         #Заходим на страницу авторизации
#             browser.get('https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2F')
#             time.sleep(random.randrange(3, 5))
#         #Передаем данные username из файла auth_date
#             username_input = browser.find_element_by_name('username')
#             username_input.clear()
#             username_input.send_keys(username)
#             time.sleep(2)
#         # Передаем данные password из файла auth_date
#             password_input = browser.find_element_by_name('password')
#             password_input.clear()
#             password_input.send_keys(password)
#             password_input.send_keys(Keys.ENTER)
#             time.sleep(10)
#         #переход по ссылке
#             try:
#                 browser.get(f'https://www.reddit.com/r/{redit}.json') #в redit передается значение
#             # time.sleep(10)
#             # Получает источник текущей страницы html на странице и записываем в переменную
#                 html = browser.page_source
#             # time.sleep(10)
#             # # сохраняем страницу в файл
#                 with open('data.html', 'w', encoding='utf=8') as file:
#                     file.write(html)
#                 browser.close()
#                 browser.quit()
#             except Exception as ex:
#                 print(ex)
#                 browser.close()
#                 browser.quit()
#         except Exception as ex: #При возникновении ошибки, в принте она появиться
#             print(ex)
#             browser.close()
#             browser.quit()
#     redit_login(username, password, 'interestingasfuck') #подставляет занчение в место {redit}
#     with open("data.html") as file:
#         src = file.read()
#     soup = BeautifulSoup(src, "lxml")
#     js = soup.get_text()# выниваем данне json из html

#     #####_Создаем data.json по данным из html
#     with open("data.json", "w") as file:
#         file.write(js)
#         dictData = json.loads(js)

#     # #####_Вынимаем необходмые данне из data.json 
#     with open("data.json") as file:
#         datJs = file.read()
#     data = json.loads(datJs)
#     dictChildren = data['data']
#     dist = dictChildren['children']

#     # #####_Создаем БД SQL
#     create_tbl()

#     #Читаем данные из переменой dist и пишем их в таблицу
#     for item in dist:
#         postOffice = item['data']
#         # print(postOffice)
#         # print(postOffice.keys())
#         created = (postOffice['created']) # дата создания поста
#         creadat = (datetime.utcfromtimestamp(created).strftime('%Y-%m-%d %H:%M:%S'))
#         # print(created)
#         # print(postOffice['title'])
#         # print(postOffice['url'])
#         title = (postOffice['title'])
#         title_ru = GoogleTranslator ( source = 'en' , target = 'ru' ).translate(title)
#         url = (postOffice['url'])
#         #####_Записываем таблицу SQL parser значения из переменных (title, url)
#         recordingDateJson(title, url, creadat, title_ru)

#     # функция для скачивания фоток и записи пути к файлу
#     link = url_fot_tbl()
#     # print(link)
#     linklen = len(link) # Считаем количество количество элементов в списке
#     # print(linklen)

#     # # Проходим в цикле по всем элементам списка для скачивания файла 
#     for linklen in link:
#         lin = linklen[0]
#         url_link= linklen[0]
#         lin = lin.split('/')[-1] #выявляет по слешу название файла
#         # path = r"C:\bottelegramm\images"
#         # add = '\\'
#         # path_file = (path + add + lin)
#         path_file = (lin)
#         # print(lin)
#         # print(path_file)
#         r = requests.get(linklen[0], allow_redirects=True)
#         os.chdir(r'C:\bottelegramm\images') # Определяем директорию
#         open(lin, 'wb').write(r.content)
#         # print(url_link)
#         sql_update(url_link, path_file)


        
# -----------------переработана ниже -----
# функция Отправки на dev поста с пометкой --- не работает как нужно
# def send_post_dev(app):
#     post_on_pub = post_on_publik()
#     row = len(post_on_pub)
#     def on_publik (app,row, post_on_pub):
#         while True:
#             for row in post_on_pub:
#                 title = (row[0]) # из списка выбераем 1е значенеие - title
#                 path_file = (row[1])
#                 id_post = int((row[2]))
#                 print(id_post)
#                 os.chdir(r'C:\bottelegramm\images')
#                 # print(path_file)    
#                 # offset = timezone(timedelta(hours=3))  # Московское время
#                 # now_h = datetime.now(offset).strftime('%H:%M')  # Текущая дата
#                 # now_date = datetime.now(offset).strftime('%Y-%m-%d')
#                 # print(now_h)
#                 # date1 = '21:29'
#                 # date2 = '21:30'
#                 # # date3 = '20:45'
#                 # dt =(now_date + ' ' + date1 + ':59')
#                 # dt = DT.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
#                 # date_ux = int((dt.timestamp()))

#                 # dt1 =(now_date + ' ' + date2 + ':59')
#                 # dt1 = DT.datetime.strptime(dt1, '%Y-%m-%d %H:%M:%S')
#                 # date_ux2 = int((dt1.timestamp()))

#                 try:
#                     print('Блок отпраки сообщений в ДЕВ')
#                     app.send_photo("Testyfakt", path_file, title)
#                     # if now_h == date1:
#                     #     attr_dev(id_post)
#                     #     app.send_photo("Testyfakt", path_file, title, schedule_date=date_ux)
#                     #     time.sleep(30)
                        
#                     # elif now_h == date2:
#                     #     attr_dev(id_post)
#                     #     app.send_photo("Testyfakt", path_file, title, schedule_date=date_ux2)
#                     #     time.sleep(30)
                        
#                     # # elif now_h == date3:
#                     # #     app.send_photo("Testyfakt", path_file, title, schedule_date=date_ux2)
#                     # #     attr_dev(id_post)
#                     # else:
#                     #     print('Совпадений нет')
#                 except:
#                     print("Ошибка с картинкой " + path_file)
#                 # time.sleep(30)
#     on_publik (app,row, post_on_pub)
# send_post_dev(app)
# -----------------переработана ниже -----
# import time

# while True:
#     print("первый ")
#     time.sleep(1)

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message,\
    InlineKeyboardButton, InlineKeyboardMarkup, user
from aiogram.utils.callback_data import CallbackData
from sql import read_tbl,moder_msgid,publication_attribute_update,to_remove,content_error_update,sql_update
import os
import time
from pyrogram import Client, filters
import requests

# app = Client("my_account")
# app.start()


bot = Bot(token="2136282741:AAH4wAhuVESWI5_6uKj-lgYVAsm25OHQCV8")
dp =Dispatcher(bot)



@dp.message_handler(commands="start")
async def start(message: types.Message):
    ### Объединение кнопок в список
    userid = int(message.from_user.id)

    if 467601941 == userid:
        start_buttons = ["Пост на одобрение", "Посты на публикацию", "Удалить пост"]
        keyboard =types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)
        await message.answer("Бот готов к работе 👍", reply_markup=keyboard)
    else:
        await message.answer("Уходи))")


# mid = other_command()
# print(mid)

##Вывод клавы

@dp.message_handler(Text(equals="Пост на одобрение"))
async def test_message(message: types.Message):
    # await message.answer('Тут должен быть текст поста', reply_markup=lnkb)
    re = read_tbl() 
    #row = len(re) # Считаем количество количество элементов в списке
    #print(row) 
    # Проходим в цикле по всем элементам списка для публикации в модерку
    for row in re:
        title = (row[0]) # из списка выбераем 1е значенеие - title
        url = (row[1])  # из списка выбераем 2е значенеие - url
        # print(url)
        # path_file = (row[2])
        id_post = str((row[3]))
        # Выполняем скачивание файла
        url_link = (row[1]) 
        lin = url_link.split('/')[-1] #выявляет по слешу название файла
        lin = str(id_post) + lin # добавляем id в название файла
        path_file = (lin)
        r = requests.get(url_link, allow_redirects=True)
        os.chdir(r'/home/ily/tb_bot/images')
        open(lin, 'wb').write(r.content)
        sql_update(url_link, path_file)
        print(path_file)
        file = open(path_file, 'rb')

        if '.gif' in path_file:
            print("анимация и пнг")
            try: 
                await bot.send_animation(chat_id=message.from_user.id, animation=file, reply_markup=lnkb, caption=title)
                moder_id = message.message_id + 1
                moder_msgid(moder_id,id_post)
            except Exception as ex:
                print("Ошибка с анимацией для DEV" + path_file)
                print(ex)
                content_error_update(id_post) #Помечаем пост с ошибкой в контенте

        elif '.jpg' in path_file or '.png' in path_file or '.jpeg' in path_file:
            try:
                await bot.send_photo(chat_id=message.from_user.id, photo=file, reply_markup=lnkb, caption=title)
                moder_id = message.message_id + 1
                moder_msgid(moder_id,id_post)
            except Exception as ex:
                print("Ошибка с картинкой для DEV" + path_file)
                print(ex)
                content_error_update(id_post) #Помечаем пост с ошибкой в контенте

        elif '.mp4' in path_file:
            print("Отправка видео")
            try:
                await bot.send_video(chat_id=message.from_user.id, video=file, reply_markup=lnkb, caption=title)
                moder_id = message.message_id + 1
                moder_msgid(moder_id,id_post)
            except Exception as ex:
                print("Ошибка с видео для DEV" + path_file)
                print(ex)
                content_error_update(id_post) #Помечаем пост с ошибкой в контенте        

        # await bot.send_photo(
        #     chat_id=message.from_user.id, photo=file, reply_markup=lnkb, caption=title)
        # moder_id = message.message_id + 1
        # moder_msgid(moder_id,id_post)
        # # print(mid)
        
        
## Описание клавиатуры
lnkb = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Опубликовать', callback_data='pudlik'),\
                            InlineKeyboardButton(text='Удалить', callback_data='del'))


##действие кнопки при нажатии 'Опубликовать'
@dp.callback_query_handler(text='pudlik')
async def public_priz(calback : types.CallbackQuery):
    moder_id = calback.message.message_id
    publication_attribute_update(moder_id) # Сделать поиск по полученному id и обновить признак публикации на "1"
    print(moder_id) # id Сообщения на публикацию 
    print('Сработала кнопка "Опубликовать"')
    await calback.answer('Пост принят на публикацию')
    await calback.message.answer('Пост принят на публикацию')

##действие кнопки при нажатии 'Удалить'
@dp.callback_query_handler(text='del')
async def public_priz(calback : types.CallbackQuery,):
    moder_id = calback.message.message_id
    to_remove(moder_id)
    # id Сообщения на удаление 
    print('Сработала кнопка "Удалить"')
    await calback.answer("Пост помечен на удаление")
    await calback.message.answer('Пост помечен на удаление')

# def kb_likes():
#     likes = num["likes"]
#     dislikes = num["dislikes"]
#     kb = types.InlineKeyboardMarkup()
#     kb.add(types.InlineKeyboardButton(text=f"👍 {likes}", callback_data="like"),
#            types.InlineKeyboardButton(text=f"👎 {dislikes}", callback_data="dislike"))
#     return kb

# #срабатывает при появлении нового поста
# @dp.channel_post_handler()
# async def add_like(mes):
#     cid = mes.chat.id
#     mid = mes.message_id
#     await bot.edit_message_reply_markup(chat_id=cid, message_id=mid, reply_markup=kb_likes(mid))

# #срабатывает при нажатии на кнопку
# @dp.callback_query_handler()
# async def callback(call):
#     cid = call.message.chat.id
#     uid = call.from_user.id
#     mid = call.message.message_id
#     cdata = call.data
#     try:
#         await bot.edit_message_reply_markup(chat_id=cid, message_id=mid, reply_markup=kb_likes())
#     except:
#         pass

#----------------
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

#----------------