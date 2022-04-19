from django.db import models
from django.utils import timezone
import datetime


# Create your models here.

# class TimeStampmodel(models.Model):
#     create_at = models.DateTimeField(auto_now_add=True,null=True)
#     update_at = models.DateTimeField(auto_now_add=True,null=True)
#     class Meta:
#         abstract = True
class Posts(models.Model): 
    title = models.CharField(max_length=100) #제목
    uploader = models.CharField(max_length=20)  #작성자
    product_desc = models.TextField() #설명글
    target = models.IntegerField(default=0) #목표금액
    fund_now = models.IntegerField(default=0) #현재금액
    end_day= models.IntegerField(default=0) # 남은 기간
    target_day = models.DateTimeField(blank = True, null = True) # 종료일
    one_fund = models.IntegerField(default=0) #1회 펀딩 금액  
    created_at = models.DateTimeField(auto_now_add=True) #글작성일
    updated_at = models.DateTimeField(auto_now=True) #수정일
    published_at = models.DateTimeField(blank = True, null = True)
    Peoplecount= models.IntegerField(default=0) #참여인원
    percent_now = models.CharField(max_length=100,default=0) #달성률
     
    def __str__(self):  
        return self.title
    def publish(self):
        self.published_at = timezone.now()
        self.save()
    # def was_published_recently(self): 
    #     return self.pub_date >= timezone.now() - datetime.timedelta(days=1)



# class Choice(TimeStrampmodel): 
#     question = models.ForeignKey(Posts, on_delete=models.CASCADE) 
#     choice_text = models.CharField(max_length=200) 
#     votes = models.IntegerField(default=0)

#     def __str__(self): 
#         return self.choice_text
