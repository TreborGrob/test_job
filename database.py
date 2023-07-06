import logging
import psycopg2

logger = logging.getLogger('discord')
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Text
# Base = declarative_base()
# engine = create_async_engine(
#     "postgresql+asyncpg://postgres:password@localhost/postgres",
#     echo=True,
# )
# session = AsyncSession(engine, future=True)
#
#
# class TestModel(Base):
#     __tablename__ = 'test'
#
#     A = Column(Text)
#     B = Column(Text)
#     C = Column(Text)
#     D = Column(Text)
#     E = Column(Text)
#
#     @staticmethod
#     async def add_line(a, b, c, d, e):
#         line = TestModel(A=a, B=b, C=c, D=d, E=e)
#         session.add(line)
#         await session.commit()
#
#     def __repr__(self):
#         return "".format(self.code)

__all__ = ['create_connection', 'add_line', 'create_table', 'delete_table']


# создание соединения к БД
def create_connection():
    # изменить данные postgreSQL на свои
    connection = psycopg2.connect(user="postgres",
                                  password="password",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
    connection.set_session(autocommit=True)
    return connection


# Создание таблицы
def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    with connection:
        return cursor.execute('''CREATE TABLE test  
     (A TEXT NOT NULL,
     B TEXT NOT NULL,
     C TEXT NOT NULL,
     D TEXT NOT NULL,
     E TEXT NOT NULL);''')


# Удаление таблицы
def delete_table():
    connection = create_connection()
    cursor = connection.cursor()
    with connection:
        return cursor.execute('''DROP TABLE IF EXISTS test;''')


# Добавление строки в таблицу
def add_line(a, b, c, d, e):
    connection = create_connection()
    cursor = connection.cursor()
    with connection:
        return cursor.execute("INSERT INTO test VALUES (%s,%s,%s,%s,%s)", (a, b, c, d, e,))


if __name__ == '__main__':
    print('Запустите main.py')
