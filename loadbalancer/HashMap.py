import math
import random
import os



# Consistent Hashing Class
class ConsistentHashMap(object):
    def __init__(self):
        self.servers = [{'id':0,'port':5001,'name':'origin'}] #It holds a list of dicts; {hostname:port}, id is the index value
        self.current_server=0

    def get_server_names(self):
        my_result=[]
        for server in self.servers:
            my_result.append(server['name']) 
        return my_result

    def get_server_ports(self):
        my_result=[]
        if len(self.servers)>0:
            for server in self.servers:
                my_result.append(server['port']) 
            return my_result
        else:
            my_result.append(5000)
            return my_result
    
    def new_available_port(self):
        new_port=5000
        while True:
            ports=self.get_server_ports()
            ports.sort()
            last_port=ports[-1]
            new_port=last_port+1
            if new_port not in self.get_server_ports():
                break
        return new_port
    
    def new_random_server_name(self):
        new_name=''
        while True:
            new_name='untitled_{}'.format(random.randrange(1,512,1))
            if new_name not in self.get_server_names():
                break
        return new_name
    

    
    def add_server(self,n,hostnames):
        error=False
        if n == len(hostnames):
            for hostname in hostnames:
                if hostname in self.get_server_names():
                    port=  self.new_available_port()
                    new_hostname= self.new_random_server_name()
                    print('docker run --name {} -e port={} -e ID={}  -d master_flask_copy:latest'.format(new_hostname,port,len(self.servers)+1))
                    res=os.popen("docker run --name {} -p {}:{} -e port={} -e ID={} --network=a0_default -d master_flask_copy:latest".format(new_hostname,port,port,port,len(self.servers)+1)).read()
                    if len(res)==0:
                        print("Unable to start test_container")
                        error=True
                    else:
                        print("successfully started test_container")
                        self.servers.append({'id':len(self.servers)+1,'name':new_hostname,'port':port})
                else:
                    port= self.new_available_port()
                    print('docker run --name {} -e port={} -e ID={} -d master_flask_copy:latest'.format(hostname,port,len(self.servers)+1))
                    res=os.popen("docker run --name {} -p {}:{} -e port={} -e ID={} --network=a0_default -d master_flask_copy:latest".format(hostname,port,port,port,len(self.servers)+1)).read()
                    if len(res)==0:
                        print("Unable to start test_container")
                        error=True
                    else:
                        print("successfully started test_container")
                        self.servers.append({'id':len(self.servers)+1,'name':hostname,'port':port})
        
            return {'message':{'N':len(self.servers),'replicas':self.get_server_names()},"status":'successful' if error==False else 'failed'}
        
        
        elif n>len(hostnames):
            extra_servers=n-len(hostnames)
            print('extra:{} servers'.format(extra_servers))

            for hostname in hostnames:
                if hostname in self.get_server_names():
                    port= self.new_available_port()
                    new_hostname= self.new_random_server_name()
                    print('docker run --name {} -e port={} -e ID={} --network=a0_default -d master_flask_copy:latest'.format(new_hostname,port,len(self.servers)+1))
                    res=os.popen("docker run --name {} -p {}:{} -e port={} -e ID={} --network=a0_default -d master_flask_copy:latest".format(new_hostname,port,port,port,len(self.servers)+1)).read()
                    if len(res)==0:
                        print("Unable to start test_container")
                        error=True
                    else:
                        print("successfully started test_container")
                        self.servers.append({'id':len(self.servers)+1,'name':new_hostname,'port':port})
                else:
                    port=self.new_available_port()
                    print('docker run --name {} -e port={} -e ID={} -d master_flask_copy:latest'.format(hostname,port,len(self.servers)+1))
                    res=os.popen("docker run --name {} -p {}:{} -e port={} -e ID={} --network=a0_default -d master_flask_copy:latest".format(new_hostname,port,port,port,len(self.servers)+1)).read()
                    if len(res)==0:
                        print("Unable to start test_container")
                        error=True
                    else:
                        print("successfully started test_container")
                        self.servers.append({'id':len(self.servers)+1,'name':hostname,'port':port})



            for i in range(0,extra_servers,1):
                port=self.new_available_port()
                new_hostname=self.new_random_server_name()
                print('docker run --name {} -e port={} -e ID={} -d master_flask_copy:latest'.format(new_hostname,port,len(self.servers)+1))
                res=os.popen("docker run --name {} -p {}:{} -e port={} -e ID={} --network=a0_default -d master_flask_copy:latest".format(new_hostname,port,port,port,len(self.servers)+1)).read()
                if len(res)==0:
                    print("Unable to start test_container")
                    error=True
                else:
                    print("successfully started test_container")
                    self.servers.append({'id':len(self.servers)+1,'name':new_hostname,'port':port})
            
            return {'message':{'N':len(self.servers),'replicas':self.get_server_names()},"status":'successful' if error==False else 'failed'}
        
        elif n<len(hostnames):
            return "Error"
    

    
    def next_server(self):
        next_server_id=self.current_server+1
        if(next_server_id==len(self.servers)):
            next_server_id=0
            self.current_server=next_server_id
            return self.servers[self.current_server]
        else:
            self.current_server=next_server_id
            return self.servers[self.current_server]

    def remove_server(self,n,hostnames):
        error=False
        error_statement=''
        if n == len(hostnames):
            for hostname in hostnames:
                if hostname in self.get_server_names():
                    #Get the index of that server and try to remove it
                    i=self.get_server_names().index(hostname)
                    print('Removing;{}'.format(self.servers[i]))
                    try:
                        os.system('docker stop {} && docker rm {}'.format(self.servers[i]['name'],self.servers[i]['name']))
                        self.servers.pop(i)
                    except Exception as e:
                        print('Error trying to close container:'+str(e))
                        error = True
                        error_statement=str(e)
                    
                else:
                    #Get a random server and remove it
                    random_index=random.randrange(0,len(self.servers))
                    print('Removing;{}'.format(self.servers[i]))
                    try:
                        os.system('docker stop {} && docker rm {}'.format(self.servers[i]['name'],self.servers[i]['name']))
                        self.servers.pop(i)
                    except Exception as e:
                        print('Error trying to close container:'+e)
                        error_statement=str(e)
                        error = True
            return {'message':{'N':len(self.servers),'replicas':self.get_server_names()},"status":'successful' if error==False else 'failed', 'error':error_statement if error else None }
        

        
        elif n>len(hostnames):
            extra_servers=n-len(hostnames)
            print('extra:{} servers'.format(extra_servers))

            for hostname in hostnames:
                if hostname in self.get_server_names():
                    #Get the index of that server and try to remove it
                    i=self.get_server_names().index(hostname)
                    print('Removing;{}'.format(self.servers[i]))
                    try:
                        os.system('docker stop {} && docker rm {}'.format(self.servers[i]['name'],self.servers[i]['name']))
                        self.servers.pop(i)
                    except Exception as e:
                        print('Error trying to close container:'+str(e))
                        error = True
                        error_statement=str(e)
                else:
                    #Get a random server and remove it
                    random_index=random.randrange(0,len(self.servers))
                    print('Removing;{}'.format(self.servers[i]))
                    i=random_index
                    try:
                        os.system('docker stop {} && docker rm {}'.format(self.servers[i]['name'],self.servers[i]['name']))
                        self.servers.pop(i)
                    except Exception as e:
                        print('Error trying to close container:'+str(e))
                        error = True
                        error_statement=str(e)

            for i in range(0,extra_servers,1):
                #Get a random server and remove it
                random_index=random.randrange(0,len(self.servers))
                i=random_index
                print('Removing;{}'.format(self.servers[i]))
                try:
                    os.system('docker stop {} && docker rm {}'.format(self.servers[i]['name'],self.servers[i]['name']))
                    self.servers.pop(i)
                except Exception as e:
                    print('Error trying to close container:'+str(e))
                    error = True
                    error_statement=str(e)
            
            return {'message':{'N':len(self.servers),'replicas':self.get_server_names()},"status":'successful'}
        
        elif n<len(hostnames):
            return "Error"

            
            
        


    