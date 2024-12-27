'Лабораторная №9'
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker
from create_db import Users, Posts
engine = create_engine("mysql+pymysql://root:P137Zapi261Krpj@localhost:3306/laborator_9")
Session = sessionmaker(bind=engine)

app = FastAPI()

@app.get("/", tags=["Начальная страница"])
def start_page():
    'инструкция'
    return ("Добавить юзера - /user/name/mail/password",
            "Добавить пост - /post/name/password/title/text",
                          )

@app.post("/user/{username}/{email}/{password}", tags=["Добавление"])
def add_user(name: str, mail: str, pasword: str):
    'добавление юзера'
    session = Session()
    users = session.query(Users).all()
    new = Users(username = name, email = mail, password = pasword)
    for user in users:
        if user.username == new.username:
            return "Данный никнейм уже занят, попробуйте другой"
        elif user.email == new.email:
            return " Данный email уже занят, попробуйте другой"
    session.add(new)
    session.commit()
    session.close()
    return "Пользователь успешно добавлен"

@app.post("/user/{username}/{password}/{title}/{text}", tags=["Добавление"])
def add_post(name: str, pas: str, new_title: str, new_text: str):
    'добавление поста'
    session = Session()
    users = session.query(Users).all()
    for user in users:
        if user.username == name and user.password == pas:
            check_id = user.id
            post = Posts(title = new_title, text = new_text, user_id = check_id)
            session.add(post)
            session.commit()
            session.close()
            return " Ваша тема успешно добавлена "
    return "Неверно введено имя или пароль "

@app.get("/user/list", tags = ["Списки"])
def show_users():
    'выводит всех юзеров сайта'
    session = Session()
    users = session.query(Users).all()
    lst = []
    for user in users:
        lst.append(f"Имя: {user.username}, email: {user.email}")
    session.close()
    return lst

@app.get("/posts/list", tags = ["Списки"])
def show_posts():
    'выводит все посты сайта'
    session = Session()
    posts = session.query(Posts).all()
    users = session.query(Users).all()
    lst = []
    for post in posts:
        for user in users:
            if user.id == post.user_id:
                lst.append(f"Заголовок: {post.title}, текст: {post.text}, автор: {user.username}")
    session.close()
    return lst

@app.get("/user/change/name/{name}/{new_name}/{password}", tags = ["Редактирование"])
def change_name(name: str, new_name: str, pas: str):
    'Изменение имени'
    session = Session()
    users = session.query(Users).all()
    for guy in users:
        if guy.username == name:
            user = session.query(Users).filter(Users.username == name).first()
            if user.password == pas:
                user.username = new_name
                session.commit()
                session.close()
            return HTMLResponse("<h1> Смена произошла удачно <h1>")
    session.close()
    return HTMLResponse("<h1> Что-то пошло не так <h1>")

@app.get("/user/change/email/{name}/{new_email}/{password}", tags = ["Редактирование"])
def change_email(name: str, new_email: str, pas: str):
    'Изменение email'
    session = Session()
    users = session.query(Users).all()
    for guy in users:
        if guy.username == name:
            user = session.query(Users).filter(Users.username == name).first()
            if user.password == pas:
                user.email = new_email
                session.commit()
                session.close()
            return HTMLResponse("<h1> Смена произошла удачно <h1>")
    session.close()
    return HTMLResponse("<h1> Что-то пошло не так <h1>")

@app.get("/post/change/title/{title}/{new_title}/{password}", tags=["Редактирование"])
def change_title(title: str, new_title: str, pas: str):
    'изменение заголовка'
    session = Session()
    post = session.query(Posts).filter(Posts.title == title).first()
    user = session.query(Users).filter(Users.id == post.user_id).first()
    if user.password == pas:
        post.title = new_title
        session.commit()
        session.close()
        return HTMLResponse("<h1> Изменения успешны <h1>")
    session.close()
    return HTMLResponse("<h1> что-то не так <h1>")

app.get("/user/delite/{username}", tags=["Удаление"])
def delite_user(username):
    'удаление пользователя и всех его постов'
    session = Session()
    user = session.query(Users).filter(Users.username == username).first()
    posts = session.query(Posts).filter(Posts.user_id == user.id)
    for post in posts:
        session.delete(post)
        session.commit()
    session.delete(user)
    session.commit()
    return HTMLResponse(f"{username} удалён")

app.get("/user/delite/{title}", tags=["Удаление"])
def delite_post(title):
    'удаление поста по теме и айди юзера'
    session = Session()
    post = session.query(Posts).filter(Posts.title == title and Posts.user_id == Users.id).first()
    session.delete(post)
    session.commit()
    return "Пост удалён"
