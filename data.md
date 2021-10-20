# SF Fire Data - v1

## Click here to download the [sqlite v1 file](https://gtvault-my.sharepoint.com/:u:/g/personal/manderson334_gatech_edu/EU1zCVuj55BCrWVUERP0QKYB5YjXZW-rMIzyZovmFETwFA?e=JyvxNT)

## Querying

* (Example of using pandas/sqlite)[https://kontext.tech/column/python/414/pandas-read-from-sqlite-database]
* Pandas supports the ability to [read entire tables](https://pandas.pydata.org/pandas-docs/version/0.15.0/generated/pandas.read_sql_table.html#pandas.read_sql_table) or read [sql queries](https://pandas.pydata.org/pandas-docs/version/0.15.0/generated/pandas.read_sql_query.html#pandas.read_sql_query)
* Visual Studio Code and the SQLite Extension (by alexcvzz) provides decent raw querying support for sqlite

## SQLite Schema

The *incident_number* column is indexed one each table to (hopefully) facilitate fasters joins.  Generally, it appears that incident_number is the preferred join key for all the below tables.

### [Fire Incidents](https://data.sfgov.org/Public-Safety/Fire-Incidents/wr8u-xric)

* **Description**: One row per fire incident (call)
* [Data Dictionary](https://data.sfgov.org/api/views/wr8u-xric/files/54c601a2-63f1-4b27-a79d-f484c620f061?download=true&filename=FIR-0001_DataDictionary_fire-incidents.xlsx)
* Table Name: fire_incidents

```
CREATE TABLE IF NOT EXISTS "fire_incidents" (
"index" INTEGER,
  "incident_number" INTEGER,
  "exposure_number" INTEGER,
  "id" INTEGER,
  "address" TEXT,
  "incident_date" TIMESTAMP,
  "call_number" INTEGER,
  "alarm_dttm" TIMESTAMP,
  "arrival_dttm" TIMESTAMP,
  "close_dttm" TIMESTAMP,
  "city" TEXT,
  "zipcode" TEXT,
  "battalion" TEXT,
  "station_area" TEXT,
  "box" TEXT,
  "suppression_units" INTEGER,
  "suppression_personnel" INTEGER,
  "ems_units" INTEGER,
  "ems_personnel" INTEGER,
  "other_units" INTEGER,
  "other_personnel" INTEGER,
  "first_unit_on_scene" TEXT,
  "estimated_property_loss" INTEGER,
  "estimated_contents_loss" INTEGER,
  "fire_fatalities" INTEGER,
  "fire_injuries" INTEGER,
  "civilian_fatalities" INTEGER,
  "civilian_injuries" INTEGER,
  "number_of_alarms" INTEGER,
  "primary_situation" TEXT,
  "mutual_aid" TEXT,
  "action_taken_primary" TEXT,
  "action_taken_secondary" TEXT,
  "action_taken_other" TEXT,
  "detector_alerted_occupants" TEXT,
  "property_use" TEXT,
  "area_of_fire_origin" TEXT,
  "ignition_cause" TEXT,
  "ignition_factor_primary" TEXT,
  "ignition_factor_secondary" TEXT,
  "heat_source" TEXT,
  "item_first_ignited" TEXT,
  "human_factors_associated_with_ignition" TEXT,
  "structure_type" TEXT,
  "structure_status" TEXT,
  "floor_of_fire_origin" INTEGER,
  "fire_spread" TEXT,
  "no_flame_spead" TEXT,
  "number_of_floors_with_minimum_damage" INTEGER,
  "number_of_floors_with_significant_damage" INTEGER,
  "number_of_floors_with_heavy_damage" INTEGER,
  "number_of_floors_with_extreme_damage" INTEGER,
  "detectors_present" TEXT,
  "detector_type" TEXT,
  "detector_operation" TEXT,
  "detector_effectiveness" TEXT,
  "detector_failure_reason" TEXT,
  "automatic_extinguishing_system_present" TEXT,
  "automatic_extinguishing_sytem_type" TEXT,
  "automatic_extinguishing_sytem_perfomance" TEXT,
  "automatic_extinguishing_sytem_failure_reason" TEXT,
  "number_of_sprinkler_heads_operating" INTEGER,
  "supervisor_district" INTEGER,
  "neighborhood_district" TEXT,
  "point" TEXT
);
```

### [Fire Department Calls for Service](https://data.sfgov.org/Public-Safety/Fire-Department-Calls-for-Service/nuek-vuh3)

* **Description:** Unit-level response data for each incident
* **Relationships:** Join to Fire Incidents by incident number (?? check this)
* [Data Dictionary](https://data.sfgov.org/api/views/nuek-vuh3/files/ddb7f3a9-0160-4f07-bb1e-2af744909294?download=true&filename=FIR-0002_DataDictionary_fire-calls-for-service.xlsx)
* Table Name: calls_for_service

```
CREATE TABLE IF NOT EXISTS "calls_for_service" (
"index" INTEGER,
  "call_number" INTEGER,
  "unit_id" TEXT,
  "incident_number" INTEGER,
  "call_type" TEXT,
  "call_date" TEXT,
  "watch_date" TIMESTAMP,
  "received_dttm" TIMESTAMP,
  "entry_dttm" TIMESTAMP,
  "dispatch_dttm" TIMESTAMP,
  "response_dttm" TEXT,
  "on_scene_dttm" TIMESTAMP,
  "transport_dttm" TIMESTAMP,
  "hospital_dttm" TIMESTAMP,
  "call_final_disposition" TEXT,
  "available_dttm" TIMESTAMP,
  "address" TEXT,
  "city" TEXT,
  "zipcode_of_incident" TEXT,
  "battalion" TEXT,
  "station_area" TEXT,
  "box" TEXT,
  "original_priority" TEXT,
  "priority" TEXT,
  "final_priority" INTEGER,
  "als_unit" INTEGER,
  "call_type_group" TEXT,
  "number_of_alarms" INTEGER,
  "unit_type" TEXT,
  "unit_sequence_in_call_dispatch" INTEGER,
  "fire_prevention_district" TEXT,
  "supervisor_district" TEXT,
  "neighborhooods_-_analysis_boundaries" TEXT,
  "rowid" TEXT,
  "case_location" TEXT,
  "analysis_neighborhoods" INTEGER
);
```

### Primary Situation Mapping

* **Description** maps the *primary_situation* column of the *fire_incidents* table to broader categories

```
CREATE TABLE IF NOT EXISTS "category_mappings" (
  "index" INTEGER,
  "primary_situation" TEXT,
  "situation_category" TEXT
);
```

### Incident Nearest Fire Station

* **Description** provides distance (euclidean, L2) between incident and the nearest fire station

```
CREATE TABLE IF NOT EXISTS "nearest_distances" (
  "index" INTEGER,
  "unnamed:_0" INTEGER,
  "incident_number" INTEGER,
  "id" INTEGER,
  "lon" REAL,
  "lat" REAL,
  "nearest_station" REAL
);
```





