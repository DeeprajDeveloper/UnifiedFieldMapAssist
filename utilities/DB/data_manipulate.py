import sqlite3 as sql
import traceback


def dml_execute_script(database: str, sql_script: str) -> None:
    sqlite_connection = sql.connect(database=database)
    try:
        sqlite_connection.executescript(sql_script)
        sqlite_connection.commit()
    except sql.Error as error:
        print(f"Error Message: {str(error)}")
        raise error
    finally:
        sqlite_connection.close()


def dml_dql_execute_parameterized_script(database: str, sql_script: str, data_input_list: dict) -> list:
    """
    Executes a DML where the SQL Script contains parameters (such as 'var1', 'var2', etc. preceding with an 'question mark').
    Returns a BOOLEAN true/false depending on the statement execution.

    :param database: SQLITE database file path
    :param sql_script: SQL Statement to be executed that contains parameters/variables
    :param data_input_list: a dictionary/json input that contains a key-value pair for the variables
    :return:
    """

    sqlite_connection = sql.connect(database=database)
    sqlite_connection.row_factory = lambda cursor, row: row[0]
    updated_sql_script = sql_script
    try:
        sqlite_cursor = sqlite_connection.cursor()
        for key, value in data_input_list.items():
            updated_sql_script = updated_sql_script.replace(key, str(value))
        sqlite_cursor.executescript(updated_sql_script)
        sql_data = sqlite_cursor.fetchall()
        return sql_data
    except Exception as err:
        error_code = f"{type(err).__name__}: {str(err)}"
        error_stack_trace = traceback.format_exc()
        print(f"{error_code}\n{error_stack_trace}")
    finally:
        sqlite_connection.close()
