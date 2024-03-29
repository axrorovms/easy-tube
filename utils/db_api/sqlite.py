import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(
            self,
            sql: str,
            parameters: tuple = None,
            fetchone=False,
            fetchall=False,
            commit=False,
    ):
        print(sql)
        if not parameters:
            parameters = ()
        with self.connection as conn:
            cursor = conn.cursor()
            data = None
            cursor.execute(sql, parameters)

            if commit:
                conn.commit()
            if fetchall:
                data = cursor.fetchall()
            if fetchone:
                data = cursor.fetchone()
            return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id int PRIMARY KEY,
            tg_id varchar(30) NOT NULL,
            username varchar(255),
            lang varchar(2),
            fullname varchar(255)
            );
"""
        self.execute(sql, commit=True)

    def create_table_screen(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Screen (
            id int PRIMARY KEY,
            user_id int NOT NULL,
            screenshot BLOB NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users (id)
            );
    """
        self.execute(sql, commit=True)

    def create_table_currency(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Currency (
           id int PRIMARY KEY,
           currency varchar(255),
           cost float 
        );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{item} = ?" for item in parameters])
        return sql, tuple(parameters.values())

    def update_user_phone(self, phone, tg_id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = """
        UPDATE Users SET phone=? WHERE tg_id=?
        """
        return self.execute(sql, parameters=(phone, tg_id), commit=True)

    def update_user_lang(self, lang, tg_id):
        sql = "UPDATE Users SET lang=? WHERE tg_id=?"
        parameters = (lang, tg_id)
        return self.execute(sql, parameters=parameters, commit=True)

    def update_currency(self, currency):
        sql = "UPDATE Currency SET cost=? WHERE currency=?"
        parameters = (currency, "yuan")
        return self.execute(sql, parameters=parameters, commit=True)

    def select_users(self):
        sql = "SELECT username, tg_id, fullname FROM Users"
        return self.execute(sql, fetchall=True)

    def select_user_lang(self, **kwargs):
        sql = "SELECT lang FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_user_phone(self, **kwargs):
        sql = "SELECT phone FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_currency(self):
        sql = "SELECT cost FROM Currency"
        return self.execute(sql, fetchone=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def create_user(self, tg_id, username, lang, fullname):
        sql = "INSERT INTO users(tg_id, username, lang, fullname) VALUES (?, ?, ?, ?)"
        parameters = (tg_id, username, lang, fullname)
        return self.execute(sql, parameters=parameters, commit=True)

    def create_screen(self, user_id, screenshot):
        sql = "INSERT INTO screen(user_id, screenshot) VALUES (?, ?)"
        parameters = (user_id, screenshot)
        return self.execute(sql, parameters=parameters, commit=True)

    def create_currency(self, currency, cost):
        sql = "INSERT INTO currency(currency, cost) VALUES (?, ?)"
        parameters = (currency, cost)
        return self.execute(sql, parameters=parameters, commit=True)


def logger(statement):
    print(
        f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
"""
    )