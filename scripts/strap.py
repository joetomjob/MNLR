#This program parses the xml topo file and creates a readable Topo file


from xml.dom import minidom
from time import gmtime, strftime
from node_connect import *



import pdb


global ip_int
ip_int = []

def hostInfo(node):
    '''
    Extract the hostname and Port number under the node tag
    :return:
    '''
    #pdb.set_trace()
    host_all = []
    login_info = node.getElementsByTagName("login") #login is the tag name
    for elem in login_info:
        hostname = (elem.attributes["hostname"]).value
        port = (elem.attributes["port"]).value

    host = str(hostname),str(port)

    return host


def ipStrip(node):
    ''' arc
    Extract the IP address from each node
    :param node:
    :param ip:
    :return:
    '''
    #pdb.set_trace()
    cat = []
    int_lst = node.getElementsByTagName("interface")
    print "No of interface: {0}".format(len(int_lst))
    #print int_lst
    for item in int_lst:
        intr = (item.attributes["client_id"]).value
        cat.append(intr)

    ip_lst = node.getElementsByTagName("ip")
    #print "No of IP: {0}".format(len(ip_lst))


    for ip in ip_lst:
        ip_address = (ip.attributes["address"]).value
        cat.append(ip_address)

    #print cat
    #print ip_int
    return tuple(cat)


def formKeys(node, client_id):

    '''
        Extract the information about
        1. Node name + portnumber
        2.IP address of the node
        3.Interface (client_IP)
    :return:
    '''
    must_keys = []


    node_lst = xmldoc.getElementsByTagName(node)
    #print "Number of Nodes: {0}".format(len(node_lst))
    for node in node_lst:
        interface = node.attributes[client_id]
        must_keys.append(interface.value)

    return must_keys

def formValues(node, interface, ip, mac):
    '''
    Extract the hostname,portnum,interface,ip and mac for forming tuples of values
    :param node:
    :param interface:
    :param ip:
    :param mac:
    :return:
    '''

    must_values = []
    node_lst = xmldoc.getElementsByTagName(node)
    #pdb.set_trace()
    for node in node_lst:
        hostname = hostInfo(node)
        #must_values.append(hostname)
        ipaddr = ipStrip(node)
        #print ipaddr
        full = hostname + ipaddr
        must_values.append(full)

    return must_values

def dumpInFile(dev_info, time):
    '''
    :return:
    '''
    #print dev_info
    file_name = "./info" + "_" #+  str(time)
    file = open(file_name, 'w')
    file.write(str(dev_info))
    file.close()

    return file_name




if __name__ == "__main__":


    #rspec_file = raw_input("Enter the rspec file location:")
    rspec_file = './sample.xml'
    xmldoc = minidom.parse(rspec_file)
    keys = formKeys('node', 'client_id')
    vals = formValues('node', 'interface', 'address', 'mac_address')
    map = dict(zip( keys, vals))
    time_now = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
    info_file = dumpInFile(map, time_now)

    #ipStrip('interface')
    #uname = raw_input("Enter the username: ")
    uname = 'jxj2428'
    code_dir = raw_input("Enter the code directory:")
    #code_dir = '/mnt/e/MNLR/code'
    info_dict = collect_info(info_file, uname, code_dir)
    trigger_MNLR(info_dict,uname, password = 'Arupara123')



