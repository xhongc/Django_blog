from fabric.api import env,run
from fabric.operations import sudo

GIT_REPD ="https://github.com/xhongc/Django_blog.git"

env.user ='104.225.154.56'
env.password ='chao123456789..'

env.hosts =['xhongc.cc']

env.port ='28298'

def deploy():
    source_folder = 'home/chao/sites/demo.xhongc.cc/Django_blog'
    run('cd %s && git pull'% source_folder)
    run('''
    cd {} &&
    ../env/bin/pip install -r requirements.txt &&
    ../env/bin/python3 manage.py collectstatic --noinput &&
    ../env/bin/python3 manage.py migrate
    '''.format(source_folder))

    sudo('restart gunicorn-xhongc.cc')
    sudo('service nginx reload')