import sqlite3 as sql
import traceback
from typing import Union


def check_data_exists(database: str, sql_script: str) -> bool:
    status: bool
    sqlite_connection = sql.connect(database=database)
    try:
        sqlite_cursor = sqlite_connection.cursor()
        sqlite_cursor.execute(sql_script)
        data_extract = sqlite_cursor.fetchone()
        if data_extract is not None:
            status = True if data_extract[0] >= 1 else False
        else:
            status = False
        return status
    except sql.Error as error:
        print(f"Error Message: {str(error)}")
        return False
    finally:
        sqlite_connection.close()


def fetch_all_rows(database: str, sql_script: str, return_list=True) -> list:
    """
    Returns SQL Statement execution results as a LIST by default.
    When return_list is set to False, this returns the SQL Statement execution results as a LIST of TUPLES

    :param database: SQLITE database file path
    :param sql_script: SQL Statement to be executed
    :param return_list: Boolean. default TRUE
    :return: LIST / LIST of TUPLES
    """
    sql_data: list
    sqlite_connection = sql.connect(database=database)

    if return_list:
        sqlite_connection.row_factory = lambda cursor, row: row[0]

    try:
        sqlite_cursor = sqlite_connection.cursor()
        sqlite_cursor.execute(sql_script)
        sql_data = sqlite_cursor.fetchall()
        return sql_data
    except Exception as err:
        error_code = f"{type(err).__name__}: {str(err)}"
        error_stack_trace = traceback.format_exc()
        print(f"{error_code}\n{error_stack_trace}")
        raise err
    finally:
        sqlite_connection.close()


def fetch_all_rows_for_range(database: str, sql_script: str, range_start: Union[int, str], range_end: Union[int, str], return_list=True) -> list:
    """
    Returns SQL Statement execution results as a LIST by default.
    When return_list is set to False, this returns the SQL Statement execution results as a LIST of TUPLES

    :param database: SQLITE database file path
    :param sql_script: SQL Statement to be executed
    :param range_start: int / string. Must be a value that will replace the ?startValue in the SQL Script
    :param range_end: int / string. Must be a value that will replace the ?endValue in the SQL Script
    :param return_list: Boolean. default TRUE
    :return: LIST / LIST of TUPLES
    """
    sql_data: list
    sqlite_connection = sql.connect(database=database)

    if return_list:
        sqlite_connection.row_factory = lambda cursor, row: row[0]

    try:
        sqlite_cursor = sqlite_connection.cursor()
        updated_sql_script = sql_script.replace('?startValue', str(range_start)).replace('?endValue', str(range_end))
        sqlite_cursor.execute(updated_sql_script)
        sql_data = sqlite_cursor.fetchall()
        return sql_data
    except Exception as err:
        error_code = f"{type(err).__name__}: {str(err)}"
        error_stack_trace = traceback.format_exc()
        print(f"{error_code}\n{error_stack_trace}")
        raise err
    finally:
        sqlite_connection.close()


def fetch_all_rows_for_one_input(database: str, sql_script: str, data_input: str, return_list=True) -> list:
    """
    Returns SQL Statement execution results after replacing the '?searchValue' with the data_input as a LIST by default.
    When return_list is set to False, this returns the SQL Statement execution results as a LIST of TUPLES

    :param database: SQLITE database file path
    :param sql_script: SQL Statement to be executed
    :param data_input: text input to replace the '?' in the SQL Statement
    :param return_list: Boolean. default TRUE
    :return: LIST / LIST of TUPLES
    """

    sqlite_connection = sql.connect(database=database)

    # if return_list:
    #     sqlite_connection.row_factory = lambda cursor, row: row[0]

    try:
        sqlite_cursor = sqlite_connection.cursor()
        updated_sql_script = sql_script.replace('?searchValue', str(data_input))
        sqlite_cursor.execute(updated_sql_script)
        sql_data = sqlite_cursor.fetchall()
        if return_list:
            return sql_data[0]
        else:
            return sql_data
    except Exception as err:
        error_code = f"{type(err).__name__}: {str(err)}"
        error_stack_trace = traceback.format_exc()
        print(f"{error_code}\n{error_stack_trace}")
        raise err
    finally:
        sqlite_connection.close()


def dql_fetch_one_row_for_one_input(database: str, sql_script: str, data_input: str) -> list:
    """
    Returns SQL Statement execution results after replacing the '?' with the data_input as one item by default.
    When return_list is set to False, this returns the SQL Statement execution results as a LIST of TUPLES

    :param database: SQLITE database file path
    :param sql_script: SQL Statement to be executed
    :param data_input: text input to replace the '?searchValue' in the SQL Statement
    :return: One item
    """

    sqlite_connection = sql.connect(database=database)
    sqlite_connection.row_factory = lambda cursor, row: row[0]

    try:
        sqlite_cursor = sqlite_connection.cursor()
        updated_sql_script = sql_script.replace('?searchValue', str(data_input))
        sqlite_cursor.execute(updated_sql_script)
        sql_data = sqlite_cursor.fetchone()
        return sql_data
    except Exception as err:
        error_code = f"{type(err).__name__}: {str(err)}"
        error_stack_trace = traceback.format_exc()
        print(f"{error_code}\n{error_stack_trace}")
        raise err
    finally:
        sqlite_connection.close()

