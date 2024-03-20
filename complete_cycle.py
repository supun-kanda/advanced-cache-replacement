
from frozen_cache import FrozenCacheDev
from proposed_cache import ProposedCache

import sys
import time
import numpy as np
from keras.models import Sequential
from keras.layers import Input, Embedding, LSTM, Dense, Dropout
from tensorflow.keras.regularizers import l2
from keras.callbacks import History
import pickle



file_name = sys.argv[1] if len(sys.argv) > 1 else 'web07.trace'
print('dataset: ', file_name)

with open(file_name, 'rb') as file:
    data = file.read(4) # integer = 4 x bytes
    data_set = []
    while data:
      data_set.append(int.from_bytes(data, "big"))
      data = file.read(4)

add_space = max(data_set)

for cache_cap in range(2500,3100,500):

  cache = FrozenCacheDev(cache_cap, data_set)
  str_cache_cap = str(cache_cap)
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

  inputs = np.array(cache_states)
  outputs = np.array(evictions)

  np.save("model_3_"+str_cache_cap+"_inputs.npy", inputs)
  np.save("model_3_"+str_cache_cap+"_outputs.npy", outputs)

  print('shapes input:',inputs.shape, ' output:', outputs.shape)

  output_add_space = cache_cap + 1
  data_len = len(outputs)
  embedding_dim = 500

  model = Sequential()
  input_seq = Input(name="input", shape=(cache_cap,))

  model.add(Embedding(input_dim=add_space, output_dim=embedding_dim, input_length=cache_cap))
  model.add(LSTM(units=250, return_sequences=False, kernel_regularizer=l2(0.001)))  # Reduced units and added L2 regularization
  model.add(Dropout(0.5))  # Added Dropout
  model.add(Dense(output_add_space, activation='softmax'))  # or another appropriate activation function

  model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['sparse_categorical_accuracy'])

  history = model.fit(inputs, outputs, batch_size=64, epochs=100, validation_split=0.2)

  model.save('model_3_'+str_cache_cap+'.keras')

  with open('model_results_3_'+str_cache_cap+'.pkl', 'wb') as file_pi:
    pickle.dump(history.history, file_pi)

  print('starting the evaluation')
  rates = []
  hits = 0
  misses = 0
  test_cache = ProposedCache(cache_cap, model)
  t = time.time()

  for index,key in enumerate(data_set):
      if(index  >0 and index % 1000 == 0):
          now = time.time()
          print(" print passed: ", index, " batch time taken sec: ", now - t, " hits %: ", hits * 100 / index, ", misses %: ", misses * 100 / index)
          t = now
      if test_cache.get(key) is None:
          test_cache.put(key, key)
          misses += 1
      else:
          hits += 1

  rates.append({
      'hit_rate': hits / index,
      'miss_rate': misses / index,
      'capacity': cache_cap
  })

  print(rates)

  with open('rate_results_'+str_cache_cap+'.pkl', 'wb') as file_r:
    pickle.dump(rates, file_r)