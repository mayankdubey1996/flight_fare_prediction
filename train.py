import pandas as pd
from sklearn.feature_extraction import DictVectorizer
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import joblib

def read_data(file_name):
    df = pd.read_csv("data/Clean_Dataset.csv",index_col=0)
    X_col = ['airline', 'source_city', 'departure_time','stops',
       'arrival_time', 'destination_city', 'class','days_left']
    y_col = 'price'
    X = df[X_col]
    y = df[y_col]
    return X,y

def get_model_result(X_train,y_train):
    X_train_dict = X_train.to_dict(orient='records')
    dv = DictVectorizer(sparse=False)
    X_train = dv.fit_transform(X_train_dict)
    model = xgb.XGBRegressor(subsample=0.8,n_jobs=-1,
                            n_estimators=100,max_depth=10,
                            learning_rate=0.2,colsample_bytree=0.6,
                            colsample_bylevel=0.4)
    print("Training model....")
    
    model.fit(X_train,y_train)
    y_pred = model.predict(X_train)
    rmse = mean_squared_error(y_train,y_pred)**.5
    print("RMSE: ", round(rmse,2))
    return model,dv 

if __name__ =="__main__":
    file_name = "data/Clean_Dataset.csv"
    X,y = read_data(file_name)
    
    model,dv = get_model_result(X,y)
    
    joblib.dump(dv, 'model/feature_vect.pkl') 
    joblib.dump(model, 'model/xgb_model.pkl')

