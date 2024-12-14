from db_connection import connect_to_db

gen_schema_sql = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE
);

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    status_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    constraint fk_tasks_status foreign key (status_id) REFERENCES status (id) ON DELETE CASCADE,
    constraint fk_tasks_users foreign key (user_id) REFERENCES users (id) ON DELETE CASCADE
);
"""

def generate_schema():
    global conn
    try:
        conn = connect_to_db()
        with conn.cursor() as cursor:
            cursor.execute(gen_schema_sql)

    except Exception as ex:
        print(ex)

    finally:
        conn.commit()
        conn.close()


if __name__ == '__main__':
    generate_schema()
