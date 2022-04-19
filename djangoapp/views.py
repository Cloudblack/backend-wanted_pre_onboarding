from http.client import HTTPResponse
from django.http import JsonResponse
from sre_constants import SUCCESS
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Posts
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PostsSerializer
import datetime

class PostsListAPI(APIView): #json api view
    def get(self, request,id=None):                 
        if 'order_by' in request.GET: # order_by를 받아 정렬한다          
            if request.GET['order_by']=='총펀딩금액':
               queryset =Posts.objects.all().order_by('target') #전체를 불러와 정렬
            elif request.GET['order_by']=='-총펀딩금액':
                queryset =Posts.objects.all().order_by('-target')
            elif request.GET['order_by']=='생성일':
                queryset =Posts.objects.all().order_by('created_at')
            elif request.GET['order_by']=='-생성일':
                queryset =Posts.objects.all().order_by('-created_at')
        elif 'search' in request.GET: #search를 받아 제목에서 검색한다
            queryset =Posts.objects.filter(title__icontains=request.GET['search'])
        elif 'funding' in request.GET: #funding 숫자만큼 펀딩을한다
            if id != None:
                get_posts = Posts.objects.get(id=id)
                fund_now=get_posts.one_fund*int(request.GET['funding'])
                get_posts.fund_now+=fund_now                
                get_posts.save()
                serializer = PostsSerializer(get_posts)
                return Response(serializer.data)#redirect('/')
        else:
            queryset = Posts.objects.all()                
        if id !=None:
            queryset = Posts.objects.get(id=id)
            serializer = PostsSerializer(queryset)
            return Response(serializer.data)    
        for queryx in queryset:
            now = datetime.datetime.now().date()
            td=datetime.datetime.strptime(str(queryx.target_day)[:10], '%Y-%m-%d').date()
            queryx.end_day=(td-now).days     
            people_now=int(queryx.fund_now/queryx.one_fund)
            fund_now=int(queryx.fund_now/queryx.target*100)
            queryx.Peoplecount=people_now
            queryx.percent_now=f"{fund_now}%"   
            now = datetime.datetime.now().date()
            td=datetime.datetime.strptime(str(queryx.target_day)[:10], '%Y-%m-%d').date()
            queryx.end_day=(td-now).days    
            queryx.save()              
        serializer = PostsSerializer(queryset, many=True)
        
        return Response(serializer.data)
    def delete(self,request,id):
        # id = request.POST['id']      
        Posts.objects.filter(id=id).delete()
        return redirect('/')
    def post(self,request,id=None):    
        if id !=None:
            get_posts=Posts.objects.get(id=id)          
            get_posts.uploader=request.data['uploader']
            get_posts.title=request.data['title']
            get_posts.one_fund=request.data['one_fund'] 
            get_posts.product_desc=request.data['product_desc']   
            get_posts.save()      
            return redirect('/')
                
        serializer = PostsSerializer(data = request.data, many=True) 
        if(serializer.is_valid()):              
            # td=datetime.datetime.strptime(serializer.data[0]['target_day'], '%Y-%m-%d').date()
            # now = datetime.datetime.now()
            # nowDate = now.strftime('%Y-%m-%d')
            now = datetime.datetime.now().date()
            td=datetime.datetime.strptime(serializer.data[0]['target_day'][:10], '%Y-%m-%d').date()
            serializer.data[0]['end_day']=(td-now).days     
            people_now=int(serializer.data[0]['fund_now']/list(serializer.data[0]['one_fund'])[0])
            fund_now=int(list(serializer.data[0]['fund_now'])[0]/list(serializer.data[0]['target'])[0]*100)
            serializer.data[0]['Peoplecount']=people_now
            serializer.data[0]['percent_now']=fund_now       
            serializer.save() 
            return Response(serializer.data ,status=200)
# JSON API        
#-------------------------------------------------------------------------------
# HTML

post=Posts()

def HTMLTemplate(articleTag, id=None):
    
    global topics
    contextUI = ''
    if id != None:
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
    # ol = ''
    # for topic in post_list:
    #     ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]} {topic["uploader"]} {topic["target"]} {topic["fund_now"]} {topic["end_day"]}</a></li>'
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

def index(request,search=None):        
    if 'search' in request.GET:
        post_list =Posts.objects.filter(title__icontains=request.GET['search'])
    if 'order_by' in request.GET:            
            if request.GET['order_by']=='총펀딩금액':
               post_list =Posts.objects.all().order_by('target')
            elif request.GET['order_by']=='-총펀딩금액':
                post_list =Posts.objects.all().order_by('-target')
            elif request.GET['order_by']=='생성일':
                post_list =Posts.objects.all().order_by('created_at')
            elif request.GET['order_by']=='-생성일':
                post_list =Posts.objects.all().order_by('-created_at')
    else:
        post_list=Posts.objects.all()
    article='<p>제목 , 작성자 , 목표금액 , 달성률 , D-day</p>'
    for topic in post_list:                
        now = datetime.datetime.now().date()
        td=datetime.datetime.strptime(str(topic.target_day)[:10], '%Y-%m-%d').date()
        topic.end_day=(td-now).days
        fund_now=int(list({topic.fund_now})[0]/list({topic.target})[0]*100)
        topic.save() 
        article += f'<li><a href="/read/{topic.id}">{topic.title}, {topic.uploader}, {topic.target}, {fund_now}%, {topic.end_day}</a></li>'
    
    # article = '''
    # <h2>Welcome</h2> 
    # Hello, Django
    # '''
    return HttpResponse(HTMLTemplate(article))


   
def read(request, id):
    get_post=Posts.objects.get(id=id)
    #print(type(list({get_post.fund_now})[0]),type({get_post.target}))
    #fund_now=list({get_post.fund_now})[0]/list({get_post.target})[0]*100
    people_now=get_post.fund_now/list(get_post.one_fund)[0]
    fund_now=int(list({get_post.fund_now})[0]/list({get_post.target})[0]*100)
    article = f'''<h2>제목 {get_post.title}</h2>
    <p>작성자 {get_post.uploader}</p>
    <p>목표 금액 {get_post.target}</p>
    <p>달성률 {fund_now}%</p>
    <p>D-day {get_post.end_day}</p>
    <p>1회 펀금 요금 {get_post.one_fund}</p>
    <p>참여인원 {int(people_now)}명</p>
    <p>{get_post.product_desc}</p>    
    ''' 
    return HttpResponse(HTMLTemplate(article, id))#JsonResponse(aa, json_dumps_params={'ensure_ascii': False}, status=200,safe=False) 


@csrf_exempt
def create(request):
    global nextId
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
def update(request,id):
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
def delete(request):    
    if request.method == 'POST':        
        id = request.POST['id']      
        Posts.objects.filter(id=id).delete()
        return HttpResponse(HTMLTemplate('Delete success'))#redirect('/')
    
@csrf_exempt
def funding(request,id):    
    if request.method == 'GET':      
        get_post=Posts.objects.get(id=id)       
        get_post.fund_now+=get_post.one_fund
        get_post.save()        
        return redirect(f'/read/{id}')
    

    