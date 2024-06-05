
from json import dumps
from kafka import KafkaProducer
from kafka.errors import KafkaError, KafkaTimeoutError

class Emotion_kafka_producer:
    def __init__(self):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=['localhost:9092'],
                value_serializer=lambda x: dumps(x).encode('utf-8')
            )
        except KafkaError as e:
            print(f"Error initializing Kafka producer: {e}")
            # Handle the exception, e.g., log the error or raise it to the calling code

    def send(self, message):
        try:
            data = {'key': None, 'value': message}
            print("Sending message to Kafka producer", data)
            future = self.producer.send('emotion-detection-stream', data)
            # Ensure the message is sent successfully before continuing
            record_metadata = future.get(timeout=10)
            print("Message sent successfully to topic:", record_metadata.topic)
        except KafkaTimeoutError as e:
            print(f"Error sending message to Kafka producer: {e}")
            # Handle the timeout error, e.g., log the error or raise it to the calling code
        except KafkaError as e:
            print(f"Error sending message to Kafka producer: {e}")
            # Handle other Kafka errors, e.g., log the error or raise it to the calling code
