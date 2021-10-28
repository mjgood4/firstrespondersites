import pandas as pd
import sqlite3

def import_fire_incidents(db_fh):
    print("\tImporting fire_incidents...")
    
    fire_incidents = pd.read_csv("raw/fire_incidents.csv")
    
    # idiomatically rename the columns (lowercase / remove spaces)
    colnames = list(fire_incidents.columns)
    clean_colnames = list(map(lambda s: s.lower().replace(" ", "_"), colnames))
    fire_incidents.columns = clean_colnames

    pd.set_option("max_rows", 100)
    print("\t fire_incidents - before")
    print(fire_incidents.dtypes)
    
    # clean up the columns
    fire_incidents['incident_number'] = fire_incidents['incident_number'].str.replace("\D", "").astype('float64').astype('Int64')    
    fire_incidents['exposure_number'] = fire_incidents['exposure_number'].astype('float64').astype('Int64')
    fire_incidents['id'] = fire_incidents['id'].astype('float64').astype('Int64')
    fire_incidents['address'] = fire_incidents['address'].astype('object')    
    fire_incidents['incident_date'] = pd.to_datetime(fire_incidents['incident_date'])
    fire_incidents['call_number'] = fire_incidents['call_number'].astype('float64').astype('Int64')        
    fire_incidents['alarm_dttm'] = pd.to_datetime(fire_incidents['alarm_dttm'])
    fire_incidents['arrival_dttm'] = pd.to_datetime(fire_incidents['arrival_dttm'])    
    fire_incidents['close_dttm'] = pd.to_datetime(fire_incidents['close_dttm'])            
    fire_incidents['city'] = fire_incidents['city'].astype('object')
    fire_incidents['zipcode'] = fire_incidents['zipcode'].astype('object')
    fire_incidents['battalion'] = fire_incidents['battalion'].astype('object')
    fire_incidents['station_area'] = fire_incidents['station_area'].astype('object')    
    fire_incidents['box'] = fire_incidents['box'].astype('object')    
    fire_incidents['suppression_units'] = fire_incidents['suppression_units'].str.replace("\D", "").astype('float64').astype('Int64')
    fire_incidents['suppression_personnel'] = fire_incidents['suppression_personnel'].str.replace("\D", "").astype('float64').astype('Int64')
    fire_incidents['ems_units'] = fire_incidents['ems_units'].astype('float64').astype('Int64')
    fire_incidents['ems_personnel'] = fire_incidents['ems_personnel'].astype('float64').astype('Int64')
    fire_incidents['other_units'] = fire_incidents['other_units'].str.replace("\D", "").astype('float64').astype('Int64')
    fire_incidents['other_personnel'] = fire_incidents['other_personnel'].str.replace("\D", "").astype('float64').astype('Int64')
    fire_incidents['first_unit_on_scene'] = fire_incidents['first_unit_on_scene'].astype('object')
    fire_incidents['estimated_property_loss'] = fire_incidents['estimated_property_loss'].str.replace("\D", "").astype('float64').astype('Int64')
    fire_incidents['estimated_contents_loss'] = fire_incidents['estimated_contents_loss'].str.replace("\D", "").astype('float64').astype('Int64')
    fire_incidents['fire_fatalities'] = fire_incidents['fire_fatalities'].astype('float64').astype('Int64')
    fire_incidents['fire_injuries'] = fire_incidents['fire_injuries'].astype('float64').astype('Int64')
    fire_incidents['civilian_fatalities'] = fire_incidents['civilian_fatalities'].astype('float64').astype('Int64')
    fire_incidents['civilian_injuries'] = fire_incidents['civilian_injuries'].astype('float64').astype('Int64')
    fire_incidents['number_of_alarms'] = fire_incidents['number_of_alarms'].astype('float64').astype('Int64')
    fire_incidents['primary_situation'] = fire_incidents['primary_situation'].astype('object')
    fire_incidents['mutual_aid'] = fire_incidents['mutual_aid'].astype('object')
    fire_incidents['action_taken_primary'] = fire_incidents['action_taken_primary'].astype('object')
    fire_incidents['action_taken_secondary'] = fire_incidents['action_taken_secondary'].astype('object')
    fire_incidents['action_taken_other'] = fire_incidents['action_taken_other'].astype('object')
    fire_incidents['detector_alerted_occupants'] = fire_incidents['detector_alerted_occupants'].astype('object')
    fire_incidents['property_use'] = fire_incidents['property_use'].astype('object')
    fire_incidents['area_of_fire_origin'] = fire_incidents['area_of_fire_origin'].astype('object')
    fire_incidents['ignition_cause'] = fire_incidents['ignition_cause'].astype('object')
    fire_incidents['ignition_factor_primary'] = fire_incidents['ignition_factor_primary'].astype('object')
    fire_incidents['ignition_factor_secondary'] = fire_incidents['ignition_factor_secondary'].astype('object')
    fire_incidents['heat_source'] = fire_incidents['heat_source'].astype('object')
    fire_incidents['item_first_ignited'] = fire_incidents['item_first_ignited'].astype('object')
    fire_incidents['human_factors_associated_with_ignition'] = fire_incidents['human_factors_associated_with_ignition'].astype('object')
    fire_incidents['structure_type'] = fire_incidents['structure_type'].astype('object')
    fire_incidents['structure_status'] = fire_incidents['structure_status'].astype('object')
    fire_incidents['floor_of_fire_origin'] = fire_incidents['floor_of_fire_origin'].astype('float64').astype('Int64')
    fire_incidents['fire_spread'] = fire_incidents['fire_spread'].astype('object')
    fire_incidents['no_flame_spead'] = fire_incidents['no_flame_spead'].astype('object')
    fire_incidents['number_of_floors_with_minimum_damage'] = fire_incidents['number_of_floors_with_minimum_damage'].astype('float64').astype('Int64')
    fire_incidents['number_of_floors_with_significant_damage'] = fire_incidents['number_of_floors_with_significant_damage'].astype('float64').astype('Int64')
    fire_incidents['number_of_floors_with_heavy_damage'] = fire_incidents['number_of_floors_with_heavy_damage'].astype('float64').astype('Int64')
    fire_incidents['number_of_floors_with_extreme_damage'] = fire_incidents['number_of_floors_with_extreme_damage'].astype('float64').astype('Int64')
    fire_incidents['detectors_present'] = fire_incidents['detectors_present'].astype('object')
    fire_incidents['detector_type'] = fire_incidents['detector_type'].astype('object')
    fire_incidents['detector_operation'] = fire_incidents['detector_operation'].astype('object')
    fire_incidents['detector_effectiveness'] = fire_incidents['detector_effectiveness'].astype('object')
    fire_incidents['detector_failure_reason'] = fire_incidents['detector_failure_reason'].astype('object')
    fire_incidents['automatic_extinguishing_system_present'] = fire_incidents['automatic_extinguishing_system_present'].astype('object')
    fire_incidents['automatic_extinguishing_sytem_type'] = fire_incidents['automatic_extinguishing_sytem_type'].astype('object')
    fire_incidents['automatic_extinguishing_sytem_perfomance'] = fire_incidents['automatic_extinguishing_sytem_perfomance'].astype('object')
    fire_incidents['automatic_extinguishing_sytem_failure_reason'] = fire_incidents['automatic_extinguishing_sytem_failure_reason'].astype('object')
    fire_incidents['number_of_sprinkler_heads_operating'] = fire_incidents['number_of_sprinkler_heads_operating'].astype('float64').astype('Int64')
    fire_incidents['supervisor_district'] = fire_incidents['supervisor_district'].astype('float64').astype('Int64')
    fire_incidents['neighborhood_district'] = fire_incidents['neighborhood_district'].astype('object')
    fire_incidents['point'] = fire_incidents['point'].astype('object')

    print("\t fire_incidents - after")
    print(fire_incidents.dtypes)

    fire_incidents.to_sql('fire_incidents', conn, if_exists='replace')
    print("\tdone creating fire_incidents")

def import_calls_for_service(db_fh):    

    print("\tImporting calls_for_service...")

    calls_for_service = pd.read_csv("raw/Fire_Department_Calls_for_Service.csv")
    
    # idiomatically rename the columns (lowercase / remove spaces)
    colnames = list(calls_for_service.columns)
    clean_colnames = list(map(lambda s: s.lower().replace(" ", "_"), colnames))
    calls_for_service.columns = clean_colnames

    calls_for_service['call_number'] = calls_for_service['call_number'].astype('int64')
    calls_for_service['unit_id'] = calls_for_service['unit_id'].astype('object')
    calls_for_service['incident_number'] = calls_for_service['incident_number'].astype('int64')
    calls_for_service['call_type'] = calls_for_service['call_type'].astype('object')
    calls_for_service['watch_date'] = pd.to_datetime(calls_for_service['watch_date'])
    calls_for_service['received_dttm'] = pd.to_datetime(calls_for_service['received_dttm'], format="%m/%d/%Y %I:%M:%S %p")
    calls_for_service['entry_dttm'] = pd.to_datetime(calls_for_service['entry_dttm'], format="%m/%d/%Y %I:%M:%S %p")
    calls_for_service['dispatch_dttm'] = pd.to_datetime(calls_for_service['dispatch_dttm'], format="%m/%d/%Y %I:%M:%S %p")
    calls_for_service['hospital_dttm'] = pd.to_datetime(calls_for_service['hospital_dttm'], format="%m/%d/%Y %I:%M:%S %p")
    calls_for_service['on_scene_dttm'] = pd.to_datetime(calls_for_service['on_scene_dttm'], format="%m/%d/%Y %I:%M:%S %p")
    calls_for_service['transport_dttm'] = pd.to_datetime(calls_for_service['transport_dttm'], format="%m/%d/%Y %I:%M:%S %p")
    calls_for_service['hospital_dttm'] = pd.to_datetime(calls_for_service['hospital_dttm'], format="%m/%d/%Y %I:%M:%S %p")  
    calls_for_service['call_final_disposition'] = calls_for_service['call_final_disposition'].astype('object')    
    calls_for_service['available_dttm'] = pd.to_datetime(calls_for_service['available_dttm'], format="%m/%d/%Y %I:%M:%S %p")        
    calls_for_service['address'] = calls_for_service['address'].astype('object')
    calls_for_service['city'] = calls_for_service['city'].astype('object')
    calls_for_service['zipcode_of_incident'] = calls_for_service['zipcode_of_incident'].astype(str).str.zfill(5)    
    calls_for_service['battalion'] = calls_for_service['battalion'].astype('object')
    calls_for_service['station_area'] = calls_for_service['station_area'].astype('object')
    calls_for_service['box'] = calls_for_service['box'].astype('object')
    calls_for_service['original_priority'] = calls_for_service['original_priority'].astype('object')
    calls_for_service['priority'] = calls_for_service['priority'].astype('object')
    calls_for_service['final_priority'] = calls_for_service['final_priority'].astype('int64')
    calls_for_service['als_unit'] = calls_for_service['als_unit'].astype('bool')
    calls_for_service['call_type_group'] = calls_for_service['call_type_group'].astype('object')
    calls_for_service['number_of_alarms'] = calls_for_service['number_of_alarms'].astype('int64')
    calls_for_service['unit_type'] = calls_for_service['unit_type'].astype('object')
    calls_for_service['unit_sequence_in_call_dispatch'] = calls_for_service['unit_sequence_in_call_dispatch'].astype('float64').astype('Int64')    
    calls_for_service['fire_prevention_district'] = calls_for_service['fire_prevention_district'].astype('object')
    calls_for_service['supervisor_district'] = calls_for_service['supervisor_district'].astype('object')
    calls_for_service['neighborhooods_-_analysis_boundaries'] = calls_for_service['neighborhooods_-_analysis_boundaries'].astype('object')
    calls_for_service['rowid'] = calls_for_service['rowid'].astype('object')
    calls_for_service['case_location'] = calls_for_service['case_location'].astype('object')
    calls_for_service['analysis_neighborhoods'] = calls_for_service['analysis_neighborhoods'].astype('float64').astype('Int64')

    pd.set_option("max_rows", 100)
    print("\t calls_for_service - after")
    print(calls_for_service.dtypes)

    calls_for_service.to_sql('calls_for_service', conn, if_exists='replace')
    print("\tdone creating calls_for_service")

def import_category_mapping(db_fh):    
    print("\tImporting category_mappings...")
    category_mappings = pd.read_csv("raw/category_mappings.csv")
    category_mappings.to_sql('category_mappings', conn, if_exists='replace')
    print("\tdone creating category_mappings")

def import_nearest_distances(db_fh):
    
    print("\tImporting nearest_distances...")
    nearest_distances = pd.read_csv("raw/incident_nearest_distances.csv")

    # idiomatically rename the columns (lowercase / remove spaces)
    colnames = list(nearest_distances.columns)
    clean_colnames = list(map(lambda s: s.lower().replace(" ", "_"), colnames))
    nearest_distances.columns = clean_colnames

    nearest_distances['incident_number'] = nearest_distances['incident_number'].str.replace("\D", "").astype('float64').astype('Int64')    
    nearest_distances['id'] = nearest_distances['id'].astype('int64')
    nearest_distances['lat'] = nearest_distances['lat'].astype('float64')    
    nearest_distances['lon'] = nearest_distances['lon'].astype('float64')    
    nearest_distances['nearest_station'] = nearest_distances['nearest_station'].astype('float64')    

    nearest_distances.to_sql('nearest_distances', conn, if_exists='replace')
    
    print("\tdone creating nearest_distances")

def import_fire_stations(db_fh):
    print("\tImporting fire stations...")
    cf = pd.read_csv("raw/city_facilities.csv")
    cf = cf.loc[cf.common_name.str.lower().str.match("^fire station.*")]
    cf.to_sql('fire_stations', conn, if_exists='replace')    

    print("\tdone creating category_mappings")

if __name__ == "__main__":    
    db_name = input("input database name for output:")
    print("Creating SQLite Database...")
    conn = sqlite3.connect(f'{db_name}.db')
    import_fire_incidents(conn)
    import_calls_for_service(conn)
    import_category_mapping(conn)
    import_nearest_distances(conn)
    import_fire_stations(conn)
