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
