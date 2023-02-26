from typing import NewType
import requests
import warnings
import os
import datetime

def quicktext():
    print('Hello, welcome to QuickSample package.')

def check_value_inputs(token: str, topic_id=None):
    if not (token and len(token)):
        warnings.warn(
            'ShorthandAI initialized with no token. Either provide one via the constructor '
            'or expose it via the SHORTHANDAI_TOKEN environment variable'
        )

class ShorthandValue:
    def __init__(self, topic_id):
        self.__topic_id = topic_id
        return
    
    def id(self):
        return self.__topic_id
    
    def value(self):
        return
    
    def info(self):
        return

class ShorthandAI:
    def __init__(self, token: str=None):
        self.__token = token if (token and len(token)) else os.environ.get("SHORTHANDAI_TOKEN")
        if not (token and len(token)):
            warnings.warn(
                'ShorthandAI initialized with no token. Either provide one via the constructor '
                'or expose it via the SHORTHANDAI_TOKEN environment variable'
            )
        return
    
    def value(
            self, 
            topic_id
            ):
        return ShorthandValue(topic_id)
    
    def get(self, topic_id: str, tag: str=None):
        """
        Given `topic_id`, returns the latest value
        """
        check_value_inputs(self.__token, topic_id=topic_id)

        return ({
            "token": self.__token
        })
    

    def geth(self, topic_id: str, since: str=datetime.datetime, tag: str=None):
        """
        Given `topic_id` and `since`, returns the last value since 
        """
        check_value_inputs(self.__token, topic_id=topic_id)

        return ({
            "token": self.__token
        })


    def set(self, topic_id: str, value):
        """
        Given `topic_id`, writes `value` to Shorthand
        """
        check_value_inputs(self.__token, topic_id=topic_id)

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

SH = ShorthandAI()

def main():
    print(SH.info())
    print(SH.GET('dev123', 'latest'))
    print(SH.GETH('dev123', datetime.datetime(2022, 12, 31)))
    return

if __name__=="__main__":
    main()