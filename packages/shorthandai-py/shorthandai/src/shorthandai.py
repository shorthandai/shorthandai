from typing import NewType
import requests
import warnings
import os
import datetime
import numpy as np
import pandas as pd
from typing import Iterable, TypedDict, Optional, Union, List

__SHORTHAND_AI_TOKEN_ENV_VAR_NAME__ = "SHORTHANDAI_TOKEN"
__API_ROOT_URL__ = "https://apiv1.shorthand.ai/api/v1"

def get_raw_value_dimensions(raw):
    # // if pandas df
    if type(raw) != list: return 0, 0
    if len(raw) == 0: return 0, 0
    if type(raw[0]) != list: return len(raw), 0
    else: return len(raw), len(raw[0])

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
    

class SHValueDocRaw(TypedDict):
    value: Union[str, int, bool, List[Union[str, int, bool]], List[List[Union[str, int, bool]]]]


def _handle_raw_data(data: dict, take_df_header: Optional[bool]=True):
    value = data['value'] if 'value' in data else None
    if take_df_header:
        n, m =  get_raw_value_dimensions(value)
        if n > 0 and m > 0:
            # pd.DataFrame(value[1:], columns=[value[0]])
            df = pd.DataFrame(value[1:], columns=[value[0]])
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = list(df.columns.get_level_values(0))
            return df

        if n > 0 or m > 0:
            return pd.DataFrame(value)

    return value
    

class GetManyTopic(TypedDict):
    topic_name: str
    tag: Optional[Union[str, int]]


class GetHistoricalTopic(TypedDict):
    topic_name: str
    asOf: datetime.datetime

class SetManyTopic(TypedDict):
    topic_name: str
    value: Union[str, int, bool, List[Union[str, int, bool]], List[List[Union[str, int, bool]]]]
    tag: Optional[str]

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
    
    def get_raw(self, topic_name: str, tag: str=None, take_df_header=True):
        """
        Given `topic_name`, returns the latest value as well as metadata 
        on the topic.
        """
        check_value_inputs(self.__token, topic_name=topic_name)
        res = requests.post(
            f"{__API_ROOT_URL__}/get",
            json={
                "topicName": topic_name,
                "tag": tag,
                "token": self.__token
            }
        )

        status_code = res.status_code
        if (res.status_code >= 400 and res.status_code  <= 500):
            raise Exception(f"ERR {status_code}") 
        
        if (res.status_code >= 500):
            raise Exception(f"ERR {status_code}") 
        
        data = res.json()

        return data
    
    
    def get(self, topic_name: str, tag: str=None, take_df_header=True):
        """
        Given `topic_name`, returns the latest value (or tagged value, 
        if provided)
        """
        check_value_inputs(self.__token, topic_name=topic_name)
        data = self.get_raw(
            topic_name,
            tag=tag,
            take_df_header=take_df_header
        )

        return _handle_raw_data(data, take_df_header=take_df_header)
    
    def get_many(self, topics: Iterable[GetManyTopic], take_df_header=True):
        """
        Given `topics`, returns their values
        """

        check_value_inputs(self.__token, topic_name=None)
        res = requests.post(
            f"{__API_ROOT_URL__}/getmany",
            json={
                "topics": [
                    {
                        "topicName": t['topic_name'],
                        "tag": t['tag'] if 'tag' in t else None
                    } for t in topics
                ],
                "token": self.__token
            }
        )

        status_code = res.status_code
        if (res.status_code >= 400 and res.status_code  <= 500):
            raise Exception(f"ERR {status_code}") 
        
        if (res.status_code >= 500):
            raise Exception(f"ERR {status_code}") 
        
        data = res.json()

        for datum in data:
            yield _handle_raw_data(datum, take_df_header=take_df_header)
    
    def set_many(self, topics: Iterable[SetManyTopic]):
        """
        Given `topics`, writes their values to Shorthand in batch
        
        Args:
            topics: An iterable of topics, where each topic has:
                - topic_name: The name of the topic
                - value: The value to set
                - tag (optional): A tag for the value
                
        Returns:
            A list of response data for each topic
        """
        check_value_inputs(self.__token, topic_name=None)
        
        # Transform pandas DataFrames to lists if present
        processed_topics = []
        for topic in topics:
            value_out = topic['value']
            if isinstance(value_out, pd.DataFrame):
                first_row = list(value_out.columns.values)
                value_out = value_out.values.tolist()
                value_out = [first_row] + value_out
                
            processed_topic = {
                "topicName": topic['topic_name'],
                "value": value_out
            }
            if 'tag' in topic:
                processed_topic["tag"] = topic['tag']
            processed_topics.append(processed_topic)

        res = requests.post(
            f"{__API_ROOT_URL__}/setmany",
            json={
                "topics": processed_topics,
                "token": self.__token
            }
        )

        status_code = res.status_code
        if (res.status_code >= 400 and res.status_code <= 500):
            raise Exception(f"ERR {status_code}")
        
        if (res.status_code >= 500):
            raise Exception(f"ERR {status_code}")
        
        return res.json()
        
    def geth_many(self, topics: Iterable[GetHistoricalTopic], take_df_header=True):
        """
        Given `topics`, returns their values as of the specified timestamp
        """

        check_value_inputs(self.__token, topic_name=None)
        res = requests.post(
            f"{__API_ROOT_URL__}/gethmany",
            json={
                "topics": [
                    {
                        "topicName": t['topic_name'],
                        "asOfTs": int(t['asOf'].timestamp() * 1000) if ('asOf' in t) else None,
                        # "tag": t['tag'] if 'tag' in t else None
                    } for t in topics
                ],
                "token": self.__token
            }
        )

        status_code = res.status_code
        if (res.status_code >= 400 and res.status_code  <= 500):
            raise Exception(f"ERR {status_code}") 
        
        if (res.status_code >= 500):
            raise Exception(f"ERR {status_code}") 
        
        data = res.json()

        for datum in data:
            yield _handle_raw_data(datum, take_df_header=take_df_header)

    def geth(
            self, 
            topic_name: str, 
            since: str=datetime.datetime, 
            # tag: str=None,
            take_df_header=True,
        ):
        """
        Given `topic_name` and `since`, returns the last value since 
        """
        check_value_inputs(self.__token, topic_name=topic_name)
        res = requests.post(
            f"{__API_ROOT_URL__}/geth",
            json={
                "topicName": topic_name,
                "asOfTs": int(since.timestamp() * 1000),
                "token": self.__token
            }
        )

        status_code = res.status_code
        if (res.status_code >= 400 and res.status_code  <= 500):
            raise Exception(f"ERR {status_code}") 
        
        if (res.status_code >= 500):
            raise Exception(f"ERR {status_code}") 
        
        data = res.json()

        return _handle_raw_data(data, take_df_header=take_df_header)


    def set(self, topic_name: str, value):
        """
        Given `topic_name`, writes `value` to Shorthand
        """
        check_value_inputs(self.__token, topic_name=topic_name)

        value_out = value
        if isinstance(value, pd.DataFrame):
            value_out = value.values.tolist()
            first_row = list(value.columns.values)
            value_out = [first_row] + value_out

        res = requests.post(
            f"{__API_ROOT_URL__}/set",
            json={
                "topicName": topic_name,
                "value": value_out,
                "token": self.__token
            }
        )

        status_code = res.status_code
        if (res.status_code >= 400 and res.status_code  <= 500):
            raise Exception(f"ERR {status_code}") 
        
        if (res.status_code >= 500):
            raise Exception(f"ERR {status_code}") 
        
        data = res.json()
        value = data['value'] if 'value' in data else None

        return data

    GET = get
    GETH = geth
    SET = set
    GETMANY = get_many
    getmany = get_many
    
    def info(self):
        return ({
            "version": '0.0.11',
        })

def main():
    import time
    SH = ShorthandAI('sh-1f64dvvvnon4NFt0yl0H')
    print(SH.info())
    print(SH.GET('dev123', '1659994710026'))
    print(SH.GET('dev123', 'notexists'))
    print('latest dev123:', SH.GET('dev123'))
    print(SH.GET('dev444'))

    print("\nT)esting GET-historical\n")
    print(SH.GETH('dev123', datetime.datetime(2022, 12, 31)))
    print(SH.GETH('dev123', datetime.datetime(2022, 11, 1)))
    print(SH.GETH('dev123', datetime.datetime(2023, 2, 24)))

    print("\nTesting SET\n")
    print(SH.SET('dev555-scalar', 1000))
    print(SH.GET('dev555-scalar'))

    new_df = pd.DataFrame({
        'Name': ['Tom', 'nick', 'krish', 'jack'],
        'Age': [20, 21, 19, 18]
    })
    print(new_df)
    print(SH.SET('dev777-pd', new_df))
    print(SH.GET('dev777-pd'))

    print(SH.GET('dev777-pd').columns)
    print("\nTesting GETMANY\n")
    print(list(SH.GETMANY([
        {
            "topic_name": "dev123",
            "tag": '1659994710026'
        },
        {
            "topic_name": "dev444",
            "tag": '1659994710026'
        },
        {
            "topic_name": "dev444",
        },
        {
            "topic_name": "dev444",
            "tag": 'latest'
        },
        {
            "topic_name": "dev555-scalar",
            "tag": '1000'
        },
        {
            "topic_name": "dev555-scalar",
            "tag": 'latest'
        }
    ])))

    start_ts = time.time()

    get_many_res = list(SH.GETMANY([
        {
            "topic_name": "dev123",
            "tag": '1659994710026'
        },
        {
            "topic_name": "dev444",
            "tag": '1659994710026'
        },
        {
            "topic_name": "dev444",
        },
        {
            "topic_name": "dev444",
            "tag": 'latest'
        },
        {
            "topic_name": "dev777-pd",
        },
        {
            "topic_name": "dev555-scalar",
            "tag": 'latest'
        }
    ] * 100))
    
    end_ts = time.time()
    elapsed = end_ts - start_ts
    print([ str(type(d)) for d in get_many_res ])
    print(f'getmany for {len(get_many_res)} topics in {elapsed}s')

    print("\nTesting SET_MANY\n")

    new_df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Score': [95, 87, 92]
    })

    set_many_res = SH.set_many([
        {
            "topic_name": "dev101",
            "value": 301
        },
        {
            "topic_name": "dev102",
            "tag": "easy",
            "value": 101
        },
        {
            "topic_name": "dev103-pd",
            "value": new_df
        }
    ])
    print("Set many response:", set_many_res)

    # Verify the values were set
    get_many_res = list(SH.GETMANY([
        {"topic_name": "dev101", "tag": "latest"},
        {"topic_name": "dev102", "tag": "easy"},
        {"topic_name": "dev103-pd"}
    ]))
    
    print("Verification get:", get_many_res)

    get_res = SH.GET("dev103-pd")
    print("Verification get dev103-pd:", get_res)
    
    return

if __name__=="__main__":
    main()