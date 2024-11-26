from utils import *
import unittest
import numpy as np

# Test the edg2key function
def t_edg2key():
    p1, p2, p3, p4 = 1, 2, 506, 987
    
    if edg2key(p1,p2) == '1,2' and edg2key(p3,p4) == '506,987':
        return True
    else:
        return False
    
# Test the key2edg function
def t_key2edg():
    key1, key2 = '1,2', '506,987'
    
    if key2edg(key1) == [1,2] and key2edg(key2) == [506,987]:
        return True
    else:
        return False
    
# Test the create_list_edges function
def t_create_list_edges():
    face1, face2 = Face(1,2,3), Face(2,3,4)
    
    if all(i in create_list_edges([face1, face2]) for i in ['1,2','2,3','1,3','2,4','3,4']) :
        return True
    else:
        return False 
    
# Test the neighbours function
def t_neighbours():
    edges = [[1,2],[2,3],[1,3],[2,4],[3,4]]
    
    if neighbours(1, edges) == [2,3] and neighbours(2, edges) == [1,3,4]:
        return True
    else:
        return False
    
def t_check_neighbour():
    edge, edges1, edges2 = [2,3], [[1,2],[2,3],[1,3],[2,4],[3,4]], [[1,2],[2,3],[1,3],[2,4],[3,4],[2,5],[3,5]]
    
    return check_neighbour(edge, edges1) and not check_neighbour(edge, edges2)

def t_calculate_plane():
    p1, p2, p3, p4, p5 = np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1]), np.array([2, 0, 0])

    result1 = calculate_plane(p1, p2, p3) # Attendu : (0, 0, 1, 0) / Equation plane : z = 0
    result2 = calculate_plane(p2, p3, p4) # Attendu : (1, 1, 1, -1) / Equation plane : x + y + z = 1
    result3 = calculate_plane(p1, p2, p5) # Attendu : (0, 0, 0, 0) car p2 et p5 sont colinéaires
    
    if result1 == (0, 0, 1, 0) and result2 == (1, 1, 1, -1) and result3 == (0, 0, 0, 0):
        return True
    else:
        return False

class TestPrime(unittest.TestCase):
    def test_edg2key(self):
        self.assertTrue(t_edg2key())
    def test_key2edg(self):
        self.assertTrue(t_key2edg())
    def test_create_list_edges(self):
        self.assertTrue(t_create_list_edges())
    def test_neighbours(self):
        self.assertTrue(t_neighbours())
    def test_check_neighbour(self):
        self.assertTrue(t_check_neighbour())
    def test_calculate_plane(self):
        self.assertTrue(t_calculate_plane())

        
        
if __name__=='__main__':
    unittest.main()
    
    
    