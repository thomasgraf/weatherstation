#!/usr/bin/env python
import datetime, pika, ssl, sys, os, json
from dotenv import load_dotenv
import psycopg2

load_dotenv()

CONNECTION = "postgres://%s:%s@%s:%s/%s" % (os.getenv('PSQL_USER'), os.getenv('PSQL_PASSWORD'), os.getenv('PSQL_HOST'), os.getenv('PSQL_PORT'), os.getenv('PSQL_DATABASE'))

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#context.verify_mode = ssl.CERT_REQUIRED
context.verify_mode = ssl.CERT_NONE
#node1 = pika.URLParameters('amqps://hub1.ise.fraunhofer.de/tg?verify=verify_none')
#node2 = pika.URLParameters('amqps://hub2.ise.fraunhofer.de/tg?verify=verify_none')
#node3 = pika.URLParameters('amqps://hub3.ise.fraunhofer.de/tg?verify=verify_none')
#rmq_endpoints = [node1, node2, node3]
#random.shuffle(rmq_endpoints)



def main():
    credentials = pika.PlainCredentials(os.getenv('RMQ_USER'), os.getenv('RMQ_PASSWORD'))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RMQ_HOST'), port=os.getenv('RMQ_PORT'), virtual_host=os.getenv('RMQ_VHOST'),credentials=credentials, ssl_options=pika.SSLOptions(context)))
    
    channel = connection.channel()

    channel.queue_declare(queue=os.getenv('RMQ_QUEUE'), passive=True)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        data = json.loads(body)
        with psycopg2.connect(CONNECTION) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ambientdata (dt, sensor, humidity, temperature) VALUES (%s, %s, %s, %s);",
                (datetime.datetime.fromtimestamp(data['dt']), data['sensor'],data['rh'],data['t'],))

    channel.basic_consume(queue=os.getenv('RMQ_QUEUE'), on_message_callback=callback, auto_ack=False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

