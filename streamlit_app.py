import streamlit as st
from calculate import Calculate

st.title('Carbon Footprint Calculator')
st.write('This application helps you calculate your monthly carbon footprint expressed in Kilograms of CO2 Equivalent.')

st.header('Personal Information')
height = st.number_input('Height (cm)', min_value=1, max_value=200, value=100, step=1)
height = height/100
weight = st.number_input('Weight (kg)', min_value=1, max_value=200, value=100, step=1)
sex = st.selectbox('Sex', ['Male', 'Female'])
diet = st.selectbox('Diet/Lifestyle', ['Omnivore', 'Pescatarian', 'Vegetarian', 'Vegan'])
social_activity = st.selectbox('How Often per Month do you Engage in Social Activity', ['Never', 'Sometimes', 'Often'])

st.header('Travel')
air_travel = st.selectbox('How Often do you Travel by Air each Month?', ['Never', 'Rarely', 'Frequently', 'Very Frequently'])
transport = st.selectbox('Which of These is your Primary Travel Method?', ['Private', 'Public', 'Walk/Bicycle'])
if transport == 'Private':
    vehicle_type = st.selectbox('Vehicle Fuel Type:', ['Petrol', 'LPG', 'Diesel', 'Hybrid', 'Electric'])
else:
    vehicle_type = None
if vehicle_type is not None:
    distance = st.number_input('How Many Miles did your Vehicle do in the Past Month?', min_value=0, max_value=1000, step=50)
else:
    distance = 0

st.header('Energy Usage')
shower = st.selectbox('How Often do you Shower?', ['Less Frequently', 'Daily', 'Twice a Day', 'More Frequently'])
heating = st.selectbox('Which of These is your Primary Heating Source?', ['Coal', 'Natural Gas', 'Wood', 'Electricity'])
energy_efficiency = st.selectbox('Do you Consider the Energy Efficiency of your Devices?', ['No', 'Sometimes', 'Yes'])

st.header('Waste and Recycling')
waste_size = st.selectbox('How Big is your Waste Bag?', ['Small', 'Medium', 'Large', 'Extra Large'])
waste_count = st.number_input('How Many Waste Bags do you Use per Week?', min_value=0, max_value=10, step=1)
recycling = st.multiselect('Which of the Following do you Recycle? (Select all that apply)', ['Paper', 'Glass', 'Plastic', 'Metal'])

st.header('Other')
screen_time = st.number_input('How Many Hours per Day do you Spend on a Screen (PC/Laptop/Phone/Tablet etc)?', min_value=0, max_value=24, step=1)
internet = st.number_input('How Many Hours per Day do you Spend Online?', min_value=0, max_value=24, step=1)
grocery = st.number_input('Roughly How Many Dollars do you Spend on Groceries Each Month?', min_value=0, max_value=2000, step=20)
clothes = st.number_input('How Many New Items of Clothing do you Buy Each Month?', min_value=0, max_value=75, step=1)
cook = st.multiselect('Which of the Following do you Cook With? (Select all that apply)', ['Stove', 'Oven', 'Microwave', 'Grill', 'Air Fryer'])

if 'calculatePressed' not in st.session_state:
    st.session_state.calculatePressed = False
    
calculate = st.button('Calculate my Emissions')
calculatePressed = False
if calculate:
    st.session_state.calculatePressed = True
    emissions = Calculate(height, weight, sex, diet, social_activity, air_travel, transport, vehicle_type, distance, shower, heating, energy_efficiency, waste_size, waste_count, recycling, screen_time, internet, grocery, clothes, cook)
    

st.header('Results')

if calculate:
    st.write(f'Your estimated monthly emission levels are: `{emissions} Kilograms CO2E`')
    if emissions < 5000:
        st.write('Keep it up! Your emissions levels are below average :D')
    elif emissions > 5000:
        st.write('Your emissions levels are above average. Consider hitting the button below for some suggestions on how to reduce your footprint.')
else:
    st.write('Click on the `Calculate my Emissions` button to see your estimated monthly emissions level!')
    
suggestions = st.button('How can I lower my emissions?')
if suggestions:
    if st.session_state.calculatePressed:
        st.write('Go vegan ;)')
    else:
        st.write('Please click the `Calculate my Emissions` button for suggestions on how to lower your environmental impact.')
