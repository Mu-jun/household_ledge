# household_ledge
## 개발환경
- OS : WINDOWS10 22H2
- DB : MYSQL 5.7.40
- Framework : django 4.1
- python : 3.9

## ./env/config.py
"""
from datetime import timedelta

SECRET_KEY = 장고 SECRET_KEY
PW_HASH_KEY = b"b78af" # ex
HASH_KEY = b"hbn9" # ex

TOKEN_MAXAGE = timedelta(hours=4) # 리프레시 토큰 유효기간
"""

## ./env/db.py
CONFIG = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "데이터베이스명",
        "USER": "유저명",
        "PASSWORD": "비밀번호",
        "CHARSET": "utf8mb4",
        "COLLATION": "utf8mb4_general_ci",
    }
}


## 2일차
- requirements
- 테이블 수정
- 가계부 CRUD
- 북마크

## 3일차
- 테이블 수정(가계부&단축url 병합)
- 회원인증(jwt)
- 단축url

## D-day
- 테스트 및 오류 수정