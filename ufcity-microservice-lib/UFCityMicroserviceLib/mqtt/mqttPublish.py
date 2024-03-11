import paho.mqtt.publish as publish

class MqttPublish:

    def __init__(self, broker_address, port):
        self.broker_address = broker_address
        self.port = port

    def publish_multiple(self, messages):
        publish.multiple(messages, hostname=self.broker_address)

    def publish_single(self, topic, message):
        publish.single(topic, message ,hostname=self.broker_address)


# mqttPublish = MqttPublish("localhost", 1883)
# mqttPublish.publish_single("test", "oiaaa")

