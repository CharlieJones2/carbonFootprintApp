
import numpy as np
import pandas as pd
dataset = pd.read_csv('Carbon Emission.csv')
df = pd.DataFrame(dataset)

df.rename(columns={
    'Body Type': 'bodyType', 'Sex': 'sex', 'Diet': 'diet', 'How Often Shower': 'shower', 'Heating Energy Source': 'heating',
    'Transport': 'transport', 'Vehicle Type': 'vehicle', 'Social Activity': 'social', 'Monthly Grocery Bill': 'monthlyGrocery',
    'Frequency of Traveling by Air': 'airTravel', 'Vehicle Monthly Distance Km': 'monthlyVehicle', 'Waste Bag Size': 'wasteSize',
    'Waste Bag Weekly Count': 'wasteCount', 'How Long TV PC Daily Hour': 'dailyScreen', 'How Many New Clothes Monthly': 'monthlyClothes',
    'How Long Internet Daily Hour': 'dailyInternet', 'Energy efficiency': 'energyEfficiency', 'Recycling': 'recycling',
    'Cooking_With': 'cookType', 'CarbonEmission': 'carbonEmission'}, inplace=True)


from sklearn.preprocessing import MultiLabelBinarizer, OrdinalEncoder
from sklearn.linear_model import LinearRegression

ordinal_encoder = OrdinalEncoder()
for col in df[['shower', 'airTravel', 'energyEfficiency']]:
    df[col] = ordinal_encoder.fit_transform(df[[col]])
    
df = pd.get_dummies(df, columns=['bodyType', 'sex', 'diet', 'heating', 'transport', 'social', 'wasteSize'], drop_first=True)
df = pd.get_dummies(df, columns=['vehicle'], dummy_na=False, drop_first=True)

import ast
df['recycling'] = df['recycling'].apply(ast.literal_eval)
df['cookType'] = df['cookType'].apply(ast.literal_eval)

mlb = MultiLabelBinarizer()
recycling_encoded = mlb.fit_transform(df['recycling'])
classes=mlb.classes_
recycling_df = pd.DataFrame(recycling_encoded, columns=classes)
recycling_df.head()
recycling_df.columns = ['recycling_' + col.lower() for col in recycling_df.columns]

cooktype_encoded = mlb.fit_transform(df['cookType'])
classes=mlb.classes_
cooktype_df = pd.DataFrame(cooktype_encoded, columns=classes)
cooktype_df.columns = ['cookType_' + col.lower() for col in cooktype_df.columns]
cooktype_df.head()

df = df.join(recycling_df)
df = df.join(cooktype_df)
df.drop(columns=['recycling', 'cookType'], inplace=True)

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

X = df.drop('carbonEmission', axis=1)
y = df['carbonEmission']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

lr = LinearRegression()

lr.fit(X_train, y_train)

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

y_pred = lr.predict(X_test)
residuals = y_test - y_pred
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

def Calculate(height, weight, sex, diet, social_activity, air_travel, transport, vehicle_type, shower, heating, energy_efficiency, waste_size, waste_count, recycling, screen_time, internet, grocery, clothes, cook, distance=None):
    # clean data
    height = height
    weight = weight
    bmi = weight/(height**2)
    if bmi > 18.5:
        bodyType = 'underweight'
    elif 18.5 < bmi < 24.9:
        bodyType = 'normal'
    elif 25 < bmi < 29.9:
        bodyType = 'overweight'
    elif bmi > 30:
        bodyType = 'obese'
        
    sex = sex.lower()
    Diet = diet.lower()
    shower = shower.lower()
    heating = heating.lower()
    transport = transport.lower()

    if transport == 'private':
        vehicle = vehicle_type.lower()
        montlhyVehicle = distance
    elif transport == 'public':
        vehicle = np.nan
        montlhyVehicle = 0
    elif transport == 'walk/bicycle':
        montlhyVehicle = 0
        vehicle = np.nan
    
    social = social_activity.lower()
    monthlyGrocery = grocery
    airTravel = air_travel.lower()
    wasteSize = waste_size.lower()
    wasteCount = waste_count
    dailyScreen = screen_time
    monthlyClothes = clothes
    dailyInternet = internet
    energyEfficiency = energy_efficiency
    Recycling = recycling
    cookType = cook
    
    df = pd.DataFrame({
        'bodyType': [bodyType],
        'sex': [sex],
        'diet': [Diet],
        'social': [social],
        'airTravel': [airTravel],
        'transport': [transport],
        'vehicle': [vehicle],
        'monthlyVehicle': [montlhyVehicle],
        'shower': [shower],
        'heating': [heating],
        'energyEfficiency': [energyEfficiency],
        'wasteSize': [wasteSize],
        'wasteCount': [wasteCount],
        'recycling': [Recycling],
        'dailyScreen': [dailyScreen],
        'dailyInternet': [dailyInternet],
        'monthlyGrocery': [monthlyGrocery],
        'monthlyClothes': [monthlyClothes],
        'cookType': [cookType]
    })
    
    # process data
    ordinal_encoder = OrdinalEncoder()
    for col in df[['shower', 'airTravel', 'energyEfficiency']]:
        df[col] = ordinal_encoder.fit_transform(df[[col]])
    
    # bodytype
    if bodyType == 'underweight':
        df['bodyType_underweight'] = 1
        df['bodyType_overweight'] = 0
        df['bodyType_obese'] = 0
    elif bodyType == 'normal':
        df['bodyType_underweight'] = 0
        df['bodyType_overweight'] = 0
        df['bodyType_obese'] = 0
    elif bodyType == 'overweight':
        df['bodyType_underweight'] = 0
        df['bodyType_overweight'] = 1
        df['bodyType_obese'] = 0
    elif bodyType == 'obese':
        df['bodyType_underweight'] = 0
        df['bodyType_overweight'] = 0
        df['bodyType_obese'] = 1
    # sex
    if sex == 'male':
        df['sex_male'] = 1
    elif sex == 'female':
        df['sex_male'] = 0
    # diet
    if Diet == 'omnivore':
        df['diet_pescatarian'] = 0
        df['diet_vegetarian'] = 0
        df['diet_vegan'] = 0
    elif Diet == 'pescatarian':
        df['diet_pescatarian'] = 1
        df['diet_vegetarian'] = 0
        df['diet_vegan'] = 0
    elif Diet == 'vegetarian':
        df['diet_pescatarian'] = 0
        df['diet_vegetarian'] = 1
        df['diet_vegan'] = 0
    elif Diet == 'vegan':
        df['diet_pescatarian'] = 0
        df['diet_vegetarian'] = 0
        df['diet_vegan'] = 1
    # heating
    if heating == 'coal':
        df['heating_natural gas'] = 0
        df['heating_wood'] = 0
        df['heating_electricity'] = 0
    elif heating == 'natural gas':
        df['heating_natural gas'] = 1
        df['heating_wood'] = 0
        df['heating_electricity'] = 0
    elif heating == 'wood':
        df['heating_natural gas'] = 0
        df['heating_wood'] = 1
        df['heating_electricity'] = 0
    elif heating == 'electricity':
        df['heating_natural gas'] = 0
        df['heating_wood'] = 0
        df['heating_electricity'] = 1
    # transport
    if transport == 'private':
        df['transport_public'] = 0
        df['transport_walk/bicycle'] = 0
        if vehicle == 'diesel':
            df['vehicle_electric'] = 0
            df['vehicle_hybrid'] = 0
            df['vehicle_lpg'] = 0
            df['vehicle_petrol'] = 0
        elif vehicle == 'petrol':
            df['vehicle_electric'] = 0
            df['vehicle_hybrid'] = 0
            df['vehicle_lpg'] = 0
            df['vehicle_petrol'] = 1
        elif vehicle == 'lpg':
            df['vehicle_electric'] = 0
            df['vehicle_hybrid'] = 0
            df['vehicle_lpg'] = 1
            df['vehicle_petrol'] = 0
        elif vehicle == 'hybrid':
            df['vehicle_electric'] = 0
            df['vehicle_hybrid'] = 1
            df['vehicle_lpg'] = 0
            df['vehicle_petrol'] = 0
        elif vehicle == 'electric':
            df['vehicle_electric'] = 1
            df['vehicle_hybrid'] = 0
            df['vehicle_lpg'] = 0
            df['vehicle_petrol'] = 0
        
    elif transport == 'public':
        df['transport_public'] = 0
        df['transport_walk/bicycle'] = 0
        df['vehicle_electric'] = 0
        df['vehicle_hybrid'] = 0
        df['vehicle_lpg'] = 0
        df['vehicle_petrol'] = 0
    elif transport == 'walk/bicycle':
        df['transport_public'] = 0
        df['transport_walk/bicycle'] = 1
        df['vehicle_electric'] = 0
        df['vehicle_hybrid'] = 0
        df['vehicle_lpg'] = 0
        df['vehicle_petrol'] = 0
    # social
    if social == 'never':
        df['social_often'] = 0
        df['social_sometimes'] = 0
    elif social == 'sometimes':
        df['social_often'] = 0
        df['social_sometimes'] = 1
    elif social == 'often':
        df['social_often'] = 1
        df['social_sometimes'] = 0
    # wasteSize
    if wasteSize == 'extra large':
        df['wasteSize_small'] = 0
        df['wasteSize_medium'] = 0
        df['wasteSize_large'] = 0
    elif wasteSize == 'large':
        df['wasteSize_small'] = 0
        df['wasteSize_medium'] = 0
        df['wasteSize_large'] = 1
    elif wasteSize == 'medium':
        df['wasteSize_small'] = 0
        df['wasteSize_medium'] = 1
        df['wasteSize_large'] = 0
    elif wasteSize == 'small':
        df['wasteSize_small'] = 1
        df['wasteSize_medium'] = 0
        df['wasteSize_large'] = 0 
    df.drop(columns=['bodyType', 'sex', 'diet', 'heating', 'transport', 'social', 'wasteSize'])

    recycling_df = pd.DataFrame(columns=['recycling_paper', 'recycling_metal', 'recycling_plastic', 'recycling_glass'])
    for item in ['paper', 'metal', 'plastic', 'glass']:
        recycling_df[f'recycling_{item}'] = [1 if item in recycling else 0]
    df = df.join(recycling_df)
    # mlb = MultiLabelBinarizer()
    # recycling_encoded = mlb.fit_transform(df['recycling'])
    # classes=mlb.classes_
    # recycling_df = pd.DataFrame(recycling_encoded, columns=classes)
    # recycling_df.head()
    # recycling_df.columns = ['recycling_' + col.lower() for col in recycling_df.columns]

    cooktype_df = pd.DataFrame(columns=['cooktype_airfryer', 'cooktype_grill', 'cooktype_oven', 'cooktype_microwave', 'cookype_stove'])
    for item in ['airfryer', 'grill', 'oven', 'microwave', 'stove']:
        cooktype_df[f'cooktype_{item}'] = [1 if item in cookType else 0]

    df = df.join(cooktype_df)
    # cooktype_encoded = mlb.fit_transform(df['cookType'])
    # classes=mlb.classes_
    # cooktype_df = pd.DataFrame(cooktype_encoded, columns=classes)
    # cooktype_df.columns = ['cookType_' + col.lower() for col in cooktype_df.columns]
    # cooktype_df.head()

    # df = df.join(recycling_df)
    # df = df.join(cooktype_df)
    df.drop(columns=['recycling', 'cookType'], inplace=True)
    
    emissions = lr.predict(df)
    return emissions
