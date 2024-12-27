'Лабораторная №9 часть 1'

from sqlalchemy import (create_engine,
    Column, Integer, String,
    MetaData, ForeignKey)
from sqlalchemy.orm import DeclarativeBase,relationship

engine = create_engine("mysql+pymysql://root:P137Zapi261Krpj@localhost:3306/laborator_9",
                       echo=True)

metadata = MetaData() #объект MetaData для управления схемой базы данных

class Base(DeclarativeBase):
    'маппед класс'
    pass

class Users(Base):
    'класс юзер'
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    relationship("Posts", back_populates="users")

class Posts(Base):
    'класс пост'
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    text = Column(String(3000), nullable=False)
    user_id = Column (Integer, ForeignKey('users.id'), nullable=False)
    relationship("Users", back_populates="posts")

Base.metadata.create_all(bind=engine)
