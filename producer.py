import sys
import os
import json
from bson import json_util
from confluent_kafka import Producer

# Params
nome = sys.argv[1] + " " + sys.argv[2] 
email = sys.argv[3]
telefone = sys.argv[4]
checkin = sys.argv[5]
pax = sys.argv[6] 
destino = sys.argv[7]

for i in range(9):
    data = {'nome': nome,
        'email' : email,
        'telefone' : telefone,
        'checkin' : checkin,
        'pax' : pax,
        'destino': destino
    }   

def delivery_callback(err, msg):
    if err:
        print(err)
    else:
        print('Orders delivered!')

def createTopic():
    print("init")
    topic = 'ezvjbeie-default'

    conf = {
        'bootstrap.servers': 'glider.srvs.cloudkafka.com:9094',
        'session.timeout.ms': 6000,
        'default.topic.config': {'auto.offset.reset': 'smallest'},
        'security.protocol': 'SASL_SSL',
	    'sasl.mechanisms': 'SCRAM-SHA-512',
        'sasl.username': 'ezvjbeie', #os.getenv('KAFKA_USER'),
        'sasl.password': 'JA3HCWSxJk2WDHEKidFlEyZ_yt5grzIs' #os.getenv('KAFKA_PASSWORD')
    }

    p = Producer(conf)

    try:
        p.produce(topic, 'orders', json.dumps(data, default=json_util.default).encode('utf-8'), callback=delivery_callback)
    except BufferError as e:
        print('Local producer queue is full, awaiting delivery. Try again')
        
    p.poll(0)

    print('Waiting for delivery...')
    p.flush()

createTopic()