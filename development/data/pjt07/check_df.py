import pandas as pd
from datetime import datetime 
import json
import os

# 생략 없이 모든 열 출력
pd.set_option('display.max_columns', None)


file_path = '../crawling/processed.parquet'
df = pd.read_parquet(file_path)
# print(len(df))
# print(df)
print('컬럼 -> ', df.columns)
# print(df.category.unique())
print(df.head())
# print(df[df.category == '사례: 게임 산업 동향'])

# idx = df[df.category == '사례: 게임 산업 동향'].index
# df = df.drop(idx)
# print(df.category.unique())

# likes 컬럼 쿠가
df.likes = ""
df.views = 0
# print(df)