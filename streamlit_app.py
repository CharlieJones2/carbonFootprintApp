import streamlit as st
from calculate import Calculate

st.title('Carbon Footprint Calculator')
st.write('This application helps you calculate your monthly carbon footprint expressed in Kilograms of CO2 Equivalent.')
improve = []
st.header('Personal Information')
height = st.number_input('Height (cm)', min_value=1, max_value=200, value=100, step=1)
height = height/100
weight = st.number_input('Weight (kg)', min_value=1, max_value=200, value=100, step=1)
sex = st.selectbox('Sex', ['Male', 'Female'])
diet = st.selectbox('Diet/Lifestyle', ['Omnivore', 'Pescatarian', 'Vegetarian', 'Vegan'])
if diet != 'Vegan':
    improve.append('According to a meta anaylsis conducted by Oxford University, going vegan is the single biggest positive change an individual can make to reduce their environmental impact. See here for details: https://doi.org/10.1126/science.aaq0216')
social_activity = st.selectbox('How Often per Month do you Engage in Social Activity', ['Never', 'Sometimes', 'Often'])
if social_activity == 'Often':
    improve.append('It is possible that engaging in less social activity could reduce your environmental impact. Consider how you travel to events and how sustainable they are.')

st.header('Travel')
air_travel = st.selectbox('How Often do you Travel by Air each Month?', ['Never', 'Rarely', 'Frequently', 'Very Frequently'])
if air_travel != 'Rarely':
    improve.append('Travelling by air is detrimental to the environment. Consider the necessity of air travel and look to reduce it where possible.')
transport = st.selectbox('Which of These is your Primary Travel Method?', ['Private', 'Public', 'Walk/Bicycle'])
if transport == 'Private':
    improve.append('Consider Public Transport or Walking where possible for a lower carbon footprint. Traveling by public transport allows the environmental impact to be spread across many people, while walking or cycling removes this impact altogether.')
    vehicle_type = st.selectbox('Vehicle Fuel Type:', ['Petrol', 'LPG', 'Diesel', 'Hybrid', 'Electric'])
else:
    vehicle_type = None
if vehicle_type is not None:
    distance = st.number_input('How Many Miles did your Vehicle do in the Past Month?', min_value=0, max_value=1000, step=50)
else:
    distance = 0

st.header('Energy Usage')
shower = st.selectbox('How Often do you Shower?', ['Less Frequently', 'Daily', 'Twice a Day', 'More Frequently'])
if shower == 'Twice a Day' or shower == 'More Frequently':
    improve.append('Consider showering less often: daily is enough for most people.')
heating = st.selectbox('Which of These is your Primary Heating Source?', ['Coal', 'Natural Gas', 'Wood', 'Electricity'])
if heating != 'Electricity':
    improve.append('Consider switching to electric heating for a much more energy efficient solution. This not only reduces your environmental impact but can save you a considerable amount of money on energy bills.')
energy_efficiency = st.selectbox('Do you Consider the Energy Efficiency of your Devices?', ['No', 'Sometimes', 'Yes'])
if energy_efficiency != 'Yes':
    improve.append('Consider the energy efficiency of your devices more. Like choosing a sustainable heating source, considering the energy efficiency of devices also reduces your environmental impact while saving you money. Look for devices rated EPC A or B.')
    
st.header('Waste and Recycling')
waste_size = st.selectbox('How Big is your Waste Bag?', ['Small', 'Medium', 'Large', 'Extra Large'])
waste_count = st.number_input('How Many Waste Bags do you Use per Week?', min_value=0, max_value=10, step=1)
if waste_count > 1:
    improve.append('Try to use less waste - the best way to do this is to recycle more and be more conscious of the packaging on the products we buy, as well as making sure to use up what we have.')
recycling = st.multiselect('Which of the Following do you Recycle? (Select all that apply)', ['Paper', 'Glass', 'Plastic', 'Metal'])
if recycling != ['Paper', 'Glass', 'Plastic', 'Metal']:
    improve.append('Try to recycle as much as possible! This helps create more sustainable products and reduces your waste simultaneously.')

st.header('Other')
screen_time = st.number_input('How Many Hours per Day do you Spend on a Screen (PC/Laptop/Phone/Tablet etc)?', min_value=0, max_value=24, step=1)
internet = st.number_input('How Many Hours per Day do you Spend Online?', min_value=0, max_value=24, step=1)
if screen_time or internet > 5:
    improve.append('Consider spending less time using technology such as laptops, phones and TVs. Try to replace these with \'offline\' activities such as walking, reading or exercising.')
grocery = st.number_input('Roughly How Many Dollars do you Spend on Groceries Each Month?', min_value=0, max_value=2000, step=20)
if grocery > 160:
    improve.append('Try to reduce the amount spent on groceries - prioritise whole plant foods over processed and animal based foods, and try to buy in bulk where possible.')
clothes = st.number_input('How Many New Items of Clothing do you Buy Each Month?', min_value=0, max_value=75, step=1)
if clothes > 3:
    improve.append('Try to cut down on the amount of new clothing you buy. Wear what you already have, and try to shop secondhand and sutainable clothes where new purchases are necessary.')
cook = st.multiselect('Which of the Following do you Cook With? (Select all that apply)', ['Stove', 'Oven', 'Microwave', 'Grill', 'Air Fryer'])
if 'Stove' or 'Oven' or 'Grill' in cook:
    improve.append('Consider cooking more with an air fryer or microwave where possible. Cooking on a stove, or in the grill or oven are particularly energy intensive processes and can generate larger emissions.')

if 'calculatePressed' not in st.session_state:
    st.session_state.calculatePressed = False
    

calculate = st.button('Calculate my Emissions')
calculatePressed = False
if calculate:
    st.session_state.calculate = True
    st.session_state.calculatePressed = True
    emissions = Calculate(height, weight, sex, diet, social_activity, air_travel, transport, vehicle_type, distance, shower, heating, energy_efficiency, waste_size, waste_count, recycling, screen_time, internet, grocery, clothes, cook)
    

st.header('Results')

if calculate:
    st.write(f'Your estimated monthly emission levels are: `{emissions} Kilograms CO2E`')
    if emissions < 2270:
        st.write('Keep it up! Your emissions levels are below average :D')
    elif emissions > 2270:
        st.write('Your emissions levels are above average. Consider hitting the button below for some suggestions on how to reduce your footprint.')
else:
    st.write('Click on the `Calculate my Emissions` button to see your estimated monthly emissions level!')
    
suggestions = st.button('How can I lower my emissions?')
if suggestions:
    if st.session_state.calculatePressed:
        for i in improve:
            st.write(i)
    else:
        st.write('Please click the `Calculate my Emissions` button for suggestions on how to lower your environmental impact.')
