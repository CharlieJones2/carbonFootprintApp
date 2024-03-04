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
df = pd.get_dummies(df, columns=['vehicle'], dummy_na=True, drop_first=True)

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

from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(random_state=42, n_estimators=200, max_features=20)

rf.fit(X_train, y_train)

def Calculate(height, weight, sex, diet, social_activity, air_travel, transport, vehicle_type, distance, shower, heating, energy_efficiency, waste_size, waste_count, recycling, screen_time, internet, grocery, clothes, cook):
    user = pd.DataFrame(columns=["shower","monthlyGrocery","airTravel","monthlyVehicle","wasteCount","dailyScreen","monthlyClothes","dailyInternet","energyEfficiency",
                                 "bodyType_obese","bodyType_overweight","bodyType_underweight","sex_male",
                                 "diet_pescatarian","diet_vegan","diet_vegetarian","heating_electricity","heating_natural gas","heating_wood","transport_public","transport_walk/bicycle","social_often",
                                 "social_sometimes","wasteSize_large","wasteSize_medium","wasteSize_small","vehicle_electric","vehicle_hybrid","vehicle_lpg","vehicle_petrol","vehicle_nan","recycling_glass","recycling_metal",
                                 "recycling_paper","recycling_plastic","cookType_airfryer","cookType_grill","cookType_microwave","cookType_oven","cookType_stove"])
    user.loc[0] = [0]*len(user.columns)
    
    # determining user inputs
    bmi = weight / (height ** 2)
    if bmi < 18.5:
        user['bodyType_underweight'] = 1
    elif 18.5 < bmi < 24.9:
        pass
    elif 25 < bmi < 29.9:
        user['bodyType_overweight'] = 1
    elif bmi > 30:
        user['bodyType_obese'] = 1
        
    if sex == 'Male':
        user['sex_male'] = 1
    
    if diet == 'Pescatarian':
        user['diet_pescatarian'] = 1
    elif diet == 'Vegetarian':
        user['diet_vegetarian'] = 1
    elif diet == 'Vegan':
        user['diet_vegan'] = 1
    
    if social_activity == 'Often':
        user['social_often'] = 1
    elif social_activity == 'Sometimes':
        user['social_sometimes'] == 1
    
    if air_travel == 'Rarely':
        user['airTravel'] = 1
    elif air_travel == 'Frequently':
        user['airTravel'] = 2
    elif air_travel == 'Very Frequently':
        user['airTravel'] = 3
        
    if transport == 'Public':
        user['transport_public'] = 1
    elif transport == 'Walk/Bicycle':
        user['transport_walk/bicycle'] = 1
    
    if vehicle_type is None:
        user['vehicle_nan'] = 1
    elif vehicle_type == 'Petrol':
        user['vehicle_petrol'] = 1
    elif vehicle_type == 'LPG':
        user['vehicle_lpg'] = 1
    elif vehicle_type == 'Hybrid':
        user['vehicle_hybrid'] = 1
    elif vehicle_type == 'Electric':
        user['vehicle_electric'] = 1
    
    user['monthlyVehicle'] = distance
    
    if shower == 'Less Frequently':
        user['shower'] = 0
    elif shower == 'Daily':
        user['shower'] = 1
    elif shower == 'Twice a Day':
        user['shower'] = 2
    elif shower == 'More Frequently':
        user['shower'] = 3
    
    if heating == 'Electricity':
        user['heating_electricity'] = 1
    elif heating == 'Natural Gas':
        user['heating_natural gas'] = 1
    elif heating == 'Wood':
        user['heating_wood'] = 1
    
    if energy_efficiency == 'No':
        user['energyEfficiency'] = 0
    elif energy_efficiency == 'Sometimes':
        user['energyEfficiency'] = 1
    elif energy_efficiency == 'Yes':
        user['energyEfficiency'] = 2
        
    if waste_size == 'Large':
        user['wasteSize_large'] = 1
    elif waste_size == 'Medium':
        user['wasteSize_medium'] = 1
    elif waste_size == 'Small':
        user['wasteSize_small'] = 1
    
    user['wasteCount'] = waste_count
    
    recyclables = ['Glass', 'Paper', 'Plastic', 'Metal']
    for item in recyclables:
        column_name = 'recycling_' + item.lower()
        if item in recycling:
            user.at[0, column_name] = 1
        else:
            user.at[0, column_name] = 0
    
    user['dailyScreen'] = screen_time
    
    user['dailyInternet'] = internet
    
    user['monthlyGrocery'] = grocery
    
    user['monthlyClothes'] = clothes
    
    cooking_methods = ['Stove', 'Oven', 'Microwave', 'Grill', 'Air Fryer']
    for method in cooking_methods:
        column_name = 'cookType_' + method.lower().replace(' ', '')
        if method in cook:
            user.at[0, column_name] = 1
        else:
            user.at[0, column_name] = 0
    
    emissions = rf.predict(user)
    emissions = round(emissions[0], 2)
    
    return emissions
