import pandas as pd
from datetime import datetime 
import json
import os

# 생략 없이 모든 열 출력
pd.set_option('display.max_columns', None)

def all_articles():
    file_path = '../crawling/processed.parquet'
    df = pd.read_parquet(file_path)
    print(len(df))
    print(df.columns)
    print(df.head)

    # JSON 형식으로 변환
    all_df_to_json = df.to_json(orient='records', indent=4)
    # print(all_df_to_json)
    return all_df_to_json

temp = json.loads(all_articles())
# print(temp[0])