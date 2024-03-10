from lru_cache import LRUCache
import time
import pickle

with open('web07.trace', 'rb') as file:
    data = file.read(4) # integer = 4 x bytes
    web07 = []
    while data:
      web07.append(int.from_bytes(data, "big"))
      data = file.read(4)

rates = []
data_len = len(web07)
for cache_cap in range(100, 3000, 100):
    hits = 0
    misses = 0
    cache = LRUCache(cache_cap)
    t = time.time()

    for index,key in enumerate(web07):
        if(index % 1000 == 0):
            now = time.time()
            print("cap: ", cache_cap, " print passed: ", index, " batch time taken sec: ", now - t, " hits %: ", hits * 100 / data_len, ", misses %: ", misses * 100 / data_len)
            t = now
        if cache.get(key) is None:
            cache.put(key, key)  
            misses += 1
        else:
            hits += 1

    rates.append({
        'hit_rate': hits / data_len,
        'miss_rate': misses / data_len,
        'capacity': cache_cap
    })

print(rates)

with open('rates.pickle', 'wb') as handle:
    pickle.dump(rates, handle, protocol=pickle.HIGHEST_PROTOCOL)