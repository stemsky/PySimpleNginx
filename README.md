PySimpleNginx
========
这是一个简单的Python程序，用于构建一个Nginx配置文件和控制Nginx。<br>

安装
------
### (1)使用git安装
```
$ git clone https://github.com/stemsky/PySimpleNginx.git
$ cd PySimpleNginx
$ python setup.py install
```
### (2)使用pip安装
```
$ pip install PySimpleNginx
```

使用
-----
### (1)创建一个配置文件
```python
from PyNginx import config
conf = config.Config()
```
你还可以从字符串创建一个配置文件：
```python
conf = config.Config('user www www;\nworker_processes 1;\nevents ...')
```
### (2)添加一个全局块
```python
block = config.global_block()
block.key = 'user'
block.value = ['www', 'www']
conf.value.append(block)
```
同样，你也可以从字符串创建一个全局块：
```python
block = config.global_block('user www www;')
conf.value.append(block)
```
### (3)添加一个events块
```python
events = config.events_block()
block = config.events_global_block()
block.key = 'worker_connections'
block.value = '1024'
events.value.append(block)
conf.value.append(events)
```
其实，对于events中的块，你可以直接使用global_block()类创建，但是这样做会更加优雅。
### (4)添加添加其它块
>其它块的操作方式和以上方式一样，但要注意的是http中的全局块必须使用http_global_block()类创建，而不是global_block()类。具体原因可以查看源码。
### (5)保存配置文件
>先将Config对象转换成字符串，然后保存到文件中。
```python
with open('nginx.conf', 'w') as f:
    f.write(str(conf))
```
### (6)控制Nginx
>另一个文件control.py，用于控制Nginx。但它只能用于Linux系统，不能在Windows上运行，否则会报错OSError。
#### (1)启动Nginx
```python
from pynginx.control import *
start()
```
>这一步要求你必须安装了Nginx，并且配置了环境变量。
#### (2)停止Nginx
```python
# 从容地关闭Nginx（结束所有服务后再关闭）
stop('clam')
# 立刻关闭Nginx
stop('quickly')
# 强制关闭Nginx
stop('force')
# 默认是从容地关闭Nginx（结束所有服务后再关闭）
stop()
```
#### (3)重启Nginx
```python
# 简单地重启Nginx（这里的简单指先关闭再启动）
restart('easy')
# 重载Nginx配置文件（不关闭Nginx，也不停止请求，只是重新加载配置文件）
restart('reload')
# 还可以指定配置文件的路径，默认是/usr/local/nginx/conf/nginx.conf
restart('reload', '/usr/local/nginx/conf/nginx.conf')
# 默认为重载Nginx配置文件
restart()
```
#### (4)测试Nginx配置文件
```python
# 测试Nginx配置文件，如果配置文件有误，会返回False
test('/usr/local/nginx/conf/nginx.conf')
# 里面的一个参数是配置文件的路径，默认是/usr/local/nginx/conf/nginx.conf
test()
```

缺点
-----
>### (1)对于配置文件格式不是很规范的数据，可以解析时会出错。我没有严谨地测试过。
>### (2)config中的类名除Config外都是小写。因为我并没有大写的习惯，所以这样写了。
>### (3)该程序的鲁棒性不是很好。
>### (4)控制Nginx的程序只能在Linux系统上运行。
>……
****
>### 总之，该程序的缺点有很多。因为这是作者第一次开发库，所以还有很多地方没有完善。如果你遇到问题请不要吐槽，可以issue给我。

