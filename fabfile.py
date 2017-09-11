from fabric.api import env,run
from fabric.operations import sudo

GIT_REPD ="https://github.com/xhongc/Django_blog.git"
env.user ='root'
env.password ='WW2CXpMUNUPt'
env.hosts =['xhongc.cc']
env.port ='28298'

def deploy():
    source_folder = '/home/chao/sites/demo.xhongc.cc/Django_blog'

    run('cd %s && git pull'% source_folder)
    run('''
    cd {0} &&
    /home/chao/sites/demo.xhongc.cc/env/bin/pip install -r requirements.txt &&
    /home/chao/sites/demo.xhongc.cc/env/bin/python3 manage.py collectstatic --noinput &&
    /home/chao/sites/demo.xhongc.cc/env/bin/python3 manage.py migrate
    '''.format(source_folder))
    with cd(source_folder):
        sudo('gunicorn --bind unix:/tmp/xhongc.cc.socket blogproject.wsgi:application')
        sudo('service nginx reload')