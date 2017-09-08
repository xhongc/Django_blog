# Django_blog
Django  blog 项目


## 本项目使用的开发环境
系统平台为 Windows 10 （64 位），Python 版本为 3.6.1 （64 位），Django 版本为 1.10.6。
<br>
## 使用虚拟环境 Virtualenv
Virtualenv 的使用非常简单，首先安装 Virtualenv，打开命令行工具，输入 `pip install virtualenv` 命令即可安装 Virtualenv。
- 安装成功后就可以开始创建虚拟环境
  指定一个你喜欢的目录，Virtualenv 会把这个新的虚拟环境装到你指定目录下。
  在命令栏输入 `virtualenv C:\安装目录\blogproject_env`
- 激活虚拟环境
  C:\安装目录\Scripts\activate
<br>

## 建立 Django 工程
<br>

- 在指定目录`django-admin startproject blogproject`

## Settins 设置

- Django 默认的语言是英语，修改配置为中文

```python
blogproject/blogproject/settings.py

## 其它配置代码...

# 把英文改为中文
LANGUAGE_CODE = 'zh-hans'

# 把国际时区改为中国时区
TIME_ZONE = 'Asia/Shanghai'

## 其它配置代码...
```

## 建立首个博客APP
- 在虚拟环境下运行 `python manage.py startapp blog` 创建一个博客应用

打开 blogproject\ 目录下的 settings.py 文件，看名字就知道 settings.py 是一个设置文件（setting 意为设置），找到 INSTALLED_APPS 设置项，将 blog 应用添加进去。

```python
blogproject/blogproject/settings.py

## 其他配置项...

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog', # 注册 blog 应用
]

## 其他配置项...
```

## 编写博客模型代码

Django 把那一套数据库的语法转换成了 Python 的语法形式，我们只要写 Python 代码就可以了，Django 会把 Python 代码翻译成对应的数据库操作语言。用更加专业一点的说法，就是 Django 为我们提供了一套 ORM（Object Relational Mapping）系统。


```python
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()

    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200,blank=True)

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag,blank=True)
    author = models.ForeignKey(User)
    views = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self,*args,**kwargs):
        if not self.excerpt:
            # 首先实例化一个Markdown 类 用于渲染body的文本
            md =markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post, self).save(*args,**kwargs)


```

## 数据库迁移

为了让 Django 完成翻译，创建好这些数据库表，我们再一次请出我的工程管理助手 manage.py。激活虚拟环境，切换到 manage.py 文件所在的目录下，分别运行 `python manage.py makemigrations` 和 `python manage.py migrate` 命令

- `python manage.py makemigrations` 把models中定义的各项翻译成数据库语言，Django 把这些变化记录在了 0001_initial.py 里。
- `python manage.py migrate` 它把这些操作翻译成数据库操作语言，从而把这些操作作用于真正的数据库。

## 博客视图

负责业务逻辑，并在适当时候调用Model和Template

```python
from django.shortcuts import render,get_object_or_404
from .models import Post,Category
import markdown
import pygments
from comments.forms import CommentForm
# Create your views here.

def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.increase_views()

    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])

    form = CommentForm()
    comment_list =post.comment_set.all()
    context ={'post':post,
              'form':form,
              'comment_list':comment_list}



    return render(request,'blog/detail.html',context=context)

def archives(request,year,month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
```

## 匹配对应URLs

```python
app_name ='blog'
urlpatterns =[
    url(r'^$',views.index,name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$',views.detail,name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.archives,name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$',views.category,name='category'),

]
```

## 模块

负责如何把页面展示给用户(html)。

本项目从[模块之家下载应用](http://www.cssmoban.com/)
具体看项目中 templates/

## 评论

新建一个app应用
添加到settings里的INSTALLED_APPS 
models 建立相应的数据类型
迁移数据库

### 评论表单设计
为什么需要表单呢？表单是用来收集并向服务器提交用户输入的数据的。考虑用户在我们博客网站上发表评论的过程。当用户想要发表评论时，他找到我们给他展示的一个评论表单（我们已经看到在文章详情页的底部就有一个评论表单，你将看到表单呈现给我们的样子），然后根据表单的要求填写相应的数据。之后用户点击评论按钮，这些数据就会发送给某个 URL。我们知道每一个 URL 对应着一个 Django 的视图函数，于是 Django 调用这个视图函数，我们在视图函数中写上处理用户通过表单提交上来的数据的代码，比如验证数据的合法性并且保存数据到数据库中，那么用户的评论就被 Django 后台处理了。如果通过表单提交的数据存在错误，那么我们把错误信息返回给用户，并在前端重新渲染，并要求用户根据错误信息修正表单中不符合格式的数据，再重新提交

下面开始编写评论表单代码。在 comments\ 目录下（和 models.py 同级）新建一个 forms.py 文件，用来存放表单代码，我们的表单代码如下：

```python
comments/forms.py

from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']
```


views中加入评论的交互逻辑
绑定urls
更新文章详情页面的视图函数

## Nginx 和 Gunicorn 部署到服务器上

### 部署前准备

我们将使用比较流行的 Nginx + Gunicorn 的方式将 Django 开发的博客部署到自己的服务器，让别人能够通过域名访问你的博客。至于 Nginx、Gunicorn 是什么暂时放到一边，读完本教程后你就会知道它们的作用和使用方法了。
为了部署我们的博客，需要满足以下两个条件：
- 有一台可以通过外网访问的服务器。
- 有一个域名。

## 搭建服务器

远程登录到服务器
服务器通常位于云端，需要使用远程登录工具登录后才能对服务器进行操作。我使用的是 Xshell，Windows 下百度 Xshell 下载安装即可，软件对学校和个人用户是免费的。
如何远程登录到服务器这里就不赘述了，相信你参考网上的一些教程肯定能够顺利登录。假如你和我一样使用 Xshell 的话。

新用户创建并切换成功了。如果是新服务器的话，最好先更新一下系统，避免因为版本太旧而给后面安装软件带来麻烦。运行下面的两条命令：

```python
chao@localhost:~$ sudo apt-get update
chao@localhost:~$ sudo apt-get upgrade
```

接下来就可以安装必要的软件了，这里我们需要用到的软件有 Nginx、Pytohn3、Git、pip 和 virtualenv。

```python
chao@localhost:~$ sudo apt-get install nginx
chao@localhost:~$ sudo apt-get install git python3 python3-pip
chao@localhost:~$ sudo pip3 install virtualenv
```

## 解析域名到服务器的 IP 地址
将域名和服务器的 IP 地址绑定后，用户就可以通过在浏览器输入域名来访问服务器了。

## 启动 Nginx 服务

Nginx 是用来处理静态文件请求的。比如当我们访问一个博客文章详情页面时，服务器会接收到下面两种请求：
显示文章的详情信息，这些信息通常保存在数据库里，因此需要调用数据库获取数据。
图片、css、js 等存在服务器某个文件夹下的静态文件。
对于前一种请求，博客文章的数据需要借助 Django 从数据库中获取，Nginx 处理不了，它就会把这个请求转发给 Django，让 Django 去处理。而对于后一种静态文件的请求，只需要去这些静态文件所在的文件夹获取，Nginx 就会代为处理，不再麻烦 Django。
用 Django 去获取静态文件是很耗时的，但 Nginx 可以很高效地处理，这就是我们要使用 Nginx 的原因（当然其功能远不止这些）。
通过前面的步骤我们已经安装了 Nginx，并且已经把域名和服务器 IP 绑定了。运行下面的命令启动 Nginx 服务：

```python
sudo service nginx start
```

## 部署代码

```python
部署前的项目配置
Django 项目中会有一些 CSS、JavaScript 等静态文件，为了能够方便地让 Nginx 处理这些静态文件的请求，我们把项目中的全部静态文件收集到一个统一的目录下，这个目录通常位于 Django 项目的根目录，并且命名为 static。为了完成这些任务，需要在项目的配置文件里做一些必要的配置：
blogproject/settings.py

# 其他配置...

STATIC_URL = '/static/'
# 加入下面的配置
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_ROOT 指明了静态文件的收集目录，即项目根目录（BASE_DIR）下的 static 文件夹。
为了安全起见，在生产环境下需要关闭 DEBUG 选项以及设置允许访问的域名。打开 settings.py 文件，找到 DEBUG 和 ALLOWED_HOSTS 这两个选项，将它们设置成如下的值：
blogproject/settings.py

DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost ', '.zmrenwu.com']
ALLOWED_HOSTS 是允许访问的域名列表，127.0.0.1 和 localhost 是本地访问的域名，.zmrenwu.com 是访问服务器的域名（换成你自己的域名）。域名前加一个点表示允许访问该域名下的子域名，比如 www.zmrenwu.com、test.zmrenwu.com 等二级域名同样允许访问。如果不加前面的点则只允许访问 zmrenwu.com。
项目还会依赖一些第三方 Python 库，为了方便在服务器上一次性安装，我们将全部依赖写入一个叫 requirements.txt 的文本文件中。激活本地的虚拟环境（如果你使用了虚拟环境的话），并进入项目的根目录，运行 pip freeze > requirements.txt 命令：
(blogproject_env) C:\Users\chao\Workspace\blogproject>
pip freeze > requirements.txt
这时项目根目录下会生成了一个 requirements.txt 的文本文件，其内容记录了项目的全部依赖。
```

## 将代码上传到 GitHub
将代码上传到 GitHub 等代码托管平台，这样我们就可以方便地把代码拉取到服务器了。Git 和 GitHub 的使用相信你已经很熟悉了，这里就不赘述过程。如果不知道如何使用地话可以自行百度相关教程。

接着再从代码仓库把项目代码拉取过来，把 git clone 后的地址换成你自己的 GitHub 仓库地址！
## 安装项目依赖

激活虚拟环境，再进入到项目根目录，即 requirements.txt 所在的目录，安装项目的全部依赖：

```python
chao@localhost:~/sites/demo.zmrenwu.com$ source env/bin/activate
(env) chao@localhost:~/sites/demo.zmrenwu.com$ cd django-blog-tutorial/
(env) chao@localhost:~/sites/demo.zmrenwu.com/django-blog-tutorial$ pip install -r requirements.txt
```
## 集静态文件
虚拟环境下继续运行 python manage.py collectstatic 命令收集静态文件到 static 目录下：

```python
(env) chao@localhost:~/sites/demo.zmrenwu.com/django-blog-tutorial$ python manage.py collectstatic
```

## 创建数据库
虚拟环境下继续运行 python manage.py migrate 命令创建数据库文件：
`env) chao@localhost:~/sites/demo.zmrenwu.com/django-blog-tutorial$ python manage.py migrate`

## 配置Nginx

先在服务器的 /etc/nginx/sites-available/ 目录下新建一个配置文件，文件名我一般就设置为域名。写上下面的配置内容：

```python
/etc/nginx/sites-available/demo.zmrenwu.com

server {
    charset utf-8;
    listen 80;
    server_name demo.zmrenwu.com; ①

    location /static { ②
        alias /home/chao/sites/demo.zmrenwu.com/django-blog-tutorial/static; 
    }

    location / { ③
        proxy_set_header Host $host;
        proxy_pass http://unix:/tmp/demo.zmrenwu.com.socket;
    }
}

```

[更详细的配置](http://www.cnblogs.com/knowledgesea/p/5175711.html)

 ## 使用 Gunicorn 
 
 Gunicorn 一般用来管理多个进程，有进程挂了Gunicorn 可以把它拉起来，防止服务器长时间停止服务，还可以动态调整 worker 的数量，请求多的时候增加 worker 的数量，请求少的时候减少。
在虚拟环境下，安装 Gunicorn：
`(env) chao@localhost:~/sites/demo.zmrenwu.com/django-blog-tutorial$ pip install gunicorn`
用 Gunicorn 启动服务器进程：
`(env) chao@localhost:~/sites/demo.zmrenwu.com/django-blog-tutorial$ gunicorn --bind unix:/tmp/demo.zmrenwu.com.socket blogproject.wsgi:application`
浏览器输入域名，可以看到访问成功了！

## 自动启动 Gunicorn
现在 Gunicorn 是我们手工启动的，万一哪天服务器崩溃重启了又得重新手工启动。为此我们写一个自动启动脚本，这样当服务器重新启动后，脚本会帮我们重启 Gunicorn。先按 Ctrl + c 停止刚才启动的服务器进程。
写一个启动脚本，这样当服务器重启后能自动引导 Gunicorn 的启动。脚本位于 /etc/init/ 目录下，且脚本文件名必须以 .conf 结尾：

```python
/etc/init/gunicorn-demo.zmrenwu.com.conf

start on net-device-up ①
stop on shutdown

respawn ②

setuid chao ③
chdir /home/chao/sites/demo.zmrenwu.com/django-blog-tutorial ④

exec ../env/bin/gunicorn --bind unix:/tmp/demo.zmrenwu.com.socket blogproject.wsgi:application ⑤

```
① start on net-device-up 确保只在服务器联网时才启动 Gunicorn。<br>
② 如果进程崩溃了（比如服务器重启或者进程因为某些以外情况被 kill），respawn 将自动重启 Gunicorn。<br>
③ setuid 确保以 chao 用户的身份（换成你自己的用户名）运行 Gunicorn 进程。<br>
④ chdir 进入到指定目录，这里进入项目的根目录。<br>
⑤ exec 执行进程，即开启服务器进程。<br>
现在可以用 start 命令启动 Gunicorn 了：<br>
`sudo start gunicorn-demo.zmrenwu.com`

## Fabric 自动化部署

### 编写 Fabric 脚本

```python
blogproject/fabfile.py

from fabric.api import env, run
from fabric.operations import sudo

GIT_REPO = "you git repository" ① 

env.user = 'you host username' ②
env.password = 'you host password'

# 填写你自己的主机对应的域名
env.hosts = ['demo.zmrenwu.com']

# 一般情况下为 22 端口，如果非 22 端口请查看你的主机服务提供商提供的信息
env.port = '22'


def deploy():
    source_folder = '/home/chao/sites/zmrenwu.com/django-blog-tutorial' ③

    run('cd %s && git pull' % source_folder) ④
    run("""
        cd {} &&
        ../env/bin/pip install -r requirements.txt &&
        ../env/bin/python3 manage.py collectstatic --noinput &&
        ../env/bin/python3 manage.py migrate
        """.format(source_folder)) ⑤ 
    sudo('restart gunicorn-demo.zmrenwu.com') ⑥
    sudo('service nginx reload')
```

① 你的代码托管仓库地址。<br>
② 配置一些服务器的地址信息和账户信息，各参数的含义分别为：<br>
env.user：用于登录服务器的用户名<br>
env.password：用户名对应的密码<br>
env.hosts：服务器的 IP 地址，也可以是解析到这个 IP 的域名<br>
env.port：SSH 远程服务器的端口号<br>
③ 需要部署的项目根目录在服务器上的位置。<br><br>
④ 通过 run 方法在服务器上执行命令，传入的参数为需要执行的命令，用字符串包裹。这里执行了两条命令，不同命令间用 && 符号连接：<br>
cd 命令进入到需要部署的项目根目录<br>
git pull 拉取远程仓库的最新代码<br>
⑤ 对应上述部署过程中 3-5 的几条命令。因为启用了虚拟环境，所以运行的是虚拟环境 ../env/bin/ 下的 pip 和 python<br>
⑥ 重启 Gunicorn 和 Nginx，由于这两条命令要在超级权限下运行，所以使用了 sudo 方法而不是 run 方法。<br>
注意全部的脚本代码要放在 deploy 函数里，Fabric 会自动检测 fabfile.py 脚本中的 deploy 函数并运行。<br>
由于脚本中有登录服务器的用户名和密码等敏感信息，不要把 fabfile.py 文件也上传到公开的代码托管仓库。<br>

## 执行 Fabric 自动部署脚本
进入 fabfile.py 文件所在的目录，在 Python2 的环境下用 fab 命令运行这个脚本文件。<br>
比如我的是 Windows 环境，Python2 安装在 C:\Python27\ 下，那么运行：<br>
`C:\Python27\Scripts\fab deploy`或`C:\Python27\Scripts\fab -f 具体目录/fabfile.py deploy`
这时 Fabric 会自动检测到 fabfile.py 脚本中的 deploy 函数并运行，你会看到命令行输出了一系列字符串，如果在最后看到
`Done. Disconnecting from zmrenwu.com... done.`
说明脚本运行成功。<br>
而如果看到<br>
`Aborting. Disconnecting from zmrenwu.com... done.`
说明脚本运行中出错，检查一下命令行输入的错误信息，修复问题后重新运行脚本即可。以后当你在本地开发完相关功能后，只需要执行这一个脚本文件，就可以自动把最新代码部署到服务器了。
