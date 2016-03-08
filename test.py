import unittest
import re
from parser import *

class TestParser(unittest.TestCase):
    def test_token(self):
        # /hoge/
        parser = token("hoge")
        s = "hoge"
        self.assertEqual(parser(s,0), [True,"hoge",4])
        self.assertEqual(parser(s,1), [False,None,1])

        s = "ahoge"
        self.assertEqual(parser(s,0), [False,None,0])
        self.assertEqual(parser(s,1), [True,"hoge",5])

    def test_many(self):
        # /(hoge)*/
        parser = many(token("hoge"))
        s = "hogehoge"
        self.assertEqual(parser(s,0), [True,["hoge","hoge"],8])
        self.assertEqual(parser(s,4), [True,["hoge"],8])
        self.assertEqual(parser(s,1), [True,[],1])

    def test_choice(self):
        # /(hoge|fuga)*/
        parser = many(choice(token("hoge"),token("fuga")))
        s = "hogefugahoge"
        self.assertEqual(parser(s,0), [True,["hoge","fuga","hoge"],12])
        self.assertEqual(parser(s,4), [True,["fuga","hoge"],12])
        self.assertEqual(parser(s,8), [True,["hoge"],12])
        self.assertEqual(parser("a",0), [True,[],0])

    def test_seq(self):
        # /hoge(hoge)*/ = /(hoge)+/
        parser = seq(token("hoge"),many(token("hoge")))
        s = "hogehoge"
        self.assertEqual(parser(s,0), [True,["hoge",["hoge"]],8])
        self.assertEqual(parser(s,4), [True,["hoge",[]],8])
        self.assertEqual(parser("abc",0), [False,None,0])

    def test_option(self):
        # /(hoge)?/
        parser = option(token("hoge"))
        self.assertEqual(parser("hoge",0), [True, "hoge", 4])
        self.assertEqual(parser("hoge",1), [True, None, 1])

    def test_regexp(self):
        parser = regexp(re.compile("[1-9][0-9]*"))
        self.assertEqual(parser("2016",0), [True, "2016", 4])
        self.assertEqual(parser("2016",1), [False, None, 1])
        self.assertEqual(parser("2016",2), [True, "16", 4])

        parser = regexp(re.compile("abc",re.I))
        self.assertEqual(parser("abc",0), [True,"abc",3])
        self.assertEqual(parser("AbC",0), [True,"AbC",3])

    def test_lazy(self):
        parser = option(seq(token("hoge"),lazy(lambda:parser)))
        self.assertEqual(parser("",0), [True, None, 0])
        self.assertEqual(parser("hoge",0), [True, ["hoge",None], 4])
        self.assertEqual(parser("hogehoge",0), [True, ["hoge", ["hoge",None]], 8])
        self.assertEqual(parser("hoge",1), [True, None, 1])
        self.assertEqual(parser("hogeh",0), [True, ["hoge",None], 4])

    def test_map(self):
        parser = map(token("hoge"),lambda x:x+"!")
        self.assertEqual(parser("hoge",0), [True, "hoge!", 4])
        self.assertEqual(parser("hoge",1), [False, None, 1])

if __name__ == "__main__":
    unittest.main()
