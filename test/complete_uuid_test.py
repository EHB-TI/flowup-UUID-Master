import pika, pytest, sys, os,pymysql, docker, os.path

#mysql-connectivity-test
def test_mysql_connectivity():
    db = pymysql.connect(host='localhost',user='testing',passwd='toor')
    cursor = db.cursor()
    query = ("SHOW DATABASES")
    cursor.execute(query)
    for r in cursor:
        assert r != None

#containers-test
def test_runningcontainers():
    client = docker.from_env()
    if client.containers.list(all=True):
        assert len(client.containers.list(all=True)) >= 2
    else:
        assert False



def test_env_isExists():
    assert os.path.isfile('.env')

#yaml-tests
def test_yaml():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filepaths = []  
    for root, dirs, files in os.walk(dir_path):
        for file in files: 
            if file.endswith('.yml'):
                filepaths.append(root+'/'+str(file))

    for fp in filepaths:
        # Split the extension from the path and normalise it to lowercase.
        ext = os.path.splitext(fp)[-1].lower()
        assert ext == ".yml"    



#rabbitmq-tests
QUEUE_MONITORING = 'QUEUE_MONITORING'
RABBITMQ_HOST = 'localhost'

def test_rabbitmq_publish():   
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    assert channel != None
    channel.queue_declare(queue=QUEUE_MONITORING)
    channel.basic_publish(exchange='', routing_key=QUEUE_MONITORING, body='Hello!') 
    connection.close()

def test_rabbitmq_consume():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    for method_frame, properties, body in channel.consume(QUEUE_MONITORING):
        channel.basic_ack(method_frame.delivery_tag)
        assert body != None    
        if method_frame.delivery_tag == 1:
            break

    requeued_messages = channel.cancel()
    channel.close()
    connection.close()

def test_rabbitmq_connectivity():
    # Check connectivity for management platform
    URL = 'amqp://guest:guest@localhost:5672/%2F'
    parameters = pika.URLParameters(URL)
    try:
        connection = pika.BlockingConnection(parameters)
        assert connection.is_open
            
    except Exception as error:
        assert False