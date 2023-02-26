from typing import NewType
import requests
import warnings
import os

def quicktext():
    print('Hello, welcome to QuickSample package.')

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
    
    def get(
            self, 
            topic_id, 
            tag="latest",
            take_header=True,
            ):
        pass

    def GET(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def geth(self, topic_id, since=None):
        pass
    
    def set(
            self, 
            topic_id, 
            value,
            tag=None
            ):
        
        tag_name = None if (tag == 'latest') else tag

        pass

    def info(self):
        return ({
            "version": '0.0.1',
        })

def main():
    SH = ShorthandAI()
    print(SH.info())
    return

if __name__=="__main__":
    main()