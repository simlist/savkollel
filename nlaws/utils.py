"""This module contains utilities needed in the nlaws app"""

import datetime

def _inner_merge_dicts(dicts):
    if len(dicts) > 1:
        dict0 = dicts.pop()
        dict1 = dicts.pop().copy()
        for key in dict0:
            val = dict1.pop(key, 0)
            dict0[key] += val
        dict0.update(dict1)
        dicts.append(dict0)
        return _inner_merge_dicts(dicts)
    else:
        return dicts[0]

def merge_dicts(*dicts):
    """Combine multiple dictionaries adding the values of duplicate keys. 
    """
    dicts = list(dicts)
    dict0 = dicts.pop().copy()
    dicts.append(dict0)
    return _inner_merge_dicts(dicts)

def date_from_string(date):
    """"Return date instance from string.
    
    Takes string in the form 'yyyy-mm-dd'.
    """
    return datetime.date(*[int(n) for n in date.split('-')])