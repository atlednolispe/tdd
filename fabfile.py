"""
fabric无法sudo写入/etc/systemd/system/gunicorn-superlists-staging.service

部署命令
fab deploy -u [user] -H [ip] -i [identity_file]
Example:
    fab deploy -u product -H 192.168.123.110 -i ~/Password/dell/product.pem

之后按照输出在远程机器上执行下面类似的5条命令
==============================
Success set configuration. Please run the following 3 command to run the site!

1. Please add the service config!
sed 's/USER/product/' /home/product/site/configurations/service/gunicorn-superlists-staging.service | sed 's,VIRTUALENVPATH,/home/product/.local/share/virtualenvs/site-Pa3_Gi3K,' | sudo tee /etc/systemd/system/gunicorn-superlists-staging.service

2. Please run the docker nginx.
docker run -d -p 80:80 -v /home/product/site/configurations/nginx:/etc/nginx/conf.d -v /home/product/site/static:/superlists/static -v /tmp:/tmp nginx

3. Please reload the service!
sudo systemctl daemon-reload

4. Please start the service!
sudo systemctl start gunicorn-superlists-staging

5. Please check the service!
systemctl status gunicorn-superlists-staging
"""
import random

from fabric.api import (
    run, env
)

REPO_URL = 'https://github.com/atlednolispe/tdd.git'
HOST = env.hosts[0]
USER = env.user
IDENTITY_FILE = env.key_filename[0]


def deploy():
    command_mkdir_site = 'mkdir -p site'
    run(command_mkdir_site)

    command_git_clone = f'git clone {REPO_URL} ~/site/'
    run(command_git_clone)

    # .profile .bashrc .bash_profile, SET PATH都没用..
    command_pipenv_sync = f'cd /home/{USER}/site && /home/{USER}/.local/bin/pipenv sync'
    run(command_pipenv_sync)

    command_ls_virtual_python = f'ls /home/{USER}/.local/share/virtualenvs/ | grep site-'
    virtualenv_name = run(command_ls_virtual_python).stdout.strip()
    virtualenv_path = f'/home/{USER}/.local/share/virtualenvs/{virtualenv_name}'
    virtualenv_python = f'{virtualenv_path}/bin/python'

    cd_superlist_workon_path = f'cd /home/{USER}/site/superlists'
    command_collectstatic = f'{cd_superlist_workon_path} && {virtualenv_python} manage.py collectstatic'
    run(command_collectstatic)

    command_make_database_dir = f'mkdir -p /home/{USER}/site/database'
    run(command_make_database_dir)

    command_migrate = f'{cd_superlist_workon_path} && {virtualenv_python} manage.py migrate'
    run(command_migrate)

    # 设置.env环境变量
    # chr(34) = '"',会导致echo写入错误
    chars = ''.join(chr(i) for i in range(33, 122) if i != 34)
    key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
    command_add_env = f'echo -e "DJANGO_DEBUG_FALSE=y\nSITENAME={HOST}\nDJANGO_SECRET_KEY={key}" > /home/{USER}/site/superlists/.env'
    run(command_add_env)

    print()
    print('='*30)
    print('Success set configuration. Please run the following 5 command to run the site!\n')

    command_sed_service = f"sed 's/USER/product/' /home/{USER}/site/configurations/service/gunicorn-superlists-staging.service | sed 's,VIRTUALENVPATH,{virtualenv_path},' | sudo tee /etc/systemd/system/gunicorn-superlists-staging.service"
    print('1. Please add the service config!')
    print(command_sed_service)
    print()

    command_docker_run_nginx = f'docker run -d -p 80:80 -v /home/{USER}/site/configurations/nginx:/etc/nginx/conf.d -v /home/{USER}/site/static:/superlists/static -v /tmp:/tmp nginx'
    print('2. Please run the docker nginx.')
    print(command_docker_run_nginx)
    print()

    command_reload_service = 'sudo systemctl daemon-reload'
    print('3. Please reload the service!')
    print(command_reload_service)
    print()

    command_systemctl_start_gunicorn = 'sudo systemctl start gunicorn-superlists-staging'
    print('4. Please start the service!')
    print(command_systemctl_start_gunicorn)
    print()

    command_check_service_status = 'systemctl status gunicorn-superlists-staging'
    print('5. Please check the service!')
    print(command_check_service_status)
    print()
    print('if Active: active (running) = Success')
    print("""Example:
    
    ● gunicorn-superlists-staging.service - Gunicorn server for superlists-staging
       Loaded: loaded (/etc/systemd/system/gunicorn-superlists-staging.service; disabled; vendor preset: enabled)
       Active: active (running) since Tue 2018-09-11 18:18:30 CST; 6s ago
     Main PID: 18814 (gunicorn)
        Tasks: 2 (limit: 4513)
       CGroup: /system.slice/gunicorn-superlists-staging.service
               ├─18814 /home/product/.local/share/virtualenvs/site-Pa3_Gi3K/bin/python3.6m /home/product/.local/share/virtualenvs/site-Pa3_Gi3K/bin/gunicorn --bind unix:/tmp/superlists-staging.socket superlis
               └─18835 /home/product/.local/share/virtualenvs/site-Pa3_Gi3K/bin/python3.6m /home/product/.local/share/virtualenvs/site-Pa3_Gi3K/bin/gunicorn --bind unix:/tmp/superlists-staging.socket superlis
    """)
    print('=' * 30)
    print()


if __name__ == '__main__':
    deploy()
