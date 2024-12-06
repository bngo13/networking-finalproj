# Networking Final Project

## Dependencies

Dependencies can be installed by running either:

-   `pip install -r requirements.txt`
-   `pip3 install -r requirements.txt`

List of requirements that will be installed after running the above command:

1. networkx[default]
2. PyQT6

## Usage

python3 graph.py

## Input

A default file is given under the name `default_input.txt`, but a custom file can be passed (added to the same directory as graph.py). The format of the file is the following:

1. Each line represents as a node and it's edges.
2. A node is represented by the first letter in each line.
3. An edge is represented by a node after the first letter in each line.
4. The format of an edge is the following: `NODE-COST`
5. For instance:
    - U V-2: An edge from U to V with a cost of 2
    - X Y-1 Z-5: An edge from X to Y with a cost of 1 and an edge from X to Z with a cost of 5
6. Each node in an edge must be accounted for as a node in a line. (You cannot reference an edge not defined)

### Input Example

This is what a possible input graph may look like

```
U V-2 X-1 W-5
V X-2 W-3
X W-3 Y-1
W Y-1 Z-5
Y Z-2
Z
```
