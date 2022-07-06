# cd "OneDrive\Área de Trabalho\Faculdade\03. Cursos\07.streamlit"

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
DATA_URL = (
	"Motor_Vehicle_Collisions_-_Crashes.csv"
	)

st.title("Motor Vehicle Collisions in New York City")
st.markdown("This application is a Streamlit dashboard that can be used "
	"to analyse motor vehicle collisions in NYC")

@st.cache(persist=True)
def load_data(nrows):
	data = pd.read_csv(DATA_URL, nrows = nrows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
	data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
	lowercase = lambda x: str(x).lower()
	data.rename(lowercase, axis='columns', inplace=True)
	data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
	return data

data = load_data(100000)
original_data = data.copy()

st.header("Where are the most people injuried in NYC")

injured_people = st.slider("number of persons injured in vehicle collisions", 0, 19)
st.map(data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))

st.header("How many colisions occur during a given time of the day?")
hour = st.sidebar.slider("Hour to look at", 0, 23)
data = data[data["data/time"].dt.hour == hour]

st.markdown(f"Vehicle collisions between {hour}:00 and {(hour+1)%24}:00")

midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))
st.write(pdk.Deck(
	map_style = "mapbox://styles/mapbox/light-v9",
	initial_view_state = {
		"latitude": midpoint[0],
		"longitude": midpoint[1],
		"zoom": 11,
		"pitch": 50
	},
	layers=[
		pdk.Layer(
			"HexagonLayer",
			data=data[['data/time', 'latitude', 'longitude']],
			get_position = ['longitude', 'latitude'],
			radius=100,
			extruded=True,
			pickable=True,
			elevation_scale=4,
			elevation_range=[0,1000],
		),
	],
))

st.subheader(f"Breakdown by minute between {hour}:00 and {(hour+1)%24}:00")
filtered = data[
	(data['data/time'].dt.hour >= hour) & (data["data/time"].dt.hour < (hour+1))
]
hist = np.histogram(filtered['data/time'].dt.minute, bins=60, range=(0,60))[0]
chart_data = pd.DataFrame({'minutes': range(60), 'crashes':hist})
fig = px.bar(chart_data, x='minutes', y='crashes', hover_data=['minutes', 'crashes'], height=400)
st.write(fig)

st.header("Top 5 dangerous streets by affected type:")
select_type = st.selectbox("Affected type of people", ['Pedestrian', 'Cyclists', 'Motrorists'])

if select_type == 'Pedestrian':
	st.write(original_data.query("injured_persons >= 1")[["on_street_name", "injured_pedestrians"]].sort_values(by=['injured_pedestrians'], ascending=False).dropna(how='any')[:5])

elif select_type == 'Cyclists':
	st.write(original_data.query("injured_cyclists >= 1")[["on_street_name", "injured_cyclists"]].sort_values(by=['injured_cyclists'], ascending=False).dropna(how='any')[:5])

elif select_type == 'Motrorists':
	st.write(original_data.query("injured_motorists >= 1")[["on_street_name", "injured_motorists"]].sort_values(by=['injured_motorists'], ascending=False).dropna(how='any')[:5])

if st.checkbox("Show Raw Data", False):
	st.subheader('Raw Data')
	st.write(data)