from utils import *
import unittest


def t_edg2key():
    p1 = 1
    p2 = 2
    
    if edg2key(p1,p2) == '1,2':
        return True
    else:
        return False
    
def t_key2edg():
    key = '1,2'
    
    if key2edg(key) == (1,2):
        return True
    else:
        return False
    
def t1_create_dict_edges():
    
    # Creation of some faces
    faces = [[1,2,3],[1,4,2],[1,5,2]]
    
    # Creation of the dict
    dic = create_dict_edges(faces)
    
    if dic['1,2'] == 3:
        return True
    else:
        return False
    
def t2_create_dict_edges():
    # Creation of some faces
    faces = [[1,2,3],[1,4,2],[1,5,2]]
    
    # Creation of the dict
    dic = create_dict_edges(faces)
    
    if dic['2,4'] == 1:
        return True
    else:
        return False
    

class TestPrime(unittest.TestCase):
    def test_edg2key(self):
        self.assertTrue(t_edg2key())
    def test_key2edg(self):
        self.assertTrue(t_key2edg())
    def test_1_create_dict_edges(self):
        self.assertTrue(t1_create_dict_edges())
    def test_2_create_dict_edges(self):
        self.assertTrue(t2_create_dict_edges())

        
        
if __name__=='__main__':
    unittest.main()
    
    
    