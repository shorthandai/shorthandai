from typing import NewType
import requests
import warnings
import os
import datetime
import numpy as np
import pandas as pd
import json

__SHORTHAND_AI_TOKEN_ENV_VAR_NAME__ = "SHORTHANDAI_TOKEN"
__API_ROOT_URL__ = "https://apiv1.shorthand.ai/api/v1/"

def __get_effective_value_dimensions(raw):
    if type(raw) != list:
        return 0, 0

    if len(raw) == 0:
        return 0, 0

    if len(raw) == 1:
        if type(raw[0]) != list:
            return 0, 0

        if len(raw[0]) < 1:
            return 0, 0

        return len(raw[0]), 0

    else:
        if type(raw[0]) != list:
            return 0, 0

        if len(raw[0]) < 1:
            return 0, 0

        return len(raw), len(raw[0])

def __get_raw_value_dimensions(raw):
    # // if pandas df
    if type(raw) != list: return 0, 0
    if len(raw) == 0: return 0, 0
    if type(raw[0]) != list: return len(raw), 0
    else: return len(raw), len(raw[0])

def __pack_up_raw_shvalue(raw):
    n, m = __get_raw_value_dimensions(raw)

    if n > 0 and m > 0:
        return ({
            "blob": json.dumps(raw),
            "isSHArrayWrapper": True,
        })

    else:
        return raw

def __unpack_sh_value_doc(doc):
    raw = doc['value'] if 'value' in doc else None

    if type(raw) == dict:
        if 'isSHArrayWrapper' in raw:
            return json.loads(
                raw['blob']
            ), 'MATRIX'

    if type(raw) == list:
        return raw, 'VECTOR'

    return raw, 'SCALAR'


# def get(key, tag=None, domainID='demo'):
#     data = get_raw(key, tag, domainID)
#     value, t = unpack_sh_value_doc(data)

#     if t == 'MATRIX':
#         return pd.DataFrame(value[1:], columns=[value[0]])

#     elif t == 'VECTOR':
#         return np.array(value)

#     return value

# def getdf(key, tag=None, domainID='demo'):
#     data = get_raw(key, tag, domainID)
#     value, t = unpack_sh_value_doc(data)

#     if t == 'MATRIX':
#         return pd.DataFrame(value[1:], columns=[value[0]])

#     elif t == 'VECTOR':
#         return pd.DataFrame(value)

#     return pd.DataFrame([value])


def check_value_inputs(token: str, topic_name=None):
    if not (token and len(token)):
        warnings.warn(
            'ShorthandAI initialized with no token. Either provide one via the constructor '
            'or expose it via the SHORTHANDAI_TOKEN environment variable'
        )

class ShorthandValue:
    def __init__(self, topic_name):
        self.__topic_name = topic_name
        return
    
    def id(self):
        return self.__topic_name
    
    def value(self):
        return
    
    def info(self):
        return

class ShorthandAI:
    def __init__(self, token: str=None):
        self.__token = token if (token and len(token)) else os.environ.get(__SHORTHAND_AI_TOKEN_ENV_VAR_NAME__)
        if not (token and len(token)):
            warnings.warn(
                'ShorthandAI initialized with no token. Either provide one via the constructor '
                'or expose it via the SHORTHANDAI_TOKEN environment variable'
            )
        return
    
    def value(
            self, 
            topic_name
            ):
        return ShorthandValue(topic_name)
    
    def get(self, topic_name: str, tag: str=None):
        """
        Given `topic_name`, returns the latest value
        """
        check_value_inputs(self.__token, topic_name=topic_name)
        res = requests.post(
            f"{__API_ROOT_URL__}/get",
            json={
                "token": self.__token
            }
        )
        data = res
        status_code = res.status_code

        if (res.status_code >= 400 and res.status_code  <= 500):
            raise Exception(f"ERR {status_code}") 
        
        if (res.status_code >= 500):
            raise Exception(f"ERR {status_code}") 

        return ({
            "token": self.__token,
            "data": data
        })
    

    def geth(self, topic_name: str, since: str=datetime.datetime, tag: str=None):
        """
        Given `topic_name` and `since`, returns the last value since 
        """
        check_value_inputs(self.__token, topic_name=topic_name)

        return ({
            "token": self.__token
        })


    def set(self, topic_name: str, value):
        """
        Given `topic_name`, writes `value` to Shorthand
        """
        check_value_inputs(self.__token, topic_name=topic_name)

        return ({
            "token": self.__token
        })

    GET = get
    GETH = geth
    SET = set
    
    def info(self):
        return ({
            "version": '0.0.1',
        })



def main():
    SH = ShorthandAI('demo')
    print(SH.info())
    print(SH.GET('dev123', 'latest'))
    # print(SH.GETH('dev123', datetime.datetime(2022, 12, 31)))
    return

if __name__=="__main__":
    main()