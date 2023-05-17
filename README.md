
## README

### 언어 프레임워크

사용언어는 python, 프레임워크는 django, django rest framework 사용
테스트 용이를 위해 debug=True로 설정한다

### 실행 방법

```
# 서버 실행
docker-compose up

# unittest 실행
docker-compose -f docker-compose.test.yaml up
```

### API

제공되는 API는 아래와 같다
- /api/v1/products

  GET/POST

  리소스 포멧과 동일

- /api/v1/products/{:id}

  GET/PUT/PATCH/DELETE

  리소스 포멧과 동일

- /api/v1/account

  POST

  POST포멧:
  ```
  {
      "phone_num" : str,
      "password" : str
  }
  ```

- /api/v1/token

  POST/DELETE

  DELETE시 아래 포멧으로 body를 입력해야 된다
  ```
  {
      "token": str
  }
  ```

product 리소스 포맷:
```
{
    "id": int,
    "category": str,
    "price": int,
    "cost": int,
    "name": str,
    "description": str,
    "barcode": str,
    "expiration_date": str in date format,
    "size": "S" or "L"
}
```

account 리소스 포멧:
```
{
    "id": int,
    "phone_num": str ^010\d{8}$ pattern ex) 01011112222
}
```

Response 포맷:
```
{
    "meta": {
        "code": int,
        "message": str
    },
    "data": {
        ...
    }
}
```

LIST GET 포멧
```
{
    "meta": {
        "code": int,
        "message": str
    },
    "data": {
        {
            "next": str(next cursor link),
            "previus": str(previous cursor link),
            "results": [
                ...
            ]
        }
    }
}
```

검색 방법:

/api/v1/products?query=<query keywords>

초성검색을 지원한다


### Authentication

Bearer 토큰 방식을 사용한다

즉 해더에 `Authorization : Bearer <Token>` 추가 필요

토큰은 1시간 timeout이 있다. 별도 refresh 토큰은 발행하지 않는다

/api/v1/token POST로 로그인이(토큰생성) 가능하고 DELETE로 로그아웃이 된다


### 디비

디비 MySQL 5.7

사용된 디비정보:
- username: mysql
- password: password
- db name: mycafe

DDL 덤프파일: `mycafe.sql`

디비 덤프 로드 방법:
```
mysql -h localhost -u mysql -p mycafe < mycafe.sql
```

django unittest 테스트 하기에 디비 사용자에 권한 설정이 필요하다
```
GRANT ALL ON *.* TO 'mysql'@'localhost';
FLUSH PRIVILEGES;
```

### 테스트 케이스 파일경로

- mycafe/tests.ppy
- menu/tests.py
- account/tests.py
