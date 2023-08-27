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




def defineDevice(num,type,array,port):
    for i in range(num):
        add_device=deviceObject(type+str(i),type+" "+str(i), "device")
        definePort(add_device,port, "fa")
        array.append(add_device)
        
        


def connect(source,target,portDevice):
    for portSource in list(source.switchPorts.keys()):
            if (source.switchPorts[portSource]==False):
                portTarget = list(target.switchPorts.keys())[0]
                if (target.switchPorts[portTarget]==False):
                    new_port=portObject(source.data,target.data,portSource,portTarget)
                    portDevice.append(new_port)
                    source.switchPorts[portSource]=True
                    source.connected +=1
                    target.switchPorts[portTarget]=True
                    target.connected +=1
                    break
                
def createPortObject(port_array, source_devices, target_devices):
    for target in target_devices:
        for source in source_devices:
            connect(source,target,port_array)



def main():
    #data input
    pcNum=2
    printerNum=4
    wifiNum=2
    sum=pcNum+printerNum+wifiNum
    accSwt_num=ceil(sum/23)
    
    portDevice = []
    accessDevice=[]
    router=[]
    portDevice = []
    accessSwitch=[]

    
    defineDevice(pcNum,"pc",accessDevice,3)
    defineDevice(printerNum,"printer",accessDevice,3)
    defineDevice(wifiNum,"wifi",accessDevice,3)

    defineDevice(accSwt_num,"accessSwt",accessSwitch,24)

    #define Router port
    add_router=deviceObject("router","Router","router")
    router.append(add_router)
    definePort(router[0],2,"Gi")
    
    createPortObject(portDevice, router, accessSwitch)
    createPortObject(portDevice, accessSwitch, accessDevice)
    networkDevice = accessDevice + accessSwitch  + router
    return networkDevice, portDevice
    
main()



    
