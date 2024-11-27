import pandas as pd
from datetime import datetime 
import os

# 생략 없이 모든 열 출력
pd.set_option('display.max_columns', None)

# file_path = '../crawling/realtime.parquet/part-00198-c188c4b3-9f60-4b70-90a5-209a2f077beb-c000.snappy.parquet'
file_path = '../crawling/realtime.parquet'
dir_path = "../crawling/processed.parquet"

# 디렉토리가 존재하지 않으면 생성
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

df = pd.read_parquet(file_path)

print(len(df))    # 전체 길이 확인

# 주어진 카테고리 이외의 값으로 분류한 경우 제거
# 필터링할 category 목록
valid_categories = ['행사', '출시', '업데이트', '사건사고 및 기타', 'e-sport', '리뷰', '기술', '게임 산업 동향']

# category 컬럼의 값이 valid_categories에 없는 경우 제거
df = df[df['category'].isin(valid_categories)]
# print(len(df))

print(len(df[df.duplicated(subset=['url'])]))    # 중복 행 수 
drop_duplicate_df = df.drop_duplicates(subset=['url'])    # 중복 제거 후 새 df 생성
print(len(drop_duplicate_df))    # 중복 제거 df 행 수

# 좋아요 및 조회수 컬럼 추가
drop_duplicate_df['likes'] = ""
drop_duplicate_df['views'] = 0

# 현재 시간을 파일명에 포함하여 고유한 파일명 생성
current_time_str = datetime.now().strftime('%Y%m%d_%H%M%S')  # 형식: 20231125_123045
file_name = f"processed_{current_time_str}.parquet"

# 파일 경로
file_path = os.path.join(dir_path, file_name)

drop_duplicate_df.to_parquet(file_path)


# ====================================================

# import pandas as pd
# import glob

# # 디렉토리 내 모든 parquet 파일 경로 찾기
# file_paths = glob.glob('../crawling/realtime.parquet/*.parquet')

# # 각 파일을 순차적으로 읽고 어떤 파일이 읽히는지 출력
# for file_path in file_paths:
#     print(f"읽은 파일: {file_path}")
#     df = pd.read_parquet(file_path)
#     # 추가적으로 데이터를 처리하는 코드가 들어갈 수 있습니다.
    
#     print(len(df))
#     print(len(df[df.duplicated(subset=['url'])]))