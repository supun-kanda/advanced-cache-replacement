def remove_values_less_than(d, threshold):
    # List to hold keys that will have empty lists after removal
    empty_keys = []

    for key, values in d.items():
        # Remove values less than the threshold
        d[key] = [value for value in values if value >= threshold]

        # If the list is empty after removal, mark the key for removal
        if not d[key]:
            empty_keys.append(key)

    # Remove keys that are associated with empty lists
    for key in empty_keys:
        del d[key]