
import os
from fabric.api import *

env.project_name = 'prototype'
env.hosts = os.environ.get('SERVER_IP').split(',')
env.user = os.environ.get('user')
env.key_filename = os.environ.get('KEYS').split(',')
env.path = '/var/www/prototype'


def setup():
    sudo('aptitude install -y python-setuptools python-dev')
    sudo('aptitude install -y zlib1g-dev libfreetype6-dev')
    sudo('aptitude install -y nginx')
    sudo('easy_install pip')
    sudo('mkdir -p /var/log/uwsgi/')


def prepare_and_upload_tar_from_git():
    local('git archive --format=tar master | gzip > release.tar.gz')
    sudo('mkdir -p %(path)s' % env, pty=True)
    sudo('chown -R %(user)s %(path)s' % env)
    put('release.tar.gz', '%(path)s/' % env)
    run('cd %(path)s && tar -zxvf release.tar.gz' % env, pty=True)
    local('rm -f release.tar.gz')


def deploy():
    setup()
    prepare_and_upload_tar_from_git()
    sudo('pip install -r %(path)s/requirements.txt' % env)
    sudo('cp %(path)s/conf/nginx/prototype /etc/nginx/sites-enabled/' % env)
    sudo('rm -f /etc/nginx/sites-enabled/default')
    sudo('uwsgi --enable-thread --touch-reload --ini /var/www/prototype/conf/uwsgi/prototype.ini')
    sudo('/etc/init.d/nginx restart')
