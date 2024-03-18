import paho.mqtt.publish as publish


class MqttPublish:

    def __init__(self, configs):
        self.broker_address = configs["broker_address"]
        self.port = configs["port"]

    def publish_multiple(self, messages):
        publish.multiple(messages, hostname=self.broker_address)

    def publish_single(self, topic, message):
        publish.single(topic, message, hostname=self.broker_address)
