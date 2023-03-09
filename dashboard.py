import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from weather import get_temp,get_wind_speed,get_wind_dir
from map import heatmap

#add CSS sheat
with open('style.css')as f:
 st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)


# DASHBOARD

st.title('FireWatch 🔥')
col1, col2= st.columns(2)
#col2.metric('Location', 'DHBW Loerrach', delta=None, delta_color="normal", help=None, label_visibility="visible")
location = col1.selectbox('Location:', ['DHBW Hangstraße','DHBW Marie-Curie-Straße'])

if location == 'DHBW Hangstraße':
    #input geocodes
    lat = 47.6169
    lon = 7.6709
elif 'DHBW Marie-Curie-Straße':
   lat = 47.6086812
   lon = 7.6579978


#FIRE
fire = 1 # Input from model
if fire == 1:
    fire_geo = [(lat, lon)] # geocodes of firespots
    fire_station = [(47.6027029, 7.6580481)] #geocodes of the next firestation



    #MAP
    heatmap(lat,lon,fire_geo,fire_station)
else:
   heatmap(lat,lon)


if fire == 1:
    col2.metric('Status', 'FIRE', delta=None, delta_color="normal", help=None, label_visibility="visible")
else:
   col2.metric('Status', 'NO FIRE', delta=None, delta_color="normal", help=None, label_visibility="visible")

#WEATHER
temp = get_temp(lat, lon)
wind_speed = get_wind_speed(lat,lon)
wind_dir = get_wind_dir(lat,lon)

col1, col2, col3 = st.columns(3)
col1.metric('Temperatur', str(temp) + '°C', delta=None, delta_color="normal", help=None, label_visibility="visible")
col2.metric('Windstärke', str(wind_speed) + ' m/s', delta=None, delta_color="normal", help=None, label_visibility="visible")
col3.metric('Windrichtung', str(wind_dir) + '°', delta=None, delta_color="normal", help=None, label_visibility="visible")

st.markdown('<hr/>', unsafe_allow_html = True)
if fire==1:
    st.info('Notfallpriorität - Feuer befindet sich in Zivilistationsnähe', icon="ℹ️")
components.iframe("http://127.0.0.1:5500/fire.html",width=700, height=500)
