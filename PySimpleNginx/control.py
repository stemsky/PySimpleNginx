# 用于控制nginx(仅限linux)

import os
import platform

if platform.system() != 'Linux':
    raise OSError('This script only supports Linux')

def start():
    # 启动nginx
    process = os.system('nginx')
    if process == 0:
        return True
    else:
        return False

def stop(way='calm'):
    # 停止nginx
    if way == 'calm':
        process = os.system('ps -ef | grep nginx | kill -QUIT cat /usr/local/nginx/logs/nginx.pid')
        if process == 0:
            return True
        else:
            return False
    elif way == 'force':
        process = os.system('ps -ef | grep nginx | kill -9 cat /usr/local/nginx/logs/nginx.pid')
        if process == 0:
            return True
        else:
            return False
    elif way == 'quickly':
        process = os.system('ps -ef | grep nginx | kill -TERM cat /usr/local/nginx/logs/nginx.pid')
        if process == 0:
            return True
        else:
            return False
    else:
        raise ValueError

def restart(way='reload', conf_path='/usr/local/nginx/conf/nginx.conf'):
    # 重启nginx
    if way == 'easy':
        process = stop('calm')
        if process == True:
            process = start()
            if process == True:
                return True
            else:
                return False
        else:
            return False
    elif way == 'reload':
        process = os.system('nginx -c {} | kill -15 cat /usr/local/nginx/logs/nginx.pid'.format(conf_path))
        if process == 0:
            return True
        else:
            return False
    else:
        raise ValueError

def test(conf_path='/usr/local/nginx/conf/nginx.conf'):
    # 测试nginx配置文件
    process = os.system('nginx -t -c {}'.format(conf_path))
    if process == 0:
        return True
    else:
        return False

