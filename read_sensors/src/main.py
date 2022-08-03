import json
import os
import pika
import random
import smbus
import socket
import ssl
import time
from dotenv import load_dotenv 


context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#context.verify_mode = ssl.CERT_REQUIRED
context.verify_mode = ssl.CERT_NONE
#node1 = pika.URLParameters('amqps://hub1.ise.fraunhofer.de/tg?verify=verify_none')
#node2 = pika.URLParameters('amqps://hub2.ise.fraunhofer.de/tg?verify=verify_none')
#node3 = pika.URLParameters('amqps://hub3.ise.fraunhofer.de/tg?verify=verify_none')
#rmq_endpoints = [node1, node2, node3]
#random.shuffle(rmq_endpoints)
load_dotenv()



def read_hyt(address = 0x28, bus = 1, delay=0.05):
    bus = smbus.SMBus(bus) # use /dev/i2c1
    bus.write_byte(address, 0x00) # send some stuff
    time.sleep(delay) # wait a bit
    # read 4 bytes for humidity and temperature
    datastream = bus.read_i2c_block_data(address, 0x00, 4) # read the bytes
    # Humidity is in the first two bits
    humidity = ((datastream[0] & 0x3F) * 0x100 + datastream[1]) * (100.0 / 16383.0)
    # temperature is in the last two bitesss
    temperature = 165.0 / 16383.0 * ((datastream[2] * 0x100 + (datastream[3] & 0xFC)) >> 2) - 40
    return humidity, temperature

def send_data(serverlist, user, password, topic, exchange):
    rh, t = read_hyt()
    data = {'dt': time.time(), 'rh': rh, 't': t, 'sensor': socket.gethostname()}
    credentials = pika.PlainCredentials(user, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="hub2.ise.fraunhofer.de", port=5671, virtual_host="tg",credentials=credentials, ssl_options=pika.SSLOptions(context)))
    channel = connection.channel()
    channel.exchange_declare(exchange='topic_ambient', exchange_type='topic', durable=True)
    channel.basic_publish(exchange='topic_ambient',
                      routing_key='ambient.wetter01',
                      body=json.dumps(data))

if __name__ == '__main__':
    send_data(serverlist=[], user=os.getenv('RMQ_USER'), password=os.getenv('RMQ_PASSWORD'), topic=os.getenv('RMQ_TOPIC'), exchange=os.getenv('RMQ_EXCHANGE'))
