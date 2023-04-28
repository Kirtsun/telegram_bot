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
