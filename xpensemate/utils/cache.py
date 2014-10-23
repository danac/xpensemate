import collections
import functools
import copy

def lru_cache(cache_size=100):
    '''Least-recently-used cache decorator, compatible with Python 2.x

    Arguments to the cached function must be hashable.

    '''
    def decorating_function(function):
        cache = collections.OrderedDict() # order: least recent to most recent
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            key = repr(args)
            if kwargs:
                key += repr(tuple(sorted(kwargs.items())))
            print("Key", key)
            try:
                result = cache.pop(key)
                print("Cache hit")
            except KeyError:
                print("Cache miss")
                result = function(*args, **kwargs)
                if len(cache) >= cache_size:
                    cache.popitem(0)    # purge least recently used cache entry
            cache[key] = copy.deepcopy(result)         # record recent use of this key
            return result
        return wrapper
    return decorating_function
