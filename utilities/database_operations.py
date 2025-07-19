from .base import DBConnection
import traceback
import utilities.custom_app_logger as log
from utilities import custom_app_error as cust_error
from app.constants import QrySQLiteMaster as QryMaster


class CheckIf(DBConnection):
    def data_exists(self, sql_script: str, data_parameter=None) -> bool:
        try:
            if sql_script == '' or sql_script is None:
                raise cust_error.MissingInput(message=f"SQL Script was not provided to be executed.")
            else:
                status: bool = False
                with self.with_connection() as connection:
                    sql_cursor = connection.cursor()
                    if data_parameter is not None:
                        sql_cursor.execute(sql_script, data_parameter)
                    else:
                        sql_cursor.execute(sql_script)
                    data_extract = sql_cursor.fetchone()
                    status = True if data_extract is not None and data_extract[0] >= 1 else False
                    return status
        except Exception as obj_err:
            print(f"Error Message: {str(obj_err)}")
            log.log_message(message=f"Error Message: {str(obj_err)}", call_type='UTIL.DB', level='error')
            return status

    def table_exists(self, table_name: str) -> bool:
        status: bool = False
        try:
            if table_name == '' or table_name is None:
                raise cust_error.MissingInput(message=f"Table Name was not provided.")
            else:
                sql_script = QryMaster.GET_TABLE_INFO
                data_param = {'searchValue': table_name}
                with self.with_connection() as connection:
                    sql_cursor = connection.cursor()
                    sql_cursor.execute(sql_script, data_param)
                    extract_info = sql_cursor.fetchone()
                    status = False if extract_info[0] == 0 else True
                    return status
        except Exception as obj_err:
            print(f"Error Message: {str(obj_err)}")
            log.log_message(message=f"Error Message: {str(obj_err)}", call_type='UTIL.DB', level='error')
            return status

    def view_exists(self, view_name: str) -> bool:
        status: bool = False
        try:
            if view_name == '' or view_name is None:
                raise cust_error.MissingInput(message=f"View Name was not provided.")
            else:
                sql_script = QryMaster.GET_VIEW_INFO
                data_param = {'searchValue': view_name}
                with self.with_connection() as connection:
                    sql_cursor = connection.cursor()
                    sql_cursor.execute(sql_script, data_param)
                    extract_info = sql_cursor.fetchone()
                    status = False if extract_info[0] == 0 else True
                    return status
        except Exception as obj_err:
            print(f"Error Message: {str(obj_err)}")
            log.log_message(message=f"Error Message: {str(obj_err)}", call_type='UTIL.DB', level='error')
            return status


class QueryInformation(DBConnection):

    def get_rows(self, sql_script: str, row_count: int = None, return_list=True) -> list:
        """
        Returns n-rows for the provided SQL Query. | return_list = TRUE - To get results as LIST | return_list = FALSE - To get results as LIST[TUPLES]

        :param sql_script: SQL Statement to be executed
        :param row_count: capture the number of records to be returned
        :param return_list: Boolean. default TRUE
        :return: LIST / LIST[TUPLES]
        """
        try:
            result_data: list
            with self.with_connection() as obj_conn:
                if return_list:
                    obj_conn.row_factory = lambda cursor, row: row[0]
                obj_cursor = obj_conn.cursor()
                obj_cursor.execute(sql_script)
                result_data = obj_cursor.fetchall()[0:row_count]
                return result_data
        except Exception as obj_err:
            error_code = f"{type(obj_err).__name__}: {str(obj_err)}"
            error_stack_trace = traceback.format_exc()
            print(f"{error_code}\n{error_stack_trace}")
            log.log_message(message=f"{error_code}\n{error_stack_trace}", call_type='UTIL.DB', level='error')
            raise obj_err

    def get_rows_with_param(self, sql_script: str, data_parameters: dict, row_count: int = None, return_list=True) -> list:
        """
        Returns n-rows for the provided SQL Query based on the data_parameters. | return_list = TRUE - To get results as LIST | return_list = FALSE - To get results as LIST[TUPLES]

        :param sql_script: SQL Statement to be executed
        :param row_count: capture the number of records to be returned
        :param data_parameters: dictionary of key-value pairs to be used for the select statement.
        :param return_list: Boolean. default TRUE
        :return: LIST / LIST[TUPLES]
        """

        try:
            with self.with_connection() as obj_conn:
                obj_cursor = obj_conn.cursor()
                obj_cursor.execute(sql_script, data_parameters)
                sql_data = obj_cursor.fetchall()[0:row_count]
                return list(sql_data[0]) if return_list else sql_data
        except Exception as err:
            error_code = f"{type(err).__name__}: {str(err)}"
            error_stack_trace = traceback.format_exc()
            print(f"{error_code}\n{error_stack_trace}")
            raise err


class DataManipulation(DBConnection):
    def insert_data(self, sql_script: str) -> None:
        try:
            with self.with_connection() as obj_conn:
                obj_conn.executescript(sql_script)
                obj_conn.commit()
        except Exception as obj_err:
            error_code = f"{type(obj_err).__name__}: {str(obj_err)}"
            error_stack_trace = traceback.format_exc()
            print(f"{error_code}\n{error_stack_trace}")
            log.log_message(message=f"{error_code}\n{error_stack_trace}", call_type='UTIL.DB', level='error')
            raise obj_err

    def insert_data_with_param(self, sql_script: str, data_parameters: dict) -> None:
        """
        Executes a DML where the SQL Script contains parameters (such as 'var1', 'var2', etc. preceding with an 'question mark').
        Returns a BOOLEAN true/false depending on the statement execution.

        :param sql_script: SQL Statement to be executed that contains parameters/variables
        :param data_parameters: a dictionary/json input that contains a key-value pair for the variables
        :return:
        """

        try:
            with self.with_connection() as obj_conn:
                obj_conn.executescript(sql_script, data_parameters)
                obj_conn.commit()
        except Exception as obj_err:
            error_code = f"{type(obj_err).__name__}: {str(obj_err)}"
            error_stack_trace = traceback.format_exc()
            print(f"{error_code}\n{error_stack_trace}")
            log.log_message(message=f"{error_code}\n{error_stack_trace}", call_type='UTIL.DB', level='error')
            raise obj_err

    def update_data(self, sql_script: str) -> None:
        try:
            with self.with_connection() as obj_conn:
                obj_conn.execute(sql_script)
                obj_conn.commit()
        except Exception as obj_err:
            error_code = f"{type(obj_err).__name__}: {str(obj_err)}"
            error_stack_trace = traceback.format_exc()
            print(f"{error_code}\n{error_stack_trace}")
            log.log_message(message=f"{error_code}\n{error_stack_trace}", call_type='UTIL.DB', level='error')
            raise obj_err

    def update_data_with_param(self, sql_script: str, data_parameters: dict) -> None:
        """
        Executes a DML where the SQL Script contains parameters (such as 'var1', 'var2', etc. preceding with an 'question mark').
        Returns a BOOLEAN true/false depending on the statement execution.

        :param sql_script: SQL Statement to be executed that contains parameters/variables
        :param data_parameters: a dictionary/json input that contains a key-value pair for the variables
        :return:
        """

        try:
            with self.with_connection() as obj_conn:
                obj_conn.execute(sql_script, data_parameters)
                obj_conn.commit()
        except Exception as obj_err:
            error_code = f"{type(obj_err).__name__}: {str(obj_err)}"
            error_stack_trace = traceback.format_exc()
            print(f"{error_code}\n{error_stack_trace}")
            log.log_message(message=f"{error_code}\n{error_stack_trace}", call_type='UTIL.DB', level='error')
            raise obj_err

