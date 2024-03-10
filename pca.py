import numpy as np
from sklearn.decomposition import IncrementalPCA
import pickle

with open('resources/cache_status.web07.trace.pkl', 'rb') as f:
  cache_stats = pickle.load(f)

data_len = len(cache_stats)
cache_cap = 500
add_space = 20484
n_components = 100  # Number of components you want to keep
pca_batch_size = cache_cap  # Adjust based on your memory constraints

ipca = IncrementalPCA(n_components=n_components, batch_size=pca_batch_size)

for index, cache in enumerate(cache_stats):
  inputs = np.zeros((cache_cap, add_space))
  for place, address in enumerate(cache):
        inputs[place, address] = 1
  print('partial fitting: ', index)
  ipca.partial_fit(inputs)

raw_list = []
for index, cache in enumerate(cache_stats):
  print('transform:', index)
  inputs = np.zeros((cache_cap, add_space))
  for place, address in enumerate(cache):
        inputs[place, address] = 1
  raw_list.append(ipca.transform(inputs))

with open('raw_list_web07.pkl', 'wb') as f:
  pickle.dump(raw_list, f)

reduced_data = np.concatenate(np.array(raw_list), axis=0)
reduced_data_3d = reduced_data.reshape(data_len, cache_cap, n_components)

np.savetxt('reduced_data_3d_web07.txt', reduced_data_3d, fmt='%d')