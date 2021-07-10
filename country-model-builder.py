import pandas as pd

df = pd.read_csv("Country Development Indicators.csv")

#Drop irrelevant columns
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

#Drop null values
dataset = df.dropna(axis=0)

#Encode variables
class_mapper = {'Least Developed Country': 0, 'Developing Country': 1, 'Developed Country': 2}

def target_encode(val):
    return class_mapper[val]

dataset['Country Classification'] = dataset['Country Classification'].apply(target_encode) 

#Split into X and Y
X = dataset.drop(['Country Classification'], axis=1)
Y = dataset.iloc[:, [-1]]

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X, Y)

#Save the model
import pickle
pickle.dump(model, open('country_model.pkl','wb'))
print("Successfully imported the model.")

from sklearn.preprocessing import LabelEncoder
test = LabelEncoder()
df["Country Classification"]=test.fit(df["Country Classification"])
