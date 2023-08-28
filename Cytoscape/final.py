from math import *
import json


class deviceObject:
    def __init__(self, id, label, layer):
        self.data = {"id": id, "label": label, "layer": layer}
        self.switchPorts = {}
        self.connected = 0


class portObject:
    def __init__(self, source, target, sourceLabel, targetLabel):
        self.data = {
            "id": source["id"] + "-" + target["id"],
            "source": source["id"],
            "target": target["id"],
        }
        self.style = {"sourceLabel": sourceLabel, "targetLabel": targetLabel}


class Vlan:
    def __init__(self, host, id, name, switch, switchport):
        self.host = host
        self.id = id
        self.name = name
        self.port = {"switch": switch, "switchport": switchport}


# funtion to sort vlan ascending based on host value
def sortVlan(vlan):
    for x in range(0, len(vlan) - 1):
        for y in range(x + 1, len(vlan)):
            if vlan[x].host > vlan[y].host:
                vlan_tg = vlan[x]
                vlan[x] = vlan[y]
                vlan[y] = vlan_tg
    return vlan


def split_vlan(vlan):
    i = 0
    # Split vlan which has big value host
    while i < len(vlan):
        if vlan[i].host > (24 - ceil(len(vlan) / 2)):
            numSplit = ceil(
                (25 - len(vlan) - sqrt((25 - len(vlan)) ** 2 - 4 * vlan[i].host)) / 2
            )
            newHost = 24 - len(vlan) - numSplit + 1
            for j in range(numSplit - 1):
                newVlan = Vlan(newHost, vlan[i].id + "_" + str(j), vlan[i].name, "", [])
                vlan.append(newVlan)
                newVlan = Vlan(
                    vlan[i].host - newHost * (numSplit - 1),
                    vlan[i].id + "_" + str(numSplit - 1),
                    vlan[i].name,
                    "",
                    [],
                )
            vlan.append(newVlan)
            vlan.pop(i)
        else:
            i = i + 1
    return vlan


# Merge vlan which has small value host
def mergeVlan(vlan):
    i = 0
    while i < len(vlan) - 1:
        if vlan[i].host + vlan[i + 1].host < 24 - ceil(len(vlan) / 2):
            newVlan = Vlan(
                vlan[i].host + vlan[i + 1].host,
                vlan[i].id + "+" + vlan[i + 1].id,
                vlan[i].name,
                "",
                [],
            )
            vlan.append(newVlan)
            vlan.pop(i)
            vlan.pop(i)
            sortVlan(vlan)
        else:
            i = i + 1
    return vlan


# function to define name and value port of deviceObject
def definePort(source, numPort, typePort):
    counter = 1
    octet = 0
    for i in range(numPort):
        if counter > 24:
            octet += 1
            counter = 1
        portLabel = ""
        if typePort == "Gi":
            portLabel = typePort + "1/" + str(octet) + "/" + str(counter)
        else:
            if typePort == "fa":
                portLabel = typePort + str(octet) + "/" + str(counter)
        counter += 1

        source.switchPorts[portLabel] = False


# Group and define Switch
def defineDevice(number, device_type, device_layer):
    devices = []
    for i in range(number):
        add_device = deviceObject(
            str(device_layer + device_type + str(i)),
            str(device_layer + " " + device_type + " ") + str(i),
            str(device_layer),
        )
        devices.append(add_device)
        if device_layer == "Core":
            definePort(devices[i], 24, "Gi")
        else:
            definePort(devices[i], 24, "fa")
    return devices


def createPortObject(port_array, source_devices, target_devices):
    count = 0
    for s_device in source_devices:
        for t_device in target_devices:
            for portSource in list(s_device.switchPorts.keys()):
                if s_device.switchPorts[portSource] == False:
                    portTarget = list(t_device.switchPorts.keys())[count]
                    if t_device.switchPorts[portTarget] == False:
                        new_port = portObject(
                            s_device.data, t_device.data, portSource, portTarget
                        )
                        port_array.append(new_port)
                        s_device.switchPorts[portSource] = True
                        s_device.connected += 1
                        t_device.switchPorts[portTarget] = True
                        t_device.connected += 1
                        break
        count += 1


# Connect 1 Vlan to 1 Access Switch
def connectVlan(vlan, accessDevice):
    for VLAN in vlan:
        portIndex = 0
        check = False
        for access in accessDevice:
            if VLAN.host <= 24 - access.connected:
                for i in range(VLAN.host):
                    for port in access.switchPorts:
                        if access.switchPorts[port] == False:
                            VLAN.port["switch"] = access.data["id"]
                            portIndex += 1
                            VLAN.port["switchport"].append(portIndex)
                            access.switchPorts[port] = True
                            access.connected += 1
                            break
                check = True
            if check == True:
                break


# Define port connect Access Switch to Vlan
def defineVlanPort(vlan, accessDevice, portDevice, number):
    for VLAN in vlan:
        labelTarget = ""
        startPort = ""
        endPort = ""
        for access in accessDevice:
            if VLAN.port["switch"] == access.data["id"]:
                startPort = list(access.switchPorts.keys())[number]
                endPort = list(access.switchPorts.keys())[number + VLAN.host - 1]
                if endPort.find("fa") != -1:
                    labelTarget = startPort + "-" + endPort[4:]
                if endPort.find("Gi") != -1:
                    labelTarget = startPort + "-" + endPort[6:]
                new_port = portObject(
                    access.data, {"id": VLAN.id}, labelTarget, "Ethernet"
                )
                portDevice.append(new_port)


def main():
    # Data input here
    vlan0 = Vlan(12, "vlan0", "An", "", [])
    vlan1 = Vlan(13, "vlan1", "Anal", "", [])
    vlan2 = Vlan(14, "vlan2", "Analyst", "", [])
    vlan = [vlan0, vlan1, vlan2]
    # --------------
    sorted_vlan = sortVlan(vlan)
    splitted_vlan = split_vlan(sorted_vlan)
    merge_vlan = mergeVlan(splitted_vlan)
    # Caculated number of Switch, Dist, Core
    accSwt_num = len(vlan)
    distSwt_num = ceil(accSwt_num / 2)
    coreSwt_num = ceil(distSwt_num / 3)
    # ____________
    accessDevice = defineDevice(accSwt_num, "Switch", "Access")
    distDevice = defineDevice(distSwt_num, "Switch", "Dist")
    coreDevice = defineDevice(coreSwt_num, "Switch", "Core")
    # define Router port
    router = []
    add_router = deviceObject("router", "Router", "router")
    router.append(add_router)
    definePort(router[0], 2, "Gi")

    # Connect Router - Core
    portDevice = []
    createPortObject(portDevice, router, coreDevice)
    # Connect Core - Dist
    createPortObject(portDevice, coreDevice, distDevice)
    createPortObject(portDevice, distDevice, accessDevice)
    # Connect Dist - Access Switch
    connectVlan(merge_vlan, accessDevice)
    defineVlanPort(vlan, accessDevice, portDevice, distSwt_num)
    networkDevice = accessDevice + distDevice + coreDevice + router
    return networkDevice, portDevice
