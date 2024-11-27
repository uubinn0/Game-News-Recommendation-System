import json
from openai import OpenAI
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, lit
from pyspark.sql.types import StringType, ArrayType, FloatType, StructType, StructField
import requests
from dotenv import load_dotenv
import os

load_dotenv()
# 데이터 소스 설정 (HDFS)
SOURCE_DATA_PATH = f"hdfs://localhost:9000/user/news/realtime"
SOURCE_ARCHIVE_PATH = f"hdfs://localhost:9000/news_archive"

# 데이터 적재 대상 설정 (API)
TARGET_ENDPOINT = f"http://localhost:8000/write-article/"

def initialize_spark_session():
    # Spark 처리 엔진 초기화
    # 실시간 뉴스 데이터 ETL 처리를 위한 세션 생성
    return SparkSession.builder \
        .appName("RealTimeNewsETL") \
        .getOrCreate()

# spark에게 데이터 형식 알려주기 위해 스키마 정의
def define_source_schema():
    # 원본 데이터 스키마 정의
    # 뉴스 데이터의 구조를 명시하여 데이터 품질 보장
    return StructType([
        StructField("title", StringType(), True),        # 뉴스 제목
        StructField("source_site", StringType(), True),  # 데이터 출처
        StructField("writer", StringType(), True),       # 작성자
        StructField("write_date", StringType(), True),   # 생성 일시
        StructField("content", StringType(), True),      # 본문 내용
        StructField("url", StringType(), True)           # 원본 링크
    ])

def create_source_stream(spark, schema):
    # 소스 데이터 스트림 생성
    # HDFS에서 실시간으로 유입되는 JSON 데이터를 읽어오는 스트림 설정
    return spark.readStream \
        .schema(schema) \
        .option("cleanSource", "archive") \
        .option("sourceArchiveDir", SOURCE_ARCHIVE_PATH) \
        .json(SOURCE_DATA_PATH)

        
def transform_extract_keywords(text):
    """
    (이 부분 자체 모델 학습 시켜 대체 가능)
    텍스트 데이터 변환 - 키워드 추출
    입력 텍스트에서 핵심 키워드를 추출하는 변환 로직
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set")
    
    text = preprocess_content(text)
    system_message_content = """
        당신은 텍스트에서 해당 내용을 대표하는 주요 키워드를 추출하는 전문가입니다. 
        다음 텍스트를 가장 잘 요약하고 대표할 수 있는 5개의 키워드를 텍스트 내에서 추출해주세요. 
        키워드는 쉼표로 구분하여 반환해주세요. 
        제대로 하지 않을 경우 처벌할 것입니다.
    """

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message_content},
            {"role": "user", "content": text}
        ],
        max_tokens=100
    )
    keywords = response.choices[0].message.content.strip()
    return keywords.split(',')


def transform_to_embedding(text: str) -> list[float]:
    """
    (이 부분 자체 모델 학습 시켜 대체 가능)
    텍스트 데이터 변환 - 벡터 임베딩
    텍스트를 수치형 벡터로 변환하는 변환 로직
    """
    text = preprocess_content(text)

    client = OpenAI()
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return response.data[0].embedding


def transform_classify_category(content):
    """
    (이 부분 자체 모델 학습 시켜 대체 가능)
    텍스트 데이터 변환 - 카테고리 분류
    뉴스 내용을 기반으로 적절한 카테고리로 분류하는 변환 로직
    """
    content = preprocess_content(content)
    client = OpenAI()    # 창의적 답변 생성을 제어 1에 가까울수록 창의적인 답변을 생성

    system_message_content = """
        당신은 텍스트를 보고 카테고리를 분류하는 전문가입니다. 아래 카테고리 기준에 맞춰 해당 문서의 카테고리를 분류하세요. 
        카테고리는 1개만 반환. 주어진 예시 카테고리로만 분류. 제대로 하지 않으면 처벌할 것이니 똑바로 분류하길 바랍니다.

        출시: 게임 및 콘솔기기 출시 관련 기사. 출시를 위한 홍보 관련 기사도 포함되어야 한다. 기존에 있는 게임의 새로운 콘텐츠 출시는 포함하지 않는다.
        업데이트: 인게임 이벤트를 포함한 일반적인 게임 업데이트 및 패치 관련 기사. 기존에 있는 게임의 새로운 콘텐츠 출시를 포함한다.
        게임 산업 동향: 국내외 게임 업계 현황, 게임 순위, 게임 관련 법률 및 기업 매출 등 국내 혹은 해외 게임 산업 동향을 알 수 있는 기사
        행사: 오프라인 게임 행사 및 IP 콜라보 행사, 굿즈 판매 관련 기사
        리뷰: 게임 혹은 업데이트에 대한 주관적 평가 및 분석이 담긴 기사
        기술: 게임 개발 관련 SW/HW적 기술 발전 소식
        e-sport: e-sport 관련 전반적인 기사
        사건사고 및 기타: 주요 사건사고 및 게임과 관련된 비게임 뉴스
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message_content},
            {"role": "user", "content": content}
        ],
        temperature=0.7
    )
    model_output = response.choices[0].message.content.strip()

    if "카테고리:" in model_output:
        model_output = model_output.split("카테고리:")[1].strip()
    model_output = model_output.replace('"', '').replace("'", "").strip()

    return model_output


def preprocess_content(content):
    """
    데이터 전처리 - 텍스트 길이 제한
    토큰 수를 제한하여 처리 효율성 확보
    """
    import tiktoken

    if not content:
        return ""

    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(content)

    if len(tokens) > 5000:
        truncated_tokens = tokens[:5000]
        return encoding.decode(truncated_tokens)

    return content

def register_transformation_udfs():
    # 데이터 변환을 위한 UDF 함수 등록
    return {
        "keywords": udf(transform_extract_keywords, ArrayType(StringType())),
        "embedding": udf(transform_to_embedding, ArrayType(FloatType())),
        "category": udf(transform_classify_category, StringType())
    }

# 강의 보고 패키지 하나 임포트하기
from pyspark.sql.functions import to_timestamp

def transform_dataframe(source_df, transformation_udfs):
    # 데이터프레임 변환 처리
    # 원본 데이터에 특성 추출 및 분류 결과 추가
    return source_df.withColumn("write_date", to_timestamp(col("write_date"), "yyyy-MM-dd HH:mm:ss")) \
                    .withColumn("keywords", transformation_udfs["keywords"](col("content"))) \
                    .withColumn("embedding", transformation_udfs["embedding"](col("content"))) \
                    .withColumn("category", transformation_udfs["category"](col("content"))) \
                    .withColumn("company", col("source_site")) \
                    .drop("source_site")

# def load_to_target(batch_df, epoch_id):
#     # 변환된 데이터를 대상 시스템으로 적재
#     records = batch_df.toJSON().collect()
#     headers = {'Content-Type': 'application/json'}
    
#     for record in records:
#         record_dict = json.loads(record)
#         response = requests.post(
#             TARGET_ENDPOINT,
#             data=record, 
#             headers=headers
#         )
        
#         load_status = f"{'적재 성공' if response.status_code == 200 else '적재 실패'}: {record_dict['title']}"
        
#         print(load_status)
#         if response.status_code != 200:
#             print(response.text)

                    
def load_to_target(batch_df, epoch_id):
    # url 기준 중복 데이터 삭제
    batch_df = batch_df.dropDuplicates(["url"])
    # 변환된 데이터를 대상 시스템으로 적재 (parquet 형식으로 저장)
    batch_df = batch_df.withColumn("keywords", col("keywords").cast(StringType())) \
                       .withColumn("embedding", col("embedding").cast(StringType()))
    batch_df.write.mode("overwrite").parquet("file:///workspace/saffy_pjt_news/data/crawling/realtime.parquet")

def start_etl_pipeline(transformed_df):
    # ETL 파이프라인 실행
    query = transformed_df.writeStream \
        .foreachBatch(load_to_target) \
        .start()
    return query

def main():
    # ETL 파이프라인 초기화 및 실행
    spark = initialize_spark_session()

    # 소스 데이터 스키마 정의
    source_schema = define_source_schema()

    # 소스 데이터 스트림 생성
    source_stream = create_source_stream(spark, source_schema)

    # 데이터 변환을 위한 UDF 함수 등록
    transformation_udfs = register_transformation_udfs()

    # 데이터프레임 변환 처리
    transformed_df = transform_dataframe(source_stream, transformation_udfs)
    # print(transformed_df)
    
    # ETL 파이프라인 실행
    query = start_etl_pipeline(transformed_df)
    query.awaitTermination()

if __name__ == "__main__":
    main()
