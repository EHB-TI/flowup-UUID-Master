import pytest, sys, os,pymysql, docker, os.path

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