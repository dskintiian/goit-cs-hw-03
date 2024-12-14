from psycopg2 import connect
from random import randint
from db_connection import connect_to_db

def run_queries(conn: connect):
    with conn.cursor() as cursor:
        user_id = randint(1, 50)
        print(user_id)
        cursor.execute('SELECT * FROM tasks WHERE user_id = %s', (user_id,))
        tasks = cursor.fetchall()
        print(tasks)
        cursor.execute('SELECT * FROM tasks WHERE status_id = (SELECT id from status where name = %s)', ('new',))
        tasks = cursor.fetchall()
        print(tasks)
        task_id = randint(1, 200)
        print(task_id)
        cursor.execute('UPDATE tasks SET status_id = (SELECT id from status where name = %s) WHERE id = %s', ('in progress', task_id))
        cursor.execute('SELECT * FROM tasks WHERE id = %s', (task_id,))
        task = cursor.fetchone()
        print(task)
        cursor.execute('SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks) ')
        users = cursor.fetchall()
        print(users)
        cursor.execute('INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)', ('New task', 'One more task', randint(1,3), randint(1,50)))
        cursor.execute('SELECT * FROM tasks WHERE status_id <> (SELECT id from status where name = %s)', ('completed',))
        tasks = cursor.fetchall()
        print(tasks)
        cursor.execute('DELETE FROM tasks WHERE id = %s', (69, ))
        cursor.execute('SELECT * FROM users WHERE email LIKE \'%@example.net\'')
        users = cursor.fetchall()
        print(users)
        cursor.execute('UPDATE users SET fullname = \'Lars Ulrich\' WHERE id = %s',(11, ))
        cursor.execute('SELECT count(1) as tasks_amount FROM tasks GROUP BY status_id')
        tasks = cursor.fetchall()
        print(tasks)
        cursor.execute('SELECT * FROM tasks t LEFT JOIN users u ON t.user_id = u.id WHERE u.email LIKE \'%@example.net\'')
        tasks = cursor.fetchall()
        print(tasks)
        cursor.execute('SELECT * FROM tasks WHERE description IS NULL')
        tasks = cursor.fetchall()
        print(tasks)
        cursor.execute('SELECT * FROM users u INNER JOIN tasks t ON t.user_id = u.id LEFT JOIN status s ON s.id = t.status_id WHERE s.name = \'in progress\'')
        tasks = cursor.fetchall()
        print(tasks)
        cursor.execute('SELECT u.*, count(1) as tasks_amount FROM users u LEFT JOIN tasks t ON t.user_id = u.id GROUP BY u.id')
        users = cursor.fetchall()
        print(users)

if __name__ == '__main__':
    global conn
    try:
        conn = connect_to_db()
        run_queries(conn)

    except Exception as ex:
        print(ex)

    finally:
        conn.close()
