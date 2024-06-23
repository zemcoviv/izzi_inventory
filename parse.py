import xml.etree.ElementTree as ET

def parse_masscan_output(file):
    tree = ET.parse(file)
    root = tree.getroot()
    devices = []
    for host in root.findall('host'):
        ip = host.find('address').attrib['addr']
        ports = [port.attrib['portid'] for port in host.findall('ports/port')]
        devices.append({'ip': ip, 'ports': ports})
    return devices

def parse_nmap_output(file):
    tree = ET.parse(file)
    root = tree.getroot()
    devices = []
    for host in root.findall('host'):
        ip = host.find('address').attrib['addr']
        os = host.find('os/osmatch').attrib['name'] if host.find('os/osmatch') else 'Unknown'
        ports = [port.attrib['portid'] for port in host.findall('ports/port')]
        devices.append({'ip': ip, 'os': os, 'ports': ports})
    return devices
