
<div align="center">
  <h1> Django를 사용한 backend 시스템 구축 </h1>
  

 
 
  
 
  
</div> 

  ## 프로젝트 배경 
   - 본 서비스는 크라우드 펀딩 기능을 제공합니다. 게시자는 크라우드 펀딩을 받기위한 상품(=게시물)을 등록합니다.
   - 유저는 해당 게시물의 펀딩하기 버튼을 클릭하여 해당 상품 ‘1회펀딩금액’ 만큼 펀딩합니다.
  <br>
  
  ## 프로젝트 조건 과 분석
  ### 요구사항
  - *상품을 등록합니다.*
    - *제목, 게시자명, 상품설명, 목표금액, 펀딩종료일, 1회펀딩금액로 구성.  *
    > 상품등록을 위해 먼저 DB(postgresql)를 Django에 연결  
    > 제목, 게시자명, 상품설명, 목표금액, 펀딩종료일, 1회펀딩금액을 입력하면 DB에 등록된다  
    > db값을 직접 넣을수있는데 현재 펀드금액(fund_now)은 반드시 0으로 들어가게 만들었다(달성률,참여인원등도 자동으로 0이된다)  

  - *상품을 수정합니다.*
    - *단, 모든 내용이 수정 가능하나 '목표금액'은 수정이 불가능합니다.*
    > html에선 DB의 기존 값을 불러와 필요한 부분 수정, json api에선 전부 다 써서 수정  
    > 수정을 하기위해 해당 id의 데이터를 불러와 값을 변경하고 save했다  
    > 목표금액이 입력되어도 수정 부분에서 목표금액부분을 수정되지 않게 했다  

  - *상품을 삭제합니다.*
    - *DB에서 삭제됩니다.*
    > filter를 사용해 해당 id의 데이터를 제거

  - *상품 리스트 가져옵니다.*
    - *제목, 게시자명, 총펀딩금액, 달성률 및 D-day(펀딩 종료일까지) 가 포함되어야 합니다. *
    > DB의 전체 데이터를 가져온 후 serializers(필요한 field만) 사용해 제목, 게시자명, 총펀딩금액, 달성률 및 D-day만 가져온다  
    > 입력된 데이터 외에 달성률, 참여인원, d-day등의 계산을 리스트를 불러올때 하게 했다(상품 하나하나에서 하면 너무 비효율적이고, 실시간적인 값을 볼 수 없다 다만 리스트가 많을 경우  속도가 느려질 수 있다)
   
  - 상품 검색 기능 구현
    - (상품 리스트 API 에 ?search=취미 조회 시 ,제목에  ‘내 취미 만들..’  ‘취미를 위한 ..’ 등 검색한 문자 포함된 상품 리스트만 조회)
    > title__icontains을 사용해 title에 값이 포함되어있는 상품 리스트를 불러온다 (icontains를 사용하지않으면 완전히 같은것만 가져온다)  
    > if를 사용해 search값이 존재하면 검색어가 포함된 상품 리스트를 가져오고 없으면 기본 상품 리스트를 가져온다
   
  - 상품 정렬 기능 구현
    - 생성일기준, 총펀딩금액 두 가지 정렬이 가능해야합니다. 
    - ?order_by=생성일 / ?order_by=총펀딩금액
    - (달성률: 1,000,000원 목표금액 일때,  총 펀딩금액이 5,000,000원 이면 500%, 소수점 무시)
    > order_by를 사용해 DB를 정렬시켜 가져온다 -를 붙여 역순도 동작하게 했다  
    > if를 사용해 order_by가 존재하면 검색어가 포함된 상품 리스트를 가져오고 없으면 기본 상품 리스트를 가져온다

  - 상품 상세 페이지를 가져옵니다.
    - 제목, 게시자명, 총펀딩금액, 달성률, D-day(펀딩 종료일까지), 상품설명, 목표금액  및 참여자 수 가 포함되어야 합니다.
    > id값을 입력받으면 해당하는 상품을 보여준다 리스트와 마찬가지로 serializers를 사용해서 제목, 게시자명, 총펀딩금액, 달성률, D-day(펀딩 종료일까지), 상품설명, 목표금액  및 참여자 수만 가져온다  
    > if를 사용해 id가 존재하면 해당 상품의 상세페이지를 보여준다 없으면 기본 상품 리스트를 가져온다

  ### 필수 기술요건
  - Django ORM or SQLAlchemy 등 ORM을 사용하여 구현.
  > ORM은 Object-Relation Mapping으로 객체와 연결해 테이블에 CRUD를 할때 sql query문을 사용하지 않고 가능하게 하는것  
  > Django ORM을 사용하기위해 DB를 연결하기위한 model (Posts)를 구현했고 posts.object를 활용해 API를 구현했다  
  - REST API 로 구현(Json response).  
  > REST API를 아직 정확히 알지 못한다 깔끔하고 사용하기 좋게 만든다는것 정도로 최대한 CRUD를 이용해 구현했다  
  - RDBMS 사용 (SQLite, PostgreSQL 등).  
  > PostgreSQl을 사용했다  
  - Backend 이외의 요소 개발 하지 않음(html, css, js 등)  
  - 개발 범위에 제외된다는 의미이며, 구현시에 불이익은 없습니다. 다만, 평가에 이점 또한 없습니다.  
  > Django와 ORM이나 이런것도 어떻게 사용하는지 아예 몰라 처음엔 눈으로 볼 수있는 HTML로 만들었습니다 뒤늦게 만들 필요가 없다는 걸 깨닫고 rest_framework를 사용했습니다 결론적으로 json api와 html api두가지를 

  
  ## JSON API
  ### 상품 리스트 가져오기    
  - ![image](https://user-images.githubusercontent.com/86823305/164138583-3e2733d2-df11-4c93-b268-498e3ad489e9.png)
  - 상품의 리스트를 가져온 화면으로(api/posts) 제목(title), 게시자명(uploader), 총펀딩금액(fund_now), 달성률(percent_now), D-day(end_day) 가 포함되어있다
    
  ### 상품 리스트 검색 
  - ![image](https://user-images.githubusercontent.com/86823305/164144444-a2e36666-d568-4994-babb-31bf41f4fb4f.png)
  - ![image](https://user-images.githubusercontent.com/86823305/164144466-0caf962c-f6cc-4c56-aab6-6d89f0c73a21.png)
  - 위의 사진처럼 (api/posts?search=값)을 통해 쿼리 값이 들어간 title을 검색 할 수 있다 
    
  ### 상품 리스트 정렬
  - ![image](https://user-images.githubusercontent.com/86823305/164144501-e5d52a1c-dbe1-43a1-bea6-5ada56f51f85.png)
  - ![image](https://user-images.githubusercontent.com/86823305/164144520-00854d00-058d-42ef-97d5-047075b10c42.png)
  - 위의 사진처럼 (api/posts?order_by=값)을 통해 정렬을 할수 있다 현재 총펀딩금액, -총펀딩금액 , 생성일, -생성일 네가지가 가능하다
    
  ### 상품 등록
  - ![image](https://user-images.githubusercontent.com/86823305/164141349-97ddfb6b-438b-4126-a1c5-7f431972849c.png)
  - 하단에 보면 post를 할 수 있는 칸이있는데 상품 리스트를 띄워 둔 상태로 post를 하면 새로운 상품을 추가 할 수 있다.
  - 새로운 글을 등록시 제목, 게시자명, 상품설명, 목표금액, 펀딩종료일(ex 2022-05-05), 1회펀딩금액을 입력하면 된다
  - []안에 여러 글을 넣으면 한번에 여러 글을 등록할 수 있다 
    
  ### 상품 상세 페이지
  - ![image](https://user-images.githubusercontent.com/86823305/164144553-81b47aac-52a5-43d7-a6d6-cff46778df11.png)
  - ![image](https://user-images.githubusercontent.com/86823305/164144568-19023f3f-8b6a-4233-a0cc-5d53158ea0a9.png)
  - 상품의 상세 페지이로 (api/posts/<id>) 제목(title), 게시자명(uploader), 총펀딩금액(fund_now), 달성률(percent_now), D-day(end_day), 상품설명(product_desc), 목표금액(target)  참여자 수(peoplecount)가 포함되어있다
  
  ### 상품 수정
  - ![image](https://user-images.githubusercontent.com/86823305/164142113-8ef92ea9-b68d-4ab6-a8f9-2c583dcc4b2c.png)
  - 상품 상세 페이지에 들어온상태로 상품을 등록하는 것처럼 post를 하면 현재 글이 수정이된다
  - ![image](https://user-images.githubusercontent.com/86823305/164142809-c05f1a83-2703-4f0e-a829-7fd765b3ea9f.png)
  - 단 목표금액은 바뀌지않는다
  
  ### 상품 삭제
  - ![image](https://user-images.githubusercontent.com/86823305/164144627-25e322c3-8657-424b-a194-e05337dbf18d.png)
  - 상품 상세 페이지에서 DELETE 버튼을 누르게되면 해당 글이 삭제된다
  - ![image](https://user-images.githubusercontent.com/86823305/164143062-bc766671-b539-4865-93d3-5728295ba55d.png)
  
  ### 상품 펀딩하기
  - ![이미지 1129](https://user-images.githubusercontent.com/86823305/164144799-73c23dfc-ae03-433e-8e29-84b1cb481162.png)
  - (api/posts/<id>?funding=<num>) 해당 id를 가진 글에 funding을 요청하면 funding의 값만큼 펀딩한다 사진에선 알 수없지만 1회 펀딩 금액은 150이었고 2회의 펀딩으로 2100=>2300이 되었다
  - ![image](https://user-images.githubusercontent.com/86823305/164144655-66553db4-e3a8-4bb8-a5b4-cdb964cc9555.png)
  - ![image](https://user-images.githubusercontent.com/86823305/164144688-fcb50b29-2143-4d89-9532-12ab2b0c0ed3.png)



  ## HTML API
  ### 상품 리스트 가져오기    
  - ![image](https://user-images.githubusercontent.com/86823305/164155432-7be3a728-19cd-468b-85f6-167e1ae94185.png)
  - 상품의 리스트를 가져온 화면으로(/) 제목(title), 게시자명(uploader), 총펀딩금액(fund_now), 달성률(percent_now), D-day(end_day) 가 포함되어있다
    
  ### 상품 리스트 검색 
  - ![image](https://user-images.githubusercontent.com/86823305/164155490-cf04541e-98a0-482b-a16d-cd9a118fbf96.png)
  - ![image](https://user-images.githubusercontent.com/86823305/164156108-5dafa821-94ad-4d30-9a05-5dba576ae7ae.png)
  - 값을 입력하고 버튼을 이용해(api/posts?search=값) title을 검색 할 수 있다 
    
  ### 상품 리스트 정렬
  - ![image](https://user-images.githubusercontent.com/86823305/164156190-6fe2d3a4-4d42-4855-87f8-dafa74c8a31d.png)
  - ![image](https://user-images.githubusercontent.com/86823305/164156214-7d2396b8-202e-40a8-a565-bd304fc8769d.png)
  - 값을 입력하고 버튼을 이용해(api/posts?order_by=값)을 통해 정렬을 할수 있다 현재 총펀딩금액, -총펀딩금액 , 생성일, -생성일 네가지가 가능하다

  ### 상품 등록
  - ![image](https://user-images.githubusercontent.com/86823305/164156267-ca08121a-8e86-4b79-98cf-d3a19ed28a70.png)
  - Create 버튼으로 새로 만들 수 있다 (api/create)
  - ![image](https://user-images.githubusercontent.com/86823305/164156289-261bce29-117b-429d-a181-537b1182498e.png)
  - ![image](https://user-images.githubusercontent.com/86823305/164156343-4e6aabff-8528-4b81-96a2-54eca913c6ed.png)
  - ![image](https://user-images.githubusercontent.com/86823305/164156363-0e0e1296-e831-416f-af75-01b1d6505b6e.png)
  - 새로운 글을 등록시 제목, 게시자명, 상품설명, 목표금액, 펀딩종료일(ex 2022-05-05), 1회펀딩금액을 입력하면 된다
    
  ### 상품 상세 페이지
  - ![image](https://user-images.githubusercontent.com/86823305/164156599-962aa44e-5bc6-4be8-8321-23ab0040f725.png)
  - 리스트에서 해당 글을 클릭 (api/read/<id>)하면 상세 페이지를 볼 수 있다
  - 제목(title), 게시자명(uploader), 총펀딩금액(fund_now), 달성률(percent_now), D-day(end_day), 상품설명(product_desc), 목표금액(target)  참여자 수(peoplecount)가 포함되어있다
  
  ### 상품 수정
  - ![image](https://user-images.githubusercontent.com/86823305/164156892-f3892f3a-95a7-4088-a191-86c681c16242.png)
  - 상품 상세 페이지에 들어온상태로 update 버튼(api/update/id)으로 수정 할 수 있다 
  - ![image](https://user-images.githubusercontent.com/86823305/164156972-6952c535-9de3-450a-a4e9-20d52bf957cf.png)
  - 기존값을 불러들여 수정 할 수 있다 단, 목표금액은 바뀌지않는다
  
  ### 상품 삭제
  - ![image](https://user-images.githubusercontent.com/86823305/164157028-3726d591-5c13-40c4-b135-94617ece552b.png)
  - 상품 상세 페이지에서 DELETE 버튼을 누르게되면 해당 글이 삭제된다
  - ![image](https://user-images.githubusercontent.com/86823305/164157056-69f18114-dc8b-48fc-8de1-310339e2ebb8.png)
  
  ### 상품 펀딩하기
  - ![image](https://user-images.githubusercontent.com/86823305/164157139-db648a99-6ca1-4513-ac88-b8c099cc2992.png)
  - funding 버튼(api/posts/funding/<id>)을 누르면 펀딩을 1회 하게된다
  - ![image](https://user-images.githubusercontent.com/86823305/164157238-9d60ea0b-751d-4adc-8d3d-4572ed863407.png)

  

## 프로젝트 결과 및 회고
  - 상품 등록, 수정 ,삭제 , 리스트 출력(검색,정렬),상세페이지, 펀딩 기능을 가진 api 구현
  - Django ORM , REST API , PostgreSQL 사용
  - Djanog와 RDB가 어떤식으로 연결되고 동작하는지를 배울 수 있었다
