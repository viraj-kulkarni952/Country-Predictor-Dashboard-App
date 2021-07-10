import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go

def app():
    st.write("""
             # Dashboard       
            
             """)
    #Sidebar for Year Filter
    year_choice=st.sidebar.slider("Choose a year:", 1990, 2015, 2015)

    country_df = pd.read_csv('Country Development Indicators_Visual.csv')
    country_df_no2016 = country_df.loc[country_df['Year'] !=2016]

    #Selectbox for Country
    selected_country=country_df_no2016['Country'].unique()
    selected_country_list=selected_country.tolist()
    selected_country_list.insert(0, "All")
    selected_countries = st.sidebar.multiselect('To select your choice of countries. Uncheck the "All" options then input your choice of countries',  selected_country_list, default=selected_country_list[0])
    if "All" in selected_countries:
        selected_countries = selected_country.tolist()

    #Prepare filtering of data
    filtered_data_le = country_df_no2016[(country_df_no2016['Year']==year_choice) & (country_df_no2016['Country'].isin(selected_countries))]
    filtered_data_fg = country_df_no2016[(country_df_no2016['Country'].isin(selected_countries))]
    filtered_data_aY = country_df_no2016[(country_df_no2016['Country'].isin(selected_countries))]
    filtered_data_ds = country_df_no2016[(country_df_no2016['Country'].isin(selected_countries))]
    
    #World Map of Life Expectancy
    lifeExpMap = go.Figure(data=go.Choropleth(
        locations = filtered_data_le['alpha-3'],
        z = filtered_data_le['Life expectancy'],
        text = filtered_data_le['Country'],
        colorscale = 'Bluered',
        reversescale = True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title = 'Life Expectancy'),)

    lifeExpectancyTitle="Life Expectancy by country - {user_year}".format(user_year = year_choice)

    lifeExpMap.update_layout(
        title_text=lifeExpectancyTitle,
        height=600,
        width=1100,
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )
    
    
    #Data Visuatlisation of gdp ppp per capita vs fertility
    if filtered_data_aY.empty:
        fertility_gdp_scatter = px.scatter(data_frame=country_df_no2016, x='GDP PPP Per Capita', y='Fertility rate, total (births per woman)',
                     color='Child Mortality Rate (per 1,000 births)', color_continuous_scale = 'bluered',
                     size='Population', hover_name='Country',
                     size_max=45,range_x=[0, 100000], range_y=[-0.1, 8.5], height=700, width=1100, 
                     animation_frame='Year', animation_group="Country",
                     title="Fertility Rate vs. GDP PPP Per Capita", template='none')
    else:
        fertility_gdp_scatter = px.scatter(data_frame=filtered_data_fg, x='GDP PPP Per Capita', y='Fertility rate, total (births per woman)',
                     color='Child Mortality Rate (per 1,000 births)', color_continuous_scale = 'bluered',
                     size='Population', hover_name='Country',
                     size_max=45,range_x=[0, 100000], range_y=[-0.1, 8.5], height=700, width=1100, 
                     animation_frame='Year', animation_group="Country",
                     title="Fertility Rate vs. GDP PPP Per Capita", template='none')            
    
    #Data Visualisation of access to water, electricity and cooking fuel
    acc_elect_title="Access to Electricity (% of population) by Country: 1990-2015"
    acc_water_title="Access to Improved Water Source (% of population) by Country: 1990-2015"
    acc_fuel_title="Access to clean cooking fuels (% of population) by Country: 2000-2015"

    if filtered_data_aY.empty:
        acc_elect = px.line(country_df_no2016, x='Year', y='Access to electricity (% of population)', 
                            color=country_df_no2016['Country'] , hover_name=country_df_no2016['Country'], title=acc_elect_title, width=550)
        acc_water = px.line(country_df_no2016, x='Year', y='Access to improved water source (% of population)', 
                            color=country_df_no2016['Country'] , hover_name=country_df_no2016['Country'], title=acc_water_title, width=550)
        acc_fuel = px.line(country_df_no2016, x='Year', y='Access to clean fuels and technologies for cooking  (% of population)', 
                            color=country_df_no2016['Country'] , hover_name=country_df_no2016['Country'], title=acc_fuel_title, width=1100)
        acc_fuel.update_layout(yaxis_title="Access to clean fuels for cooking (% of population)", showlegend=True)        
        acc_fuel.update_xaxes(range=[2000, 2015])
    else:
        acc_elect = px.line(filtered_data_aY, x='Year', y='Access to electricity (% of population)', 
                            color=filtered_data_aY['Country'] , hover_name=filtered_data_aY['Country'], title=acc_elect_title, width=550)
        acc_water = px.line(filtered_data_aY, x='Year', y='Access to improved water source (% of population)', 
                            color=filtered_data_aY['Country'] , hover_name=filtered_data_aY['Country'], title=acc_water_title, width=550)
        acc_fuel = px.line(filtered_data_aY, x='Year', y='Access to clean fuels and technologies for cooking  (% of population)', 
                            color=filtered_data_aY['Country'] , hover_name=filtered_data_aY['Country'], title=acc_fuel_title, width=1100)
        acc_fuel.update_layout(yaxis_title="Access to clean fuels for cooking (% of population)", showlegend=False)
        acc_fuel.update_xaxes(range=[2000, 2015])
    
    #Diseases related visualisations
    hiv_death_title="HIV/AIDS Deaths per 100,000"
    malaria_death_title="Malaria Deaths per 100,000"

    if filtered_data_ds.empty:
        hiv_death = px.line(country_df_no2016, x='Year', y='HIV/AIDS Deaths per 100,000', 
                                color=country_df_no2016['Country'] , hover_name=country_df_no2016['Country'], title=hiv_death_title, width=550)
        hiv_death.update_layout(showlegend=False)
        malaria_death = px.line(country_df_no2016, x='Year', y='Malaria Deaths per 100,000', 
                                color=country_df_no2016['Country'] , hover_name=country_df_no2016['Country'], title=malaria_death_title, width=550)
        malaria_death.update_layout(showlegend=False)

    else:
        hiv_death = px.line(filtered_data_ds, x='Year', y='HIV/AIDS Deaths per 100,000', 
                            color=filtered_data_aY['Country'] , hover_name=filtered_data_ds['Country'], title=hiv_death_title, width=550)
        hiv_death.update_layout(showlegend=True)
        malaria_death = px.line(filtered_data_ds, x='Year', y='Malaria Deaths per 100,000', 
                            color=filtered_data_aY['Country'] , hover_name=filtered_data_ds['Country'], title=malaria_death_title, width=550)
        malaria_death.update_layout(showlegend=True)
    
    
    #Display the visualisations
    st.plotly_chart(lifeExpMap)
    st.plotly_chart(fertility_gdp_scatter)
    acc1,acc2= st.beta_columns(2)
    acc1.plotly_chart(acc_elect)
    acc2.plotly_chart(acc_water)
    st.plotly_chart(acc_fuel)
    ds1,ds2= st.beta_columns(2)
    ds1.plotly_chart(hiv_death)
    ds2.plotly_chart(malaria_death)


    

    