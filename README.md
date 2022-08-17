# Diagonal-rectangulation-generator
This program generates all diagonal rectangulations of n rectangles and then visualises the graph associated with them. 
The program uses objects to represent the rectangles that are part of the diagonal rectangulation and performs pivots by moving the corners of the rectangles that are affected by the pivot. The relations between diagoanl rectangulations are stored in the adjacency matrix which indicates whether two diagonal rectangulations can be produced by using one pivot and also indicate the type of pivot required.

The program uses the python packages Numpy, Pillow and Graphviz.

In order to recreate the rectangulations we use Pillow. It creates a new file for each rectangulation.
Each rectangle is represented by using the coordinates produced by the program, each rectangle has an associated label and color.

The graph is produced using Graphviz. Each node of the graph is associated with a rectangulation and uses the image produced by Pillow.
The edges are placed based on the adjacency matrix produced. Two nodes are connected only if the corrsponding rectangulations can be produced by using a pivot.
The edges of the graph are colored to show that connection between the rectangulations, red for simple flips and blue for T-flips.
