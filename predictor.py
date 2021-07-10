import pandas as pd
import streamlit as st
import pickle
import numpy as np

def app():
    st.title('Country Prediction App')
    st.write("""
             This app is used to predict the classification of a country based on its development. You can also go onto the "dashboard" to get an insight into countries' development indicators.
            
            The dataset is from Kaggle: https://www.kaggle.com/virajkulkarni952/country-development-indicators
            
            App made by Viraj Kulkarni.            
            
             """)
    
    #Sidebar user input variables - prediction
    st.write("")
    st.sidebar.subheader("User Input Variables")
    
    #Give example of CSV file
    st.sidebar.markdown("Example CSV file input: https://raw.githubusercontent.com/viraj-kulkarni952/Country-Predictor-Dashboard-App/main/country-example-format.csv")
    
    user_input_csv=st.sidebar.file_uploader("Upload your CSV file here:", type=['csv'])
    if user_input_csv is not None:
        input_dataframe = pd.read_csv(user_input_csv)
    else:
        def user_input_features():
            gdp_per_capita = st.sidebar.slider("GDP Per Capita", 50, 200000, 100000)
            gdp_ppp_per_capita = st.sidebar.slider("GDP PPP Per Capita", 50, 200000, 100000)
            electricity_access = st.sidebar.slider("Access to Electricity (% of Population)", 0, 100, 50)
            water_access = st.sidebar.slider("Access to Water (% of Population)", 0, 100, 50) 
            life_expectancy = st.sidebar.slider("Life Expectancy", 20, 100, 60)
            fertility_rate = st.sidebar.slider("Fertility Rate (Births per Woman)", 0, 10, 5)
            child_mortality_rate = st.sidebar.slider("Child Mortality Rate (per 1,000 births)", 1, 350, 172)
            measles_cases = st.sidebar.slider("Reported Measles Cases", 0, 250000, 125000)
            polio_immunisation = st.sidebar.slider("Polio Immunisation Rate (% of one-year olds", 0, 100, 50)
            hiv_deaths = st.sidebar.slider("HIV/AIDS Deaths per 100,000", 0, 1300, 650)
            malaria_deaths = st.sidebar.slider("Malaria Deaths per 100,000", 0, 250, 125)
            data = {'GDP Per Capita': [gdp_per_capita],
                        'GDP PPP Per Capita': [gdp_ppp_per_capita],
                        'Access to electricity (% of population)': [electricity_access],
                        'Access to improved water source (% of population)': [water_access],
                        'Life expectancy': [life_expectancy],
                        'Fertility rate, total (births per woman)': [fertility_rate],
                        'Child Mortality Rate (per 1,000 births)': [child_mortality_rate],
                        'Reported cases of measles (WHO (2019))': [measles_cases],
                        'Polio Immunisation Rate (% of one-year olds)': [polio_immunisation],
                        'HIV/AIDS Deaths per 100,000': [hiv_deaths],
                        'Malaria Deaths per 100,000': [malaria_deaths]
                }
            features = pd.DataFrame(data)
            return features
        input_dataframe = user_input_features()
    
    #Combine user input with the dataset
    raw_country = pd.read_csv('Country Development Indicators.csv')
    country = raw_country.drop(columns=['Country Classification'])
    df = pd.concat([input_dataframe, country], axis=0)
    df = df.drop(['Country',
              'Year',
              'GDP',
              'GDP PPP',
              'Population',
              'Access to clean fuels and technologies for cooking  (% of population)',
              'Government expenditure on education (% of GDP)',
              'Adult Mortality',
              'Public Expenditure on Health (% of GDP)',
              ], axis=1)
    
    df = df[:1]
    
    #Display User Input
    st.subheader("User Input Variables")
    st.write("Awaiting for user input of CSV file. Currently using the example input parameters:")
    st.table(df)
    
    #Load model and predict classification
    load_clf = pickle.load(open('country_model.pkl', 'rb'))
    pred=load_clf.predict(df)
    pred_proba=load_clf.predict_proba(df)
    
    #Change column names for pred probability
    pred_probability = pd.DataFrame(pred_proba)
    column_name_predprob = ["Least Developed Country","Developing Country","Developed Country"]
    pred_probability.columns = column_name_predprob
    
    #Put pred on using streamlit
    st.subheader("Prediction")
    penguin_prediction = np.array(["Least Developed Country","Developing Country","Developed Country"])
    st.write(penguin_prediction[pred])
    
    #Put pred_probability on using streamlit
    st.write('')
    st.subheader("Prediction Probability")
    st.write(pred_probability)
    st.write("")
    
