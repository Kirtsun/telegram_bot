import psycopg2
import time
# db_postgres = psycopg2.connect(
#             dbname='mydatabase',
#             user='postgres',
#             password='postgres_password',
#             host='db_bot',
#             port='5432'
#         )


class DataBase:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='mydatabase',
            user='postgres',
            password='postgres_password',
            host='db_bot',
            port='5432'
        )
        self.cur = self.conn.cursor()

    def create_table(self):
        with self.conn:
            self.cur.execute('CREATE TABLE if not exists currency_usd('
                             'id SERIAL PRIMARY KEY,'
                             ' name TEXT NOT NULL, buy TEXT NOT NULL,'
                             ' sell TEXT NOT NULL)')
            self.cur.execute('CREATE TABLE if not exists currency_eur('
                             'id SERIAL PRIMARY KEY,'
                             'name TEXT NOT NULL,'
                             'buy TEXT NOT NULL,'
                             'sell TEXT NOT NULL)')
            self.cur.execute('CREATE TABLE if not exists users('
                             'id SERIAL PRIMARY KEY,'
                             'pk_in_bot INTEGER NOT NULL,'
                             'name TEXT NOT NULL,'
                             'user_name TEXT NOT NULL,'
                             'email TEXT NOT NULL,'
                             'time_sub INTEGER DEFAULT 0)')

    def new_currency(self, data):
        with self.conn:
            buy_usd = data['USD'][0]
            sell_usd = data['USD'][1]
            buy_eur = data['EUR'][0]
            sell_eur = data['EUR'][1]
            self.cur.execute("INSERT INTO currency_usd (name, buy, sell) VALUES(%s, %s, %s)",
                             ('USD', buy_usd, sell_usd,))
            self.cur.execute("INSERT INTO currency_eur (name, buy, sell) VALUES(%s, %s, %s)",
                             ('USD', buy_eur, sell_eur,))

    def check_currency(self):
        data = {}
        with self.conn:
            self.cur.execute("SELECT * FROM currency_usd ORDER BY id DESC LIMIT 1")
            self.cur.execute("SELECT * FROM currency_eur ORDER BY id DESC LIMIT 1")
            usd = self.cur.fetchone()
            eur = self.cur.fetchone()
        if usd and eur:
            data['USD'] = [usd[0][2], usd[0][3]]
            data['EUR'] = [eur[0][2], eur[0][3]]
            return data
        else:
            data = False
            return data

    def check_user_in_db(self, pk):
        if self.cur is None:
            # или бросить исключение или инициализировать курсор
            raise ValueError("Cursor is not initialized")
        with self.conn:
            self.cur.execute(f'SELECT pk_in_bot FROM users WHERE pk_in_bot = %s', (pk,))
            check = self.cur.fetchone()
        if check is not None:
            return True
        else:
            return False

    def check_sub_status(self, pk):
        with self.conn:
            self.cur.execute('SELECT time_sub FROM users WHERE pk_in_bot = %s', (pk,))
            res = self.cur.fetchone()
        if res:
            if int(res[0]) > int(time.time()):
                return True
            else:
                return False
        else:
            return False

    def update_sub(self, user_name, times):
        with self.conn:
            self.cur.execute('UPDATE users SET time_sub = %s WHERE user_name = %s', (times, user_name))
            if self.cur.rowcount > 0:
                return True
            else:
                return False

    def get_user_name(self, user_name):
        with self.conn:
            self.cur.execute('SELECT pk_in_bot FROM users WHERE user_name = %s', (user_name,))
            res = self.cur.fetchone()
        if res is not None:
            return True
        else:
            return False

    def create_user(self, data):
        with self.conn:
            self.cur.execute('INSERT INTO users (pk_in_bot, name, user_name, email) VALUES(%s, %s, %s, %s)',
                             (str(data['pk_in_bot']), data['name'], data['user_name'], data['email'],))
            if self.cur.rowcount > 0:
                return True
            else:
                return False

    def dell_base(self):
        with self.conn:
            self.cur.execute('DROP TABLE users')
