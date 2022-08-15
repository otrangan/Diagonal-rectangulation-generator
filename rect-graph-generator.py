# -----------------------------------------------------------
# This program generates all rectangulations of n rectangles
# and visualises the graph associated with them
#
# (C) 2022 Orestis Tranganidas, Brussels, Belgium
# Released under GNU Public License (GPL)
# email Orestis.Tranganidas@ulb.be
# -----------------------------------------------------------

from numpy import sign
from copy import deepcopy
from PIL import Image, ImageDraw
import graphviz

class Rectangle:
    """
    Rectangle object 
    contains the coordinates of the four corners and the label of the rectangle
    """
    def __init__(self, bottom_left, bottom_right, top_left, top_right, i):
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right
        self.top_left = top_left
        self.top_right = top_right
        self.label = i
    
    #The following functions change the coordinates of the specified corner of the rectangle
    def set_bottom_left(self, p):
        self.bottom_left[0] = p[0]
        self.bottom_left[1] = p[1]
    
    def set_bottom_right(self, p):
        self.bottom_right[0] = p[0]
        self.bottom_right[1] = p[1]
        
    def set_top_left(self, p):
        self.top_left[0] = p[0]
        self.top_left[1] = p[1]
    
    def set_top_right(self, p):
        self.top_right[0] = p[0]
        self.top_right[1] = p[1]

    #Representation of the rectangle in string form    
    def __repr__(self):
        return  "bottom_left:% s bottom_right:% s top_left:% s top_right:% s label:% s" % (self.bottom_left, self.bottom_right, self.top_left, self.top_right, self.label) 
    
    def __str__(self):
        return  "bottom_left:% s bottom_right:% s top_left:% s top_right:% s label:% s" % (self.bottom_left, self.bottom_right, self.top_left, self.top_right, self.label) 

    #The following functions give the coordinates of the specified edge of the rectangle   
    def get_top_edge(self):
        return (self.top_left, self.top_right)
    
    def get_bottom_edge(self):
        return (self.bottom_left, self.bottom_right)
    
    def get_left_edge(self):
        return (self.bottom_left, self.top_left)
    
    def get_right_edge(self):
        return (self.bottom_right, self.top_right)
    
    def point_inside_rect(self, point):
        return point[0] > self.bottom_left[0] and point[0] < self.bottom_right[0] and point[1] > self.bottom_left[1] and point[1] < self.top_left[1]        

class Rectangulation:
    """
    Rectangulation object 
    
    contains a list of all the rectangles of the rectangulation
    """
    def __init__(self, n):
        #Initialization of the first rectangulation
        self.rects = []
        size = 100/n
        for i in range(n):
            self.rects.append(Rectangle([0+(size*i),0],[size+(size*i),0],[0+(size*i),100],[size+(size*i),100],i+1))
    
    def __eq__(self, other):
        #Returns if two rectangulations are equivalent
        same = True
        for i in range(len(self.rects)):
            self_top = []
            self_left = []
            self_bottom = []
            self_right = []
            other_top = []
            other_left = []
            other_bottom = []
            other_right = []
            """
            For every rectangle in the first rectangulation 
            checks if the rectangle with the same label in the second rectangulation
            comes in contact with the same rectangles
            """
            for j in range(len(self.rects)):
                if i != j:
                    if self.rects[j].bottom_right[1] == self.rects[i].top_right[1]:
                        if self.rects[i].top_left[0] <= self.rects[j].bottom_right[0] <= self.rects[i].top_right[0] or \
                           self.rects[i].top_left[0] <= self.rects[j].bottom_left[0] <= self.rects[i].top_right[0]:
                            self_top.append(self.rects[j].label)
                    elif self.rects[j].bottom_right[0] == self.rects[i].top_left[0]:
                        if self.rects[i].top_left[1] <= self.rects[j].bottom_right[1] <= self.rects[i].bottom_left[1] or \
                           self.rects[i].top_left[1] <= self.rects[j].top_right[1] <= self.rects[i].bottom_left[1]:
                            self_left.append(self.rects[j].label)
                    elif self.rects[j].bottom_left[0] == self.rects[i].top_right[0]:
                        if self.rects[i].top_right[1] <= self.rects[j].bottom_left[1] <= self.rects[i].bottom_right[1] or \
                           self.rects[i].top_right[1] <= self.rects[j].top_left[1] <= self.rects[i].bottom_right[1]:
                            self_right.append(self.rects[j].label)
                    elif self.rects[j].top_right[1] == self.rects[i].bottom_right[1]:
                        if self.rects[i].bottom_left[0] <= self.rects[j].top_right[0] <= self.rects[i].bottom_right[0] or \
                           self.rects[i].bottom_left[0] <= self.rects[j].top_left[0] <= self.rects[i].bottom_right[0]:
                            self_bottom.append(self.rects[j].label)
                    
                    if other.rects[j].bottom_right[1] == other.rects[i].top_right[1]:
                        if other.rects[i].top_left[0] <= other.rects[j].bottom_right[0] <= other.rects[i].top_right[0] or \
                           other.rects[i].top_left[0] <= other.rects[j].bottom_left[0] <= other.rects[i].top_right[0]:
                            other_top.append(other.rects[j].label)
                    elif other.rects[j].bottom_right[0] == other.rects[i].top_left[0]:
                        if other.rects[i].top_left[1] <= other.rects[j].bottom_right[1] <= other.rects[i].bottom_left[1] or \
                           other.rects[i].top_left[1] <= other.rects[j].top_right[1] <= other.rects[i].bottom_left[1]:
                            other_left.append(other.rects[j].label)
                    elif other.rects[j].bottom_left[0] == other.rects[i].top_right[0]:
                        if other.rects[i].top_right[1] <= other.rects[j].bottom_left[1] <= other.rects[i].bottom_right[1] or \
                           other.rects[i].top_right[1] <= other.rects[j].top_left[1] <= other.rects[i].bottom_right[1]:
                            other_right.append(other.rects[j].label)
                    elif other.rects[j].top_right[1] == other.rects[i].bottom_right[1]:
                        if other.rects[i].bottom_left[0] <= other.rects[j].top_right[0] <= other.rects[i].bottom_right[0] or \
                           other.rects[i].bottom_left[0] <= other.rects[j].top_left[0] <= other.rects[i].bottom_right[0]:
                            other_bottom.append(other.rects[j].label)
                    
                    if (self_top != other_top) or (self_left != other_left) or (self_bottom != other_bottom) or (self_right != other_right):
                        same = False
                        break
        return same
    
    def __repr__(self):
        #String representation of the rectangulation
        result = ""
        for i in self.rects:
            result += str(i)
            result += "\n"
        return result
        
def generate(n):
    #Function that generates all rectangulations
    r = Rectangulation(n)
    results = []#List of all generated rectangulations
    not_tested = []#Queue of all rectangulations that have not been used
    results.append(r)
    not_tested.append(r)
    adj_matrix = [[0]]#Matrix containing the relations between rectangulations
    while len(not_tested) > 0:
        """
        While there are unused rectangulations take the top of the queue
        """
        for i in range(n):
            for j in range(i+1, n):
                #Find all pairs of rectangles that come in contact and their common edge
                edge = common_edge(not_tested[0].rects[i], not_tested[0].rects[j])
                if edge != ([0,0],[0,0]):
                    temp,r = pivot(deepcopy(not_tested[0]), i, j, edge)
                    if temp not in results:
                        """
                        If the resulting rectangulation is new increase the adjacency matrix
                        and add the new rectangulation to the queue
                        """
                        print("New")
                        results.append(temp)
                        not_tested.append(temp)
                        for k in range(len(adj_matrix)):
                            if k == results.index(not_tested[0]):
                                adj_matrix[k].append(r)
                            else:
                                adj_matrix[k].append(0)
                        adj_matrix.append([0 if x != not_tested[0] else 1 for x in results])
                    elif temp != not_tested[0]:
                        """
                        If the resulting rectangulation has been generated before
                        add the relation between the two rectangulations to the adjacency matrix
                        """
                        print("Old")
                        adj_matrix[results.index(temp)][results.index(not_tested[0])] = r
                        adj_matrix[results.index(not_tested[0])][results.index(temp)] = r
        if len(not_tested) > 0:
            not_tested.pop(0)
    return results, adj_matrix

def common_edge(a, b):
    #Returns the common edge of two rectangles if it exists, otherwise returns ([0,0],[0,0])
    #Compares the corners of the rectangles
    if a.bottom_right == b.bottom_left:
        if (a.top_right[1] >= b.top_left[1]) and (a.top_right[0] == b.top_left[0]):
            return a.get_right_edge()
            
    elif a.bottom_right == b.top_right:
        if (a.bottom_left[0] <= b.top_left[0]) and (a.bottom_left[1] == b.top_left[1]):
            return a.get_bottom_edge()
            
    elif a.bottom_left == b.bottom_right:
        if (a.top_left[1] <= b.top_right[1]) and (a.top_left[0] == b.top_right[0]):
            return b.get_right_edge()
            
    elif a.bottom_left == b.top_left:
        if (a.bottom_right[0] <= b.top_right[0]) and (a.bottom_right[1] == b.top_right[1]):
            return b.get_top_edge()
            
    elif a.top_right == b.top_left:
        if (a.bottom_right[1] >= b.bottom_left[1]) and (a.bottom_right[0] == b.bottom_left[0]):
            return b.get_left_edge()
            
    elif a.top_right == b.bottom_right:
        if (a.top_left[0] >= b.bottom_left[0]) and (a.top_left[1] == b.bottom_left[1]):
            return b.get_bottom_edge()
            
    elif a.top_left == b.top_right:
        if (a.bottom_left[1] <= b.bottom_right[1]) and (a.bottom_left[0] == b.bottom_right[0]):
            return a.get_left_edge()
            
    elif a.top_left == b.bottom_left:
        if (a.top_right[0] >= b.bottom_right[0]) and (a.top_right[1] == b.bottom_right[1]):
            return a.get_top_edge()            
    return ([0,0],[0,0])
    
def pivot(rect, a, b, edge):
    """
    Perform a pivot based on the relation of the two rectangles
    
    return the result and the kind of flip that was performed if it was performed,
    return the original rectangulation otherwise 
    """
    if edge == rect.rects[a].get_top_edge():
        if edge == rect.rects[b].get_bottom_edge():
            return flip(rect,a,b,False,True),"f"
                
        elif rect.rects[a].top_left == rect.rects[b].bottom_left:
            return t_flip(rect,a,b,edge,False,True),"t"
            
    elif edge == rect.rects[a].get_left_edge():
        if edge == rect.rects[b].get_right_edge():
            return flip(rect,a,b,True,False),"f"
            
        elif rect.rects[a].top_left == rect.rects[b].top_right:
            return t_flip(rect,a,b,edge,True,False),"t"
            
    elif edge == rect.rects[a].get_bottom_edge():
        if edge == rect.rects[b].get_top_edge():
            return flip(rect,a,b,False,False),"f"
            
        elif rect.rects[a].bottom_right == rect.rects[b].top_right:
            return t_flip(rect,a,b,edge,False,False),"t"
            
    elif edge == rect.rects[a].get_right_edge():
        if edge == rect.rects[b].get_left_edge():
            return flip(rect,a,b,True,True),"f"
            
        elif rect.rects[a].bottom_right == rect.rects[b].bottom_left:
            return t_flip(rect,a,b,edge,True,True),"t"
            
    elif edge == rect.rects[b].get_top_edge() and rect.rects[a].bottom_left == rect.rects[b].top_left:
        return t_flip(rect,a,b,edge,False,False),"t"
        
    elif edge == rect.rects[b].get_left_edge() and rect.rects[a].top_right == rect.rects[b].top_left:
        return t_flip(rect,a,b,edge,True,True),"t"
        
    elif edge == rect.rects[b].get_bottom_edge() and rect.rects[a].top_right == rect.rects[b].bottom_right:
        return t_flip(rect,a,b,edge,False,True),"t"
        
    elif edge == rect.rects[b].get_right_edge() and rect.rects[a].bottom_left == rect.rects[b].bottom_right:
        return t_flip(rect,a,b,edge,True,False),"t"
        
    return rect,0

def flip(rect,a,b,vertical,afirst):
    """
    Perform simple flip and return the result
    
    First, find the points so that the new edge intersects the diagonal
    then, change the coordinates of the corners of the two rectangles so that they are separated by the new edge
    and their order in the rectangulation has been changed
    """
    print("Flip")
    if vertical:
    #The common edge is vertical
        middle = (rect.rects[a].bottom_left[1] + rect.rects[a].top_left[1])/2
        if afirst:
        #Rectangle a is first in the ordering
            spot = find_spot(middle, rect.rects[a].bottom_left, rect.rects[b].top_right, 1)
            rect.rects[a].set_top_right(rect.rects[b].top_right)
            rect.rects[a].set_bottom_right([rect.rects[b].top_right[0],spot])
            rect.rects[b].set_bottom_left(rect.rects[a].bottom_left)
            rect.rects[a].set_bottom_left([rect.rects[a].top_left[0],spot])
            rect.rects[b].set_top_left(rect.rects[a].bottom_left)
            rect.rects[b].set_top_right(rect.rects[a].bottom_right)
        else:
        #Rectangle b is first in the ordering
            spot = find_spot(middle, rect.rects[b].bottom_left, rect.rects[a].top_right, 1)
            rect.rects[b].set_top_right(rect.rects[a].top_right)
            rect.rects[b].set_bottom_right([rect.rects[a].top_right[0],spot])
            rect.rects[a].set_bottom_left(rect.rects[b].bottom_left)
            rect.rects[b].set_bottom_left([rect.rects[b].top_left[0],spot])
            rect.rects[a].set_top_left(rect.rects[b].bottom_left)
            rect.rects[a].set_top_right(rect.rects[b].bottom_right)
    else:
    #The common edge is horizontal
        middle = (rect.rects[a].bottom_left[0] + rect.rects[a].bottom_right[0])/2
        if afirst:
        #Rectangle a is first in the ordering
            spot = find_spot(middle, rect.rects[a].bottom_left, rect.rects[b].top_right, 0)
            rect.rects[b].set_bottom_left(rect.rects[a].bottom_left)
            rect.rects[a].set_top_right(rect.rects[b].top_right)
            rect.rects[b].set_top_right([spot,rect.rects[b].top_left[1]])
            rect.rects[b].set_bottom_right([spot,rect.rects[b].bottom_left[1]])
            rect.rects[a].set_top_left(rect.rects[b].top_right)
            rect.rects[a].set_bottom_left(rect.rects[b].bottom_right)
        else:
        #Rectangle b is first in the ordering
            spot = find_spot(middle, rect.rects[b].bottom_left, rect.rects[a].top_right, 0)
            rect.rects[a].set_bottom_left(rect.rects[b].bottom_left)
            rect.rects[b].set_top_right(rect.rects[a].top_right)
            rect.rects[a].set_top_right([spot,rect.rects[a].top_left[1]])
            rect.rects[a].set_bottom_right([spot,rect.rects[a].bottom_left[1]])
            rect.rects[b].set_top_left(rect.rects[a].top_right)
            rect.rects[b].set_bottom_left(rect.rects[a].bottom_right)
    return rect
    
def find_spot(middle, bottom_left, top_right, vertical):
    #Find the points that has to be used in order for the new edge to intersect the diagonal
    found = False
    spot = middle#Start from the middle of the rectangle that is formed by the combination of the two rectangles
    max_spot = top_right[vertical]#Highest point of the rectangle that is the combination of the two rectangles
    min_spot = bottom_left[vertical]#Lowest point of the rectangle that is the combination of the two rectangles
    if vertical:
        pointa = [top_right[0], spot]
        pointb = [bottom_left[0], spot]
    else:
        pointa = [spot, top_right[1]]
        pointb = [spot, bottom_left[1]]
    #Claculate cross product to find the points are above or below the diagonal
    v1 = [100,-100]
    va2 = [100-pointa[0],0-pointa[1]]
    vb2 = [100-pointb[0],0-pointb[1]]
    da = sign(int(v1[0]*va2[1] - v1[1]*va2[0]))
    db = sign(int(v1[0]*vb2[1] - v1[1]*vb2[0]))
    while not found and max_spot != min_spot:
        """
        If both points are on the same side of the diagonal
        we move them by half the distance to the maximum or minimum spot and repeat
        """
        if (da*db) < 0:
            found = True
        else:
            if da < 0:
                spot = (min_spot+spot)/2
            elif da > 0:
                spot = (max_spot+spot)/2
            elif da == 0 and db < 0:
                spot = (min_spot+spot)/2
            elif da == 0 and db > 0:
                spot = (max_spot+spot)/2
            #Recalculate cross product
            pointa[vertical] = spot
            pointb[vertical] = spot
            va2 = [100-pointa[0],0-pointa[1]]
            vb2 = [100-pointb[0],0-pointb[1]]
            da = sign(int(v1[0]*va2[1] - v1[1]*va2[0]))
            db = sign(int(v1[0]*vb2[1] - v1[1]*vb2[0]))                
    return spot
    
def t_flip(rect,a,b,edge,vertical,afirst):
    """
    Perform T-flip and return the result
    
    Change the coordinates of the corners of the two rectangles so that they are separated by the new edge
    and their order in the rectangulation has been changed
    """
    print("T-flip")
    if vertical:
    #The common edge is vertical
        if afirst:
        #Rectangle a is first in the ordering
            if rect.rects[a].get_right_edge() == edge:
                rect.rects[a].set_bottom_right(rect.rects[b].top_left)
                rect.rects[b].set_bottom_left(rect.rects[a].bottom_left)
                rect.rects[a].set_bottom_left([rect.rects[a].top_left[0],rect.rects[b].top_right[1]])
                rect.rects[b].set_top_left(rect.rects[a].bottom_left)
            else:
                rect.rects[a].set_top_right(rect.rects[b].top_right)
                rect.rects[b].set_top_left(rect.rects[a].bottom_right)
                rect.rects[b].set_top_right([rect.rects[b].bottom_right[0],rect.rects[a].bottom_left[1]])
                rect.rects[a].set_bottom_right(rect.rects[b].top_right)
        else:
        #Rectangle b is first in the ordering
            if rect.rects[b].get_right_edge() == edge:
                rect.rects[b].set_bottom_right(rect.rects[a].top_left)
                rect.rects[a].set_bottom_left(rect.rects[b].bottom_left)
                rect.rects[b].set_bottom_left([rect.rects[b].top_left[0],rect.rects[a].top_right[1]])
                rect.rects[a].set_top_left(rect.rects[b].bottom_left)
            else:
                rect.rects[b].set_top_right(rect.rects[a].top_right)
                rect.rects[a].set_top_left(rect.rects[b].bottom_right)
                rect.rects[a].set_top_right([rect.rects[a].bottom_right[0],rect.rects[b].bottom_left[1]])
                rect.rects[b].set_bottom_right(rect.rects[a].top_right)
    else:
    #The common edge is horizontal
        if afirst:
        #Rectangle a is first in the ordering
            if rect.rects[a].get_top_edge() == edge:
                rect.rects[a].set_top_left(rect.rects[b].bottom_right)
                rect.rects[b].set_bottom_left(rect.rects[a].bottom_left)
                rect.rects[a].set_bottom_left([rect.rects[b].top_right[0],rect.rects[a].bottom_right[1]])
                rect.rects[b].set_bottom_right(rect.rects[a].bottom_left)
            else:
                rect.rects[a].set_top_right(rect.rects[b].top_right)
                rect.rects[b].set_bottom_right(rect.rects[a].top_left)
                rect.rects[a].set_top_left([rect.rects[a].bottom_left[0],rect.rects[b].top_left[1]])
                rect.rects[b].set_top_right(rect.rects[a].top_left)
        else:
        #Rectangle b is first in the ordering
            if rect.rects[b].get_top_edge() == edge:
                rect.rects[b].set_top_left(rect.rects[a].bottom_right)
                rect.rects[a].set_bottom_left(rect.rects[b].bottom_left)
                rect.rects[b].set_bottom_left([rect.rects[a].top_right[0],rect.rects[b].bottom_right[1]])
                rect.rects[a].set_bottom_right(rect.rects[b].bottom_left)
            else:
                rect.rects[b].set_top_right(rect.rects[a].top_right)
                rect.rects[a].set_bottom_right(rect.rects[b].top_left)
                rect.rects[b].set_top_left([rect.rects[b].bottom_left[0],rect.rects[a].top_left[1]])
                rect.rects[a].set_top_right(rect.rects[b].top_left)
    return rect
        
def main():
    n = 3#Choose number of rectangles used
    colors = ["red","yellow","blue","orange","purple","green"]#List of colors to be used in visualization
    rects, mat = generate(n)
    #For each rectangulation produce a image using Pillow and the corresponding node using Graphviz
    dot = graphviz.Graph("graph"+str(n),format="png")
    for rect in range(len(rects)):
        im = Image.new('RGB', (100, 100), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        for i in range(len(rects[rect].rects)):
            draw.rectangle((rects[rect].rects[i].bottom_left[0], 100-rects[rect].rects[i].bottom_left[1],
                            rects[rect].rects[i].top_right[0], 100-rects[rect].rects[i].top_right[1]),outline="black",fill=colors[i],width=2)
        draw.line((0,0,100,100),fill=(0,0,0),width=2)
        im.save(str(rect)+".png", quality=95)
        dot.node(str(rect), shape="box", label="", image=str(rect)+".png")
    #Draw the edges between two nodes on Graphviz based on the adjacency matrix
    for i in range(len(mat)):
        for j in range(i+1,len(mat[i])):
            if mat[i][j] == "f":
                dot.edge(str(i),str(j),color="red")
            elif mat[i][j] == "t":
                dot.edge(str(i),str(j),color="blue")
    dot.render(directory="", view=True)
    
if __name__ == '__main__':
    main()
    
    
