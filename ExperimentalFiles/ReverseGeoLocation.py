import pandas as pd
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="geoapiExercises")
dayOfWeek = []
locations = []
df = pd.read_csv("Output\\processedTelematics.csv")
for index in range(len(df)):
    location = geolocator.reverse(df["TripStartLatLong"].iloc[index])
    locations.append(location.raw["address"]['state'])
df["Locations"] = locations
df.to_csv("Output.csv")
