def get_eviction_address(key, cache, future):
    if key in cache:
        return -1

    capacity = len(cache)
    removables = [address for address in cache if address not in future]

    if not removables:
        # this means all the cache is used in future
        # if key not in future:
        #   return -1

        # frequencies = OrderedDict()
        # for i in future:
        #   frequencies[i] = frequencies[i]+1 if i in frequencies else 1
        # frequencies[key] += 1 # considering frequencies after key request
        # frequencies.move_to_end(key, last=False)

        # frequency_sorted = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
        # significance_order = [tup[0] for tup in frequency_sorted]
        # return significance_order[-1]
        return -1
    return removables[0]