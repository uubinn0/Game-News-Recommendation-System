import pandas as pd
from datetime import datetime 
import json
import os

# 생략 없이 모든 열 출력
# pd.set_option('display.max_columns', None)
def parquet_category_to_json():

    file_path = '../crawling/processed.parquet'
    df = pd.read_parquet(file_path)
    print(len(df))
    # print(df)
    # print(df.columns)
    # print(df.category.unique())
    # print(df[df.category == '사례: 게임 산업 동향'])
    # print(df.category.unique())

    # category를 기준으로 그룹화하고 각 그룹에 해당하는 url들을 리스트로 묶음
    category_urls = df.groupby('category')['url'].apply(list).to_dict()
    # print(category_urls.keys())

    # JSON 형식으로 변환
    category_urls_json = json.dumps(category_urls, ensure_ascii=False, indent=4)
    # print(category_urls_json)
    
    return category_urls_json

