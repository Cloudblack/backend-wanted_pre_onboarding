#product/serializers.py
from rest_framework import serializers
from .models import Posts

class PostsSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Posts        # Posts 모델 사용
        fields = '__all__'            # 모든 필드 포함
class PostsSerializer_list(serializers.ModelSerializer) :
    class Meta :
        model = Posts        # Posts 모델 사용
        fields = ('id','title','uploader','fund_now','percent_now','end_day','created_at') # 글제목에 필요한 데이터만 
class PostsSerializer_detail(serializers.ModelSerializer) :
    class Meta :
        model = Posts        # Posts 모델 사용
        fields = ('id','title','uploader','fund_now','percent_now','end_day','product_desc','created_at','target','Peoplecount')         # 모든 필드 포함