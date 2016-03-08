import re
import parser as p
import unittest
from functools import reduce

number = p.map(p.regexp(re.compile("[1-9][0-9]*|[0-9]")),lambda x:int(x))
operator = p.regexp(re.compile("\+|\-"))
popen = p.token("(")
pclose = p.token(")")
parenthesis = p.lazy(lambda:p.map(p.seq(popen,expression,pclose),lambda parsed:parsed[1]))
atom = p.choice(number, parenthesis)
def convert(parsed):
    ret = [parsed[0]]
    for pi in parsed[1]:
        ret.extend(pi)
    return ret
expression = p.map(p.seq(atom, p.many(p.seq(operator,atom))), convert)


class TestArithmetic(unittest.TestCase):
    def test_number(self):
        self.assertEqual(number("1",0), [True, 1, 1])
        self.assertEqual(number("123",0), [True, 123, 3])
        self.assertEqual(number("a1",0), [False, None, 0])

    def test_operator(self):
        self.assertEqual(operator("+",0), [True, "+", 1])
        self.assertEqual(operator("-",0), [True, "-", 1])
        self.assertEqual(operator("*",0), [False, None, 0])

    def test_expression(self):
        self.assertEqual(expression("1+2+3+(4-1)",0),[True,[1,"+",2,"+",3,"+",[4,"-",1]],11])
        self.assertEqual(expression("1+a",0), [True, [1], 1])

if __name__=="__main__":
    unittest.main()
