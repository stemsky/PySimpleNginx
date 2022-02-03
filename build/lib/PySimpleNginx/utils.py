def extract_bracket(s: str):
    """
    在字符串中提取括号“{}”，存放在列表中
    """
    result = []
    indexs = []
    for i, k in enumerate(s):
        if k == '{' or k == '}':
            result.append(k)
            indexs.append(i)
    return result, indexs

def find_bracket(l: list, index: int):
    """
    在列表中找出配对的括号
    :l : 列表
    :index : 要配对的括号位置
    """
    if l[index] == '{':
        for i, j in enumerate(l):
            if j == '}':
                if l[i-1] == '{':
                    if i-1 == index:
                        return i
                    else:
                        l[i] = l[i-1] = '#'
                elif l[i-1] == '#':
                    m = i
                    while l[i-1] == '#':
                        i -= 1
                    if l[i-1] == '{':
                        if i-1 == index:
                            return m
                        else:
                            l[m] = l[i-1] = '#'
                    else:
                        raise ValueError
                else:
                    raise ValueError
    elif l[index] == '}':
        l.reverse()
        index = len(l) - index - 1
        for i, j in enumerate(l):
            if j == '{':
                if l[i-1] == '}':
                    if i-1 == index:
                        return len(l) - i - 1
                    else:
                        l[i] = l[i-1] = '#'
                elif l[i-1] == '#':
                    m = i
                    while l[i-1] == '#':
                        i -= 1
                    if l[i-1] == '}':
                        if i-1 == index:
                            return len(l) - m - 1
                        else:
                            l[m] = l[i-1] = '#'
                    else:
                        raise ValueError
                else:
                    raise ValueError

def find_bracket_in_str(s: str, index: int):
    """
    在字符串中找出配对的括号
    :s : 字符串
    :index : 要配对的括号位置
    """
    _s = s.split('\n')
    new_s = []
    for i in _s:
        if i.strip().startswith('#'):
            new_s.append('#'*len(i))
        else:
            new_s.append(i)
    s = '\n'.join(new_s)
    brackets, indexs = extract_bracket(s)
    if index not in indexs:
        raise ValueError
    index = indexs.index(index)
    return indexs[find_bracket(brackets, index)]