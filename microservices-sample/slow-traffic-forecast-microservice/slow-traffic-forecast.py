from UFCityMicroserviceLib import MqttClient, MqttPublish, Observer
import requests
from joblib import load
import pandas as pd

url = ('https://github.com/makleyston-ufc/ufcity-cloud-openstack/raw/main/ufcity-ai-models/slow-traffic-forecast/slow'
       '-traffic-forecast-model.joblib')
response = requests.get(url)
with open('slow-traffic-forecast-model.joblib', 'wb') as f:
    f.write(response.content)

_configs = {"broker_address": "localhost", "port": 1883}
_topics = ["resource_data/#"]
interests = ['resource_data/weather', 'resource_data/day_of_week', 'resource_data/hour_of_day',
             'resource_data/is_peak_hour', 'resource_data/random_event_occurred', 'resource_data/traffic_density']
data_dict = {interest: None for interest in interests}
model = load('slow-traffic-forecast-model.joblib')

client = MqttClient(_configs)
publish = MqttPublish(_configs)

def process_data():

    if all(data_dict.values()):
        new_data = {
            'Weather': [int(data_dict['resource_data/weather'])],
            'Day Of Week': [int(data_dict['resource_data/day_of_week'])],
            'Hour Of Day': [int(data_dict['resource_data/hour_of_day'])],
            'Is Peak Hour': [int(data_dict['resource_data/is_peak_hour'])],
            'Random Event Occurred': [int(data_dict['resource_data/random_event_occurred'])],
            'Traffic Density': [float(data_dict['resource_data/traffic_density'])]
        }

        new_df = pd.DataFrame(new_data)
        prediction = model.predict(new_df)
        print(prediction)
        if prediction < 50:
            send_notification(f"Possibility of slow traffic. Average speed: {prediction} k/h")
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
