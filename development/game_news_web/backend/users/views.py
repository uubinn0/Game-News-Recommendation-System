from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@csrf_exempt
@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    password_confirm = request.data.get('password_confirm')

    # 비밀번호 확인
    if password != password_confirm:
        return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

    # 사용자 중복 확인
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    # 사용자 생성
    try:
        User.objects.create(
            username=username,
            email=email,
            password=make_password(password)  # 비밀번호 해싱
        )
        return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # 사용자 인증
    user = authenticate(username=username, password=password)
    if user:
        return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User

@api_view(["PUT"])
def update_user_info(request):
    user = request.user  # 인증된 유저
    data = request.data
    order = data.get("order", "remove")
    new_name = data.get("name", "")

    if not new_name:
        return Response({"error": "name 필드는 필수입니다."}, status=400)

    # user.name이 비어 있으면 초기화
    if not user.name:
        user.name = ""

    name_list = user.name.split(',')

    if order == "add":
        # 중복 추가 방지
        if new_name not in name_list:
            name_list.append(new_name)
    elif order == "remove":
        # 값이 리스트에 있으면 제거
        if new_name in name_list:
            name_list.remove(new_name)
        else:
            return Response({"error": f"'{new_name}'은(는) 목록에 없습니다."}, status=400)
    else:
        return Response({"error": "유효하지 않은 order 값입니다. 'add' 또는 'remove'를 사용하세요."}, status=400)

    # 리스트를 문자열로 변환하여 저장
    user.name = ','.join(name_list)
    user.save()

    return Response({"message": "유저 정보가 성공적으로 수정되었습니다."})