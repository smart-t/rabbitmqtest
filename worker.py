#!/usr/bin/env python
import os
import pika
import time

# Set the connection parameters to connect to rabbit-server1 on port 5672
# on the / virtual host using the username "rabbitx" and password environ['RMQ_SECRET']
credentials = pika.PlainCredentials('rabbitx', os.environ['RMQ_SECRET'])
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

# prefetch count will prevent a working thread to accept new work
# when working on a task allready.
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='task_queue')

channel.start_consuming()