import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

data = pd.read_csv("training_data.csv")

X = data.iloc[:,:-1]
y = data.iloc[:,-1]

model = RandomForestClassifier()

model.fit(X,y)

with open("optimizer_model.pkl","wb") as f:
    pickle.dump(model,f)

print("Model trained successfully")
