from numpy import e
import pandas as pd
import os
import json
import re

def create_distance_file(rootdir):
    zone_from = []
    zone_to = []
    list_travel_distance = []
    list_travel_time_notraffic = []
    list_travel_time_traffic = []
    errors = []
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            dist_regexp = re.compile("^(\d+)_to_(\d+)\.json$")
            dist_parts = dist_regexp.match(file)
            zone_1 = dist_parts[1]
            zone_2 = dist_parts[2]
            with open(rootdir + "/" + file) as fh:
                json_data = [x if type(x) == str else x.decode('utf-8') for x in fh.readlines()]
                json_data = "".join(json_data)

                if json_data == "":
                    errors.append(file)                    
                    next

                try:
                    data = json.loads(json_data)
                except:
                    errors.append(file)                    
                    next
               
                driving_data = data['resourceSets'][0]['resources'][0]
                travel_distance = driving_data['travelDistance']
                travel_time_notraffic = driving_data['travelDuration']
                travel_time_traffic = driving_data['travelDurationTraffic']

                zone_from.append(zone_1)
                zone_to.append(zone_2)
                list_travel_distance.append(float(travel_distance))
                list_travel_time_notraffic.append(int(travel_time_notraffic))
                list_travel_time_traffic.append(int(travel_time_traffic))

                zone_from.append(zone_2)
                zone_to.append(zone_1)
                list_travel_distance.append(float(travel_distance))
                list_travel_time_notraffic.append(int(travel_time_notraffic))
                list_travel_time_traffic.append(int(travel_time_traffic))

    travel_distance_df = pd.DataFrame({
        "zone_from" : pd.Series(zone_from),
        "zone_to": pd.Series(zone_to),
        "travel_distance_km" : pd.Series(list_travel_distance),
        "travel_time_notraffic_seconds" : pd.Series(list_travel_time_notraffic),
        "travel_time_traffic_seconds" : pd.Series(list_travel_time_traffic)
    })

    travel_distance_df.to_csv("data/raw/zone_distances.csv")
    
    for e in errors:
        print(f"Removing file with error {e}")
        os.remove(rootdir+"/"+e)
    

if __name__ == "__main__":
    create_distance_file("data/distance_output")