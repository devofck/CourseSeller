import sqlite3
BASE = 'base/course.db'


def reg(tg_id):
    conn = sqlite3.connect(BASE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT tg_id FROM users WHERE tg_id = ?',
        [
            tg_id
        ]
    )
    if cursor.fetchone() is None:
        cursor.execute(
            'INSERT INTO users(tg_id) VALUES(?)',
            [
                tg_id
            ]
        )
        conn.commit()
    conn.close()


def is_demo(tg_id):
    conn = sqlite3.connect(BASE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT demo_used FROM users WHERE tg_id = ?',
        [
            tg_id
        ]
    )
    if cursor.fetchone()[0] == 0:
        return True
    return False


def end_demo(tg_id):
    conn = sqlite3.connect(BASE)
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE users SET demo_used = 1 WHERE tg_id = ?',
        [
            tg_id
        ]
    )
    conn.commit()


def is_admin(tg_id):
    conn = sqlite3.connect(BASE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT is_admin FROM users WHERE tg_id = ?',
        [
            tg_id
        ]
    )
    if cursor.fetchone()[0] == 0:
        return False
    return True


def get_stat():
    conn = sqlite3.connect(BASE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM users'
    )
    data = cursor.fetchall()
    payed, demo = 0, 0
    for i in data:
        payed += i[2]
        demo += i[3]
    return [
        len(data),
        payed,
        demo
    ]


def give_sub(tg_id):
    conn = sqlite3.connect(BASE)
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE users SET premium = 1 WHERE tg_id = ?',
            [
                int(tg_id)
            ]
        )
    except:
        return False
    conn.commit()
    return True


def is_premium(tg_id):
    conn = sqlite3.connect(BASE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT premium FROM users WHERE tg_id = ?',
        [
            tg_id
        ]
    )
    if cursor.fetchone()[0] == 0:
        return False
    return True
