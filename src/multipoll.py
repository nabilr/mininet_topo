#!/usr/bin/python

"""
Simple example of sending output to multiple files and
monitoring them
"""


#from mininet.topo import SingleSwitchTopo
import random
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import info, setLogLevel
from mininet.cli import CLI

from time import sleep
from time import time
from select import poll, POLLIN
from subprocess import Popen, PIPE
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info


user_list = []

cmd_list = ['USER', 'PASS', 'PWD', '!PWD','CD','!CD', 'PWD', '!PWD','GET','PUT', 'QUIT']

user_list = [ ('Nabil','1234'), ('Brooke','qwer'), ('Martin','iluvnet'),('Yasir','ethernet')]
server_files = ['bigfile', 'small_file1']
dir_list = ['h', 'level1']

class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def build(self, n=2,lossy=True, **opts):
        switch = self.addSwitch('s1')
        for h in range(n):
            # Each host gets 50%/n of system CPU
            host = self.addHost('h%s' % (h + 1),
                                cpu=.5 / n)
            if lossy:
                # 10 Mbps, 5ms delay, 10% packet loss
                self.addLink(host, switch,
                             bw=10, delay='10ms', loss=10, use_htb=True)
            else:
                # 10 Mbps, 5ms delay, no packet loss
                self.addLink(host, switch,
                             bw=10, delay='10ms', loss=0, use_htb=True)

def monitorTest( N=4, seconds=20 ):
    "Run pings and monitor multiple hosts"
    topo = SingleSwitchTopo( N, lossy=True )
    #net = Mininet( topo )
    net = Mininet( topo=topo,
                   host=CPULimitedHost, link=TCLink,
                   autoStaticArp=True )
    devnull = open( '/dev/null', 'w' )
    net.start()
    hosts = net.hosts
    info( "Starting test...\n" )
    server = hosts[ 0 ]
    print server
    #server.cmd("cd h1")
    server.cmd("strace ../obj/FTPserver " +  server.IP() + " 5000 2> /tmp/server &")
    print "../obj/FTPserver " +  server.IP() + " 5000 &"

    
    ftp_cmd,cmds, outfiles, errfiles, infiles = {}, {}, {}, {}, {}
    for h in hosts[1:]:
        # Create and/or erase output files
        outfiles[ h ] = '/tmp/%s.out' % h.name
        errfiles[ h ] = '/tmp/%s.err' % h.name
        infiles[ h ] = '/tmp/%s.in' % h.name
        h.cmd( 'echo >', outfiles[ h ] )
        h.cmd( 'echo >', errfiles[ h ] )
        h.cmd( 'echo >', infiles[ h ] )
        h.cmd('tail -f %s | stdbuf -o 0   ../obj/FTPclient %s %s > %s &'%(infiles[h], server.IP(), '5000', outfiles[ h ] ))
        ftp_cmd[h] = [] + cmd_list




    tmp_hosts = [] + hosts[1:]
    print hosts[0]
    print tmp_hosts[0]

    print hosts[0].cmd("ps -ef | egrep FTP");
    print hosts[1].cmd("ps -ef | egrep FTP");
    while True:

        if len(tmp_hosts) == 0:
            break

        i = random.randint(0, len(tmp_hosts)-1)

        print i, tmp_hosts[i]
        h = tmp_hosts[i]
        if len(ftp_cmd[h]) > 0:
            sub_cmd = ftp_cmd[h].pop(0)
            print tmp_hosts[i].cmd("ps -ef | egrep 'FTP|tail'");
            if sub_cmd == 'USER':
                print h.name, 'USER'
                h.cmd('echo >> %s' %(infiles[h]))
                h.cmd('echo USER %s >> %s' %(user_list[i][0], infiles[h]))
                sleep(1);
            if sub_cmd == 'PASS':
                print h.name, 'PASS'
                h.cmd('echo  PASS %s >> %s' %(user_list[i][1], infiles[h]))
                sleep(1);
            if sub_cmd == '!CD':
                print h.name, '!CD'
                print h.cmd('echo  "!""CD %s" >> %s' %(h.name, infiles[h]))
                sleep(1);
            if sub_cmd == 'CD':
                print h.name, 'CD'
                h.cmd('echo  CD %s >> %s' %(server.name, infiles[h]))
                sleep(1);
            if sub_cmd == '!PWD':
                print h.name, '!PWD'
                h.cmd('echo  "!""PWD >> %s"' %(infiles[h]))
                sleep(1);
            if sub_cmd == 'PWD':
                print h.name, 'PWD'
                h.cmd('echo  PWD >> %s' %(infiles[h]))
                sleep(1);
            if sub_cmd == 'GET':
                print h.name, 'GET'
                if len(server_files) == 2:
                    bigfile = server_files.pop(0);
                    h.cmd('echo  GET %s >> %s' %(bigfile, infiles[h]))
                else:
                    smallfile = server_files[0];
                    h.cmd('echo  GET %s >> %s' %(smallfile, infiles[h]))
                sleep(1);
            if sub_cmd == 'PUT':
                print h.name, 'PUT'
            if sub_cmd == 'QUIT':
                print h.name, 'QUIT'
                h.cmd('echo QUIT >> %s' %(infiles[h]))
                sleep(1);
            if sub_cmd == 'GET':
                print h.name, 'GET'
            if sub_cmd == 'PUT':
                print h.name, 'PUT'
            if sub_cmd == 'QUIT':
                print h.name, 'QUIT'
                h.cmd('echo QUIT >> %s' %(infiles[h]))
                sleep(1);
        else:
            tmp_hosts.pop(i)
    output = server.cmd(' ls h2/in h3/in h4/in')

    print output

    while 'No such file' in output:
        print 'Sleep......'
        sleep(1);
    for h in hosts:
        h.cmd('pkill FTPserver')
        h.cmd('pkill FTPclient')
        h.cmd('pkill cat')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    monitorTest()
