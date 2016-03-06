import unittest
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

if __name__ == "__main__":
    unittest.main()
