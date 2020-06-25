'''
A point in n dimensional space
'''
class Point(object):
    '''
    coords - A list of values, one per dimension
    '''
    def __init__(self, coords):
        self.coords = coords
        self.n = len(coords)

    def __repr__(self):
        return str(self.coords)