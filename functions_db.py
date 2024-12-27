'Лабораторная №9 часть 2'

from sqlalchemy import (create_engine, )
from sqlalchemy.orm import sessionmaker
from create_db import Users, Posts
engine = create_engine("mysql+pymysql://root:P137Zapi261Krpj@localhost:3306/laborator_9")
Session = sessionmaker(bind=engine)
session = Session()

conn = engine.connect()
def add_user():
    'добавляет пользователей в таблицу'
    users = [
    Users(username = "Egor", email = "egorkrylovv@yandex.ru", password = 123123),
    Users(username = "Yasha", email = "mops@yandex.ru", password = 45354),
    Users(username = "Olga", email =  "mango@yandex.ru", password = 909090)]
    session.add_all(users)
    session.commit()

def add_posts():
    'добавляет посты в таблицу'
    users = session.query(Users).all()
    posts = [
        Posts(title = "test 1", text = "new text 1", user_id = users[0].id),
        Posts(title = "test 2", text = "new text 2", user_id = users[0].id),
        Posts(title = "mango", text = "vkusnoye", user_id = users[2].id)
    ]
    session.add_all(posts)
    session.commit()

def show_posts():
    'выводит всех юзеров'
    users = session.query(Users).all()
    for user in users:
        print(f"id: {user.id}, username: {user.username},"
              f" email: {user.email}")

def show_post_wautrhors():
    'выводит пост и юзера'
    posts = session.query(Posts).all()
    for post in posts:
        users = session.query(Users).all()
        for user in users:
            if user.id == post.user_id:
                print (f"Заголовок {post.title}, текст: {post.text}, Автор: {user.username}")

def search_by_id(user_id):
    'поиск постов по айди автора'
    posts = session.query(Posts).filter(Posts.user_id == user_id).all()
    for post in posts:
        print(f"Юзер: {user_id}, Заголовок: {post.title}, Текст: {post.text}")

def recreate_email(old_email, new_email):
    'замена почты'
    user = session.query(Users).filter(Users.email == old_email).first()
    print(f"Ваша старая почта {old_email}")
    user.email = new_email
    session.commit()
    print(f"Изменина на {user.email}")

def recreate_text(title, new_text):
    'замена почты'
    post = session.query(Posts).filter(Posts.title == title and Posts.user_id == Users.id).first()
    print(f"Вы поменяли текст ({post.text})")
    post.text = new_text
    session.commit()
    print(f"Изменина на ({post.text})")

def delite_post(title):
    'удаление поста по теме и айди юзера'
    post = session.query(Posts).filter(Posts.title == title and Posts.user_id == Users.id).first()
    print(f"Удаление поста: {post.title}, текст: {post.text}")
    session.delete(post)
    session.commit()
    print("Пост удалён")

def delite_user(username):
    'удаление пользователя и всех его постов'
    user = session.query(Users).filter(Users.username == username).first()
    posts = session.query(Posts).filter(Posts.user_id == user.id)
    for post in posts:
        print(f"Пост {post.title} Удалён")
        session.delete(post)
        session.commit()
    print(f"пользователь {username} удалён")
    session.delete(user)
    session.commit()

delite_user("Egor")
