# SF Fire Data

## SQLite Schema

### [Fire Incidents](https://data.sfgov.org/Public-Safety/Fire-Incidents/wr8u-xric)

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
CREATE INDEX "ix_fire_incident_number_index"ON "fire_incidents" ("incident_number");
```
