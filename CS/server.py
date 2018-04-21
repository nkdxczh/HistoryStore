#!/usr/bin/env python

import sys
sys.path.append('../gen-py')

from historystore import HistoryStore
from historystore.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

import socket

import core as core
import cache as cache

store = core.StoreWithHistory()
#the cache layer for getAt function
getAtCache = cache.GetAtCache()

class HSHandler:
    def __init__(self):
        self.log = {}
        
    def put(self, key, val):
        store.put(key, val)
            
    def get(self, key):
        return store.get(key)

    def getAt(self, key, time):
        #get the closet result from cache
        closetTime, vals = getAtCache.getAt(key, time)
        if closetTime == time:
            return vals
        elif closetTime == -1:
            res = store.getAt(key, time)
            #save the result to cache
            getAtCache.put(key, time, res)
            return res
        else:
            #get the diff between closetTime and target time
            diff = store.diff(key, min(closetTime, time), max(closetTime, time))
            res = set(vals)
            #merge the two sets
            for val in diff:
                if val in res:
                    res.remove(val)
                else:
                    res.add(val)
            getAtCache.put(key, time, res)
            return res

    def delKey(self, key):
        store.delKey(key)

    def delVal(self, key, val):
        store.delVal(key, val)

    def diff(self, key, time1, time2):
        return store.diff(key, time1, time2)

PORT = 8081
handler = HSHandler()
processor = HistoryStore.Processor(handler)
transport = TSocket.TServerSocket(port=PORT)
                                         
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print "Starting python server..."
server.serve()
print "done!"

