#!/usr/bin/env python
# coding: utf-8

# # Eindopdracht VA

# Vincent Kemme en Kim Nap

# https://www.kaggle.com/utkarshxy/who-worldhealth-statistics-2020-complete?select=lifeExpectancyAtBirth.csv
# https://www.kaggle.com/utkarshxy/who-worldhealth-statistics-2020-complete?select=basicDrinkingWaterServices.csv

# ### Packages en data inladen

# In[ ]:





# In[1]:


import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import geopandas as gpd
import folium
import requests
import statsmodels.api as sm


# In[2]:


df_life = pd.read_csv("lifeExpectancyAtBirth.csv")
df_water = pd.read_csv("basicDrinkingWaterServices.csv")


# In[3]:


df_life = df_life[df_life["Period"] != 1920]
df_life.head()


# In[4]:


df_water.head()


# ### Data inspecteren

# In[5]:


geslacht_color_map = {'Male':'blue', 'Female':'red', 'Both sexes':'purple'}

ann1 = {'x': 31, 'y':10, 'showarrow': False, 
                    'font': {'color': 'black'}, 'text': "Haiti in 2010"}

hist1 = px.histogram(df_life, x = "First Tooltip", 
                   title = 'Levensverwachting',
                   labels = {'First Tooltip': 'Levensverwachting'},)
hist1.update_layout(yaxis_title = 'Hoeveelheid')
hist1.update_layout({'annotations': [ann1]})
hist1.show()


# In[38]:


outliers_life = df_life[df_life['First Tooltip'] < 40]
print(outliers_life)


# We kiezen ervoor om Haiti in 2010 er toch in te laten staan, dit omdat het waarschijnlijk geen foutieve waarneming is: in 2010 was er een aardbeving in Haiti die van grote invloed heeft kunnen zijn op de levensverwachting.

# In[7]:


ann1 = {'x': 2017, 'y':18, 'showarrow': False, 
                    'font': {'color': 'black'}, 'text': "Congo"}

box1 = px.box(data_frame = df_water, 
             x = 'Period', 
             y = 'First Tooltip', 
             title = 'Verdeling drinkwater per jaar',
             labels = { 
                 'First Tooltip': 'Percentage van de bevolking met toegang tot schoon drinkwater',
                 'Period': 'Jaren'})

box1.update_layout({'annotations': [ann1]})
box1.show()


# **Gaat om percentages, dus weet niet of dit een goeie visualisatie is, maar de histogram zag er al helemaal niet uit haha**,
# 
# Zo te zien maar 1 outlier in 2017, wel een grote spreiding

# In[41]:


outliers_water = df_water[df_water['First Tooltip'] == 22.83]
print(outliers_water)


# ### Data 'Life Expectancy' bewerken en visualiseren

# In[9]:


df_man = df_life[df_life['Dim1'] == 'Male']
df_vrouw = df_life[df_life['Dim1'] == 'Female']
df_beide = df_life[df_life['Dim1'] == 'Both sexes']


# In[10]:


df_beide.sort_values('First Tooltip').head()


# In[11]:


df_beide.sort_values('First Tooltip', ascending = False).head()


# In[12]:


fig1 = go.Figure()

locations = ['Haiti', 'Burundi', 'Central African Republic', 'Zambia', 'Malawi']

for location in locations:
    df = df_beide[df_beide.Location == location]
    fig1.add_trace(go.Scatter(x=df['Period'],
                             y= df['First Tooltip'],
                             name = location,
                             mode='lines+markers'))
for location in locations:
    df = df_man[df_man.Location == location]
    fig1.add_trace(go.Scatter(x=df['Period'],
                             y= df['First Tooltip'],
                             name = location,
                             mode='lines+markers'))
for location in locations:
    df = df_vrouw[df_vrouw.Location == location]
    fig1.add_trace(go.Scatter(x=df['Period'],
                             y= df['First Tooltip'],
                             name = location,
                             mode='lines+markers'))

# Add dropdown
fig1.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="Beide geslachten",
                     method="update",
                     args=[{"visible": [True, False, False]},
                           {"title": "Beide geslachten"}]),
                dict(label="Man",
                     method="update",
                     args=[{"visible": [False, True, False]},
                           {"title": "Mannen",
                            }]),
                dict(label="Vrouw",
                     method="update",
                     args=[{"visible": [False, False, True]},
                           {"title": "Vrouwen",
                            }]),
            ]),
        )
    ])

fig1.update_layout(title = 'Landen met de laagste levensverwachting van 2000 - 2019')

fig1.show()


# In de figuur hierboven is de levensverwachting van mannen en vrouwen te zien door de jaren heen. De 5 landen met de laagste levensverwachting door de jaren heen zijn afgebeeld. Wat opvalt is dat Haïti in 2010 een erg lage levensverwachting had. Er is onderzocht naar hoe dit kon en waarschijnlijk heeft de aardbeving die in 2010 plaatsvond hier een grote invloed op gehad. Wat verder te zien is, is dat in alle landen de vrouwen ouder worden dan de mannen.

# In[13]:


fig2 = go.Figure()

locations = ['Japan', 'Switzerland','Republic of Korea','Singapore', 'Spain']

for location in locations:
    df = df_beide[df_beide.Location == location]
    fig2.add_trace(go.Scatter(x=df['Period'],
                             y= df['First Tooltip'],
                             name = location,
                             mode='lines+markers'))
for location in locations:
    df = df_man[df_man.Location == location]
    fig2.add_trace(go.Scatter(x=df['Period'],
                             y= df['First Tooltip'],
                             name = location,
                             mode='lines+markers'))
for location in locations:
    df = df_vrouw[df_vrouw.Location == location]
    fig2.add_trace(go.Scatter(x=df['Period'],
                             y= df['First Tooltip'],
                             name = location,
                             mode='lines+markers'))

# Add dropdown
fig2.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="Beide geslachten",
                     method="update",
                     args=[{"visible": [True, False, False]},
                           {"title": "Beide geslachten"}]),
                dict(label="Man",
                     method="update",
                     args=[{"visible": [False, True, False]},
                           {"title": "Mannen",
                            }]),
                dict(label="Vrouw",
                     method="update",
                     args=[{"visible": [False, False, True]},
                           {"title": "Vrouwen",
                            }]),
            ]),
        )
    ])

fig2.update_layout(title = 'Landen met de hoogste levensverwachting van 2000 - 2019')

fig2.show()


# In de figuur hierboven is de levensverwachting van mannen en vrouwen te zien door de jaren heen. De 5 landen met de hoogste levensverwachting door de jaren heen zijn afgebeeld. De verschillen tussen de landen met hoogste levensverwachting en laagste levensverwachting is erg groot.

# ### Data 'Toegang Schoon Drinkwater' bewerken en visualiseren

# In[14]:


df_water['Location'].value_counts()


# In[15]:


df_water_kaart = df_water


# In[16]:


df_water_kaart["Location"].replace({"Viet Nam": "Vietnam",
                                   "Bolivia (Plurinational State of)" : "Bolivia",
                                    "Brunei Darussalam" : "Brunei",
                                    "Cabo Verde" : "Cape Verde",
                                    "Congo" : "Republic of Congo",
                                    "Czechia" : "Czech Republic",
                                    "Guinea-Bissau" : "Guinea Bissau",
                                    "Iran (Islamic Republic of)" : "Iran",
                                    "Lao People's Democratic Republic" : "Laos",
                                    "Venezuela (Bolivarian Republic of)" : "Venezuela",
                                    "United Kingdom of Great Britain and Northern Ireland" : "United Kingdom",
                                    "Syrian Arab Republic" : "Syria",
                                    "Sudan (until 2011)" : "Sudan",
                                    "Russian Federation" : "Russia",
                                    "Serbia" : "Republic of Serbia",
                                    "Côte d’Ivoire" : "Ivory Coast",
                                    "Democratic People's Republic of Korea" : "North Korea",
                                    "Eswatini" : "Swaziland",
                                    "Micronesia (Federated States of)" : "Federated States of Micronesia",
                                    "Timor-Leste" : "East Timor",
                                    "The former Yugoslav Republic of Macedonia" : "Macedonia",
                                    "Republic of Moldova" : "Moldova",
                                    "Republic of Korea" : "South Korea"}, inplace=True)


# In[17]:


df_countries = gpd.read_file("countries.geojson")


# In[18]:


df_countries.head()


# In[19]:


df_wc = df_water_kaart.merge(df_countries, left_on = ['Location'], right_on = ['ADMIN'], how = 'inner', suffixes = ['_water', '_countries'])
df_wc = df_wc.sort_values(['Location','Period'])
gdf = gpd.GeoDataFrame(df_wc)


# In[20]:


gdf.head()


# In[21]:


# Kaart, nog een slider toevoegen voor de jaren

fig3 = px.choropleth(gdf, locations='ISO_A3', color='First Tooltip',
                           color_continuous_scale="rdylgn",
                           range_color=(0, 100),
                           labels={'First Tooltip':'Percentage'},
                           hover_name="Location",
                           animation_frame = "Period",
                           height = 800,
                           width = 1200)

fig3.update_layout(title = "Percentage van de bevolking dat toegang heeft tot schoon drinkwater; 2000 - 2017")
fig3.show()


# ### 'Life Expectancy' en 'Toegang Schoon Drinkwater' samenvoegen

# In[22]:


df_lw = df_life.merge(df_water, on = ['Location', 'Period'], how = 'inner', suffixes = ['_life', '_water'])
df_lw.sort_values('First Tooltip_life', ascending = False)


# ### Data Covid inladen en bewerken

# Bron: https://rapidapi.com/api-sports/api/covid-193/

# In[23]:


url = "https://covid-193.p.rapidapi.com/countries"

headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "fd8556f0d0msh78edd7dceb165a6p167072jsna10aefd84705"
    }

response = requests.request("GET", url, headers=headers)


# In[24]:


url = "https://covid-193.p.rapidapi.com/statistics"

headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "fd8556f0d0msh78edd7dceb165a6p167072jsna10aefd84705"
    }

response = requests.request("GET", url, headers=headers)


# In[25]:


test =  response.json()
print(test)


# In[42]:


df_covid = pd.json_normalize(test['response'])
print(df_covid.head())


# In[27]:


# - door een spatie vervangen omdat dat het format is in de water dataframe
df_covid['country'] = df_covid.country.replace("-", " ", regex = True)


# In[28]:


# landen in de covid dataframe een matchende naam geven in de water dataframe

df_covid['country'] = df_covid.country.replace("Cabo Verde", "Cape Verde", regex = True)
df_covid['country'] = df_covid.country.replace("Czechia", "Czech Republic", regex = True)
## Commented want hij bleef Congo replacen 
df_covid['country'] = df_covid.country.replace("Congo", "Republic of Congo", regex = True)
df_covid['country'] = df_covid.country.replace("DRC", "Democratic Republic of the Congo", regex = True)
df_covid['country'] = df_covid.country.replace("Timor Leste", "East Timor", regex = True)
## Commented want hij bleef Micronesia replacen
df_covid['country'] = df_covid.country.replace("Micronesia", "Federated States of Micronesia", regex = True)
df_covid['country'] = df_covid.country.replace("North Macedonia", "Macedonia", regex = True)
## Commented want hij bleef Serbia replacen
df_covid['country'] = df_covid.country.replace("Serbia", "Republic of Serbia", regex = True)
df_covid['country'] = df_covid.country.replace("St Vincent Grenadines", "Saint Vincent and the Grenadines", regex = True)
df_covid['country'] = df_covid.country.replace("S Korea", "South Korea", regex = True)
df_covid['country'] = df_covid.country.replace("Eswatini", "Swaziland", regex = True)
df_covid['country'] = df_covid.country.replace("UAE", "United Arab Emirates", regex = True)
df_covid['country'] = df_covid.country.replace("UK", "United Kingdom", regex = True)
df_covid['country'] = df_covid.country.replace("USA", "United States of America", regex = True)
df_covid['country'] = df_covid.country.replace("CAR", "Central African Republic", regex = True)
## Commented want hij bleef Tanzania replacen
df_covid['country'] = df_covid.country.replace("Tanzania", "United Republic of Tanzania", regex = True)


# ### Kijken of er een verband zit tussen de levensverwachting en schoon drink water

# In[29]:


# Filteren op het meest recente jaar (2015)
df_lw_2015 = df_lw[df_lw['Period'] == 2015]
df_lw_2015.head()


# In[30]:


fig4 = px.scatter(data_frame = df_lw_2015, x = 'First Tooltip_water', y = 'First Tooltip_life',
                color = 'Dim1',
                color_discrete_map = geslacht_color_map,
                symbol = 'Dim1',
                labels = {'Location':'Land','First Tooltip_water':'Percentage van de bevolking met toegang tot schoon drinkwater in 2015', 'First Tooltip_life':'Levensverwachtinging 2015', 'Dim1':'Geslacht'},
                trendline="ols", hover_name = 'Location')

fig4.update_layout(title = 'Levensverwachting tegenover toegang tot schoon drinkwater per geslacht')

fig4.show()


# In[31]:


fig5 = px.scatter(data_frame = df_lw_2015, x = 'First Tooltip_water', y = 'First Tooltip_life',
                color = 'Dim1',
                color_discrete_map = geslacht_color_map,
                symbol = 'Dim1',
                labels = {'Location':'Land','First Tooltip_water':'Percentage van de bevolking met toegang tot schoon drinkwater in 2015', 'First Tooltip_life':'Levensverwachtinging 2015', 'Dim1':'Geslacht'},
                hover_name = 'Location')

fig5.update_layout(title = 'Levensverwachting tegenover toegang tot schoon drinkwater per geslacht')

fig5.show()


# In[43]:


list1 = df_wc['Location'].unique()
list2 = df_covid['country'].unique()
diff = [x for x in list1 if x not in list2]
print(diff)


# In[44]:


df_wc_2017 = df_wc[df_wc['Period'] == 2017]
df_wc_2017_simple = df_wc_2017[['Location', 'First Tooltip']]
print(df_wc_2017_simple)


# In[45]:


df_covid_simple = df_covid[['country', 'cases.1M_pop']]
df_covid_simple = df_covid_simple.rename(columns={'country':'Location', 'cases.1M_pop':'Cases'})
print(df_covid_simple)


# In[35]:


df_wcc = df_wc_2017_simple.merge(df_covid_simple, on = 'Location', how = 'inner')
df_wcc['Cases'] = pd.to_numeric(df_wcc['Cases'])


# In[36]:


fig6 = px.scatter(data_frame = df_wcc, x = 'First Tooltip', y = 'Cases',
                trendline="ols", hover_name = 'Location',
                labels = {'Location':'Land','First Tooltip':'Percentage van de bevolking met toegang tot schoon drinkwater', 'Cases':'Aantal Coronagevallen per 1 miljoen inwoners'})

fig6.update_layout(title = 'Coronagevallen per land tegenover toegang tot schoon drinkwater')

fig6.show()


# In[37]:


fig7 = px.scatter(data_frame = df_wcc, x = 'First Tooltip', y = 'Cases',
                 hover_name = 'Location',
                 labels = {'Location':'Land','First Tooltip':'Percentage van de bevolking met toegang tot schoon drinkwater', 'Cases':'Aantal Coronagevallen per 1 miljoen inwoners'})

fig7.update_layout(title = 'Coronagevallen per land tegenover toegang tot schoon drinkwater')

fig7.show()

## Streamlit code hieronder
import streamlit as st
import streamlit_folium
from streamlit_folium import folium_static

st.set_page_config(page_title = 'VA Eindopdracht', layout = 'wide')
st.title("Dashboard over levensverwachting, toegang tot drinkwater en coronagevallen wereldwijd")
st.markdown('Kim Nap (500830599) en Vincent Kemme (500838439)')


add_selectbox = st.sidebar.selectbox(
    "Wat wil je zien?",
    ("Levensverwachting en drinkwater", "Kaart over toegang tot drinkwater", "Regressie en bronnen")
)

if add_selectbox == "Levensverwachting en drinkwater":
  st.header("Informatie over de levensverwachting en de toegang tot drinkwater in verschillende landen")
  col1, col2= st.columns(2)
  with col1:
      st.plotly_chart(hist1)
      st.markdown('''
      In dit histogram van de levensverwachting per geslacht per land is te zien dat de meest voorkomende levensverwachting 74 is,
      maar dat hij ook een stuk lager uit kan vallen. Zo zien we helemaal links bij 27-jaar-oud waar het histogram begint Haiti liggen.
      Hier was in 2010 een grote natuurramp, waardoor zoveel mensen direct of indirect omgekomen zijn dat de levensverwachting 
      ver onder de maat ligt. 
      ''')

  with col2:
      st.plotly_chart(box1)
      st.markdown('''
      Hierboven is het percentage van de wereldbevolking met toegang tot drinkwater door de jaren heen te zien. We zien dat de IQR 
      elk jaar net iets krimpt, en dat de mediaan ook door de jaren heen stijgt. Dit betekent dat over het algemeen het net wat beter 
      gaat met de toegang tot drinkwater. Toch kan je zien dat het minumum vaak erg laag ligt, dus er zijn nog zeker gebieden waar
      een hoop verbetering nodig is.
      ''')


  col3, col4= st.columns(2)
  with col1:
      st.plotly_chart(fig1)

  with col2:
      st.plotly_chart(fig2)
  
  st.markdown('''
  De vijf landen met de hoogste en laagste levensverwachting zijn hier op twee grafieken naast elkaar gezet om het verschil goed
  in te kunnen beelden. Ze kunnen allebei los van elkaar ingesteld worden op geslacht, om zo alle waarden met elkaar te kunnen
  vergelijken. De lijnen lijken gelukkig allemaal een stijgende trend te hebben, dus de levensverwachting gaat omhoog. Zoals 
  ook bij het histogram hierboven te zien was is in 2010 Haiti weer een erg laag punt. Dit komt, nogmaals, door een 
  natuurramp die dat jaar in Haiti voorkwam. Opvallend genoeg ligt de levensverwachting van vrouwen bij elk van deze 
  landen hoger dan de levensverwachting van de mannen. 
  ''')
     
if add_selectbox == "Kaart over toegang tot drinkwater":
  st.header("Een kaart over de toegang tot drinkwater per land")
  st.plotly_chart(fig3)
  st.markdown('''
  Door het afspelen van de animatie van deze kaart is te zien dat het percentage van de wereld wat toegang heeft tot 
  drinkwater door de jaren heen hoger wordt. Wereldwijd verhoogt het van gemiddeld 73.7% naar 82.6%, maar kijkend
  naar bijvoorbeeld Zuid-Amerika zien we dat de landen daar vaak nog veel meer dan 9% meer toegang tot drinkwater
  hebben. Over enkele landen is geen data, deze zijn lichtgrijs gelaten.
  ''')
  
  
elif add_selectbox == "Regressie en bronnen":
  st.header("Regressies over levensverwachting en coronagevallen tegenover toegang tot schoon drinkwater") 
  lijnen = st.sidebar.radio(
           "Regressielijnen tonen?",
           ('Tonen', 'Niet tonen'))


  col7, col8= st.columns(2)
  with col7:
      if lijnen == 'Tonen':
          st.plotly_chart(fig4)
      else:
          st.plotly_chart(fig5)
      st.markdown('''
      Hier is de levensverwachting ten opzichte van de toegang tot schoondrinkwater te zien. Met een R-kwadraat waarde van tussen
      de 0,6 en de 0,7 bij alledrie de regressielijnen is te zien dat er een sterke correlatie lijkt te zijn tussen deze twee variabelen.
      Omdat het per geslacht geplot is is ook te zijn dat de levensverwachting van mannen lager ligt dan de levensverwachting van vrouwen.
      ''')

  with col8:
      if lijnen == 'Tonen':
          st.plotly_chart(fig6)
      else:
          st.plotly_chart(fig7)     
      st.markdown('''
      Dit is het aantal geregistreerde coronagevallen per 1 miljoen inwoners per land, tegenover het percentage van de bevolking wat
      toegang heeft tot schoon drinkwater. Opvallend genoeg zegt dit plaatje met een R-kwadraat van 0,31 dat toegang tot schoon drinkwater
      correlatie heeft met het aantal coronagevallen in dat land. We hadden dit eigenlijk precies andersom verwacht, dat landen met 
      schoon drinkwater gezondere mensen hadden. Het zou door verschillende redenen kunnen komen dat het zo is dat landen met toegang 
      tot schoon drinkwater meer coronagevallen hebben, bijvoorbeeld: De mensen wonen dichter bij elkaar, er is meer infrastructuur 
      om te testen dus er wordt meer getest of er is meer internationale uitwisseling in deze landen waardoor het virus zich makkelijker verspreidt.
      ''')
  
  st.header("Bronnen") 
    
  st.markdown('''
  Toegang tot water dataset: 
  https://www.kaggle.com/utkarshxy/who-worldhealth-statistics-2020-complete?select=basicDrinkingWaterServices.csv
  
  Levensverwachting dataset: 
  https://www.kaggle.com/utkarshxy/who-worldhealth-statistics-2020-complete?select=lifeExpectancyAtBirth.csv
  
  Covid dataset:
  https://rapidapi.com/api-sports/api/covid-193/
  ''')

