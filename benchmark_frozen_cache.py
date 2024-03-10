from frozen_cache import FrozenCacheDev
import time
import pickle
import sys

file_name = sys.argv[1] if len(sys.argv) > 1 else 'web07.trace'
print('dataset: ', file_name)

with open(file_name, 'rb') as file:
    data = file.read(4) # integer = 4 x bytes
    data_set = []
    while data:
      data_set.append(int.from_bytes(data, "big"))
      data = file.read(4)

rates = []
data_len = len(data_set)
for cache_cap in range(100, 3000, 100):
    hits = 0
    misses = 0
    cache = FrozenCacheDev(cache_cap, data_set)
    t = time.time()

    for index,key in enumerate(data_set):
        if(index % 1000 == 0):
            now = time.time()
            print("cap: ", cache_cap, len(cache.cache.keys()), " print passed: ", index, " batch time taken sec: ", now - t, " hits %: ", hits * 100 / data_len, ", misses %: ", misses * 100 / data_len)
            t = now
        if cache.get(key) is None:
            cache.put(key, key, index)  
            misses += 1
        else:
            hits += 1

    rates.append({
        'hit_rate': hits / data_len,
        'miss_rate': misses / data_len,
        'capacity': cache_cap
    })

print(rates)

with open('rates.' + file_name + '.pkl', 'wb') as handle:
    pickle.dump(rates, handle, protocol=pickle.HIGHEST_PROTOCOL)