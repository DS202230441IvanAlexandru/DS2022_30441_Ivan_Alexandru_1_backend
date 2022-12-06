import csv
import datetime
import json
import sched
import time
import pika
import environ

# Reading the device_id from the configuration file
env = environ.Env()
environ.Env.read_env()

# Setting up the scheduler
scheduler = sched.scheduler(time.time,
                            time.sleep)

# Setting up the connection to RabbitMQ
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='sensors')

# Getting the deviceId from the configuration file
deviceId = env('DEVICE_ID')
speed = env('SPEED')


def publish(body):
    channel.basic_publish(exchange='',
                          routing_key='sensors',
                          body=body)
    print("sent")


def send_message(value):
    print("I read: " + value)
    timestamp = datetime.datetime.now().timestamp()
    data = {"timestamp": timestamp,
            "device_id": deviceId,
            "measurement_value": value
            }
    json_data = json.dumps(data)
    publish(json_data)


def read_csv():
    file = open('sensor.csv')
    csvreader = csv.reader(file)

    data = []
    for row in csvreader:
        data.append(row)

    return data


def main():
    data = read_csv()
    for i in range(0, len(data)):
        delay = i * speed
        scheduler.enter(delay, 1, send_message, (data[i][0],))
    scheduler.run()


main()
