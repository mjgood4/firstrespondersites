-- SQLite
SELECT 
fi.zipcode, fi.supervisor_district
, Response_DtTm
, On_Scene_DtTm
, fi.box
, fi.ems_units
, fi.station_area
, cfs.case_location 
FROM fire_incidents AS fi 
INNER JOIN calls_for_service AS cfs ON fi.incident_number = cfs.incident_number 
INNER JOIN nearest_distances AS nd ON fi.incident_number = nd.incident_number
limit 1000


select floating_catchment_output.[index]
, floating_catchment_output.zone_idx
, floating_catchment_output.accessibility_score
, floating_catchment_output.scenario_name
, calls_for_service.on_scene_dttm
, calls_for_service.response_dttm 
, calls_for_service.supervisor_district
from floating_catchment_output
inner join zone_idx_to_incident on 
zone_idx_to_incident.zone_idx = floating_catchment_output.zone_idx
inner join calls_for_service on calls_for_service.incident_number = zone_idx_to_incident.incident_number
where calls_for_service.unit_type in ('TRUCK', 'ENGINE')
and scenario_name = 'baseline'
limit 1000

select fire_stations.common_name
, Unit
, count(*)
, avg(floating_catchment_output.accessibility_score)
from floating_catchment_output
inner join zone_idx_to_incident on 
zone_idx_to_incident.zone_idx = floating_catchment_output.zone_idx
inner join calls_for_service on calls_for_service.incident_number = zone_idx_to_incident.incident_number
left join Truck_Engine_Fire_Station on calls_for_service.unit_id = Truck_Engine_Fire_Station.Unit
left join fire_stations on fire_stations.facility_id = Truck_Engine_Fire_Station.Facility_ID
where calls_for_service.unit_type in ('TRUCK', 'ENGINE')
and scenario_name = 'baseline'
GROUP BY fire_stations.common_name, Unit
order by Unit

--2736508
--128456
--137544

select count(*) from calls_for_service
inner join zone_idx_to_incident on calls_for_service.incident_number = zone_idx_to_incident.incident_number
where calls_for_service.unit_type in ('TRUCK', 'ENGINE')

select datetime("01-05-2019 04:10:58 PM") 

select * 
from floating_catchment_output
where scenario_name = 'baseline'

select *
from Truck_Engine_Fire_Station
