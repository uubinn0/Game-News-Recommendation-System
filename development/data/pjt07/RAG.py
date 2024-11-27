import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sentence_transformers import SentenceTransformer

def get_top_k_similar_urls(url, top_k, parquet_file, model_name= "all-MiniLM-L6-v2"):
    """
    주어진 URL의 기사와 Parquet 파일의 데이터프레임에서 유사도가 높은 상위 K개의 URL 반환.

    Args:
        url (str): 기준 기사의 URL.
        top_k (int): 반환할 문서 개수.
        model_name (str): 사용할 임베딩 모델 이름.
        parquet_file (str): Parquet 파일 경로.

    Returns:
        list of str: 유사도가 높은 상위 K개의 기사 URL 리스트.
    """
    # Parquet 파일 로드
    df = pd.read_parquet(parquet_file, engine="pyarrow")

    # 입력 URL과 매칭되는 기준 기사 찾기
    target_row = df[df['url'] == url]
    if target_row.empty:
        raise ValueError(f"URL '{url}'에 해당하는 기사가 데이터프레임에 없습니다.")

    # 기준 기사의 임베딩 추출
    target_embedding = target_row['embedding'].iloc[0]
    
    # target_embedding 타입 확인 (문자열인 경우 변환)
    if isinstance(target_embedding, str):
        target_embedding = np.fromstring(target_embedding[1:-1], sep=',')  # 문자열을 리스트로 변환
    elif not isinstance(target_embedding, np.ndarray):
        raise ValueError("기준 기사의 임베딩이 유효하지 않습니다.")
    
    # 임베딩 확인 (None 처리 방지)
    if not isinstance(target_embedding, np.ndarray):
        raise ValueError("기준 기사의 임베딩이 유효하지 않습니다.")

    # 모든 기사 임베딩 추출 (문자열인 경우 변환)
    def convert_embedding(embedding):
        if isinstance(embedding, str):
            return np.fromstring(embedding[1:-1], sep=',')  # 문자열을 리스트로 변환
        elif isinstance(embedding, np.ndarray):
            return embedding
        else:
            raise ValueError("임베딩 데이터 형식이 잘못되었습니다.")
    
    all_embeddings = np.vstack(df['embedding'].apply(convert_embedding).values)

    # 코사인 유사도 계산
    similarities = cosine_similarity([target_embedding], all_embeddings).flatten()

    # 유사도를 기준으로 정렬하고 상위 K개의 인덱스 선택
    top_k_indices = np.argsort(similarities)[::-1][1:top_k + 1]  # 1부터 시작해 자기 자신 제외

    # 상위 K개의 URL 반환
    top_k_urls = df.iloc[top_k_indices]['url'].tolist()

    return top_k_urls



# 테스트 예시
if __name__ == "__main__":
    test_url = "https://m.thisisgame.com/webzine/news/nboard/263/?page=11&n=197292"
    top_k = 5
    # model_name = "all-MiniLM-L6-v2"
    parquet_file = "/workspace/saffy_pjt_news/data/crawling/processed.parquet"

    try:
        similar_urls = get_top_k_similar_urls(test_url, top_k, parquet_file)
        print("Top K Similar URLs:")
        for i, url in enumerate(similar_urls, 1):
            print(f"{i}. {url}")
    except ValueError as e:
        print(f"Error: {e}")
