import sqlite3

__connection = None


def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('tasker.db', check_same_thread=False)
    return __connection


def init_db(force: bool = False):
    """ Проверить что нужные таблицы существуют, иначе создать их

        Важно: миграции на такие таблицы вы должны производить самостоятельно!

        :param conn: подключение к СУБД
        :param force: явно пересоздать все таблицы
    """
    conn = get_connection()
    c = conn.cursor()

    # Информация о пользователе
    # TODO: создать при необходимости...

    # Сообщения от пользователей
    if force:
        c.execute('DROP TABLE IF EXISTS user_tasks')

    c.execute('''
        CREATE TABLE IF NOT EXISTS user_tasks (
            id          INTEGER PRIMARY KEY,
            user_id     INTEGER NOT NULL,
            task        TEXT NOT NULL
        )
    ''')

    # Сохранить изменения
    conn.commit()
    print('table created !')


def add_task(conn, user_id: int, task: str):
    c = conn.cursor()
    c.execute('INSERT INTO user_tasks (user_id, task) VALUES (?, ?)', (user_id, task))
    conn.commit()


def get_tasks(conn, user_id: int, task: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT task, id FROM user_tasks WHERE user_id = ?', (user_id, ))
    tasks = c.fetchall()
    return tasks


def drop_task(conn, task_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM user_tasks WHERE id = ?', (task_id, ))
    conn.commit()




if __name__ == '__main__':
    init_db()