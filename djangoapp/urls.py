"""django1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path,include
from djangoapp import views
from djangoapp.views import PostsListAPI

urlpatterns = [       
    #json api
	path('api/posts/', PostsListAPI.as_view()), #리스트
    path('api/posts/<id>', PostsListAPI.as_view()),#게시글 자세히보기    
    #html api    
    path('', views.index), #메인화면
    path('create/', views.create), #만들기
    path('read/<id>/', views.read),#게시글 자세히보기
    path('update/<id>/', views.update),#게시글 수정
    path('delete/', views.delete), #게시글 삭제
    path("funding/<id>", views.funding), #게시글 1회 펀딩하기
    
    
]
    
