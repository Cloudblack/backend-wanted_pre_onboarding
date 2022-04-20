
<div align="center">
  <h1> Django를 사용한 backend 시스템 구축 </h1>
  

 
 
  
 
  
</div> 

  ### 프로젝트 배경 
   - 본 서비스는 크라우드 펀딩 기능을 제공합니다. 게시자는 크라우드 펀딩을 받기위한 상품(=게시물)을 등록합니다.
   - 유저는 해당 게시물의 펀딩하기 버튼을 클릭하여 해당 상품 ‘1회펀딩금액’ 만큼 펀딩합니다.
  <br>
  
  ### 프로젝트 조건
  - 요구사항
  - 상품을 등록합니다.
    - 제목, 게시자명, 상품설명, 목표금액, 펀딩종료일, 1회펀딩금액로 구성.

  - 상품을 수정합니다.
    - 단, 모든 내용이 수정 가능하나 '목표금액'은 수정이 불가능합니다.

  - 상품을 삭제합니다.
    - DB에서 삭제됩니다.

  - 상품 목록을 가져옵니다.
    - 제목, 게시자명, 총펀딩금액, 달성률 및 D-day(펀딩 종료일까지) 가 포함되어야 합니다.
  - 상품 검색 기능 구현
    - (상품 리스트 API 에 ?search=취미 조회 시 ,제목에  ‘내 취미 만들..’  ‘취미를 위한 ..’ 등 검색한 문자 포함된 상품 리스트만 조회)
  - 상품 정렬 기능 구현
    - 생성일기준, 총펀딩금액 두 가지 정렬이 가능해야합니다. 
    - ?order_by=생성일 / ?order_by=총펀딩금액
    - (달성률: 1,000,000원 목표금액 일때,  총 펀딩금액이 5,000,000원 이면 500%, 소수점 무시)

  - 상품 상세 페이지를 가져옵니다.
    - 제목, 게시자명, 총펀딩금액, 달성률, D-day(펀딩 종료일까지), 상품설명, 목표금액  및 참여자 수 가 포함되어야 합니다.

  - 필수 기술요건
    - Django ORM or SQLAlchemy 등 ORM을 사용하여 구현.
    - REST API 로 구현(Json response).
    - RDBMS 사용 (SQLite, PostgreSQL 등).
    - Backend 이외의 요소 개발 하지 않음(html, css, js 등)
    - 개발 범위에 제외된다는 의미이며, 구현시에 불이익은 없습니다. 다만, 평가에 이점 또한 없습니다.

  
  ### JSON API
  - 상품 리스트 가져오기    
    - ![image](https://user-images.githubusercontent.com/86823305/164138583-3e2733d2-df11-4c93-b268-498e3ad489e9.png)
    - 상품의 리스트를 가져온 화면으로(api/posts) 제목(title), 게시자명(uploader), 총펀딩금액(fund_now), 달성률(percent_now), D-day(end_day) 가 포함되어있다
    
  - 상품 리스트 검색 
    - ![image](https://user-images.githubusercontent.com/86823305/164144444-a2e36666-d568-4994-babb-31bf41f4fb4f.png)
    - ![image](https://user-images.githubusercontent.com/86823305/164144466-0caf962c-f6cc-4c56-aab6-6d89f0c73a21.png)
    - 위의 사진처럼 (api/posts?search=값)을 통해 쿼리 값이 들어간 title을 검색 할 수 있다 
    
  - 상품 리스트 정렬
    - ![image](https://user-images.githubusercontent.com/86823305/164144501-e5d52a1c-dbe1-43a1-bea6-5ada56f51f85.png)
    - ![image](https://user-images.githubusercontent.com/86823305/164144520-00854d00-058d-42ef-97d5-047075b10c42.png)
    - 위의 사진처럼 (api/posts?order_by=값)을 통해 정렬을 할수 있다 현재 총펀딩금액, -총펀딩금액 , 생성일, -생성일 네가지가 가능하다
    
  - 상품 등록
    - ![image](https://user-images.githubusercontent.com/86823305/164141349-97ddfb6b-438b-4126-a1c5-7f431972849c.png)
    - 하단에 보면 post를 할 수 있는 칸이있는데 상품 리스트를 띄워 둔 상태로 post를 하면 새로운 상품을 추가 할 수 있다.
    - 새로운 글을 등록시 제목, 게시자명, 상품설명, 목표금액, 펀딩종료일(ex 2022-05-05), 1회펀딩금액을 입력하면 된다
    - []안에 여러 글을 넣으면 한번에 여러 글을 등록할 수 있다 
    
  - 상품 상세 페이지
    - ![image](https://user-images.githubusercontent.com/86823305/164144553-81b47aac-52a5-43d7-a6d6-cff46778df11.png)
    - ![image](https://user-images.githubusercontent.com/86823305/164144568-19023f3f-8b6a-4233-a0cc-5d53158ea0a9.png)
    - 상품의 상세 페지이로 (api/posts/<id>) 제목(title), 게시자명(uploader), 총펀딩금액(fund_now), 달성률(percent_now), D-day(end_day), 상품설명(product_desc), 목표금액(target)  참여자 수(peoplecount)가 포함되어있다
  
  - 상품 수정
    - ![image](https://user-images.githubusercontent.com/86823305/164142113-8ef92ea9-b68d-4ab6-a8f9-2c583dcc4b2c.png)
    - 상품 상세 페이지에 들어온상태로 상품을 등록하는 것처럼 post를 하면 현재 글이 수정이된다
    - ![image](https://user-images.githubusercontent.com/86823305/164142809-c05f1a83-2703-4f0e-a829-7fd765b3ea9f.png)
    - 단 목표금액은 바뀌지않는다
  
  - 상품 삭제
    - ![image](https://user-images.githubusercontent.com/86823305/164144627-25e322c3-8657-424b-a194-e05337dbf18d.png)
    - 상품 상세 페이지에서 DELETE 버튼을 누르게되면 해당 글이 삭제된다
    - ![image](https://user-images.githubusercontent.com/86823305/164143062-bc766671-b539-4865-93d3-5728295ba55d.png)
  
  - 상품 펀딩하기
    - ![이미지 1129](https://user-images.githubusercontent.com/86823305/164144799-73c23dfc-ae03-433e-8e29-84b1cb481162.png)
    - (api/posts/<id>?funding=<num>) 해당 id를 가진 글에 funding을 요청하면 funding의 값만큼 펀딩한다 사진에선 알 수없지만 1회 펀딩 금액은 150이었고 2회의 펀딩으로 2100=>2300이 되었다
    - ![image](https://user-images.githubusercontent.com/86823305/164144655-66553db4-e3a8-4bb8-a5b4-cdb964cc9555.png)
    - ![image](https://user-images.githubusercontent.com/86823305/164144688-fcb50b29-2143-4d89-9532-12ab2b0c0ed3.png)



  ### HTML API
  ## 프로젝트 결과
  - 실시간 ETL data pipeline 구축
  - 입력되는 데이터 중 미리 설정된 필요한 데이터만 클라우드(S3)에 저장할 수 있다.
  - 데이터 변환 및 압축을 통해 89.6%의 데이터 용량 감소로 비용을 절약 할 수 있다.
    - Original data 2495kb ⇒ trans data 261kb
  - SQL 쿼리를 이용 해 압축된 데이터를 복원하여 제공하는 API 구현했다.
  <br>
  
  ### 파일
  - pipeline.py : 변환, 압축 등에 사용된 코드 모음 
  - kinesis_producer.py : kinesis를 통해 샘플 데이터를 보내는 역할
  - kinesis_consumer.py : kinesis로 데이터를 받아 S3에 올려주는 역할
  - lambda_test.py : lambda에 들어가는 코드 (pipeline.py 필요)
