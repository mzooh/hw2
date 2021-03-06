from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Blog
from .form import BlogPost


def home(request):
    blogs=Blog.objects
    # 블로그 모든 글들을 대상으로
    blog_list = Blog.objects.all()
    # 블로그 객체 세 개를 한 페이지로 자르기
    paginator = Paginator(blog_list, 3)
    # request된 페이지가 무엇인지 알아내고
    page = request.GET.get('page')
    # request된 페이지를 얻어 온 뒤 return 해준다.
    posts=paginator.get_page(page)
    return render(request, 'home.html', {'blogs':blogs, 'posts':posts})    

def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html',{'blog':blog_detail})

# new.html 띄워주는 함수
def new(request):
    return render(request, 'new.html')

# 입력받은 내용을 데이터베이스에 넣어주는 함수
def create(request):
    blog=Blog()     # 객체 생성
    blog.title=request.GET['title']     # form에서 임력한 내용
    blog.body=request.GET['body']
    blog.pub_date=timezone.datetime.now()
    blog.save() # 메소드 중 하나 : 객채를 데이터베이스에 저장하라
    # redirect import
    # url은 항상 str
    return redirect('/blog/'+str(blog.id))

    # redirect와 render의 차이
    # redirect(url(다른 url 사용가능),)

### blog.id vs. blog_id 차이점 숙지하기

def blogpost(request):
    # 1. 입력된 내용을 처리하는 기능 >> POST
    # 2. 빈 페이지를 띄워주는 기능 >> GET
    if request.method == 'POST':
        form = BlogPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.save()
            return redirect('home')
    else:
        form = BlogPost()
        return render(request,'new.html', {'form':form})
    