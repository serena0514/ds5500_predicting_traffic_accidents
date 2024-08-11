from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import numpy as np
import pandas as pd


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


def predict_for_city(df, road_surface_condition, Day_Start_Time, Month_Start_Time,
                     Hour_Start_Time, Minute_Start_Time, Second_Start_Time, city_ranges=None, city='Boston'):

    # Filter for city
    filtered_df = df[df['City'] == city].copy()
    if filtered_df.empty:
        raise ValueError(f"No data found for city: {city}")

    print(f"Filtered DataFrame for {city}:")
    print(filtered_df.head())

    # Define features and target columns based on available columns
    numeric_features = ['Start_Lat', 'Start_Lng']
    categorical_features = ['City', 'Road_Surface_Condition']

    target_columns = ['Amenity','Crossing', 'Station','Traffic_Signal','Railway','Give_Way','Junction','Stop']

    print("Numeric features:", numeric_features)
    print("Categorical features:", categorical_features)
    print("Target columns:", target_columns)

    # Prepare the data
    X = filtered_df[numeric_features + categorical_features]
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])

    # Train models for each target column
    models = {}
    for target in target_columns:
        y = filtered_df[target]
        clf = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
        clf.fit(X, y)
        models[target] = clf

    #Use Boston coordinate as example
    lat_min = 42.2279
    lat_max = 42.3975
    lng_min = -71.1912
    lng_max = -70.9228



    # Define the grid of latitudes and longitudes for the city
    latitudes = np.round(np.arange(lat_min, lat_max, 0.001), 3)
    longitudes = np.round(np.arange(lng_min, lng_max, 0.001), 3)

    # Function to predict for a single location
    def predict_location(lat, lng):
        sample = pd.DataFrame({
            'Start_Lat': [lat],
            'Start_Lng': [lng],
            'City': [city],
        })
        if 'Road_Surface_Condition' in categorical_features:
            sample['Road_Surface_Condition'] = [road_surface_condition]

        predictions = {}
        for target, model in models.items():
            predictions[target] = bool(model.predict(sample)[0])

        predictions.update({
            'Start_Lat': lat,
            'Start_Lng': lng,
            'Day_Start_Time': Day_Start_Time,
            'Month_Start_Time': Month_Start_Time,
            'Hour_Start_Time': Hour_Start_Time,
            'Minute_Start_Time': Minute_Start_Time,
            'Second_Start_Time': Second_Start_Time,
            'Road_Surface_Condition': road_surface_condition
        })

        return predictions

    # Generate predictions for all unique locations
    results = []
    for lat in latitudes:
        for lng in longitudes:
            result = predict_location(lat, lng)
            results.append(result)

    # Create the final DataFrame
    final_df = pd.DataFrame(results)

    # Convert True/False to 1/0
    for col in target_columns:
        final_df[col] = final_df[col].astype(int)

    # Reorder columns
    column_order = ['Start_Lat', 'Start_Lng', 'Day_Start_Time', 'Month_Start_Time',
                    'Hour_Start_Time', 'Minute_Start_Time', 'Second_Start_Time', 'Road_Surface_Condition'] + target_columns

    final_df = final_df[column_order]

    return final_df