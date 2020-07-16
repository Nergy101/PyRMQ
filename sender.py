import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_messages', exchange_type='topic')  # fanout, direct, topic
channel.exchange_declare(exchange='messages', exchange_type='direct')
channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = "PythonSender: Hello World!"

channel.basic_publish(exchange='logs',  routing_key="", body="Hello 1")
channel.basic_publish(exchange='logs',  routing_key="", body="Hello 2")
channel.basic_publish(exchange='logs',  routing_key="", body="Hello 3")

channel.basic_publish(exchange='messages',  routing_key="red", body=message)
channel.basic_publish(exchange='messages',  routing_key="white", body=message)
channel.basic_publish(exchange='messages',  routing_key="blue", body=message)

channel.basic_publish(exchange='topic_messages',  routing_key="JavaBackend.RED", body=message)
channel.basic_publish(exchange='topic_messages',  routing_key="JavaBackend.BLUE", body=message)
channel.basic_publish(exchange='topic_messages',  routing_key="RustBackend.RED", body=message)


print("sent all messages")

connection.close()
