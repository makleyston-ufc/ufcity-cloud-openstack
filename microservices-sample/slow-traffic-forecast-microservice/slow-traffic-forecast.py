# from UFCityMicroserviceLib import MqttClient, MqttPublish, Observer
import requests
from joblib import load
import sklearn

print(sklearn.__version__)

# url = ('https://github.com/makleyston-ufc/ufcity-cloud-openstack/raw/main/ufcity-ai-models/slow-traffic-forecast/slow'
#        '-traffic-forecast-model.joblib')
# response = requests.get(url)
#
# with open('slow-traffic-forecast-model.joblib', 'wb') as f:
#     f.write(response.content)

model = load('slow-traffic-forecast-model.joblib')
#
#
# class Obs(Observer):
#
#     def update(self, topic: str, message: str) -> None:
#         print(f"Topic: {topic}, Message:  {message}")
#
#
# obs = Obs()
#
# _configs = {"broker_address": "localhost", "port": 1883}
# _topics = ["resource_data/#"]
#
# client = MqttClient.__init__(_configs)
# client.attach(obs)
# client.set_topics(_topics)
# client.subscribe_to_topics()
