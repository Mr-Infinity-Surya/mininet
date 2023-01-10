from mininet.net import Mininet
from mininet.node import Node, Controller, OVSController
from mininet.link import Link, TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

def myNetwork():
    net = Mininet( controller=Controller, link=TCLink )

    # Add hosts
    h1 = net.addHost( 'h1', ip='10.0.0.1' )
    h2 = net.addHost( 'h2', ip='10.0.0.2' )

    # Add router
    r1 = net.addHost( 'r1', cls=Node, ip='0.0.0.0' )
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')

    # Add links
    net.addLink( h1, r1, intfName1='h1-eth0', intfName2='r1-eth0' )
    net.addLink( h2, r1, intfName1='h2-eth0', intfName2='r1-eth1' )

    net.start()
    # configure the router's IP addresses
    r1.cmd('ifconfig r1-eth0 10.0.0.254 netmask 255.255.255.0')
    r1.cmd('ifconfig r1-eth1 192.168.0.1 netmask 255.255.255.0')
    # configure host1's default gateway
    h1.cmd('route add default gw 10.0.0.254')
    h2.cmd('route add default gw 192.168.0.1')
    # start iperf server on host2
    h2.cmd('iperf -s -u &')
    # measure throughput without NAT
    print("Without NAT:")
    h1.cmd('iperf -c '+ h2.IP() +' -t 10 -u')
    h1.cmd('iperf -c '+ h2.IP() +' -t 10')
    # configure NAT
    r1.cmd('iptables -t nat -A POSTROUTING -o r1-eth1 -j MASQUERADE')
    # measure throughput with NAT
    print("With NAT:")
    h1.cmd('iperf -c '+ h2.IP() +' -t 10 -u')
    h1.cmd('iperf -c '+ h2.IP() +' -t 10')
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
