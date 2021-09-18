import pandas as pd
import numpy as np

def read_facilities():
    fac_df = pd.read_csv("/data/city_facilities.csv")
    # filter for fire department owned buildings
    fac_df = fac_df[fac_df["jurisdiction"] == "Fire Department"]
    # filter for "fire station"
    fire_stations = fac_df['common_name'].str.lower().str.startswith("fire station")
    return fac_df[fire_stations]

def read_incidents():
    inc_df = pd.read_csv("/data/fire_incidents.csv")
    # take string "POINT (<lon> <lat>)" and convert to two floating point cols
    # extract lat/lon values via regex
    inc_df["clean_point"] = inc_df.point.\
        str.replace("^\\s*POINT\\s*\\(([-.0-9]+)\\s*([-.0-9]+)\\)", "\\1 \\2", case=False, regex=True)
    # split into floating point cols & relabel
    lon_lat = inc_df["clean_point"].str.split(" ", expand=True).astype(float, copy=False)
    lon_lat.columns = ['lon', 'lat']
    # return Incident Number, ID, lon, lat in DF
    inc_coords_df = pd.concat([inc_df[['Incident Number', 'ID']], lon_lat], axis=1)
    return inc_coords_df

def compute_incident_distances(fac_df, inc_coords_df):
    
    fac_dist = fac_df[['latitude', 'longitude']].to_numpy(dtype=float)
    counter_i = 0

    def compute_row_dist(df_row):
        # print progress
        nonlocal counter_i
        counter_i = counter_i + 1
        if counter_i % 10000 == 0: print(f"\t{counter_i}/{inc_coords_df.shape[0]}")        
        # calculate euclidean distance
        row_dist = np.sqrt(np.sum(np.power((fac_dist - df_row.to_numpy()), 2), axis=1))
        return pd.Series(row_dist)

    incident_dist = inc_coords_df[['lat', 'lon']].apply(compute_row_dist, axis=1)
    incident_dist.columns = fac_df.common_name.tolist()
    
    return pd.concat([inc_coords_df, incident_dist], axis=1)

def compute_nearest_distance(fac_df, inc_coords_df):
    
    fac_dist = fac_df[['latitude', 'longitude']].to_numpy(dtype=float)
    counter_i = 0

    def compute_row_dist(df_row):
        # print progress
        nonlocal counter_i
        counter_i = counter_i + 1
        if counter_i % 10000 == 0: print(f"\t{counter_i}/{inc_coords_df.shape[0]}")        
        # calculate euclidean distance
        row_dist = np.min(np.sqrt(np.sum(np.power((fac_dist - df_row), 2), axis=1)))
        return row_dist

    incident_dist = inc_coords_df[['lat', 'lon']].apply(compute_row_dist, axis=1, raw=True, result_type="reduce")
    incident_dist.name = "nearest_station"    
    
    return pd.concat([inc_coords_df, incident_dist.to_frame()], axis=1)


if __name__ == "__main__":
    print("reading facilities")
    fac_df = read_facilities()
    print("reading incidents")
    inc_coords_df = read_incidents()
    #print("computing incident distances")
    #dist_df = compute_incident_distances(fac_df, inc_coords_df)
    #print("writing csv...")
    #dist_df.to_csv("/data/incident_distances.csv")
    print("computing nearest distances")
    dist_df = compute_nearest_distance(fac_df, inc_coords_df)
    print("writing csv...")
    dist_df.to_csv("/data/incident_nearest_distances.csv")
    print("done")