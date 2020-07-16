import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.exchange_declare(exchange='topic_messages', exchange_type='topic')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# will only receive anything that starts with JavaBackend.<some_event>
channel.queue_bind(exchange='topic_messages', queue=queue_name, routing_key="JavaBackend.*")  # JavaBackend.*


def topic_callback(ch, method, properties, body):
    print(method)
    print(f" [x] {method.routing_key}: {body.decode('ascii')}")


channel.basic_consume(queue=queue_name, on_message_callback=topic_callback, auto_ack=True)

print(' [*] Waiting for logs. To exit press CTRL+C')
channel.start_consuming()

