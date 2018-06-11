#!/usr/bin/env python
import os
import pika
import sys

# Set the connection parameters to connect to rabbit-server1 on port 5672
# on the / virtual host using the username "rabbitx" and password environ['RMQ_SECRET']
credentials = pika.PlainCredentials('rabbitx', os.environ['RMQ_SECRET'])
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
print(" [x] Sent %r" % message)
connection.close()