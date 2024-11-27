from django.conf import settings
import os
import pandas as pd
from django.http import JsonResponse

def read_article_list(request, category="all", page_num=1, count=100):
    try:
        # 데이터 폴더 경로 설정
        folder_path = os.path.join(settings.BASE_DIR, "data")

        if not os.path.exists(folder_path):
            return JsonResponse({'status': 'error', 'message': '파일 경로가 비어있습니다.'})

        # Parquet 파일 읽기
        parquet_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.parquet')]

        if not parquet_files:
            return JsonResponse({'status': 'error', 'message': 'No Parquet files found in the data folder.'})

        # Parquet 파일을 읽어 DataFrame으로 합치기
        df = pd.concat([pd.read_parquet(file) for file in parquet_files], ignore_index=True)

        # category 필터링
        if category != "all":
            if 'category' not in df.columns:
                return JsonResponse({'status': 'error', 'message': 'Data does not contain a "category" column.'})
            df = df[df['category'] == category]

        # 페이지네이션 처리
        total_records = len(df)
        start_idx = (page_num - 1) * count
        end_idx = start_idx + count
        paged_data = df.iloc[start_idx:end_idx]

        # 데이터가 없는 경우 처리
        if paged_data.empty:
            return JsonResponse({'status': 'success', 'data': [], 'message': 'No more data available.'})

        # 데이터 변환 및 반환
        data = paged_data.to_dict(orient='records')
        return JsonResponse({
            'status': 'success',
            'data': data,
            'total_records': total_records,
            'current_page': page_num,
            'page_size': count
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

from urllib.parse import unquote
def get_news_RAG(request, url):
    try:
    # 데이터 폴더 경로 설정
        while '%' in url:
            url = unquote(url)

        folder_path = os.path.join(settings.BASE_DIR, "data")
        
        if not os.path.exists(folder_path):
            return JsonResponse({'status': 'error', 'message': '파일 경로가 비어있습니다.'})

        # Parquet 파일 읽기
        parquet_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.parquet')]

        if not parquet_files:
            return JsonResponse({'status': 'error', 'message': 'No Parquet files found in the data folder.'})
        # Parquet 파일을 읽어 DataFrame으로 합치기
        df = pd.concat([pd.read_parquet(file) for file in parquet_files], ignore_index=True)
        urls = []
        urls.append(url)
        # print(urls)
        urls.extend(get_top_k_similar_urls(url))
        # print(urls)
        filtered_df = df[df['url'].isin(urls)]
        data = filtered_df.to_dict(orient='records')
        return JsonResponse({
            'status': 'success',
            'data': data
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sentence_transformers import SentenceTransformer

def get_top_k_similar_urls(url, top_k = 5, model_name= "all-MiniLM-L6-v2"):
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
    folder_path = os.path.join(settings.BASE_DIR, "data")

    if not os.path.exists(folder_path):
        return JsonResponse({'status': 'error', 'message': '파일 경로가 비어있습니다.'})

    # Parquet 파일 읽기
    parquet_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.parquet')]
    if not parquet_files:
        return JsonResponse({'status': 'error', 'message': 'No Parquet files found in the data folder.'})

    # Parquet 파일을 읽어 DataFrame으로 합치기
    df = pd.concat([pd.read_parquet(file) for file in parquet_files], ignore_index=True)
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


def push_like(request, url):
    try:
        # URL 디코딩
        while '%' in url:
            url = unquote(url)
        
        # 데이터 폴더 경로 설정
        folder_path = os.path.join(settings.BASE_DIR, "data")
        if not os.path.exists(folder_path):
            return JsonResponse({'status': 'error', 'message': '파일 경로가 비어있습니다.'})

        # Parquet 파일 읽기
        parquet_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.parquet')]
        if not parquet_files:
            return JsonResponse({'status': 'error', 'message': 'No Parquet files found in the data folder.'})

        # 첫 번째 Parquet 파일 선택
        file_name = parquet_files[0]
        df = pd.concat([pd.read_parquet(file) for file in parquet_files], ignore_index=True)

        # 인증된 사용자 정보 가져오기
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated.'})
        
        user_email = user.email
        if not user_email:
            return JsonResponse({'status': 'error', 'message': 'User email not available.'})

        # URL과 같은 행 찾기
        if 'url' not in df.columns or 'likes' not in df.columns:
            return JsonResponse({'status': 'error', 'message': "'url' or 'likes' column not found in the data."})

        matching_rows = df[df['url'] == url]

        if matching_rows.empty:
            return JsonResponse({'status': 'error', 'message': 'No matching URL found in the data.'})

        # likes 열 업데이트
        df.loc[df['url'] == url, 'likes'] = df.loc[df['url'] == url, 'likes'].apply(
            lambda likes: f"{likes},{user_email}" if pd.notnull(likes) and user_email not in likes.split(',') else (
                user_email if pd.isnull(likes) else likes
            )
        )

        # 업데이트된 데이터프레임 저장
        df.to_parquet(file_name, index=False)

        return JsonResponse({'status': 'success', 'message': 'Like added successfully.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
def remove_like(request, url):
    try:
        # URL 디코딩
        while '%' in url:
            url = unquote(url)
        
        # 데이터 폴더 경로 설정
        folder_path = os.path.join(settings.BASE_DIR, "data")
        if not os.path.exists(folder_path):
            return JsonResponse({'status': 'error', 'message': '파일 경로가 비어있습니다.'})

        # Parquet 파일 읽기
        parquet_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.parquet')]
        if not parquet_files:
            return JsonResponse({'status': 'error', 'message': 'No Parquet files found in the data folder.'})

        # 첫 번째 Parquet 파일 선택
        file_name = parquet_files[0]
        df = pd.concat([pd.read_parquet(file) for file in parquet_files], ignore_index=True)

        # 인증된 사용자 정보 가져오기
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated.'})
        
        user_email = user.email
        if not user_email:
            return JsonResponse({'status': 'error', 'message': 'User email not available.'})

        # URL과 같은 행 찾기
        if 'url' not in df.columns or 'likes' not in df.columns:
            return JsonResponse({'status': 'error', 'message': "'url' or 'likes' column not found in the data."})

        matching_rows = df[df['url'] == url]

        if matching_rows.empty:
            return JsonResponse({'status': 'error', 'message': 'No matching URL found in the data.'})

        # likes 열에서 이메일 제거
        df.loc[df['url'] == url, 'likes'] = df.loc[df['url'] == url, 'likes'].apply(
            lambda likes: ','.join([email for email in likes.split(',') if email != user_email]) if pd.notnull(likes) else likes
        )

        # 업데이트된 데이터프레임 저장
        df.to_parquet(file_name, index=False)

        return JsonResponse({'status': 'success', 'message': 'Like removed successfully.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})