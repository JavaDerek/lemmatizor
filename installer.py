import io
import os
import yaml
import boto3
import subprocess

def getQueueName(y):
    print('getting service name')
    return y["queues"]["words_name"]

def getLemmasQueueName(y):
    print('getting lemmas queue name')
    return y["queues"]["lemmas_name"]

def getFunctionName(y):
    print('getting function name')
    return y["function_name"]
    
def main():

    command = 'rm -rf ./mystem-mac;'
    subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

    stream = open('config.yaml', 'r')
    y = yaml.load(stream)
    stream.close()

    queueName = getQueueName(y)
    lemmasQueueName = getLemmasQueueName(y)
    functionName = getFunctionName(y)

    print(functionName)

    client = boto3.resource('sqs', region_name='us-east-1')

    try:
        lemmas_queue = client.get_queue_by_name(QueueName=lemmasQueueName)
    except:
        lemmas_queue = client.create_queue(QueueName=lemmasQueueName)

    cl = boto3.client('sqs', region_name='us-east-1')
    response = cl.get_queue_url(QueueName=lemmasQueueName)
    qu = response['QueueUrl']
    y['environment_variables']['lemmaQueues'] = qu
    
    stream = open('config.yaml', 'w')
    stream.write(yaml.dump(y))
    stream.close()

    try:
        queue = client.get_queue_by_name(QueueName=queueName)
    except:
        queue = client.create_queue(QueueName=queueName)

    arn = queue.attributes.get('QueueArn')

    lmb = boto3.client('lambda', region_name='us-east-1')

    response = lmb.list_event_source_mappings(
        EventSourceArn=arn,
        FunctionName=functionName
    )

    if (response["EventSourceMappings"]==[]):
        response = lmb.create_event_source_mapping(
            EventSourceArn=arn,
            FunctionName=functionName)
        print(response)

if __name__ == '__main__':
    main()