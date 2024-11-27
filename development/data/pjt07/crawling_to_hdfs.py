import json
import random
import time
from hdfs import InsecureClient
from datetime import datetime
import os

# HDFS 클라이언트 설정 (URL과 HDFS 경로를 본인 환경에 맞게 수정)
  # 'localhost'와 'hadoop-user' 부분을 환경에 맞게 수정하세요.
hdfs_path = '/user/news/realtime/'  # HDFS 내 데이터 저장 경로

# 데이터 소스 경로
base_directory = '/workspace/saffy_pjt_news/data/crawling'


def load_json_files_and_merge(base_directory, max_files=5):
    # 데이터 소스 경로에 있는 모든 JSON 파일을 읽어와서 하나의 리스트로 병합
    all_data = []
    print('->', os.listdir(base_directory))
    for category_name in os.listdir(base_directory):
        category_path = os.path.join(base_directory, category_name)

        if os.path.isdir(category_path):
            print(f'{category_name} 진입')
            file_count = 0
            for json_file in os.listdir(category_path):
                if file_count >= max_files:
                    break

                if json_file.endswith('.json'):
                    file_path = os.path.join(category_path, json_file)

                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            dataset = json.load(file)
                            for data in dataset:
                                # 본문이 비어있는 경우 다음 기사로 넘어감
                                if not data['content']:
                                    continue

                                # 본문이 있는 기사의 경우 본문을 text 형태로 붙이고 리스트에 추가
                                data['content'] = ' '.join(data['content'])
                                all_data.append(data)

                        file_count += 1
                    except Exception as e:  # Typo 수정: Execption -> Exception
                        print(e)

    return all_data


# 데이터 로드 및 병합 (이 부분을 크롤링으로 대체해도 좋습니다)
merged_data_list = load_json_files_and_merge(base_directory)
# 처리된 데이터 개수 출력
print(f"총 {len(merged_data_list)}개의 뉴스 데이터를 처리합니다.")
hdfs_client = InsecureClient('http://localhost:9870', user='hadoop_user')
# 모든 데이터를 순회하며 1초마다 전송
for (index,data) in enumerate(merged_data_list):
    # 데이터를 JSON 형식으로 변환
    json_data = json.dumps(data, ensure_ascii=False)

    # HDFS에 저장될 파일명 생성
    file_name = f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{index}.json"
    
    if index % 100 == 0:
        print("hdfs_client reset")
        hdfs_client = InsecureClient('http://localhost:9870', user='hadoop_user')
        time.sleep(20)
        
    # HDFS에 데이터 저장
    with hdfs_client.write(hdfs_path + file_name, encoding='utf-8') as writer:
        writer.write(json_data)

    # 저장된 파일 경로 출력
    print(f"Data sent to HDFS: {hdfs_path + file_name}")

    # 1초 대기 (데이터 전송 간격)
    # time.sleep(1)
