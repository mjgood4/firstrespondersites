from pybingmaps.bingmaps import Bing
import os, sys
import pandas as pd
import time

if __name__ == "__main__":
    print("Starting distance calc")
    with open(".bingapikey", "r") as f:
        apikey = f.readline()
    print(f"\t API KEY: {apikey}")

    b = Bing(apikey)
    grid_data = pd.read_csv('raw/zone_grid.csv')

    coords = grid_data.centroid.str.replace("[^-.0-9 ]", "", regex=True).str.strip().str.split("\s+")
    n_coords = len(coords)

    output_dir = "distance_output/"
    for i_idx in range(0, n_coords):
        print(f"\t{i_idx} of {n_coords}...")
        i_pt = coords[i_idx]
        i_lat = float(i_pt[1])
        i_lon = float(i_pt[0])        
        for j_idx in range(i_idx+1, n_coords):
            j_pt = coords[j_idx]
            j_lat = float(j_pt[1])
            j_lon = float(j_pt[0])
            fname = f"{i_idx}_to_{j_idx}.json"
            full_fname = output_dir+fname
            
            if not os.path.exists(full_fname):
                with open(full_fname, "w") as outfile:
                    error_cnt = 0
                    while error_cnt < 3:                                        
                        try:
                            travel_time_output = b.travelData((i_lat, i_lon), (j_lat, j_lon), startTime="2021-11-01T8:00:00-07:00")
                            time.sleep(2.1)
                            break
                        except:
                            print("\tRequest error")
                            error_cnt += 1
                            time.sleep(3)
                    if error_cnt >= 3:
                        print(f"\terror reading: {fname}")
                        os.remove(full_fname)
                        sys.exit(0)
                    else:
                        outfile.write(travel_time_output.decode("utf-8"))
                

    print("done")



