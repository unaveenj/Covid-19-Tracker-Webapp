import streamlit as st
from streamlit.script_runner import StopException,RerunException
import pandas as pd
import requests
import plotly.graph_objs as go
from pandas.io.json import json_normalize
from PIL import Image



fig = go.Figure()
#Web Image
img = Image.open("covid_bg.jpg")
st.image(img,use_column_width=True)


st.write("""
# Covid-19 interactive Tracker 
Data is collected using the [Coronavirus COVID19 API](https://documenter.getpostman.com/view/10808728/SzS8rjbc)
""")

URL_GET_COUNTRIES = 'https://api.covid19api.com/countries'
r_countries = requests.get(URL_GET_COUNTRIES)
first_row = pd.DataFrame({'Country':['Choose a country'],'Slug':['Empty'],'ISO2':['E']})
df_original = json_normalize(r_countries.json())
df_original = pd.concat([first_row,df_original]).reset_index(drop=True)

#Side bar user inputs
st.sidebar.header("Fill in your search criteria :")
categories = st.sidebar.selectbox('Case Categories: ',('World Stats','confirmed','deaths','recovered'))
st.sidebar.subheader('Choose Countries: 📍')
country1 = st.sidebar.selectbox('Country:',df_original.Country)
country2=st.sidebar.selectbox('Choose another country to compare: ',df_original.Country)




#Selecting country dropdown
if categories != 'World Stats':
    if country1!='Choose a country':
        slug = df_original.Slug[df_original['Country']==country1].to_string(index=False)[1:]
        # st.write(slug)
        url = f'https://api.covid19api.com/dayone/country/{slug}/status/{categories}'
        st.write(url)
        r=requests.get(url)
        st.markdown("""# Total """+categories+""" cases in """+country1+""":"""+str(r.json()[-1].get("Cases")))
        df = json_normalize(r.json())
        layout = go.Layout(
            title=country1 + '\'s ' + categories + ' cases Data',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Number of cases'), )
        fig.layout.update(dict1=layout)
        fig.add_trace(go.Scatter(x=df.Date, y=df.Cases, mode='lines', name=country1))

        if country2 != 'Choose a country':
            slug = df_original.Slug[df_original['Country'] == country2].to_string(index=False)[1:]
            url = f'https://api.covid19api.com/dayone/country/{slug}/status/{categories}'
            r = requests.get(url)
            st.markdown(f"# Total  {categories} cases in {country2}: {str(r.json()[-1].get('Cases'))}")
            df = json_normalize(r.json())
            layout = go.Layout(
                title=country1+' vs '+country2+' '+categories+' cases Data',
                xaxis=dict(title='Date'),
                yaxis=dict(title='Number of cases'), )
            fig.layout.update(dict1=layout)
            fig.add_trace(go.Scatter(x=df.Date, y=df.Cases, mode='lines', name=country2))
        #Plot the interactive graph
        st.plotly_chart(fig, use_container_width=True)

else:
    #This is when no countries are chosen
    #Here we display general stats
    url = 'https://api.covid19api.com/world/total'
    r = requests.get(url)
    total_recovered = r.json()["TotalRecovered"]
    total_cases = r.json()["TotalConfirmed"]
    total_deaths = r.json()["TotalDeaths"]

    st.write("""# Current Worldwide Statistics:""")
    st.write("Total cases: " + str(total_cases) + ", Total deaths: " + str(total_deaths) + ", Total recovered: " + str(total_recovered))
    x = ["TotalCases", "TotalDeaths", "TotalRecovered"]
    y = [total_cases, total_deaths, total_recovered]

    layout = go.Layout(
        title='World Data',
        xaxis=dict(title='Category'),
        yaxis=dict(title='Number of cases'), )

    fig.layout.update(dict1=layout)
    fig.add_trace(go.Bar(name='World Data', x=x, y=y))
    st.plotly_chart(fig, use_container_width=True)


















