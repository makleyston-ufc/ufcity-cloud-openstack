import paho.mqtt.client as mqtt
from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    @abstractmethod
    def update(self, topic: str, message: str) -> None:
        pass


class MqttClient:
    def __init__(self, configs):
        self.broker_address = configs["broker_address"]
        self.port = configs["port"]
        self.qos = 0
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_message = self.on_message
        self.client.connect(self.broker_address, self.port, 60)
        self.topics = ["resource_data/#"]
        self.on_subscribe = self
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, topic: str, message: str) -> None:
        for observer in self._observers:
            observer.update(topic, message[2:-1])

    def on_message(self, client, userdata, message):
        print(f"Received payload: {str(message.payload)} in topic {message.topic}")
        self.notify(message.topic, str(message.payload))

    def subscribe_to_topics(self):
        for topic in self.topics:
            self.client.subscribe(topic)
        self.client.loop_forever()

    def set_topics(self, topics):
        self.topics = topics
        return self

    def set_qos(self, qos):
        self.qos = qos
        return self