import os
from flask import Flask, jsonify,request,Response
from requests import get
import requests
import random

from HashMap import ConsistentHashMap


hash_map=ConsistentHashMap()

app = Flask(__name__)


@app.route('/rep', methods=['GET'])
def rep():
    return jsonify({"message" : {"N" : len(hash_map.servers),"replicas" : hash_map.get_server_names()} ,"status" : "successful"})

@app.route('/add', methods=['POST'])
def add():
    json_data = request.get_json()
    print('add',json_data)
    result=hash_map.add_server(json_data['n'],json_data['hostnames'])
    return jsonify(result)



@app.route('/add_test', methods=['POST'])
def add_test():
    json_data     = request.get_json()
    print(json_data)
    n=json_data['n']
    hostnames=json_data['hostnames']
    error=False
    if n == len(hostnames):
            for hostname in hostnames:
                if hostname in hash_map.get_server_names():
                    port=hash_map.new_available_port()
                    new_hostname=hash_map.new_random_server_name()
                    print('docker run --name {} -e port={} -e ID={} -d master_flask_copy:latest'.format(new_hostname,port,len(hash_map.servers)+1))
                    res=os.popen("docker run --name {} -e port={} -e ID={} -d master_flask_copy:latest".format(new_hostname,port,len(hash_map.servers)+1)).read()
                    if len(res)==0:
                        print("Unable to start test_container")
                        error=True
                    else:
                        print("successfully started test_container")
                        hash_map.servers.append({'id':len(hash_map.servers)+1,'name':new_hostname,'port':port})
                else:
                    port=hash_map.new_available_port()
                    hash_map.servers.append({'id':len(hash_map.servers)+1,'name':hostname,'port':port})
            #return {'message':{'N':len(hash_map.servers),'replicas':hash_map.get_server_names()},"status":'successful' if error==False else 'failed'}
    
    # res=os.popen("docker run -p 5002:5002 --name test_container -e port=5002 -e ID=1 -d master_flask_copy:latest").read()
    # if len(res)==0:
    #     print("Unable to start test_container")
    # else:
    #     print("successfully started test_container")
    return jsonify({'message':{"N" : len(hash_map.servers),"replicas" : hash_map.get_server_names()},"status" : 'successful' if error==False else 'failed'})



@app.route('/rm', methods=['POST'])
def rm():
    json_data     = request.get_json()
    print(json_data)
    result=hash_map.remove_server(json_data['n'],json_data['hostname'])
    return jsonify(result)


@app.route('/<path>')
def proxy1(path):
    print(request.cookies.get('server_id'))
    if(request.cookies.get('server_id')==None):
        print('Rerouting to the next slot alocatable')
    else:
        print('Rerouting to the same ')


    #Call the hash map here
    server=hash_map.next_server()
    print(server)


    res = requests.request(
        method          = request.method,
        url             = request.url.replace(request.host_url, 'http://host.docker.internal:{}/'.format(server['port'])),
        headers         = {k:v for k,v in request.headers if k.lower() != 'host'},
        data            = request.get_data(),
        cookies         = request.cookies,
        allow_redirects = False,
    )
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']  
    headers          = [
        (k,v) for k,v in res.raw.headers.items()
        if k.lower() not in excluded_headers
    ]
    response = Response(res.content, res.status_code, headers)
    response.set_cookie('server_id','0')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
