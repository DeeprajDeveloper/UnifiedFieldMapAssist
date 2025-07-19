class Information:
    VERSION: str = 'v.0.0.1'
    AUTHOR: str = 'Adhikary, Deepraj'
    CREATE_DATE: str = 'May 03, 2025'
    RELEASE_DATE: str = 'TBC'


class QrySQLiteMaster:
    GET_TABLE_INFO = r"SELECT count(*) FROM sqlite_master WHERE type = 'table' and name = :searchValue"
    GET_VIEW_INFO = r"SELECT count(*) FROM sqlite_master WHERE type = 'view' and name = :searchValue"


class QryGetGuiInfo:
    TABLE_REC_COUNT = r"SELECT count(*) FROM guiInformation WHERE RecordStatus = 1"
    TABLE_GET_ALL_IDS = r"SELECT id FROM guiInformation WHERE RecordStatus = 1"
    TABLE_GET_ALL_IDS_BTW_RANGE = r"SELECT id FROM guiInformation WHERE RecordStatus = 1 and id between :startValue and :endValue"
    TABLE_GET_INFO_BY_ID = r"SELECT screenName, sectionName, fieldName, fieldDescription, fieldStateId, uiTypId, dependencyId FROM guiInformation where RecordStatus = 1 and id = :searchValue"
    VIEW_GET_INFO_BY_ID = r"SELECT screenName, sectionName, fieldName, fieldDescription, fieldStateDesc, uiTypDesc, dependencyId FROM vw_guiInformation where id = :searchValue"


class QryGetApiInfo:
    TABLE_REC_COUNT = r"SELECT count(*) FROM apiInformation WHERE RecordStatus = 1"
    TABLE_GET_ALL_IDS = r"SELECT id FROM apiInformation WHERE RecordStatus = 1"
    TABLE_GET_ALL_IDS_BTW_RANGE = r"SELECT id FROM apiInformation WHERE RecordStatus = 1 and id between :startValue and :endValue"
    TABLE_GET_INFO_BY_GUI_ID = r"SELECT entityName, domainName, subdomainName, childDomainLvl1, childDomainLvl2, businessFieldName, datatypeId FROM apiInformation where RecordStatus = 1 and guiId = :searchValue"
    TABLE_GET_INFO_BY_API_ID = r"SELECT entityName, domainName, subdomainName, childDomainLvl1, childDomainLvl2, businessFieldName, datatypeId FROM apiInformation where RecordStatus = 1 and id = :searchValue"
    VIEW_GET_INFO_BY_GUI_ID = r"SELECT entityName, domainName, subdomainName, childDomainLvl1, childDomainLvl2, businessFieldName, dataTypDesc FROM vw_apiInformation where id = :searchValue"


class QryGetDbInfo:
    TABLE_REC_COUNT = r"SELECT count(*) FROM databaseInformation WHERE RecordStatus = 1"
    TABLE_GET_ALL_IDS = r"SELECT id FROM databaseInformation WHERE RecordStatus = 1"
    TABLE_GET_ALL_IDS_BTW_RANGE = r"SELECT id FROM databaseInformation WHERE RecordStatus = 1 and id between :startValue and :endValue"
    TABLE_GET_INFO_BY_API_ID = r"SELECT tableName, columnName, columnSize, datatypeId FROM databaseInformation where RecordStatus = 1 and apiId = :searchValue"
    VIEW_GET_INFO_BY_GUI_ID = r"Select tableName, columnName, columnSize, dataTypDesc from vw_dbInformation where id = :searchValue"


class QryGetFlagsInfo:
    TABLE_REC_COUNT = r"SELECT count(*) FROM apiExposure WHERE RecordStatus = 1"
    TABLE_GET_ALL_IDS = r"SELECT id FROM apiExposure WHERE RecordStatus = 1"
    TABLE_GET_ALL_IDS_BTW_RANGE = r"SELECT id FROM apiExposure WHERE RecordStatus = 1 and id between :startValue and :endValue"
    TABLE_GET_INFO_BY_API_ID = r"SELECT ae.isRead, ae.isWrite, ae.isKafka from apiExposure WHERE ae.apiId = :searchValue"
    TABLE_GET_INFO_BY_GUI_ID = r"SELECT ae.isRead, ae.isWrite, ae.isKafka from apiExposure ae INNER JOIN apiInformation ai ON ai.id = ae.apiId WHERE ai.RecordStatus = 1 AND ai.guiId = :searchValue"


class QryGetConfiguration:
    TABLE_REC_COUNT = r"SELECT count(*) FROM configParameters"
    TABLE_GET_ALL_IDS = r"SELECT paramId FROM configParameters"
    TABLE_GET_ALL_CATEGORIES = r"SELECT distinct category FROM configParameters"
    TABLE_GET_ALL_PARAM_KEYS = r"SELECT distinct paramKey FROM configParameters"
    TABLE_GET_INFO_BY_PARAMID = r"SELECT paramId, paramKey, paramValue FROM configParameters where paramId = :searchValue"
    TABLE_GET_ALL_INFO = r"SELECT paramId, paramKey, paramValue FROM configParameters"
    TABLE_GET_INFO_BY_PARAM_KEY = r"SELECT paramId, paramKey, paramValue FROM configParameters where paramKey = :searchValue"
    TABLE_GET_INFO_BY_CATEGORY = r"SELECT paramKey, paramValue FROM configParameters where category = :searchValue"
    TABLE_GET_INFO_BY_PARAM_CATEGORY = r"SELECT paramId, paramKey, paramValue FROM configParameters where category = :category AND paramKey = :paramKey"
    TABLE_GET_PARAM_VALUES_BY_PARAM_CATEGORY = r"SELECT paramValue FROM configParameters where category = :category AND paramKey = :paramKey"
    TABLE_GET_PARAM_VALUES_BY_PARAMID = r"SELECT paramValue FROM configParameters where paramId = :searchValue"
    TABLE_GET_UPDATE_PAYLOAD_KEYS = r"SELECT paramValue from configParameters where category='updatePayload' and paramKey = :searchValue"


class QryGetLookup:
    TABLE_DATATYPE = r"SELECT dataTypeId from dataType where dataTypeDesc = :searchValue"
    TABLE_FIELD_STATE = r"SELECT fieldStateId from fieldState where fieldStateDesc = :searchValue"
    TABLE_UI_TYPE = r"SELECT uiTypId from guiFieldType where uiTypDesc = :searchValue"


class QryGetUpdateQueryMapping:
    TABLE_QRY_MAPPING_BY_KEY = r"SELECT queryString FROM dataQueryMapping WHERE entityType = :entityType AND keyName = :keyName"


class DataInsertStatement:
    ADD_GUI_MAPPING = (r"INSERT INTO guiInformation (screenName, sectionName, fieldName, fieldDescription, fieldStateId, uiTypId, dependencyId) "
                       r"VALUES(':screenName', ':sectionName', ':fieldName', ':fieldDescription', :fieldStateId, :uiTypeId, :dependencyId);")
    ADD_API_MAPPING = (r"INSERT INTO apiInformation (guiId, entityName, domainName, subdomainName, childDomainLvl1, childDomainLvl2, businessFieldName, datatypeId) "
                       r"VALUES(:guiId, ':entityName', ':domainName', ':subDomainName', ':childDomainLvl1', ':childDomainLvl2', ':businessFieldName', :datatypeId);")


class DataUpdateStatement:
    UPDATE_CONFIG_BY_PARAMID = r"UPDATE configParameters SET paramValue = :updateValue WHERE paramId = :paramId"


class QryMappingMatrix:
    """
    Result Format: List[Tuple]. Tuple Format: (sqlKeyName, apiPathKey)
    """
    API_GET_SQL_API_KEYS_BY_XL_COLUMN = r"SELECT sqlKeyName, apiPathKey FROM mappingMatrix WHERE mappingType = 'API' AND xlColumnName = :xlColName"
    GUI_GET_SQL_API_KEYS_BY_XL_COLUMN = r"SELECT sqlKeyName, apiPathKey FROM mappingMatrix WHERE mappingType = 'GUI' AND xlColumnName = :xlColName"
    FLAG_GET_SQL_API_KEYS_BY_XL_COLUMN = r"SELECT sqlKeyName, apiPathKey FROM mappingMatrix WHERE mappingType = 'FLAG' AND xlColumnName = :xlColName"
    DB_GET_SQL_API_KEYS_BY_XL_COLUMN = r"SELECT sqlKeyName, apiPathKey FROM mappingMatrix WHERE mappingType = 'DB' AND xlColumnName = :xlColName"

    API_GET_SQL_KEYS_BY_UI_TAG = r"SELECT sqlKeyName FROM mappingMatrix WHERE mappingType = 'API' AND uiTagName = :uiTagName"
    GUI_GET_SQL_KEYS_BY_UI_TAG = r"SELECT sqlKeyName FROM mappingMatrix WHERE mappingType = 'GUI' AND uiTagName = :uiTagName"
    FLAG_GET_SQL_KEYS_BY_UI_TAG = r"SELECT sqlKeyName FROM mappingMatrix WHERE mappingType = 'FLAG' AND uiTagName = :uiTagName"
    DB_GET_SQL_KEYS_BY_UI_TAG = r"SELECT sqlKeyName FROM mappingMatrix WHERE mappingType = 'DB' AND uiTagName = :uiTagName"

    GET_SQL_KEYS_BY_UI_TAG = r"SELECT sqlKeyName FROM mappingMatrix WHERE uiTagName = :uiTagName"

    MATRIX_UI_TAG_SQL_QUERY = {
        'api': API_GET_SQL_KEYS_BY_UI_TAG,
        'gui': GUI_GET_SQL_KEYS_BY_UI_TAG,
        'db': DB_GET_SQL_KEYS_BY_UI_TAG,
        'flag': FLAG_GET_SQL_KEYS_BY_UI_TAG,
    }
    MATRIX_XL_COL_SQL_QUERY = {
        'api': API_GET_SQL_API_KEYS_BY_XL_COLUMN,
        'gui': GUI_GET_SQL_API_KEYS_BY_XL_COLUMN,
        'db': DB_GET_SQL_API_KEYS_BY_XL_COLUMN,
        'flag': FLAG_GET_SQL_API_KEYS_BY_XL_COLUMN,
    }


class MiscInfo:
    MAPPING_INSERT_PRIORITY = {
        'gui': 1,
        'api': 2,
        'db': 3,
        'flag': 4
    }
