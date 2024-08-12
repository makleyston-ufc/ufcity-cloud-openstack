from UFCityMicroserviceLib import MqttClient, MqttPublish, Observer
import requests
from joblib import load
import pandas as pd

url = ('https://github.com/makleyston-ufc/ufcity-cloud-computing/raw/main/ufcity-ai-models-samples/toronto-bus-delay-forecast/toronto-bus-demand-forecast-model.joblib')
response = requests.get(url)
with open('toronto-bus-demand-forecast-model.joblib', 'wb') as f:
    f.write(response.content)

_configs = {"broker_address": "localhost", "port": 1883}
_topics = ["resource_data/#"]
interests = ['resource_data/route', 'resource_data/time', 'resource_data/day',
             'resource_data/location', 'resource_data/incident', 'resource_data/min_gap',
             'resource_data/direction', 'resource_data/vehicle', 'resource_data/month',
             'resource_data/day_of_week', 'resource_data/is_weekend']

data_dict = {interest: None for interest in interests}
model = load('toronto-bus-demand-forecast-model.joblib')

client = MqttClient(_configs)
publish = MqttPublish(_configs)

def process_data():

    if all(data_dict.values()):
        new_data = {
            'Route': [int(data_dict['resource_data/route'])],
            'Time': [int(data_dict['resource_data/time'])],
            'Day': [int(data_dict['resource_data/day'])],
            'Location': [int(data_dict['resource_data/location'])],
            'Incident': [int(data_dict['resource_data/incident'])],
            'Min Gap': [float(data_dict['resource_data/min_gap'])],
            'Direction': [float(data_dict['resource_data/direction'])],
            'Vehicle': [float(data_dict['resource_data/vehicle'])],
            'Month': [float(data_dict['resource_data/month'])],
            'DayOfWeek': [float(data_dict['resource_data/day_of_week'])],
            'IsWeekend': [float(data_dict['resource_data/is_weekend'])]
        }

        new_df = pd.DataFrame(new_data)
        prediction = model.predict(new_df)
        print(prediction)
        if prediction > 0: # There is bus delay
            send_notification(f"The bus may be {prediction} minutes late.")
            clear_data()
        else:
            print("Waiting for data from all sensors...")

def send_notification(message):
    publish.publish_single("/notification", message)
    print("Message sent to /notification:", message)

def clear_data():
    for interest in interests:
        data_dict[interest] = None

class Obs(Observer):
    def update(self, topic: str, message: str) -> None:
        print(f"Topic: {topic}, Message:  {message}")
        data_dict[topic] = message
        process_data()

client.attach(Obs())
client.set_topics(_topics)
client.subscribe_to_topics()
