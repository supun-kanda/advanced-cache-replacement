import numpy as np
from frozen_cache import FrozenCacheDev
import pickle
import sys
import time

file_name = sys.argv[1] if len(sys.argv) > 1 else 'web07.trace'
print('dataset: ', file_name)

with open(file_name, 'rb') as file:
    data = file.read(4) # integer = 4 x bytes
    data_set = []
    while data:
      data_set.append(int.from_bytes(data, "big"))
      data = file.read(4)

data_len = len(data_set)
cache_cap = 500
add_space = max(data_set)

cache = FrozenCacheDev(cache_cap, data_set)

cache_states = []
i = 0
t = time.time()
for index, key in enumerate(data_set):
    if(index % 1000 == 0):
        now = time.time()
        print("passed: ", index, " batch time taken sec: ", now - t)
        t = now
    if cache.get(key) is None:
      eviction = cache.put(key, key, index)
      if eviction > 0:
        cache_states.append(list(cache.cache.keys()))

with open('cache_status.' + file_name + '.pkl', 'wb') as handle:
    pickle.dump(cache_states, handle, protocol=pickle.HIGHEST_PROTOCOL)