CREATE INDEX "ix_fire_incident_incident_number_index" ON "fire_incidents" ("incident_number");
CREATE INDEX "ix_fire_incident_primary_situation_index" ON "fire_incidents" ("primary_situation");
CREATE INDEX "ix_calls_for_service_incident_number_index" ON "calls_for_service" ("incident_number");
CREATE INDEX "ix_nearest_distances_incident_number_index" ON "nearest_distances" ("incident_number");