# 导入需要的库
import re
from PySimpleNginx.utils import *
class global_block:
    # 全局块
    def __init__(self, s: str=None) -> None:
        if s:
            self.parse(s)
        else:
            self.key = None
            self.value = None

    def parse(self, s: str) -> None:
        # 从字符串中解析出全局块
        data = s.strip().strip(';').split()
        self.key = data[0]
        if len(data) > 2:
            self.value = data[1:]
        else:
            self.value = data[1]

    def __str__(self) -> str:
        # 将全局块转换为字符串
        if isinstance(self.value, list):
            return '{} {};'.format(self.key, ' '.join(self.value))
        else:
            return '{} {};'.format(self.key, self.value)

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash(self.__repr__())


class events_block:
    # events块
    def __init__(self, s: str = None) -> None:
        if s:
            self.parse(s)
        else:
            self.key = 'events'
            self.value = []

    def parse(self, s: str) -> None:
        # 从字符串中解析出events块
        self.key = 'events'
        data = s.strip('events ').strip().strip('{').strip('}')
        global_block_pattern = re.compile(r'\s*(\w+)\s+(.*);')
        comments_pattern = re.compile(r'\s*#.*')
        self.value = []
        while len(data.strip()) > 0:
            data = data.strip()
            if global_block_pattern.match(data):
                match_block = global_block_pattern.match(data)
                self.value.append(events_global_block(match_block.group()))
                data = data.replace(match_block.group(), '', 1)
            elif comments_pattern.match(data):
                match_block = comments_pattern.match(data)
                self.value.append(comments(match_block.group()))
                data = data.replace(match_block.group(), '', 1)
            else:
                raise ValueError

    def __str__(self) -> str:
        # 将events块转换为字符串
        data = []
        for i in self.value:
            _data = str(i)
            _data = _data.split('\n')
            for i in _data:
                data.append('\t' + i)
        return '{} {{\n{}\n}}'.format(self.key, '\n'.join(data))

    def __repr__(self) -> str:
        return self.__str__()
    
    def __hash__(self) -> int:
        return hash(self.__repr__())

class events_global_block(global_block):
    # events块中的全局块
    def __init__(self, s: str = None) -> None:
        super().__init__(s)


class comments:
    # 注释
    def __init__(self, s: str = None) -> None:
        if s:
            self.parse(s)
        else:
            self.key = 'comments'
            self.value = None

    def parse(self, s: str) -> None:
        # 从字符串中解析出注释
        self.key = 'comments'
        self.value = s.replace('#', '', 1)

    def __str__(self) -> str:
        # 将注释转换为字符串
        return '#{}'.format(self.value)

    def __repr__(self) -> str:
        return self.__str__()
    
    def __hash__(self) -> int:
        return hash(self.__repr__())
    
    
class http_block:
    # http块
    def __init__(self, s: str = None) -> None:
        if s:
            self.parse(s)
        else:
            self.key = 'http'
            self.value = []

    def parse(self, s: str) -> None:
        # 从字符串中解析出http块
        self.key = 'http'
        data = s.strip('http ').strip().strip('{').strip('}')
        global_block_pattern = re.compile(r'\s*(\w+)\s+(.*);')
        cross_line_global_block_pattern = re.compile(r"\s*(\w+)\s+(\w+)\s+('(.*)'\s*\n\s*)+'(.*)';")
        server_block_pattern = re.compile(r'\s*server\s+{')
        comments_pattern = re.compile(r'\s*#.*')
        self.value = []
        while len(data.strip()) > 0:
            data = data.strip()
            if global_block_pattern.match(data):
                match_block = global_block_pattern.match(data)
                self.value.append(http_global_block(match_block.group()))
                data = data.replace(match_block.group(), '', 1)
            elif comments_pattern.match(data):
                match_block = comments_pattern.match(data)
                self.value.append(comments(match_block.group()))
                data = data.replace(match_block.group(), '', 1)
            elif server_block_pattern.match(data):
                match_block = server_block_pattern.match(data)
                index = data.find('{')
                end_index = find_bracket_in_str(data, index)
                _data = data[:end_index + 1].strip()
                self.value.append(server_block(_data))
                data = data.replace(_data, '', 1)
            elif cross_line_global_block_pattern.match(data):
                match_block = cross_line_global_block_pattern.match(data)
                self.value.append(http_global_block(match_block.group()))
                data = data.replace(match_block.group(), '', 1)
            else:
                raise ValueError


    def __str__(self) -> str:
        # 将http块转换为字符串
        data = []
        for i in self.value:
            _data = str(i)
            _data = _data.split('\n')
            for i in _data:
                data.append('\t' + i)
        return '{} {{\n{}\n}}'.format(self.key, '\n'.join(data))

    def __repr__(self) -> str:
        return self.__str__()
    
    def __hash__(self) -> int:
        return hash(self.__repr__())

class http_global_block(global_block):
    # http块中的全局块
    def __init__(self, s: str = None) -> None:
        if '\n' in s:
            self.parse_(s)
        else:
            super().__init__(s)
    def parse_(self, s: str) -> None:
        data = s.split('\n')
        self.key = data[0].strip().strip(';').split()[0]
        for i, j in enumerate(data):
            value = j.strip().strip("'")
            data[i] = value
        data = data[0].strip(';').split()[-1:] + data[1:]
        self.value = ' '.join(data)


class server_block:
    # server块
    def __init__(self, s: str = None) -> None:
        if s:
            self.parse(s)
        else:
            self.key = 'server'
            self.value = []

    def parse(self, s: str) -> None:
        # 从字符串中解析出server块
        self.key = 'server'
        data = s.strip('server ').strip().strip('{').strip('}')
        global_block_pattern = re.compile(r'\s*(\w+)\s+(.*);')
        location_block_pattern = re.compile(r'\s*location\s+(.*)\s+{')
        comments_pattern = re.compile(r'\s*#.*')
        self.value = []
        while len(data.strip()) > 0:
            data = data.strip()
            if global_block_pattern.match(data):
                match_block = global_block_pattern.match(data)
                self.value.append(server_global_block(match_block.group()))
                data = data.replace(match_block.group(), '', 1)
            elif comments_pattern.match(data):
                match_block = comments_pattern.match(data)
                self.value.append(comments(match_block.group()))
                data = data.replace(match_block.group(), '', 1)
            elif location_block_pattern.match(data):
                match_block = location_block_pattern.match(data)
                index = data.find('{')
                end_index = find_bracket_in_str(data, index)
                _data = data[:end_index + 1].strip()
                self.value.append(location_block(_data))
                data = data.replace(_data, '', 1)
            else:
                raise ValueError

    def __str__(self) -> str:
        # 将server块转换为字符串
        data = []
        for i in self.value:
            _data = str(i)
            _data = _data.split('\n')
            for i in _data:
                data.append('\t' + i)
        return '{} {{\n{}\n}}'.format(self.key, '\n'.join(data))

    def __repr__(self) -> str:
        return self.__str__()
    
    def __hash__(self) -> int:
        return hash(self.__repr__())

class server_global_block(global_block):
    # server块中的全局块
    def __init__(self, s: str = None) -> None:
        super().__init__(s)

class location_block:
    # location块
    def __init__(self, s: str = None) -> None:
        if s:
            self.parse(s)
        else:
            self.key = 'location'
            self.value = []

    def parse(self, s: str) -> None:
        # 从字符串中解析出location块
        self.key = 'location'
        bracket_start = s.find('{')
        data = s[bracket_start + 1:].strip('}')
        self.path = s[:bracket_start].replace('location', '').strip()
        global_block_pattern = re.compile(r'\s*(\w+)\s+(.*);')
        comments_pattern = re.compile(r'\s*#.*')
        self.value = []
        while len(data.strip()) > 0:
            data = data.strip()
            if global_block_pattern.match(data):
                match_block = global_block_pattern.match(data)
                self.value.append(location_global_block(match_block.group()))
                data = data.replace(match_block.group(), '', 1)
            elif comments_pattern.match(data):
                match_block = comments_pattern.match(data)
                self.value.append(comments(match_block.group()))
                data = data.replace(match_block.group(), '', 1)
            else:
                raise ValueError
        
    def __str__(self) -> str:
        # 将location块转换为字符串
        data = []
        for i in self.value:
            _data = str(i)
            _data = _data.split('\n')
            for i in _data:
                data.append('\t' + i)
        return '{} {} {{\n{}\n}}'.format(self.key, self.path, '\n'.join(data))
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __hash__(self) -> int:
        return hash(self.__repr__())


class location_global_block(global_block):
    # location块中的全局块
    def __init__(self, s: str = None) -> None:
        super().__init__(s)

class Config:
    # 配置文件
    def __init__(self, s: str = None) -> None:
        if s:
            self.parse(s)
        else:
            self.value = []
    
    def parse(self, s: str) -> None:
        # 从字符串中解析出配置文件
        self.value = []
        events_block_pattern = re.compile(r'\s*events\s+{')
        global_block_pattern = re.compile(r'\s*(\w+)\s+(.*);')
        http_block_pattern = re.compile(r'\s*http\s*{')
        comments_pattern = re.compile(r'\s*#.*')
        data = s.strip()
        while len(data.strip()) > 0:
            data = data.strip()
            if events_block_pattern.match(data):
                match_block = events_block_pattern.match(data)
                index = data.find('{')
                end_index = find_bracket_in_str(data, index)
                _data = data[:end_index + 1].strip()
                self.value.append(events_block(_data))
                data = data.replace(_data, '', 1)
            elif global_block_pattern.match(data):
                match_block = global_block_pattern.match(data)
                self.value.append(global_block(match_block.group()))
                data = data.replace(match_block.group(), '', 1)
            elif http_block_pattern.match(data):
                match_block = http_block_pattern.match(data)
                index = data.find('{')
                end_index = find_bracket_in_str(data, index)
                _data = data[:end_index + 1].strip()
                self.value.append(http_block(_data))
                data = data.replace(_data, '', 1)
            elif comments_pattern.match(data):
                match_block = comments_pattern.match(data)
                self.value.append(comments(match_block.group()))
                data = data.replace(match_block.group(), '', 1)
            else:
                raise ValueError
    
    def __str__(self) -> str:
        # 将配置文件转换为字符串
        data = []
        for i in self.value:
            data.append(str(i))
        return '\n'.join(data)

    def __repr__(self) -> str:
        return self.__str__()
    
    def __hash__(self) -> int:
        return hash(self.__repr__())
        
