import sys
sys.path.append('../gen-py')

from historystore import HistoryStore
from historystore.ttypes import *
from historystore.constants import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

try:
    # Make socket
    transport = TSocket.TSocket('localhost', 8081)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = HistoryStore.Client(protocol)

    # Connect!
    transport.open()

    client.put("A","c")
    client.put("B","d")
    print client.get("A")
    client.put("A","e")
    print client.get("A")
    print client.getAt("A", 2)
    client.delKey("A")
    print client.get("A")
    print client.getAt("A",5)
    client.put("B","f")
    client.delVal("B","d")
    print client.get("B")
    print client.diff("A", 1, 2)
    print client.diff("A", 3, 5)
    print client.diff("A", 1, 4)
    print client.diff("B", 0, 1)
    
    transport.close()

except Thrift.TException, tx:
    print "%s" % (tx.message)

