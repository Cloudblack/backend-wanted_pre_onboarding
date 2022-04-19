#product/serializers.py
from rest_framework import serializers
from .models import Posts

class PostsSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Posts        # Posts 모델 사용
        fields = '__all__'            # 모든 필드 포함