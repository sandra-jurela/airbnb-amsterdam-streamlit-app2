import pandas as pd
import streamlit as st
import plotly.express as px

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

# load data
df = pd.read_csv('WK2_Airbnb_Amsterdam_listings_proj_solution.csv', index_col=0)
df["price_string"] = "Price per night: $" + df.price_in_dollar.astype("int").astype("string")
df.available = df.available.round(2)
df.five_day_dollar_price = df.five_day_dollar_price.round(2)
df.rename(columns={"available": "available_%"}, inplace=True)

st.title("Search Airbnb Amsterdam Listings")

st.header("Filters")

sorted_room_type = df.room_type.unique()
selected_room_type = st.multiselect('Room Type', sorted_room_type, sorted_room_type)
sorted_superhost = df.host_is_superhost.unique()
selected_superhost = st.multiselect('Host is Superhost', sorted_superhost, sorted_superhost)
selected_accommodates = st.slider("Number of Guests", 1, int(df.accommodates.max()), value=2)
price_range = st.slider("Price per Night (US$)", 
                        0.0, 
                        float(df.price_in_dollar.max()), 
                        value=(50.0, float(df.price_in_dollar.max())), 
                        step=25.0)
rating = st.slider("Rating Score", 
                   float(df.review_scores_rating.min()), 
                   float(df.review_scores_rating.max()), 
                   value=(4.0, float(df.review_scores_rating.max())), 
                   step=0.1)

st.header("Table")
# Filtering data
df_filtered = df[(df.room_type.isin(selected_room_type)) & 
                 (df.host_is_superhost.isin(selected_superhost)) & 
                 (df.accommodates >= selected_accommodates) &
                 ((df.price_in_dollar >= price_range[0]) & (df.price_in_dollar <= price_range[1])) &
                 ((df.review_scores_rating >= rating[0]) & (df.review_scores_rating <= rating[1]))
                  ]

st.write('Total Number of Listings: ' + str(df.shape[0]))
st.write('Number of Filtered Listings: ', str(df_filtered.shape[0]))

st.dataframe(df_filtered.drop(columns="price_string"))

st.header("Map")

fig = px.scatter_mapbox(
    df_filtered,
    lat="latitude",
    lon="longitude",
    color="room_type",
    zoom=11,
    height=500,
    width=800,
    hover_name="price_string",
    hover_data=["accommodates", "available_%", "five_day_dollar_price"]
)
fig.update_geos(center=dict(lat=df.iloc[0][4], lon=df.iloc[0][5]))
fig.update_layout(mapbox_style="stamen-terrain")
fig.update_layout(hoverlabel=dict(font_size=14))
fig.update_layout(legend=dict(
   yanchor="top",
   y=0.99,
   xanchor="left",
   x=0.01
))


st.plotly_chart(fig, use_container_width=True)




