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
    
    if key2edg(key) == [1,2]:
        return True
    else:
        return False
    
    
def t1_check_neighbour():
    # Creation of an edge
    edge = [0,1]
    
    # List of the edges of the problematic figure (b)
    edges = create_dict_edges([[0,1,2],[0,1,4],[0,3,1]])
    
    # Return of the check
    return check_neighbour(edge, edges)

def t2_check_neighbour():
    # Creation of an edge
    edge = [0,2]
    
    # List of the edges of the problematic figure (b)
    edges = create_dict_edges([[0,1,2],[0,1,4],[0,3,1]])
    
    # Return of the check
    return check_neighbour(edge, edges)

def t_check_second_condition():
    
    # List of the edges of the problematic figure (b)
    edges = create_dict_edges([[0,1,2],[0,1,4],[0,3,1]])
    
    verifedges = edges
    
    edges = check_second_condition(edges)
    
    verifedges[edg2key(0,1)] = False
    
    return edges == verifedges
    

class TestPrime(unittest.TestCase):
    def test_edg2key(self):
        self.assertTrue(t_edg2key())
    def test_key2edg(self):
        self.assertTrue(t_key2edg())
    def test_1_check_neighbour(self):
        self.assertFalse(t1_check_neighbour())
    def test_2_check_neighbour(self):
        self.assertTrue(t2_check_neighbour())
    def test_check_second_condition(self):
        self.assertTrue(t_check_second_condition())

        
        
if __name__=='__main__':
    unittest.main()
    
    
    