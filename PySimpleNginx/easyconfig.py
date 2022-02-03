from distutils.command import config
from config import *

def default_config(conf: Config):
    # 默认配置
    default = Config('''user www www;
worker_processes  1;
error_log /usr/local/webserver/nginx/logs/nginx_error.log crit;
pid /usr/local/webserver/nginx/nginx.pid;
events {
    worker_connections  1024;
}
 
 
http {
    include       mime.types;
    default_type  application/octet-stream;
 
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
 
    #access_log  logs/access.log  main;
 
    sendfile        on;
    server_names_hash_bucket_size 128;
    client_header_buffer_size 32k;
    large_client_header_buffers 4 32k;
    client_max_body_size 8m;
     
    sendfile on;
    tcp_nopush on;
    keepalive_timeout 60;
    tcp_nodelay on;
    astcgi_connect_timeout 300;
    fastcgi_send_timeout 300;
    fastcgi_read_timeout 300;
    fastcgi_buffer_size 64k;
    fastcgi_buffers 4 64k;
    fastcgi_busy_buffers_size 128k;
    fastcgi_temp_file_write_size 128k;
    gzip on; 
    gzip_min_length 1k;
    gzip_buffers 4 16k;
    gzip_http_version 1.0;
    gzip_comp_level 2;
    gzip_types text/plain application/x-javascript text/css application/xml;
    gzip_vary on;
    server {
        listen       80;
        server_name  localhost;
 
        location / {
            root   /usr/local/webserver/nginx/html;
            index  index.html index.htm;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}''')
    conf.value = default.value
    return conf

def add_server(http: http_block, listen: int = 80, server_name: str = 'localhost', path: str = '/', root: str = 'www/default/htdocs', index: str = 'index.html'):
    # 添加一个server
    server = server_block()
    listen_block = http_global_block('listen {};'.format(listen))
    server_name_block = http_global_block('server_name {};'.format(server_name))
    location = location_block()
    root_block = location_global_block('root {};'.format(root))
    index_block = location_global_block('index {};'.format(index))
    location.value.append(root_block)
    location.value.append(index_block)
    location.path = path
    server.value.append(listen_block)
    server.value.append(server_name_block)
    server.value.append(location)
    http.value.append(server)
    return http

def add_static_location(server: server_block, path: str, root: str, index: str = 'index.html'):
    # 添加一个静态文件路径
    location = location_block()
    root_block = location_global_block('root {};'.format(root))
    index_block = location_global_block('index {};'.format(index))
    location.value.append(root_block)
    location.value.append(index_block)
    location.path = path
    server.value.append(location)
    return server

def add_fastcgi_location(server: server_block, path: str = '~ \.php$', fastcgi_pass: str = '127.0.0.1:9000', fastcgi_param: str = 'SCRIPT_FILENAME \$document_root\$fastcgi_script_name;', fastcgi_index: str = 'index.php'):
    # 添加一个fastcgi路径
    location = location_block()
    fastcgi_pass_block = location_global_block('fastcgi_pass {};'.format(fastcgi_pass))
    fastcgi_param_block = location_global_block('fastcgi_param {};'.format(fastcgi_param))
    fastcgi_index_block = location_global_block('fastcgi_index {};'.format(fastcgi_index))
    include_block = location_global_block('include fastcgi_params;')
    location.value.append(include_block)
    location.value.append(fastcgi_pass_block)
    location.value.append(fastcgi_param_block)
    location.value.append(fastcgi_index_block)
    location.path = path
    server.value.append(location)
    return server

def add_uwsgi_location(server: server_block, path: str, uwsgi_pass: str = '127.0.0.1:8888'):
    # 添加一个uwsgi路径
    location = location_block()
    include_block = location_global_block('include uwsgi_params;')
    uwsgi_pass_block = location_global_block('uwsgi_pass {};'.format(uwsgi_pass))
    uwsgi_ignore_client_abor_block = location_global_block('uwsgi_ignore_client_abort on;')
    location.value.append(include_block)
    location.value.append(uwsgi_pass_block)
    location.value.append(uwsgi_ignore_client_abor_block)
    location.path = path
    server.value.append(location)
    return server

def add_proxy_location(server: server_block, path: str, proxy_pass: str = 'http://localhost:8080'):
    # 添加一个代理路径
    location = location_block()
    proxy_pass_block = location_global_block('proxy_pass {};'.format(proxy_pass))
    proxy_set_header_block_1 = location_global_block('proxy_set_header Host \$host;')
    proxy_set_header_block_2 = location_global_block('proxy_set_header X-Real-IP \$remote_addr;')
    proxy_set_header_block_3 = location_global_block('proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;')
    proxy_set_header_block_4 = location_global_block('proxy_set_header X-Forwarded-Proto \$scheme;')
    location.value.append(proxy_pass_block)
    location.value.append(proxy_set_header_block_1)
    location.value.append(proxy_set_header_block_2)
    location.value.append(proxy_set_header_block_3)
    location.value.append(proxy_set_header_block_4)
    location.path = path
    server.value.append(location)
    return server

def add_waf(conf: Config):
    # 添加防火墙
    http = http_block()
    for i in conf.value:
        if isinstance(i, http_block):
            http = i
    server = server_block()
    for i in http.value:
        if isinstance(i, server_block):
            server = i
    
    waf_in_global = http_global_block('include /opt/verynginx/verynginx/nginx_conf/in_external.conf;')
    waf_in_http = http_global_block('include /opt/verynginx/verynginx/nginx_conf/in_http_block.conf;')
    waf_in_server = server_global_block('include /opt/verynginx/verynginx/nginx_conf/in_server_block.conf;')
    
    server.value.append(waf_in_server)
    http.value.append(waf_in_http)
    conf.value.append(waf_in_global)
    return conf