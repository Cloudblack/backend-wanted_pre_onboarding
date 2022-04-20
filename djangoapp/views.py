from http.client import HTTPResponse
from django.http import JsonResponse
from sre_constants import SUCCESS
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Posts
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PostsSerializer ,PostsSerializer_list,PostsSerializer_detail
import datetime

class PostsListAPI(APIView): #json api view
    def get(self, request,id=None):                 
        if 'order_by' in request.GET: # order_by를 받아 정렬한다          
            if request.GET['order_by']=='총펀딩금액':
               post_list =Posts.objects.all().order_by('fund_now') #전체를 불러와 정렬
            elif request.GET['order_by']=='-총펀딩금액':
                post_list =Posts.objects.all().order_by('-fund_now')
            elif request.GET['order_by']=='생성일':
                post_list =Posts.objects.all().order_by('created_at')
            elif request.GET['order_by']=='-생성일':
                post_list =Posts.objects.all().order_by('-created_at')
        elif 'search' in request.GET: #search를 받아 제목에서 검색한다
            post_list =Posts.objects.filter(title__icontains=request.GET['search'])
        elif 'funding' in request.GET: #funding 숫자만큼 펀딩을한다
            if id != None: #id 가 있을때만 그 게시글을 펀딩
                get_posts = Posts.objects.get(id=id)
                fund_now=get_posts.one_fund*int(request.GET['funding'])
                get_posts.fund_now+=fund_now                
                get_posts.save()
                serializer = PostsSerializer_detail(get_posts)
                return Response(serializer.data)#redirect('/')
            return 
        else:
            post_list = Posts.objects.all()  #위의 조건이 아무것도 없을때 그냥 전체를 불러옴              
        if id !=None: #id가 입력되면 그 게시글을 상세보기
            post_list = Posts.objects.get(id=id)
            serializer = PostsSerializer_detail(post_list)
            return Response(serializer.data)   
        #리스트를 불러올때 남은 일수, 참여인원, 달성률을 수정한다 
        for get_post in post_list: #쿼리셋을 하나씩불러와서 수정
            #남은 일수 수정
            now = datetime.datetime.now().date()
            td=datetime.datetime.strptime(str(get_post.target_day)[:10], '%Y-%m-%d').date()
            get_post.end_day=(td-now).days     
            #참여인원 수정
            people_now=int(get_post.fund_now/get_post.one_fund)
            fund_now=int(get_post.fund_now/get_post.target*100)
            get_post.Peoplecount=people_now
            #달성률 수정
            get_post.percent_now=f"{fund_now}%"  
            
            get_post.save()              
        serializer = PostsSerializer_list(post_list, many=True)
        return Response(serializer.data)
    def delete(self,request,id): #입력된 id의 글을 삭제         
        Posts.objects.filter(id=id).delete()
        return redirect('/')
    def post(self,request,id=None):#업로드 ,하나라서 대괄호가 필요없다
        if id !=None: #id가 입력되면 수정을 한다
            get_posts=Posts.objects.get(id=id)          
            get_posts.uploader=request.data['uploader']
            get_posts.title=request.data['title']
            get_posts.one_fund=request.data['one_fund'] 
            get_posts.product_desc=request.data['product_desc']   
            get_posts.save()      
            serializer = PostsSerializer_detail(get_posts)
            return Response(serializer.data)#redirect('/')
            
        #새 글을 추가할때 강제로 현재 펀드금액은 0으로 초기화
        for get_post in request.data:
            get_post['fund_now']=0
        serializer = PostsSerializer(data = request.data, many=True) #입력된값    
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data ,status=200)
""" 데이터 추가 예시
원본
{
        "id": 43,
        "title": "골드",
        "uploader": "장사꾼",
        "product_desc": "신용거래",
        "target": 20000,
        "fund_now": 0,
        "end_day": 51,
        "target_day": "2022-06-11T00:00:00+09:00",
        "one_fund": 150,
        "created_at": "2022-04-20T00:11:39.930293+09:00",
        "updated_at": "2022-04-20T11:13:10.634119+09:00",
        "published_at": null,
        "Peoplecount": 0,
        "percent_now": "0%"
    }
추가할때 필요한것
    [{
       
        "title": "골드",
        "uploader": "장사꾼",
        "product_desc": "신용거래",
        "target": 20000,               
        "target_day": "2022-06-11",
        "one_fund": 150
        
    }]
"""
# JSON API        
#-------------------------------------------------------------------------------
# HTML

post=Posts() #table

def HTMLTemplate(articleTag, id=None): #자주사용할 템플릿
    contextUI = ''
    if id != None: #게시글에 들어갔을때만 작동
        #펀딩 버튼, 삭제버튼, 수정버튼
        contextUI = f'''
            <li>
                <form action="/funding/{id}" method="get">
                        <input type="hidden" name="id" value={id}>
                        <input type="submit" value="funding">
                    </form>
            </li>
            <li>
                <form action="/delete/" method="post">
                    <input type="hidden" name="id" value={id}>
                    <input type="submit" value="delete">
                </form>
            </li>
            <li><form action="/update/{id}" method="get">
                    <input type="hidden" name="id" value={id}>
                    <input type="submit" value="update">
                </form>
            </li>
          
        '''
   #글 작성 버튼, 검색, 정렬
    return f'''
    <html>
    <body>
        <h1><a href="/">FUNDING</a></h1>
        
        {articleTag}
        <ul>
            {contextUI}
            <form action="/create/" method="get">
            <input type="submit" value="create">                    
            </form>    
            
            <form action="" method="get">
                <p><input type="text" name="search" placeholder="검색"><input type="submit"></p>
            </form>
            <form action="" method="get">
                <p><input type="text" name="order_by" placeholder="정렬= 총펀딩금액,생성일"><input type="submit"></p>
            </form>
            
            
        </ul>
        
    </body>
    </html>
    '''
#기본 화면, 글 목록
def index(request,search=None):     
    print(request.GET)   
    if 'search' in request.GET:#search 가 입력되면 검색
        print(request.GET)
        post_list =Posts.objects.filter(title__icontains=request.GET['search'])
    elif 'order_by' in request.GET: #order_by가 입력되면 정렬       
            if request.GET['order_by']=='총펀딩금액':
               post_list =Posts.objects.all().order_by('fund_now')
            elif request.GET['order_by']=='-총펀딩금액':
                post_list =Posts.objects.all().order_by('-fund_now')
            elif request.GET['order_by']=='생성일':
                post_list =Posts.objects.all().order_by('created_at')
            elif request.GET['order_by']=='-생성일':
                post_list =Posts.objects.all().order_by('-created_at')
    else:        
        post_list=Posts.objects.all()
    article='<p>제목 , 작성자 , 목표금액 , 달성률 , D-day</p>'
    for get_post in post_list: #목록 작성
        #남은 일수                
        now = datetime.datetime.now().date()
        td=datetime.datetime.strptime(str(get_post.target_day)[:10], '%Y-%m-%d').date()
        get_post.end_day=(td-now).days
        #달성률
        get_post.percent_now=int(list({get_post.fund_now})[0]/list({get_post.target})[0]*100)
        get_post.save() 
        # 글로 하나씩 작성
        article += f'<li><a href="/read/{get_post.id}">{get_post.title}, {get_post.uploader}, {get_post.target}, {get_post.percent_now}%, {get_post.end_day}</a></li>'
    
    #html 템플릿에 article을 넣어서만듬
    return HttpResponse(HTMLTemplate(article))


   
def read(request, id): #id를 입력해 상세보기
    get_post=Posts.objects.get(id=id)
    #참여인원수
    get_post.Peoplecount=get_post.fund_now/get_post.one_fund
    get_post.save()
    #상세보기
    article = f'''<h2>제목 {get_post.title}</h2>
    <p>작성자 {get_post.uploader}</p>
    <p>목표 금액 {get_post.target}</p>
    <p>달성률 {get_post.percent_now}%</p>
    <p>D-day {get_post.end_day}</p>
    <p>1회 펀금 요금 {get_post.one_fund}</p>
    <p>참여인원 {int(get_post.Peoplecount)}명</p>
    <p>{get_post.product_desc}</p>    
    ''' 
    return HttpResponse(HTMLTemplate(article, id))


@csrf_exempt
def create(request):# 글작성
    #GET요청을 받을시 입력하는 란을 생성
    if request.method == 'GET':
        article = '''
            <form action="/create/" method="post">
                <p><input type="text" name="uploader" placeholder="작성자"></p>
                <p><input type="text" name="title" placeholder="제목"></p>
                <p><input type="int" name="target" placeholder="목표금액"></p>
                <p><input type="text" name="target_day" placeholder="펀딩종료일"></p>
                <p><input type="int" name="one_fund" placeholder="1회 펀드금액"></p>                  
                <p><textarea name="product_desc" placeholder="설명"></textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    #POST요청을 받을 시 입력받은 값을 table에 저장
    elif request.method == 'POST':        
        post.uploader=request.POST['uploader']
        post.title=request.POST['title']     
        post.target=request.POST['target']   
        post.target_day=request.POST['target_day']  
        post.one_fund=request.POST['one_fund'] 
        post.product_desc=request.POST['product_desc']        
        post.fund_now=0     
        post.save()        
        return redirect('/')

@csrf_exempt
def update(request,id): #글 수정
    #GET 요청시 이미 써놨던 글을 수정할 수 있게 생성
    if request.method == 'GET':                  
        print(id)   
        get_post=Posts.objects.get(id=id)
    
        article = f'''
            <form action="/update/{id}/" method="post">
                <p><input type="text" name="uploader" placeholder="작성자" value={get_post.uploader}></p>
                <p><input type="text" name="title" placeholder="제목" value={get_post.title}></p>
                <p><input type="text" name="target_day" placeholder="펀딩종료일" value={get_post.end_day}></p>
                <p><input type="int" name="one_fund" placeholder="1회 펀드금액" value={get_post.one_fund}></p>                  
                <p><textarea name="product_desc" placeholder="설명">{get_post.product_desc}</textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
      
        return HttpResponse(HTMLTemplate(article, id))
    #POST요청을 받을 시 입력받은 값을 기존값에 저장
    elif request.method == 'POST':        
        get_posts=Posts.objects.get(id=id)          
        get_posts.uploader=request.POST['uploader']
        get_posts.title=request.POST['title']  
        get_posts.target_day=request.POST['target_day']  
        get_posts.one_fund=request.POST['one_fund'] 
        get_posts.product_desc=request.POST['product_desc']   
        get_posts.save()       
        return redirect(f'/read/{id}')
    



@csrf_exempt
def delete(request): #삭제
    #입력 id의  글 삭제   
    if request.method == 'POST':        
        id = request.POST['id']      
        Posts.objects.filter(id=id).delete()
        return HttpResponse(HTMLTemplate('Delete success'))#redirect('/')
    
@csrf_exempt
def funding(request,id):
    #요청시 1회 펀딩    
    if request.method == 'GET':      
        get_post=Posts.objects.get(id=id)       
        get_post.fund_now+=get_post.one_fund
        get_post.save()        
        return redirect('/')
    

    