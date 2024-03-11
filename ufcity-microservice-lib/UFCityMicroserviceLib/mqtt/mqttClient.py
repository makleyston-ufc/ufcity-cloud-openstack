import paho.mqtt.client as mqtt

class mqttClient:
    def __init__(self, broker_address, port):
        # self.client = mqtt.Client()
        self.broker_address = broker_address
        self.port = port
        self.qos = 0
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_message = self.on_message
        self.client.connect(broker_address, port, 60)
        self.topics = ["resource_data/#"]

    def on_message(self, client, userdata, message):
        print(f"Recebido o payload: {str(message.payload)} no tópico {message.topic}")

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


mqttClient = mqttClient("localhost", 1883)
# mqttClient.set_topics(["resource_data/#", "test1"])
# mqttClient.subscribe_to_topics()
mqttClient.publish_single("resource_data/", "Hello World")
mqttClient.publish_multiple()


