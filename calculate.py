
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
    diet = diet.lower()
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
        'diet': [diet],
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
        
    df = pd.get_dummies(df, columns=['bodyType', 'sex', 'diet', 'heating', 'transport', 'social', 'wasteSize'], drop_first=True)
    df = pd.get_dummies(df, columns=['vehicle'], dummy_na=False, drop_first=True)

    print(df['recycling'])
    print(df['recycling']).dtypes

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
    
    emissions = lr.predict(df)
    return emissions
