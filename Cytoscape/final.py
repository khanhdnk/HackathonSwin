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


#Create portObject with source, target are distionary (data of deviceObject), *label are strings
class portObject:
    def __init__(self,source, target, sourceLabel, targetLabel):
        self.data = {
            "id": source.id + "-" + target.id,
            "source": source["id"],
            "target": target["id"]
        }
        self.style = {
            "sourceLabel": sourceLabel,
            "targeLabel": targetLabel
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
i=0
while i < len(vlan)-1:
    if (vlan[i].host+vlan[i+1].host<24-ceil(len(vlan)/2)):
        newVlan=Vlan(vlan[i].host+vlan[i+1].host,
                        vlan[i].id + "+" + vlan[i+1].id,
                        vlan[i].name,
                        "",
                        []
        )
        vlan.append(newVlan)
        vlan.pop(i)
        vlan.pop(i)
        sortVlan(vlan)
    else: i=i+1

accSwt_num=len(vlan)
distSwt_num=ceil(accSwt_num/2)
coreSwt_num=ceil(distSwt_num/3)










