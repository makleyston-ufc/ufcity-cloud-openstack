from io import StringIO

from UFCityMicroserviceLib import MqttClient, Observer, MongoDB
from joblib import load
import pandas as pd
import json
from statsmodels.tsa.holtwinters import ExponentialSmoothing

modelCO = load('CO Mean-ETS-pollution-trend-analysis-model.joblib')
modelNO2 = load('NO2 Mean-ETS-pollution-trend-analysis-model.joblib')
modelO3 = load('O3 Mean-ETS-pollution-trend-analysis-model.joblib')
modelSO2 = load('SO2 Mean-ETS-pollution-trend-analysis-model.joblib')
ets_models_dict = {'CO Mean': modelCO, 'NO2 Mean': modelNO2, 'O3 Mean': modelO3, 'SO2 Mean': modelSO2}

_configsMQTT = {"broker_address": "localhost", "port": 1883}
_topics = ["resource_data/#"]

_configsStore = {
        'host': '172.19.0.3',
        'port': '27017',
        'database': 'ufcity',
        'collection': 'pollution-trend-analysis',
        'username': 'root',
        'password': 'example'
    }

client = MqttClient(_configsMQTT)
mongoDB = MongoDB(_configsStore)

def update_model(data_frame):
    for col in data_frame.columns:
        new_values = data_frame[col]
        model = ExponentialSmoothing(new_values, seasonal='add', seasonal_periods=12)
        result = model.fit()
        ets_models_dict[col] = result

def save_forecasts():
    for key, model in ets_models_dict.items():
        json_data = json.dumps(model.forecast(steps=12).tolist())
        mongoDB.create(key, json_data)

class Obs(Observer):
    def update(self, topic: str, message: str) -> None:
        print(f"Topic: {topic}, Message:  {message}")
        df = pd.read_json(StringIO(message), orient='index')
        df = df.transpose()
        update_model(df)
        save_forecasts()

client.attach(Obs())
client.set_topics(_topics)
client.subscribe_to_topics()
