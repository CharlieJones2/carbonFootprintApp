import streamlit as st
from calculate import Calculate

# Title and description
st.title('Carbon Footprint Calculator')
st.write('This application helps you calculate your carbon footprint.')

# Create tabs
tabs = ['Personal', 'Travel', 'Energy', 'Waste', 'Consumption', 'Results']
selected_tab = st.sidebar.selectbox('Choose a tab', tabs)

if selected_tab == 'Personal':
    st.header('Personal Information')
    height = st.number_input('Height (cm)', min_value=1, max_value=200, value=100, step=1)
    height = height/100
    weight = st.number_input('Weight (kg)', min_value=1, max_value=200, value=100, step=1)
    bmi = weight/(height**2)
    sex = st.selectbox('Sex', ['Male', 'Female'])
    diet = st.selectbox('Diet', ['Omnivore', 'Pescatarian', 'Vegetarian', 'Vegan'])
    social_activity = st.selectbox('Social Activity', ['Never', 'Sometimes', 'Often'])
    

elif selected_tab == 'Travel':
    st.header('Travel Information')
    air_travel = st.selectbox('How Often do you Travel by Air each Month?', ['Never', 'Rarely', 'Frequently', 'Very Frequently'])
    transport = st.selectbox('Which of These is your Primary Travel Method?', ['Private', 'Public', 'Walk/Bicycle'])
    if transport == 'Private':
        vehicle_type = st.selectbox('Vehicle Fuel Type:', ['Petrol', 'LPG', 'Diesel', 'Hybrid', 'Electric'])
    else:
        vehicle_type = None
    if vehicle_type is not None:
        distance = st.number_input('How Many Miles did your Vehicle do in the Past Month?', min_value=0, max_value=1000, step=1)
    else:
        distance = 0
    
elif selected_tab == 'Energy':
    st.header('Energy Consumption')
    shower = st.selectbox('How Often do you Shower?', ['Daily', 'Twice a Day', 'More Frequently', 'Less Frequently'])
    heating = st.selectbox('Which of These is your Primary Heating Source?', ['Coal', 'Natural Gas', 'Wood', 'Electricity'])
    energy_efficiency = st.selectbox('Is your Home Energy Efficient?', ['No', 'Sometimes', 'Yes'])
    
elif selected_tab == 'Waste':
    waste_size = st.selectbox('How Big is your Waste Bag?', ['Small', 'Medium', 'Large', 'Extra Large'])
    waste_count = st.number_input('How Many Waste Bags do you Use per Week?', min_value=0, max_value=10, step=1)
    recycling = st.multiselect('Which of the Followind do you Recycle?', ['Paper', 'Glass', 'Plastic', 'Metal'])
    
elif selected_tab == 'Consumption':
    screen_time = st.number_input('How Many Hours per Day do you Spend on a Screen (PC/Laptop/Phone/Tablet etc)?', min_value=0, max_value=24, step=1)
    internet = st.number_input('How Many Hours per Day do you Spend Online?', min_value=0, max_value=24, step=1)
    grocery = st.number_input('Roughly How Many Dollars do you Spend on Groceries Each Month?', min_value=0, max_value=2000, step=1)
    clothes = st.number_input('How Many New Items of Clothing do you Buy Each Month?', min_value=0, max_value=75, step=1)
    cook = st.multiselect('Which of the Following do you Cook With? (Select all that apply)', ['Stove', 'Oven', 'Microwave', 'Grill', 'Air Fryer'])

elif selected_tab == 'Results':
    calculate = st.button('Calculate')
    if calculate:
        Calculate(bmi, sex, diet, social_activity, air_travel, transport, vehicle_type, shower, heating, energy_efficiency, waste_size, waste_count, recycling, screen_time, internet, grocery, clothes, cook, distance=None)
        