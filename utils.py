from dash import html

def make_break(num_breaks):
    br_list = [html.Br()] * num_breaks
    return br_list

city_ranges = {
    'Boston': (42.2279, 42.3975, -71.1912, -70.9228),
    'Cambridge': (42.3584, 42.4045, -71.1667, -71.0639),
    'Worcester': (42.2370, 42.3136, -71.8745, -71.7533),
    'Springfield': (42.0759, 42.1276, -72.6181, -72.4862),
    'Lowell': (42.6054, 42.6664, -71.3796, -71.2713),
    'Brockton': (42.0336, 42.1095, -71.0720, -70.9644),
    'Quincy': (42.2179, 42.2851, -71.0520, -70.9515),
    'Lynn': (42.4396, 42.4993, -70.9920, -70.9109),
    'New Bedford': (41.6149, 41.6859, -70.9607, -70.8830),
    'Fall River': (41.6690, 41.7359, -71.1867, -71.1225),
    'Newton': (42.283, 42.367, -71.258, -71.172),
    'Somerville': (42.373, 42.408, -71.125, -71.075),
    'Framingham': (42.270, 42.340, -71.460, -71.380),
    'Waltham': (42.348, 42.420, -71.272, -71.200),
    'Haverhill': (42.736, 42.815, -71.145, -70.970),
    'Malden': (42.408, 42.450, -71.090, -71.020),
    'Medford': (42.400, 42.460, -71.150, -71.050),
    'Taunton': (41.870, 41.950, -71.150, -71.030),
    'Chicopee': (42.140, 42.210, -72.660, -72.520),
    'Weymouth': (42.160, 42.240, -70.950, -70.850),
    'Revere': (42.380, 42.440, -71.020, -70.940),
    'Peabody': (42.510, 42.570, -70.970, -70.870),
    'Methuen': (42.700, 42.750, -71.230, -71.130),
    'Barnstable': (41.630, 41.710, -70.360, -70.220),
    'Pittsfield': (42.430, 42.470, -73.300, -73.210),
    'Attleboro': (41.930, 41.990, -71.330, -71.250),
    'Arlington': (42.400, 42.440, -71.190, -71.120),
    'Everett': (42.390, 42.430, -71.080, -71.020),
    'Salem': (42.510, 42.530, -70.920, -70.860),
    'Beverly': (42.540, 42.590, -70.930, -70.840),
    'Chelsea': (42.380, 42.400, -71.040, -71.020)
}

def assign_city(lat, lon):
    for city, (lat_min, lat_max, lon_min, lon_max) in city_ranges.items():
        if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
            return city
    return 'Other'


# def assign_city_df(df):
#     df['City'] = df.apply(lambda row: assign_city(row['Start_Lat'], row['Start_Lng']), axis=1)
#     return df
