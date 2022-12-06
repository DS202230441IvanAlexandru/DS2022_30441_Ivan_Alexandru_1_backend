import asyncio
import json
import websockets
import pika
import django
from os import environ


async def send_notification(client_id, device_name, max_hourly_consumption):
    print(client_id)
    async with websockets.connect(f'ws://127.0.0.1:8000/ws/user/{client_id}/') as websocket:
        await websocket.send(
            f"The device {device_name} has exceeded its maximum hourly consumption of {max_hourly_consumption}kW!")
        response = await websocket.recv()
        print(response)


def start_consumer():
    print("started")
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='sensors')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        obj = json.loads(body)
        measurement = float(obj["measurement_value"])
        deviceId = int(obj["device_id"])

        consumption = Consumption()
        consumption.consumption = measurement
        userDevice = UserDevice.objects.filter(device_id_id=deviceId).first()

        if not userDevice:
            return

        consumption.user_device_id = userDevice
        consumption.save()

        consumptions = Consumption.objects.all().filter(user_device_id=userDevice.id)
        device = Device.objects.filter(id=deviceId).first()
        print(device.consumption)

        lastHourConsumption = measurement
        if len(consumptions) >= 6:
            lastHourConsumption -= consumptions[len(consumptions) - 6].consumption

        if lastHourConsumption >= device.consumption:
            print("BIGGER")
            asyncio.run(send_notification(userDevice.user_id.id, device.name, device.consumption))
        else:
            print("ITS OKE")

    channel.basic_consume(queue='sensors', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    environ.setdefault('DJANGO_SETTINGS_MODULE', 'EUP_backend.settings')
    django.setup()
    from backend.models import Consumption, UserDevice, Device

    start_consumer()
