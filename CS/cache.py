import core as core

class GetAtCache:
    '''
    cache: the value is [timestamp, values(list)]
    SIZE: the maximium size for each key
    '''
    def __init__(self):
        self.cache = dict()
        self.SIZE = 10
        
    #if the target value is not cached, return the closet cached timestamp and its value
    def getAt(self, key, time):
        #if not cache, return timestamp = -1
        if key not in self.cache:
            return -1, []

        #find the value of the closet cached time
        closetTime = -1
        minGap = time + 1
        res = []
        for record in self.cache[key]:
            if abs(record[0] - time) < minGap:
                minGap = abs(record[0] - time)
                closetTime = record[0]
                res = record[1]

        return closetTime, res

    #cache a value, if the cache exceed SIZE, remove the oldest one
    def put(self, key, time, values):
        #initilize if key not exist
        if key not in self.cache:
            self.cache[key] = []

        #check if already been cached:
        for record in self.cache[key]:
            if record[0] == time:
                return

        self.cache[key].append([time, values])
        if len(self.cache[key]) > self.SIZE:
            self.cache[key].popleft()

if __name__ == '__main__':
    cache = GetAtCache()
    cache.put('A', 1, ['B','C'])
    cache.put('B', 3, ['C'])
    cache.put('C', 4, ['A','B'])
    cache.put('A', 7, ['B'])
    assert cache.getAt('B', 3) == (3, ['C'])
    assert cache.getAt('A', 3) == (1, ['B','C'])
    assert cache.getAt('A', 100) == (7, ['B'])

