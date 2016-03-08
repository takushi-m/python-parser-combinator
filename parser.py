def token(tk):
    l = len(tk)

    def parser(target, pos):
        if target[pos:pos+l]==tk:
            return [True,tk,pos+l]
        else:
            return [False,None,pos]

    return parser

def many(p):
    def parser(target, pos):
        ret = []
        while True:
            parsed = p(target, pos)
            if parsed[0]:
                ret.append(parsed[1])
                pos = parsed[2]
            else:
                break
        return [True,ret,pos]
    return parser

def choice(*ary_parser):
    def parser(target,pos):
        for p in ary_parser:
            parsed = p(target,pos)
            if parsed[1]:
                return parsed
        return [False, None, pos]
    return parser

def seq(*ary_parser):
    def parser(target,pos):
        ret = []
        position = pos
        for p in ary_parser:
            parsed = p(target,position)
            if not parsed[0]:
                return [False, None, pos]
            else:
                ret.append(parsed[1])
                position = parsed[2]
        return [True, ret, position]
    return parser

def option(p):
    def parser(target,pos):
        parsed = p(target,pos)
        if parsed[0]:
            return parsed
        else:
            return [True, None, pos]
    return parser

def regexp(regobj):
    def parser(target,pos):
        m = regobj.match(target[pos:])
        if m:
            return [True, m.group(0),pos+len(m.group(0))]
        else:
            return [False, None, pos]
    return parser

def lazy(callback):
    p = None
    def parser(target,pos):
        nonlocal p
        if not p:
            p = callback()
        return p(target,pos)
    return parser

def map(p,fn):
    def parser(target,pos):
        parsed = p(target,pos)
        if parsed[0]:
            return [parsed[0],fn(parsed[1]),parsed[2]]
        else:
            return parsed
    return parser
