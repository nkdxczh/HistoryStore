#Wrap history as transactions to support undo
class Transaction:
    def __init__(self, time, value, op):
        self.time = time
        self.value = value
        self.op = op

    def __str__(self):
        return str(self.time) + ', ' + str(self.value) + ', ' + self.op

#Encapsulate the operations with Transaction
class Cache:
    def __init__(self):
        self.set = set()

    def do(self, t):
        if t.op == '+':
            self.set.add(t.value)
        elif t.op == '-':
            if t.value in self.set:
                self.set.remove(t.value)
                
    def undo(self, t):
        if t.op == '-':
            self.set.add(t.value)
        elif t.op == '+':
            if t.value in self.set:
                self.set.remove(t.value)

class StoreWithHistory:
    '''
    map: save all history (transactions)
    cache: save the current content for each key
    clock: record the current time, increase by each operation
    '''
    def __init__(self):
        self.map = dict()
        self.cache = dict()
        self.clock = 0

    def get(self, key):
        self.clock += 1
        if key not in self.map:
            return []
        return list(self.cache[key].set)

    def put(self, key, value):
        if key not in self.map:
            self.map[key] = [] 
            self.cache[key] = Cache()

        #generate an add transaction
        t = Transaction(self.clock, value,'+')
        self.clock += 1
        self.map[key].append(t)
        self.cache[key].do(t)

    def deleteKey(self, key):
        self.clock += 1
        if key not in self.map:
            return

        #generate delete transaction for all element
        for ele in self.cache[key].set:
            t = Transaction(self.clock, ele, '-')
            self.map[key].append(t)
        self.cache[key].set.clear()
        self.clock += 1

    def deleteValue(self, key, value):
        if key not in self.map or value not in self.cache[key].set:
            self.clock += 1
            return

        #generate a delete transaction
        t = Transaction(self.clock, value,'-')
        self.clock += 1
        self.map[key].append(t)
        self.cache[key].do(t)

    def getAt(self, key, time):
        self.clock += 1
        if key not in self.map:
            return []

        res = Cache()
        #redo all transactions from beginning to time
        for t in self.map[key]:
            if t.time > time:
                break
            res.do(t)
        return list(res.set)

    def diff(self, key, time1, time2):
        self.clock += 1
        if key not in self.map:
            return []

        res = Cache()
        #redo all transactions from time1 to time2
        for t in self.map[key]:
            if t.time > time1 and t.time <=time2:
                res.do(t)

        return list(res.set)

if __name__ == '__main__':
    #test operations between Cache and Transaction
    c1 = Cache()
    t1 = Transaction(0, 'a', '+')
    c1.do(t1)
    assert c1.set == set(['a'])
    c1.undo(t1)
    assert c1.set == set([])

    #test the example
    store = StoreWithHistory()
    store.put("A","c")
    store.put("B","d")
    assert store.get("A") == ["c"]
    store.put("A","e") 
    assert store.get("A") == ["c", "e"]
    assert store.getAt("A", 2) == ["c"]
    store.deleteKey("A") 
    assert store.get("A") == []
    assert store.getAt("A",5) == ["c", "e"] 
    store.put("B","f") 
    store.deleteValue("B","d") 
    assert store.get("B") == ["f"]
    assert store.diff("A", 1, 2) == []
    assert store.diff("A", 3, 5) == []
    assert store.diff("A", 1, 4) == ["e"]
    assert store.diff("B", 0, 1) == ["d"]
