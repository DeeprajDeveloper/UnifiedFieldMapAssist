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


class APIKeysList:
    GUI_INFO_KEYS: list = ['screenName', 'sectionName', 'fieldName', 'fieldDescription', 'fieldState', 'fieldType', 'fieldDependencyId']
    API_INFO_KEYS: list = ['entityName', 'domainName', 'subdomainName', 'childDomainNameLvl1', 'childDomainNameLvl2', 'businessFieldName', 'type']
    DB_MAPPING_KEYS: list = ['tableName', 'columnName', 'columnSize', 'dataType']
    API_EXPOSURE_KEYS: list = ['readAPI', 'writeAPI', 'kafka']
    CONFIG_KEYS: list = ['configParameterName', 'configParameterValue']
    VALID_CONFIG_SEARCH_KEYS: list = ['rowCountPerPage', 'paginationDisplayButtonsCount']


class FileSystemInformation:
    DATA_TEMPLATE_FOLDER = r'app\gui\static\fileSystem\fileTemplate'
    DATA_TEMPLATE_FILENAME = r'sample.txt'
    UPLOAD_FOLDER = r'fileSystem/fileUploads'
    DOWNLOAD_FOLDER = r'fileSystem/fileDownloads'


class GuiConfigInformation:
    CONFIG_KEY_VALUE_MAPPING = {
        "rowCountPerPage": 25
    }

