import streamlit as st
import pandas as pd

# Title and description
st.title('Carbon Footprint Calculator')
st.write('This application helps you calculate your carbon footprint.')

# Create tabs
tabs = ['Personal', 'Travel', 'Tab 3', 'Tab 4', 'Tab 5']
selected_tab = st.sidebar.selectbox('Choose a tab', tabs)

if selected_tab == 'Personal':
    st.header('Personal Information')
    sex = st.selectbox('Sex', ['Male', 'Female'])
    diet = st.selectbox('Diet', ['Omnivore', 'Pescatarian', 'Vegetarian', 'Vegan'])
    social_activity = st.selectbox('Social Activity', ['Never', 'Sometimes', 'Often'])

elif selected_tab == 'Travel':
    st.header('Travel Information')
    