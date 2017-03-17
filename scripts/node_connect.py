
import paramiko
import sys
import os
import re
import time
import subprocess
import pdb




def collect_info(info_file, user, code_dir):
    '''
    Read the dev info from the file and form a dictionary
    :return:
    '''
    my_dict = eval(open(info_file).read())




    print "Number of Nodes: {0}".format(len(my_dict))
    print "RIT username : {0}".format(user)

    #try to copy the latest MNLR code from the execution server to each of the
    #nodes in the GENI
    #print my_dict
    for node in my_dict:
        conn_info = my_dict[node]
        scp_cmd = "scp -i ~/.ssh/id_geni_ssh_rsa -P {0} -r {1} {2}@{3}:/users/{4}".format(conn_info[1], code_dir, user, conn_info[0], user)
        #print scp_cmd
        proc = subprocess.Popen(scp_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        op, err = proc.communicate()
        print op, err
        time.sleep(3)
        match = re.search("(yes/no)", op)
        if match:
            print match.group()
            os.system("yes")
            time.sleep(10)
        print "Copied the MNLR updated Code to {0}".format(node)

    return my_dict


def connect_args(full_dict, node):
    '''
    It Returns three parameters
    :param full_dict:
    :return: hostname, port
    '''
    tmp_host = full_dict[node]
    host,port = tmp_host[0],tmp_host[1]


    return host,port

def trigger_MNLR(info_dict, user, password):

    '''
    Execute appropriate MNLR commands on each nodes
    :return:
    '''
    #read the command file
    nodes = []
    for node in info_dict:
        nodes.append(node)


    node_nam = []
    node_cmd = []
    fileop = open('cmd_file.txt', 'r')
    cmd_lst = fileop.read().splitlines()

    print cmd_lst

    for i in cmd_lst:
        tmp_i = i.strip()
        cmd_split = tmp_i.split(',')
        node_nam.append(cmd_split[0])
        node_cmd.append(cmd_split[1])



    #Forming Cmd Dictionary
    Mcmd_dict = dict(zip(node_nam, node_cmd))
    #print Mcmd_dict


    #Maintain a list for the hostnames
    #import pdb; pdb.set_trace()
    ssh = []
    for i in range(0, len(info_dict)):
        ssh.append(paramiko.SSHClient())
        tmp_info = info_dict[node]
        ssh[i].set_missing_host_key_policy(paramiko.AutoAddPolicy())
        mykey = paramiko.RSAKey.from_private_key_file('/home/joe/.ssh/id_geni_ssh_rsa',password=password)
        sys.stdout.write("\rConnecting: %s" % (tmp_info[0]))
        sys.stdout.flush()

        #call the command args function
        host, port = connect_args(info_dict, nodes[i])
        ssh[i].connect(host, username= user, pkey=mykey, port=int(port))
        sys.stdout.write("\rConnected: %s" % (tmp_info[0][1]))
        sys.stdout.flush()
        #pdb.set_trace()



        if  not  nodes[i][:-2] == 'ipnode':

            stdin, stdout, stderr = ssh[i].exec_command('rm -rf logs')

            x = 'cd /users/ss9979/MNLR_LATEST/src;'+ str(Mcmd_dict[nodes[i]]) + ' ' + '&'
            print x
            stdin, stdout, stderr = ssh[i].exec_command('sudo pkill run')
            stdin, stdout, stderr = ssh[i].exec_command('ps -ef | grep tshark')
            stdin, stdout, stderr = ssh[i].exec_command('uptime')
            #stdin, stdout, stderr = ssh[i].exec_command('cd MNLR_changedCode')
            #stdin, stdout, stderr = ssh[i].exec_command('pwd')
            #stdin,stdout, stderr = ssh[i].exec_command('sudo su')
            #stdin,stdout, stderr = ssh[i].exec_command('echo 0 > /proc/sys/net/ipv4/ip_forward')
            stdin, stdout, stderr = ssh[i].exec_command('cd /users/ss9979/MNLR_LATEST/src;gcc  -o run *.c -lm')
            stdin, stdout, stderr = ssh[i].exec_command('pwd')
            print "Current DiR: {}".format(stdout.read())
            print "DEST DIR : {}".format(x)
            stdin,stdout,stderr = ssh[i].exec_command(x)
            stdin.write('\n')
            stdin.flush()
            sys.stdout.write("\r MNLR is Running on :%s\n" % (nodes[i]))
            stdin,stdout,stderr = ssh[i].exec_command('\n')
            ssh[i].close()

            print "cmd : {}".format(Mcmd_dict[nodes[i]])


        else:

            print "{0} is a IP node".format(nodes[i])


        print 'Cleared the Existing Stale configurations...'























