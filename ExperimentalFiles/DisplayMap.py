from geopy.distance import geodesic
import datetime as dt
import pandas as pd
import folium


def tz_from_utc_ms_ts(utc_ms_ts):
    # convert from time stamp to datetime
    utc_datetime = dt.datetime.utcfromtimestamp(utc_ms_ts / 1000.)

    # set the timezone to UTC, and then convert to desired timezone
    return utc_datetime


def read_transform():
    df = pd.read_csv("Output\\telematics.csv")
    df = df[df["Creation_Time"] != ""]
    df["Creation_Time"] = df["Time Message Container Created"].apply(lambda x: tz_from_utc_ms_ts(x))
    df["Receipt_Time"] = df["Time Received"].apply(lambda x: tz_from_utc_ms_ts(x))
    distances = [-1]
    interval = [-1]
    for index in range(len(df)):
        if index < len(df) - 1:
            origin = (df["Latitude"].iloc[index], df["Longitude"].iloc[index])
            destin = (df["Latitude"].iloc[index + 1], df["Longitude"].iloc[index + 1])
            time_interval = df["Time Message Container Created"].iloc[index + 1] - \
                            df["Time Message Container Created"].iloc[index]
            interval.append(time_interval / 1000)
            distances.append(geodesic(origin, destin).meters)
    df["Distance"] = distances
    df["Interval"] = interval
    df.to_csv("Output\\interim.csv")


df_ = pd.read_csv("Output\\Heatmap.csv")
df_ = df_[df_["OBU ID"] == 14]


pizza_map = folium.Map(location=(df_.Latitude.mean(), df_.Longitude.mean()), zoom_start=14, control_scale=True)
for index_, row in df_.iterrows():
    folium.Marker(location=(row['Latitude'],
                            row['Longitude']),
                  popup=row['OBU ID']).add_to(pizza_map)

pizza_map.save("map.html")
