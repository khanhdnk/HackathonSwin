from math import *


class deviceObject:
    def __init__(self, id, label, layer):
        self.data = {
            "id": id,
            "label": label,
            "layer": layer
        }
        self.switchPorts = {}
        self.connected = 0



class portObject:
    def __init__(self,source, target, sourceLabel, targetLabel):
        self.data = {
            "id": source["id"] + "-" + target["id"],
            "source": source["id"],
            "target": target["id"]
        }
        self.style = {
            "sourceLabel": sourceLabel,
            "targetLabel": targetLabel
        }


def definePort(source, numPort, typePort):
    counter=1
    octet=0
    for i in range(numPort):
        if (counter>24):
            octet+=1
            counter=1
        if (typePort=="Gi"):
            portLabel=typePort+"1/"+str(octet)+"/"+str(counter)
        else: 
            if (typePort=="fa"):
                portLabel= typePort+str(octet)+"/"+str(counter)
        counter+=1
        source.switchPorts[portLabel]=False


#data input
pcNum=3
printerNum=2
wifiNum=2
portDevice = []
accessDevice=[]
router=[]
sum=pcNum+printerNum+wifiNum
accessSwitch=[]
accSwt_num=ceil(sum/23)
#define Device
for i in range(pcNum):
    add_device=deviceObject("pc"+str(i),"PC "+str(i), "device")
    definePort(add_device,3, "fa")
    accessDevice.append(add_device)
    

for i in range(printerNum):
    add_device=deviceObject("printer"+str(i),"Printer "+str(i), "device")
    definePort(add_device,3, "fa")
    accessDevice.append(add_device)

for i in range(wifiNum):
    add_device=deviceObject("wifi"+str(i),"Wifi "+str(i), "device")
    definePort(add_device,3, "fa")
    accessDevice.append(add_device)

#define Switch
for i in range(accSwt_num):
    add_switch=deviceObject("accessSwt"+str(i),"Access Switch "+str(i), "access")
    definePort(add_switch,24, "fa")
    accessSwitch.append(add_switch)

#define Router port
add_router=deviceObject("router","Router","router")
router.append(add_router)
definePort(router[0],2,"Gi")


#Connect Router - Switch
portDevice = []
for rt in router:
    for access in accessSwitch:
        for portSource in list(rt.switchPorts.keys()):
            if (rt.switchPorts[portSource]==False):
                portTarget = list(access.switchPorts.keys())[list(rt.switchPorts.keys()).index(portSource)]
                if (access.switchPorts[portTarget]==False):
                    new_port=portObject(rt.data,access.data,portSource,portTarget)
                    portDevice.append(new_port)
                    rt.switchPorts[portSource]=True
                    rt.connected +=1
                    access.switchPorts[portTarget]=True
                    access.connected +=1
                    break

#connect Device to Switch
counterDe=0
counterSwt=0

