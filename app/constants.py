class Information:
    VERSION: str = 'v.0.0.1'
    AUTHOR: str = 'Adhikary, Deepraj'
    CREATE_DATE: str = 'May 03, 2025'
    RELEASE_DATE: str = 'TBC'


class QueriesRead:
    DQL_TBL_GUI_RECORD_COUNT = f"SELECT count(*) FROM guiInformation WHERE RecordStatus = 1"
    DQL_TBL_GUI_ALL_IDS = f"SELECT id FROM guiInformation WHERE RecordStatus = 1"
    DQL_TBL_GUI_RANGE_IDS = f"SELECT id FROM guiInformation WHERE RecordStatus = 1 and id between ?startValue and ?endValue"
    DQL_TBL_GUI_INFO = f"SELECT screenName, sectionName, fieldName, fieldDescription, fieldStateId, uiTypId, dependencyId FROM guiInformation where RecordStatus = 1 and id = ?searchValue"
    DQL_TBL_API_INFO = f"SELECT entityName, domainName, subdomainName, childDomainLvl1, childDomainLvl2, businessFieldName, datatypeId FROM apiInformation where RecordStatus = 1 and guiId = ?searchValue"
    DQL_TBL_DB_INFO = f"SELECT tableName, columnName, columnSize, datatypeId FROM databaseInformation where RecordStatus = 1 and apiId = ?searchValue"
    DQL_TBL_API_EXPOSURE_INFO = f"Select ae.isRead, ae.isWrite, ae.isKafka from apiExposure ae inner join apiInformation ai on ai.id = ae.apiId where ai.RecordStatus = 1 and ai.guiId = ?searchValue"
    DQL_VW_GUI_INFO = f"SELECT screenName, sectionName, fieldName, fieldDescription, fieldStateDesc, uiTypDesc, dependencyId FROM vw_guiInformation where id = ?searchValue"
    DQL_VW_API_INFO = f"SELECT entityName, domainName, subdomainName, childDomainLvl1, childDomainLvl2, businessFieldName, dataTypDesc FROM vw_apiInformation where id = ?searchValue"
    DQL_VW_DB_INFO = f"Select tableName, columnName, columnSize, dataTypDesc from vw_dbInformation where id = ?searchValue"
    DQL_TBL_DATATYPE = f"SELECT dataTypeId from dataType where dataTypeDesc = '?searchValue'"
    DQL_TBL_FIELD_STATE = f"SELECT fieldStateId from fieldState where fieldStateDesc = '?searchValue'"
    DQL_TBL_UI_TYPE = f"SELECT uiTypId from guiFieldType where uiTypDesc = '?searchValue'"


class SQLInsert:
    DML_INSERT_GUI_INFO = (f"INSERT INTO guiInformation (screenName, sectionName, fieldName, fieldDescription, fieldStateId, uiTypId, dependencyId) "
                           f"VALUES('?screenName', '?sectionName', '?fieldName', '?fieldDescription', ?fieldStateId, ?uiTypeId, ?dependencyId);")
    DML_INSERT_API_INFO = (f"INSERT INTO apiInformation (guiId, entityName, domainName, subdomainName, childDomainLvl1, childDomainLvl2, businessFieldName, datatypeId) "
                           f"VALUES(?guiId, '?entityName', '?domainName', '?subDomainName', '?childDomainLvl1', '?childDomainLvl2', '?businessFieldName', ?datatypeId);")


class APIKeysList:
    GUI_INFO_KEYS: list = ['screenName', 'sectionName', 'fieldName', 'fieldDescription', 'fieldState', 'fieldType', 'fieldDependencyId']
    API_INFO_KEYS: list = ['entityName', 'domainName', 'subdomainName', 'childDomainNameLvl1', 'childDomainNameLvl2', 'businessFieldName', 'type']
    DB_MAPPING_KEYS: list = ['tableName', 'columnName', 'columnSize', 'dataType']
    API_EXPOSURE_KEYS: list = ['readAPI', 'writeAPI', 'kafka']
    CONFIG_KEYS: list = ['configParameterName', 'configParameterValue']
    VALID_CONFIG_SEARCH_KEYS: list = ['rowCountPerPage', 'paginationDisplayButtonsCount']


class FileSystemInformation:
    DATA_TEMPLATE_FOLDER = r'app\gui\static\fileSystem\fileTemplate'
    DATA_TEMPLATE_FILENAME = r'MappingInformationTemplate.xlsx'
    UPLOAD_FOLDER = r'fileSystem\fileUploads'
    DOWNLOAD_FOLDER = r'fileSystem\fileDownloads'


class GuiConfigInformation:
    CONFIG_KEY_VALUE_MAPPING = {
        "rowCountPerPage": 25
    }


class TemplateInformation:
    WORKSHEET_NAME = r"DataEntry"
    EXCEL_TABLE_NAME = r"DataTable"
    XL_COLUMNS_API = ['API_EntityName', 'API_DomainName', 'API_SubdomainName', 'API_ChildDomainNameL1', 'API_ChildDomainNameL2', 'API_BusinessFieldName', 'API_Type']
    XL_COLUMNS_FLAGS = ['Flag_ReadAPI', 'Flag_WriteAPI', 'Flag_KafkaMsg']
    XL_COLUMNS_GUI = ['GUI_ScreenName', 'GUI_SectionName', 'GUI_LabelName', 'GUI_LabelDescription', 'GUI_FieldState', 'GUI_FieldType', 'GUI_DependencyOn']
    XL_COLUMNS_ALL = XL_COLUMNS_API + XL_COLUMNS_FLAGS + XL_COLUMNS_GUI


class MappingMatrix:
    DESCRIPTION_TO_CODE_KEYS = ["GUI_FieldState", "GUI_FieldType", "API_Type"]
    XL_COLUMNS_KEYS_API_MAPPING = {
        'API_EntityName': {
            "sqlKey": "?entityName",
            "apiKey": 'apiInformation.entityName'
        },
        'API_DomainName': {
            "sqlKey": "?domainName",
            "apiKey": 'apiInformation.domainName'
        },
        'API_SubdomainName': {
            "sqlKey": "?subDomainName",
            "apiKey": 'apiInformation.subdomainName'
        },
        'API_ChildDomainNameL1': {
            "sqlKey": "?childDomainLvl1",
            "apiKey": 'apiInformation.childDomainNameLvl1'
        },
        'API_ChildDomainNameL2': {
            "sqlKey": "?childDomainLvl2",
            "apiKey": 'apiInformation.childDomainNameLvl2'
        },
        'API_BusinessFieldName': {
            "sqlKey": "?businessFieldName",
            "apiKey": 'apiInformation.businessFieldName'
        },
        'API_Type': {
            "sqlKey": "?datatypeId",
            "apiKey": 'apiInformation.type'
        }
    }
    XL_COLUMNS_KEYS_GUI_MAPPING = {
        'GUI_ScreenName': {
            "sqlKey": "?screenName",
            "apiKey": 'guiInformation.screenName'
        },
        'GUI_SectionName': {
            "sqlKey": "?sectionName",
            "apiKey": 'guiInformation.sectionName'
        },
        'GUI_LabelName': {
            "sqlKey": "?fieldName",
            "apiKey": 'guiInformation.fieldName'
        },
        'GUI_LabelDescription': {
            "sqlKey": "?fieldDescription",
            "apiKey": 'guiInformation.fieldDescription'
        },
        'GUI_FieldState': {
            "sqlKey": "?fieldStateId",
            "apiKey": 'guiInformation.fieldState'
        },
        'GUI_FieldType': {
            "sqlKey": "?uiTypeId",
            "apiKey": 'guiInformation.fieldType'
        },
        'GUI_DependencyOn': {
            "sqlKey": "?dependencyId",
            "apiKey": 'guiInformation.fieldDependencyId'
        }
    }
    XL_COLUMNS_KEYS_FLAG_MAPPING = {
        'Flag_ReadAPI': 'apiExposureFlags.readAPI',
        'Flag_WriteAPI': 'apiExposureFlags.writeAPI',
        'Flag_KafkaMsg': 'apiExposureFlags.kafkaAPI'
    }
    XL_COLUMNS_KEYS_MAPPING_ALL = [XL_COLUMNS_KEYS_API_MAPPING, XL_COLUMNS_KEYS_FLAG_MAPPING, XL_COLUMNS_KEYS_GUI_MAPPING]
    DESCRIPTION_TO_CODE_QRY_MAPPING = {
        "GUI_FieldState": QueriesRead.DQL_TBL_FIELD_STATE,
        "GUI_FieldType": QueriesRead.DQL_TBL_UI_TYPE,
        "API_Type": QueriesRead.DQL_TBL_DATATYPE
    }
