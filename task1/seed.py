from faker import Faker
from random import randint
from db_connection import connect_to_db

def seed_db():
    seed_statuses()
    seed_users()
    seed_tasks()

def seed_statuses():
    sql = 'INSERT INTO status (name) VALUES (%s)'
    data = [('new',), ('in progress',), ('completed',)]

    execute_sql(sql, data)

def seed_users():
    faker = Faker()
    sql = 'INSERT INTO users (fullname, email) VALUES (%s, %s)'
    data = [(faker.name(), faker.unique.email()) for _ in range(50)]

    execute_sql(sql, data)

def seed_tasks():
    faker = Faker()
    sql = 'INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)'
    data = [(faker.sentence(nb_words=3), faker.text(), randint(1,3), randint(1,50)) for _ in range(200)]

    execute_sql(sql, data)

def execute_sql(sql, data):
    global conn
    try:
        conn = connect_to_db()
        with conn.cursor() as cursor:
            cursor.executemany(sql, data)

    except Exception as ex:
        print(ex)

    finally:
        conn.commit()
        conn.close()

if __name__ == '__main__':
    seed_db()
