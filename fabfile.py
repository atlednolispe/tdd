"""
fabric无法sudo写入/etc/systemd/system/gunicorn-superlists-staging.service

修改HOST和USER以及IDENTITY_FILE
"""
import random

from fabric import Connection


REPO_URL = 'https://github.com/atlednolispe/tdd.git'
HOST = '192.168.123.110'
USER = 'product'
IDENTITY_FILE = '/home/atlednolispe/Password/dell/product.pem'


def deploy():
    conn = Connection(host=HOST, user=USER, connect_kwargs={'key_filename': IDENTITY_FILE})

    command_mkdir_site = 'mkdir -p site'
    conn.run(command_mkdir_site)

    command_git_clone = f'git clone {REPO_URL} ~/site/'
    conn.run(command_git_clone)

    # .profile .bashrc .bash_profile, SET PATH都没用..
    command_pipenv_sync = f'cd /home/{USER}/site && /home/{USER}/.local/bin/pipenv sync'
    conn.run(command_pipenv_sync)

    command_ls_virtual_python = f'ls /home/{USER}/.local/share/virtualenvs/ | grep site-'
    virtualenv_name = conn.run(command_ls_virtual_python).stdout.strip()
    virtualenv_path = f'/home/{USER}/.local/share/virtualenvs/{virtualenv_name}'
    virtualenv_python = f'{virtualenv_path}/bin/python'

    cd_superlist_workon_path = f'cd /home/{USER}/site/superlists'
    command_collectstatic = f'{cd_superlist_workon_path} && {virtualenv_python} manage.py collectstatic'
    conn.run(command_collectstatic)

    command_make_database_dir = f'mkdir -p /home/{USER}/site/database'
    conn.run(command_make_database_dir)

    command_migrate = f'{cd_superlist_workon_path} && {virtualenv_python} manage.py migrate'
    conn.run(command_migrate)

    # 设置.env环境变量
    chars = ''.join(i for i in range(33, 122))
    key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
    command_add_env = f'echo -e "DJANGO_DEBUG_FALSE=y\nSITENAME=192.168.123.110\nDJANGO_SECRET_KEY={key}" > /home/{USER}/site/superlists/.env'
    conn.run(command_add_env)

    print('Success set configuration. Please run the following 3 command to run the site!\n')

    command_sed_service = f"sed 's/USER/product/' /home/{USER}/site/configurations/service/gunicorn-superlists-staging.service | sed 's,VIRTUALENVPATH,{virtualenv_path},' | sudo tee /etc/systemd/system/gunicorn-superlists-staging.service"
    print('1. Please add the service config!')
    print(command_sed_service)
    print()

    command_docker_run_nginx = f'docker run -d -p 80:80 -v /home/{USER}/site/configurations/nginx:/etc/nginx/conf.d -v /home/{USER}/site/static:/superlists/static -v /tmp:/tmp nginx'
    print('2. Please run the docker nginx.')
    print(command_docker_run_nginx)
    print()

    command_systemctl_start_gunicorn = 'sudo systemctl start gunicorn-superlists-staging'
    print('3. Please start the service!')
    print(command_systemctl_start_gunicorn)
    print()


if __name__ == '__main__':
    deploy()
