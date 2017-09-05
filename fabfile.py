from fabric.api import env,run
from fabric.operations import sudo

GIT_REPD ="https://github.com/xhongc/Django_blog.git"

env.user ='chao'
env.password ='xiehongchao'

env.hosts =['xhongc.cc']

env.port ='28298'


def deploy():
    source_folder = '/home/chao/sites/demo.xhongc.cc/Django_blog'
    run('cd ..')
    run('cd %s && git stash && git pull && git stash pop'% source_folder)
    run('''
    cd {0} &&
    /home/chao/sites/demo.xhongc.cc/env/bin/pip install -r requirements.txt &&
    /home/chao/sites/demo.xhongc.cc/env/bin/python3 manage.py collectstatic --noinput &&
    /home/chao/sites/demo.xhongc.cc/env/bin/python3 manage.py migrate
    '''.format(source_folder))

    sudo('restart gunicorn-xhongc.cc')
    sudo('service nginx reload')