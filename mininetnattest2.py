from mininet.net import Mininet
from mininet.node import Node, Controller, OVSController
from mininet.link import Link, TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import Node, Controller, OVSController
from mininet.link import Link, TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

def myNetwork():
    net = Mininet( controller=Controller, link=TCLink )

    # Add hosts and switches
    h1 = net.addHost( 'h1', ip='10.0.0.1' )
    h2 = net.addHost( 'h2', ip='10.0.0.2' )
    s1 = net.addSwitch( 's1' )
    s2 = net.addSwitch( 's2' )
    s3 = net.addSwitch( 's3' )

    # Add links
    net.addLink( h1, s1 )
    net.addLink( s1, s2 )
    net.addLink( s2, s3 )
    net.addLink( s3, h2 )
    net.addNAT().configDefault()
    net.start()
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
