--select transform_values(cast(json_parse(_col0) as MAP(varchar, json)) , (k, v) -> if(k!='name',v)) from pse_restore_ms
--select REGEXP_EXTRACT(_col0,'(.*)\"name\"\:\"ML_Demos') from pse_restore_ms
WITH unnest_config AS(
  SELECT 
    element_at(
      m,
      'name'
    ) AS name,
    element_at(
      m,
      'description'
    ) AS description,
    element_at(
      m,
      'scheduleType'
    ) AS scheduleType,
    element_at(
      m,
      'scheduleOption'
    ) AS scheduleOption,
    element_at(
      m,
      'timezone'
    ) AS timezone,
    element_at(
      m,
      'matrixUpdatedAt'
    ) AS matrixUpdatedAt,
    element_at(
      m,
      'workflowHiveOnly'
    ) AS workflowHiveOnly,
    element_at(
      m,
      'hiveEngineVersion'
    ) AS hiveEngineVersion,
    element_at(
      m,
      'hivePoolName'
    ) AS hivePoolName,
    element_at(
      m,
      'prestoPoolName'
    ) AS prestoPoolName,
    element_at(
      m,
      'population'
    ) AS population,
    element_at(
      m,
      'master'
    ) AS master,
    element_at(
      m,
      'attributes'
    ) AS attributes,
    element_at(
      m,
      'behaviors'
    ) AS behaviors,
    element_at(
      m,
      'customerGroup'
    ) AS customerGroup,
    element_at(
      m,
      'createdAt'
    ) AS createdAt,
    element_at(
      m,
      'updatedAt'
    ) AS updatedAt,
    element_at(
      m,
      'createdBy'
    ) AS createdBy,
    element_at(
      m,
      'updatedBy'
    ) AS updatedBy
  FROM (
      SELECT 
        CAST(
          json_parse(_col0) AS MAP(
            VARCHAR,
            json
          )
        ) m
      FROM
        ${td.database}.${restore.ms_table_restore}
    )
),
inter AS(
  SELECT 
    CAST(
      '${restore.ms_name}' AS JSON 
    ) AS name,
    description,
    scheduleType,
    scheduleOption,
    timezone,
    matrixUpdatedAt,
    workflowHiveOnly,
    hiveEngineVersion,
    hivePoolName,
    prestoPoolName,
    population,
    master,
    attributes,
    behaviors,
    customerGroup,
    createdAt,
    updatedAt,
    createdBy,
    updatedBy
  FROM
    unnest_config
) SELECT 
  CAST(
    MAP_FROM_ENTRIES(
      ARRAY[(
        'name',
        name
      ),
      (
        'description',
        description
      ),
      (
        'scheduleType',
        scheduleType
      ),
      (
        'scheduleOption',
        scheduleOption
      ),
      (
        'timezone',
        timezone
      ),
      (
        'matrixUpdatedAt',
        matrixUpdatedAt
      ),
      (
        'workflowHiveOnly',
        workflowHiveOnly
      ),
      (
        'hiveEngineVersion',
        hiveEngineVersion
      ),
      (
        'hivePoolName',
        hivePoolName
      ),
      (
        'prestoPoolName',
        prestoPoolName
      ),
      (
        'population',
        population
      ),
      (
        'master',
        master
      ),
      (
        'attributes',
        attributes
      ),
      (
        'behaviors',
        behaviors
      ),
      (
        'customerGroup',
        customerGroup
      ),
      (
        'createdAt',
        createdAt
      ),
      (
        'updatedAt',
        updatedAt
      ),
      (
        'createdBy',
        createdBy
      ),
      (
        'updatedBy',
        updatedBy
      ) ]
    ) AS JSON
  )
FROM
  inter