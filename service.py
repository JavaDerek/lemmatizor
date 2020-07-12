# -*- coding: utf-8 -*-
import nltk
import subprocess
import platform
import boto3
import os
import json
#--------#

from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
from kafka import KafkaProducer

if (platform.system() == 'Darwin'):
    mystem = Mystem(mystem_bin='./mystem-mac')
else:
    #Create lemmatizer and stopwords list
    command = 'cp ./mystem /tmp/mystem; chmod 755 /tmp/mystem;'
    subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    mystem = Mystem(mystem_bin='/tmp/mystem') 
    
russian_stopwords = stopwords.words("russian")

def tokenize(event):
    tmp1 = mystem.lemmatize(event.get('text').lower())
    tmp2 = [token for token in tmp1 if token not in russian_stopwords\
              and token != " " \
              and token.strip() not in punctuation]

    # the next line is supposed to de-dupe our list
    return list(set(tmp2))

def handler(event, context):
    # Your code goes here!
    tokens = tokenize(event)

    # Send the SQS message
    print("writing to queue")
    env = os.environ.copy()
    sqs_queue_url = env.get("lemmaQueues", '')
    if (len(sqs_queue_url) > 0):
        sqs_client = boto3.client('sqs')
        sqs_client.send_message(QueueUrl=sqs_queue_url,
                                        MessageBody=json.dumps(tokens))
    
    return tokens