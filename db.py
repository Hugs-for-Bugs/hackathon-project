import sqlite3

from cfg import config_dict
from typing import Union, List, Tuple


conn = sqlite3.connect(config_dict["DATABASE"])
cursor = conn.cursor()


def create_tables() -> None:
    cursor.execute(
        """create table if not exists users(
            id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            tg_user_id integer UNIQUE,
            location text,
            page text NOT NULL,
            reg_date text
        )""",
    )

    cursor.execute(
        """create table if not exists vacancies (
            id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            tg_user_id integer,
            title text,
            info text,
            location text,
            contacts text,
            reg_date text
        )""",
    )

    conn.commit()


def set_start_page_or_ignore(tg_user_id: int) -> None:
    sql_stmt = "insert or ignore into users (reg_date, tg_user_id, page) values(datetime('now'), ?, ?)"

    cursor.execute(
        sql_stmt, (tg_user_id, "start"))

    sql_stmt = "insert or ignore into vacancies (reg_date, tg_user_id) values(datetime('now'), ?)"

    cursor.execute(
        sql_stmt, (tg_user_id,))

    conn.commit()


def change_value_in_DB(**kwargs: dict) -> None:
    sql_stmt = "update {table} set {field_to_update} = ? where {pivot}  = ? and id = (select MAX(id) from {table} where {pivot} = ?)".format(
        **kwargs)

    cursor.execute(
        sql_stmt, (kwargs["field_to_update_value"], kwargs["pivot_value"], kwargs["pivot_value"]))

    conn.commit()


def return_value_from_DB(**kwargs: dict) -> Union[int, str, None]:
    sql_stmt = "select {field} from {table} where {pivot} = ?".format(
        **kwargs,
    )

    cursor.execute(sql_stmt, (kwargs["pivot_value"],))

    return cursor.fetchall()[0][0]


def check_if_vacancy_is_full(tg_user_id: int) -> bool:
    sql_stmt = "select * from vacancies where tg_user_id = ?"

    cursor.execute(sql_stmt, (tg_user_id,))

    return not (None in cursor.fetchall()[-1])


def insert_empty(tg_user_id: int) -> None:
    sql_stmt = "insert into vacancies (reg_date, tg_user_id) values(datetime('now'), ?)"

    cursor.execute(sql_stmt, (tg_user_id,))

    conn.commit()


def get_vacancies(location: str = "") -> List[Tuple[Union[str, int]]]:
    sql_stmt: str

    if location:
        sql_stmt = "select * from vacancies where location = ?"

        cursor.execute(sql_stmt, (location,))
    else:
        sql_stmt = "select * from vacancies"

        cursor.execute(sql_stmt)

    return [vacancy for vacancy in cursor.fetchall() if not (None in vacancy)]
