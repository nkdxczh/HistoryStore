service HistoryStore {
  void put(1:string key,2:string val),
  list<string> get(1:string key),
  list<string> getAt(1:string key,2:i32 value),
  void delKey(1:string key),
  void delVal(1:string key,2:string value),
  list<string> diff(1:string key,2:i32 time1,3:i32 time2)
}
