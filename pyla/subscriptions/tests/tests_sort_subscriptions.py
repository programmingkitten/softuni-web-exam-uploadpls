def sort_subscription_by_len_of_features(subscriptions):
    subscriptions_features_new = {}
    while subscriptions:
        lowest_key = list(subscriptions.keys())[0]
        for key, value in subscriptions.items():
            if len(value) < len(subscriptions[lowest_key]):
                lowest_key = key
        new_value = subscriptions[lowest_key]
        subscriptions.pop(lowest_key)
        subscriptions_features_new[lowest_key] = new_value
    return subscriptions_features_new
