import sqlite3

DATABASE = 'database.sql'


def get_db():
    connection = sqlite3.connect(DATABASE)
    cur = connection.cursor()
    cur.execute('CREATE TABLE if not exists currency_usd('
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'name TEXT NOT NULL,'
                'buy TEXT NOT NULL,'
                'sell TEXT NOT NULL)')
    cur.execute('CREATE TABLE if not exists currency_eur('
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'name TEXT NOT NULL,'
                'buy TEXT NOT NULL,'
                'sell TEXT NOT NULL)')
    cur.execute('CREATE TABLE if not exists users('
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'pk_in_bot INTEGER NOT NULL,'
                'user_name TEXT NOT NULL,'
                'email TEXT NOT NULL)')
    cur.execute('DELETE FROM currency_usd WHERE id NOT IN (SELECT ID FROM currency_usd ORDER BY ID DESC LIMIT 1)')
    cur.execute('DELETE FROM currency_usd WHERE id NOT IN (SELECT ID FROM currency_usd ORDER BY ID DESC LIMIT 1)')
    cur.close()
    return connection


def new_currency(data):
    with get_db() as con:
        cur = con.cursor()
        buy_usd = data['USD'][0]
        sell_usd = data['USD'][1]
        buy_eur = data['EUR'][0]
        sell_eur = data['EUR'][1]
        cur.execute("INSERT INTO currency_usd (name, buy, sell) VALUES(?, ?, ?)",
                    ('USD', buy_usd, sell_usd,))
        cur.execute("INSERT INTO currency_eur (name, buy, sell) VALUES(?, ?, ?)",
                    ('USD', buy_eur, sell_eur,))


def check_currency():
    data = {}
    with get_db() as con:
        cur = con.cursor()
        usd = cur.execute("SELECT * FROM currency_usd ORDER BY id DESC LIMIT 1").fetchall()
        eur = cur.execute("SELECT * FROM currency_eur ORDER BY id DESC LIMIT 1").fetchall()
    if usd and eur:
        data['USD'] = [usd[0][2], usd[0][3]]
        data['EUR'] = [eur[0][2], eur[0][3]]
        return data
    else:
        data = False
        return data


def check_user_in_db(pk):
    with get_db() as con:
        cur = con.cursor()
        check = cur.execute(f'SELECT pk_in_bot FROM users WHERE pk_in_bot = {pk}').fetchone()
    if check is not None:
        return True
    else:
        return False


def create_user(data):
    with get_db() as con:
        cur = con.cursor()
        cur.execute('INSERT INTO users (pk_in_bot, user_name, email) VALUES(?, ?, ?)',
                    (str(data['pk_in_bot']), data['name'], data['email'],))
        if cur.rowcount > 0:
            return True
        else:
            return False


def dell_base():
    with get_db() as con:
        cur = con.cursor()
        cur.execute('DROP TABLE users')


# def insert():
#     with get_db() as con:
#         cur = con.cursor()
#         cur.execute('INSERT INTO users (pk_in_bot, user_name, email) VALUES(?, ?, ?)',
#                     (465659759, 'Oleg', 'olegkirtsun@mail.com',))
#         cur.execute('INSERT INTO users (pk_in_bot, user_name, email) VALUES(?, ?, ?)',
#                     (465659765, 'Oleg', 'olegkirtsun@mail.com',))
#
#
# if __name__ == '__main__':
# #     # check_user_in_db(465659765)
# #     # insert()
    dell_base()
