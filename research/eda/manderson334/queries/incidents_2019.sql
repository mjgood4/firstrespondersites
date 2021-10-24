-- SQLite
SELECT 
    call_number, incident_number, call_type, call_type_group, 
    unit_id, unit_type, 
    call_date, received_dttm, dispatch_dttm, on_scene_dttm,
    `neighborhooods_-_analysis_boundaries`, case_location
FROM calls_for_service 
WHERE cast(strftime('%Y', received_dttm) as int) = 2019