import os
import threading
import sqlite3 as sq
#####Создаем БД SQL
with sq.connect("parsreddit.db", check_same_thread=False) as con:
        cur = con.cursor()


##Создаем таблицу. Добавить столбец для отслеживания отправленных постов
def create_tbl():
    cur.execute("""CREATE TABLE IF NOT EXISTS parser (
    id_post INTEGER PRIMARY KEY AUTOINCREMENT,
    title_en TEXT,
    title_ru TEXT,
    url TEXT,
    path_file TEXT,
    publication_attribute INTEGER DEFAULT 0,
    date_created TEXT,
    date_publication TEXT,
    public_attr_dev TEXT,
    to_remove INTEGER DEFAULT 0,
    for_editing INTEGER DEFAULT 0,
    moder_id INTEGER DEFAULT 0,
    content_format TEXT,
    content_error TEXT,
    likes INTEGER
    )
    """)

# проверка на дубли в БД и записывать только уникальные занчения title
def recordingDateJson(title, url,creadat, title_ru, format_cont, likes):
    cur.execute("""SELECT title_en FROM parser WHERE title_en=?""", (title,))
    if not cur.fetchall():
        cur.execute("INSERT INTO parser (title_en, url, date_created, title_ru, content_format, likes) VALUES (?,?,?,?,?,?)", (title, url, creadat, title_ru,format_cont, likes)) #записываем данные в БД
        con.commit()
        return title, url,creadat, title_ru, format_cont, likes

# Получение всех строк из таблицы
def read_tbl():
        con = """SELECT * from (SELECT title_ru, url, max(likes) as likes, id_post from parser where title_ru is not null and publication_attribute =0 and public_attr_dev is NULL and content_error is NULL and to_remove =0 and for_editing =0) LIMIT 1"""
        #con = """SELECT * from (SELECT title_ru, url, likes, id_post from parser where id_post in ('80')) LIMIT 1"""
        cur.execute(con)
        records = cur.fetchall()
        return (records)

# Получение url для определения пути (только для фото)
# Для гифак сделать другую функцию. Раззобраться с тяжелыми картинками, почему не скачались
def url_fot_tbl():
        con = """SELECT url,id_post from parser
                WHERE url like '%.jpg' and path_file is null
                UNION
                SELECT url,id_post from parser
                WHERE url like '%.png' and path_file is null
                UNION
                SELECT url,id_post from parser
                WHERE url like '%.jpeg' and path_file is null
                UNION
                SELECT url,id_post from parser
                WHERE url like '%.mp4' and path_file is null
                UNION
                SELECT url,id_post from parser
                WHERE url like '%.gif' and path_file is null
            """
        cur.execute(con)
        url = cur.fetchall()
        return (url)

#Запись пути до файла
def sql_update(url_link, path_file):
    cur.execute("""UPDATE parser SET path_file=? where url = ?""", (path_file,url_link))
    con.commit()

#проверка на пост без признака 
def last_post():
        con = """SELECT count(publication_attribute) from parser where publication_attribute =0 and path_file NOTNULL"""
        cur.execute(con)
        publication_attribute = cur.fetchall()
        # Перевод лита в ИНТ
        publication_attribute = list((publication_attribute[0]))
        publication_attribute = int(publication_attribute[0])
        return (publication_attribute)

# функция установки признака публикации 
def publication_attribute_update(moder_id):
    cur.execute("""UPDATE parser SET publication_attribute=1, to_remove=0, for_editing=0 where publication_attribute =0 AND moder_id = ?""", (moder_id,))
    con.commit()

# функция выборки постов на публикацию
def post_on_publik():
        con = """SELECT title_ru, path_file,id_post,url from parser where likes in(SELECT max(likes) from parser where path_file is not null and publication_attribute=1 and public_attr_dev is NULL and content_error is NULL and to_remove=0 and for_editing =0)"""
        cur.execute(con)
        on_publik = cur.fetchall()
        return (on_publik)

# функция пометки постов на публикацию
def attr_dev(id_post):
        cur.execute("""UPDATE parser SET public_attr_dev=1 where id_post = ?""", (id_post,))
        con.commit()
        
# функция пометки постов c Ошибкой в контенте
def  content_error_update(id_post):
        cur.execute("""UPDATE parser SET content_error=1 where id_post = ?""", (id_post,))
        con.commit()

# функция пометки постов на удаление
def to_remove(moder_id):
        cur.execute("""UPDATE parser SET to_remove=1, for_editing=0, publication_attribute=0 where moder_id = ?""", (moder_id,))
        con.commit()

# функция пометки постов на редактирование
def for_editing(kb_text, moder_id):
        cur.execute("""UPDATE parser SET title_ru=? where moder_id = ?""", (kb_text, moder_id))
        con.commit()

# функция записи id сообщения из модер бота
def moder_msgid(moder_id, id_post):
        cur.execute("""UPDATE parser SET moder_id=? where id_post = ?""", (moder_id, id_post))
        con.commit()

#Функция для вывода всех файлов на удаление
def remov():
        con = """SELECT path_file,id_post from parser where to_remove=1"""
        cur.execute(con)
        rem = cur.fetchall()
        return (rem)

#Функция для удаления постов 
def delite_post(id_post):
        cur.execute("""DELETE FROM parser where id_post = ?""", (id_post,))
        con.commit()

# функция вывода кол-ва постов на публикацию
def post_on_publik_all():
        con = """SELECT count(id_post) as post from parser where publication_attribute=1 and public_attr_dev is NULL"""
        cur.execute(con)
        post_on_publik_all = cur.fetchall()
        return (post_on_publik_all)
