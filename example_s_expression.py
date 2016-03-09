import re
import parser as p
import unittest

number = p.map(p.regexp(re.compile("[1-9][0-9]*|[0-9]")),lambda x:int(x))
symbol = p.regexp(re.compile("[^\s\[\()]"))
popen = p.token("(")
pclose = p.token(")")
ws = p.regexp(re.compile("\s*"))
atom = p.choice(number,symbol)
expression = p.lazy(lambda:p.choice(
    p.map(p.seq(ws,atom,ws),lambda parsed:parsed[1])
    ,p.map(p.seq(popen,p.many(expression),pclose),lambda parsed:parsed[1])
))

class TestSExpression(unittest.TestCase):
    def test_number(self):
        self.assertEqual(number("1",0), [True, 1, 1])
        self.assertEqual(number("123",0), [True, 123, 3])
        self.assertEqual(number("a1",0), [False, None, 0])

    def test_sexp(self):
        self.assertEqual(expression("(+ 1 2)",0),[True,["+",1,2],7])
        self.assertEqual(expression("(+ 1 (- 3 4))",0),[True,["+",1,["-",3,4]],13])


if __name__ == '__main__':
    unittest.main()
