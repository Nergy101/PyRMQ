import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
direct_channel = connection.channel()


direct_channel.exchange_declare(exchange='messages', exchange_type='direct')

result = direct_channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

direct_channel.queue_bind(
        exchange='messages', queue=queue_name, routing_key="red")
direct_channel.queue_bind(
        exchange='messages', queue=queue_name, routing_key="white")

def direct_callback(ch, method, properties, body):
    # print(method)
    if method.routing_key == "red":
        print("RED")
        print(body)
    if method.routing_key == "white":
        print("WHITE")
    if method.routing_key == "blue":
        print("BLUE")
    # print(f" [x] {method.routing_key}:{body}")


direct_channel.basic_consume(queue=queue_name, on_message_callback=direct_callback, auto_ack=True)

print(' [*] Waiting for logs. To exit press CTRL+C')
direct_channel.start_consuming()

