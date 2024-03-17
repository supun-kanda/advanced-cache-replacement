from frozen_cache import FrozenCacheDev
import sys
import time
import numpy as np

file_name = sys.argv[1] if len(sys.argv) > 1 else 'web07.trace'
print('dataset: ', file_name)

with open(file_name, 'rb') as file:
    data = file.read(4) # integer = 4 x bytes
    data_set = []
    while data:
      data_set.append(int.from_bytes(data, "big"))
      data = file.read(4)

cache_cap = 500

cache = FrozenCacheDev(cache_cap, data_set)

cache_states = []
evictions = []
i = 0
t = time.time()
is_rerun = False
for index, key in enumerate(data_set):
    if(index % 1000 == 0):
        now = time.time()
        print("passed: ", index, " batch time taken sec: ", now - t)
        t = now

    if cache.get(key) is None:
      cache_snapshot = list(cache.cache.keys())

      eviction = cache.put(key, key, index)

      if (eviction > 0) or (eviction == -1 and is_rerun is False):
        evictions.append(cache_snapshot.index(eviction) if eviction > 0 else -1)
        reversed(cache_snapshot)
        cache_states.append(cache_snapshot)

        if eviction > 0:
          is_rerun = False
        else:
          is_rerun = True

data_len = len(evictions)
output_address_space = cache_cap + 1

inputs = np.array(cache_states)

outputs = np.zeros((data_len, output_address_space))
for index, eviction in enumerate(evictions):
    outputs[index, (output_address_space - 1) if eviction == -1 else eviction] = 1

np.save("resources/model_3_inputs.npy", inputs)
np.save("resources/model_3_outputs.npy", outputs)