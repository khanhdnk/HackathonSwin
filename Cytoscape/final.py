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


class Vlan:
    def __init__(self, host, id, name, switch, switchport):
        self.host = host
        self.id = id
        self.name = name
        self.port = {
            "switch": switch,
            "switchport": switchport
        }

#funtion to sort vlan ascending based on host value
def sortVlan(vlan):
    for x in range(0,len(vlan)-1):
        for y in range(x+1,len(vlan)):
            if vlan[x].host > vlan[y].host:
                vlan_tg=vlan[x]
                vlan[x]=vlan[y]
                vlan[y]=vlan_tg

#Data input here
vlan0 = Vlan(12,"vlan0","An","",[])
vlan1= Vlan(13,"vlan1","Anal","", [])
vlan2= Vlan(14,"vlan2","Analyst","",[])
vlan = [vlan0,vlan1,vlan2]
#--------------

sortVlan(vlan)
i=0


#Split vlan which has big value host
while i < len(vlan):    
    if vlan[i].host>(24-ceil(len(vlan)/2)):
        numSplit=ceil((25-len(vlan)-sqrt((25-len(vlan))**2-4*vlan[i].host))/2)
        newHost=24-len(vlan)-numSplit+1
        for j in range(numSplit-1):
            newVlan=Vlan(newHost,
                        vlan[i].id + "_" + str(j),
                        vlan[i].name,
                        "",
                        []
            )
            vlan.append(newVlan)
        newVlan =Vlan(vlan[i].host-newHost*(numSplit-1),
                        vlan[i].id + "_" + str(numSplit-1),
                        vlan[i].name,
                        "",
                        []
        )
        vlan.append(newVlan)
        vlan.pop(i)
        
    else: i=i+1


sortVlan(vlan)

#Merge vlan which has small value host
i=0
while i < len(vlan)-1:
    if (vlan[i].host+vlan[i+1].host<24-ceil(len(vlan)/2)):
        newVlan=Vlan(vlan[i].host+vlan[i+1].host,
                        vlan[i].id + "+" + vlan[i+1].id,
                        vlan[i].name,
                        "",
                        {}
        )
        vlan.append(newVlan)
        vlan.pop(i)
        vlan.pop(i)
        sortVlan(vlan)
    else: i=i+1

#Caculated number of Switch, Dist, Core
accSwt_num=len(vlan)
distSwt_num=ceil(accSwt_num/2)
coreSwt_num=ceil(distSwt_num/3)
#____________


coreDevice=[]
distDevice=[]
accessDevice=[]
router=[]
i=0

#function to define name and value port of deviceObject
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



#Group and define Switch  
for i in range(accSwt_num):
    add_access=deviceObject("accessSwt"+str(i),"Access Switch "+ str(i), "access")
    accessDevice.append(add_access)
    definePort(accessDevice[i], 24, "fa")

#Group and define Dist 
for i in range(distSwt_num):
    add_dist=deviceObject("distSwt"+str(i),"Distribution Switch "+ str(i), "distribution")
    distDevice.append(add_dist)
    definePort(distDevice[i],24,"Gi")

#Group and define Core 
for i in range(coreSwt_num):
    add_core=deviceObject("coreSwt"+str(i),"Core Switch "+ str(i), "core")
    coreDevice.append(add_core)
    definePort(coreDevice[i],24,"Gi")

#define Router port
add_router=deviceObject("router","Router","router")
router.append(add_router)
definePort(router[0],2,"Gi")


#Connect Router - Core
portDevice = []
for rt in router:
    for core in coreDevice:
        for portSource in list(rt.switchPorts.keys()):
            if (rt.switchPorts[portSource]==False):
                portTarget = list(core.switchPorts.keys())[list(rt.switchPorts.keys()).index(portSource)]
                if (core.switchPorts[portTarget]==False):
                    new_port=portObject(rt.data,core.data,portSource,portTarget)
                    portDevice.append(new_port)
                    rt.switchPorts[portSource]=True
                    rt.connected +=1
                    core.switchPorts[portTarget]=True
                    core.connected +=1
                    break


#Connect Core - Dist
for core in coreDevice:
    for dist in distDevice:
        for portSource in list(core.switchPorts.keys()):
            if (core.switchPorts[portSource]==False):
                portTarget= list(dist.switchPorts.keys())[list(core.switchPorts.keys()).index(portSource)]
                if (dist.switchPorts[portTarget]==False):
                    new_port=portObject(core.data,dist.data,portSource,portTarget)
                    portDevice.append(new_port)
                    core.switchPorts[portSource]=True
                    core.connected +=1
                    dist.switchPorts[portTarget]=True
                    dist.connected +=1
                    break

#Connect Dist - Access Switch
count=0
for dist in distDevice:
    for access in accessDevice:
        for portSource in list(dist.switchPorts.keys()):
            if (dist.switchPorts[portSource]==False):
                portTarget= list(access.switchPorts.keys())[count]
                if (access.switchPorts[portTarget]==False):
                    new_port=portObject(dist.data,access.data,portSource,portTarget)
                    portDevice.append(new_port)
                    dist.switchPorts[portSource]=True
                    dist.connected +=1
                    access.switchPorts[portTarget]=True
                    access.connected +=1
                    break
    count+=1  


#Connect 1 Vlan to 1 Access Switch 
for VLAN in vlan:
    portIndex=0
    check = False
    for access in accessDevice:
        if (VLAN.host<=24-access.connected):
            for i in range(VLAN.host):
                for port in access.switchPorts:
                    if (access.switchPorts[port]==False):
                        VLAN.port["switch"]=access.data["id"]
                        portIndex+=1
                        VLAN.port["switchport"].append(portIndex)
                        access.switchPorts[port]=True
                        access.connected += 1
                        break
            check=True
        if (check==True):
            break

#Define port connect Access Switch to Vlan    
for VLAN in vlan:
    labelTarget = ""
    startPort=""
    endPort=""
    for accdv in accessDevice:
        if (VLAN.port["switch"] == accdv.data["id"]):
            startPort = list(access.switchPorts.keys())[distSwt_num]
            endPort = list(access.switchPorts.keys())[distSwt_num+VLAN.host-1]
            if (endPort.find("fa")!=-1):
                labelTarget = startPort+ "-" + endPort[4:]
            if (endPort.find("Gi")!=-1):
                labelTarget = startPort + "-" + endPort[6:] 
            new_port=portObject(accdv.data,{"id": VLAN.id},labelTarget,"Ethernet" )
            portDevice.append(new_port)













