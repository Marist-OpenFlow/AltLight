#Pushes static flows
#Deletes currents static flows
#Gets current flows

#Zach Meath

import httplib, json

class StaticFlowPusher(object):

    def __init__(self, server):
        self.server = server

    def get(self, data):
        path = '/wm/staticflowentrypusher/list/' + data + '/json'
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request("GET", path)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        ret1 = str(ret)
        print ret1
        x=1
        ret1 = ret1[ret1.find("\":{\"",0)+4:]
        name = ret1[:ret1.find("\"",0)]
        ret1 = ret1[ret1.find("\"port\"",0)-1:]
        outport = ret1[ret1.find(":",0)+1:ret1.find(",",0)]
        ret1 = ret1[ret1.find("\"inputPort\"",0)+11:]
        inport = ret1[1:ret1.find(",")]

        if name == "0, 'OK', '{":
            print "\nNo flows\n"
        else:
        
            print "\n\n"
            print"Flow "+"1"+": " + name
            print "Inport: "+inport
            print "Outport: "+outport
            print "\n"

            while ret1.find("\"port\"",0) != -1:

                ret2 = ret1[:ret1.find("\":{\"actions",0)]
                name = ret2[ret2.rfind("\"",0)+1:]
                ret1 = ret1[ret1.find("\"port\"",0)-1:]
                outport = ret1[ret1.find(":",0)+1:ret1.find(",",0)]
                ret1 = ret1[ret1.find("\"inputPort\"",0)+11:]
                inport = ret1[1:ret1.find(",")]
                x+=1
                
                print "Flow "+str(x)+": " + name
                print "Inport: "+inport
                print "Outport: "+outport
                print "\n"


            
        #print ret1
        conn.close()
        return ret

    def set(self, data):
        ret = self.rest_call(data, 'POST')
        return ret[0] == 200

    def remove(self, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200

    def remove_all(self):
        path = '/wm/staticflowentrypusher/clear/all/json'
        action = 'GET'
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path)
        print "DELETED...\n"
        conn.close()

    def rest_call(self, data, action):
        path = '/wm/staticflowentrypusher/json'
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        print ret
        conn.close()
        return ret

pusher = StaticFlowPusher('10.11.17.20')
##pusher = StaticFlowPusher('192.168.56.1')
text = raw_input("Enter PUSH, DELETE, GET, or QUIT:  \n")

while text.lower() != "quit":
    if text.lower() == "push":
        name = raw_input("Enter a name for the flow:  \n")
        inp = raw_input("Enter an ingress port:  \n")
        a= raw_input("Enter an output port:  \n")
        outp = "output=" + a

        flow1 = {
            'switch':"00:00:00:00:00:00:00:0a",
            "name":name,
            "cookie":"0",
            "priority":"32768",
            "ingress-port":inp,
            "active":"true",
            "actions":outp
            }
        pusher.set(flow1)
    if text.lower() == "delete":
        name1 = raw_input("Enter a name for the flow you wish to delete (\"all\" to delete all flows):  \n")
        if name1.lower() == "all":
            pusher.remove_all()
        else:
            flow1 = {
                'switch':"00:00:00:00:00:00:00:0a",
                "name":name1,
                "cookie":"0",
                "priority":"32768",
                "ingress-port":"1",
                "active":"true",
                "actions":"output=9"
                }
            pusher.remove(flow1)
    if text.lower() == "get":
        pusher.get("all")
    text = raw_input("Enter PUSH, DELETE, GET or QUIT:  \n")
