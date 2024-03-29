# Bridge Edges v4
#
# Find the bridge edges in a graph given the
# algorithm in lecture.
# Complete the intermediate steps
#  - create_rooted_spanning_tree
#  - post_order
#  - number_of_descendants
#  - lowest_post_order
#  - highest_post_order
#
# And then combine them together in
# `bridge_edges`

# So far, we've represented graphs
# as a dictionary where G[n1][n2] == 1
# meant there was an edge between n1 and n2
#
# In order to represent a spanning tree
# we need to create two classes of edges
# we'll refer to them as "green" and "red"
# for the green and red edges as specified in lecture
#
# So, for example, the graph given in lecture
# G = {'a': {'c': 1, 'b': 1},
#      'b': {'a': 1, 'd': 1},
#      'c': {'a': 1, 'd': 1},
#      'd': {'c': 1, 'b': 1, 'e': 1},
#      'e': {'d': 1, 'g': 1, 'f': 1},
#      'f': {'e': 1, 'g': 1},
#      'g': {'e': 1, 'f': 1}
#      }
# would be written as a spanning tree
# S = {'a': {'c': 'green', 'b': 'green'},
#      'b': {'a': 'green', 'd': 'red'},
#      'c': {'a': 'green', 'd': 'green'},
#      'd': {'c': 'green', 'b': 'red', 'e': 'green'},
#      'e': {'d': 'green', 'g': 'green', 'f': 'green'},
#      'f': {'e': 'green', 'g': 'red'},
#      'g': {'e': 'green', 'f': 'red'}
#      }
#


def create_rooted_spanning_tree(G, root):
    S = {}
    marked = {root}
    openlist = [root]
    # your code here
    while len(openlist) > 0:
        node=openlist.pop()
        for neighbor in G[node]:
            if neighbor not in marked:
                marked.add(neighbor)
                openlist.append(neighbor)
                if neighbor not in S:
                    S[neighbor] = {}
                S[neighbor][node] = 'green'
                if node not in S:
                    S[node] = {}
                S[node][neighbor] = 'green'
            elif neighbor not in S[node]:
                if neighbor not in S:
                    S[neighbor] = {}
                S[neighbor][node] = 'red'
                if node not in S:
                    S[node] = {}
                S[node][neighbor] = 'red'
    return S

# This is just one possible solution
# There are other ways to create a
# spanning tree, and the grader will
# accept any valid result
# feel free to edit the test to
# match the solution your program produces


def test_create_rooted_spanning_tree():
    G = {'a': {'c': 1, 'b': 1},
         'b': {'a': 1, 'd': 1},
         'c': {'a': 1, 'd': 1},
         'd': {'c': 1, 'b': 1, 'e': 1},
         'e': {'d': 1, 'g': 1, 'f': 1},
         'f': {'e': 1, 'g': 1},
         'g': {'e': 1, 'f': 1}
         }
    S = create_rooted_spanning_tree(G, "a")
    assert S == {'a': {'c': 'green', 'b': 'green'},
                 'b': {'a': 'green', 'd': 'red'},
                 'c': {'a': 'green', 'd': 'green'},
                 'd': {'c': 'green', 'b': 'red', 'e': 'green'},
                 'e': {'d': 'green', 'g': 'green', 'f': 'green'},
                 'f': {'e': 'green', 'g': 'red'},
                 'g': {'e': 'green', 'f': 'red'}
                 }

###########


def post_order(S, root):
    # return mapping between nodes of S and the post-order value
    # of that node
    output = {root: 1}
    marked = {root}
    openlist = [root]
    counter = 0

    # your code here
    while len(openlist) > 0:
        pendingList = []
        node=openlist.pop()
        for neighbor in S[node]:
            if S[node][neighbor] == 'green':
                if neighbor not in marked:
                    marked.add(neighbor)
                    pendingList.append(neighbor)
        counter += 1
        output[node] = counter
        openlist = pendingList+openlist
        del pendingList
    for i in output:
        output[i]=1+counter-output[i]
    return output

# This is just one possible solution
# There are other ways to create a
# spanning tree, and the grader will
# accept any valid result.
# feel free to edit the test to
# match the solution your program produces


def test_post_order():
    S = {'a': {'c': 'green', 'b': 'green'},
         'b': {'a': 'green', 'd': 'red'},
         'c': {'a': 'green', 'd': 'green'},
         'd': {'c': 'green', 'b': 'red', 'e': 'green'},
         'e': {'d': 'green', 'g': 'green', 'f': 'green'},
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'}
         }
    po = post_order(S, 'a')
    assert po == {'a': 7, 'b': 1, 'c': 6, 'd': 5, 'e': 4, 'f': 2, 'g': 3}
##############


def number_of_descendants(S, root):
    # return mapping between nodes of S and the number of descendants
    # of that node
    output = {}
    marked = {root}

    number_of_descendants_rec(S, root, output, marked)
    return output
    # your code here

def number_of_descendants_rec(S, currentNode, output, marked):
    desCount = 1
    for neighbor in S[currentNode]:
        if neighbor not in marked:
            if S[currentNode][neighbor] == 'green':
                marked.add(neighbor)
                desCount+=number_of_descendants_rec(S, neighbor, output, marked)
    output[currentNode] = desCount
    return desCount

def test_number_of_descendants():
    S = {'a': {'c': 'green', 'b': 'green'},
         'b': {'a': 'green', 'd': 'red'},
         'c': {'a': 'green', 'd': 'green'},
         'd': {'c': 'green', 'b': 'red', 'e': 'green'},
         'e': {'d': 'green', 'g': 'green', 'f': 'green'},
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'}
         }
    nd = number_of_descendants(S, 'a')
    print(nd)
    assert nd == {'a': 7, 'b': 1, 'c': 5, 'd': 4, 'e': 3, 'f': 1, 'g': 1}

###############


def lowest_post_order(S, root, po):
    # return a mapping of the nodes in S
    # to the lowest post order value
    # below that node
    # (and you're allowed to follow 1 red edge)
    marked = {root}
    output = {}
    lowest_post_order_rec(S, po, output, marked, root)
    return output

def lowest_post_order_rec(S, po, output, marked, currentNode):
    temp = lowestPO = po[currentNode]
    for neighbor in S[currentNode]:
        if S[currentNode][neighbor]=='green':
            if neighbor not in marked:
                marked.add(neighbor)
                temp = lowest_post_order_rec(S,po,output,marked,neighbor)
        else:
            temp = po[neighbor]
        if temp<lowestPO:
            lowestPO=temp
    output[currentNode]=lowestPO
    return lowestPO

def test_lowest_post_order():
    S = {'a': {'c': 'green', 'b': 'green'},
         'b': {'a': 'green', 'd': 'red'},
         'c': {'a': 'green', 'd': 'green'},
         'd': {'c': 'green', 'b': 'red', 'e': 'green'},
         'e': {'d': 'green', 'g': 'green', 'f': 'green'},
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'}
         }
    po = post_order(S, 'a')
    l = lowest_post_order(S, 'a', po)
    print(l)
    assert l == {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 2, 'f': 2, 'g': 2}

################

def highest_post_order(S, root, po):
    # return a mapping of the nodes in S
    # to the highest post order value
    # below that node
    # (and you're allowed to follow 1 red edge)
    marked = {root}
    output = {}
    highest_post_order_rec(S, po, output, marked, root)
    return output

def highest_post_order_rec(S, po, output, marked, currentNode):
    temp = highestPO = po[currentNode]
    for neighbor in S[currentNode]:
        if S[currentNode][neighbor]=='green':
            if neighbor not in marked:
                marked.add(neighbor)
                temp = highest_post_order_rec(S,po,output,marked,neighbor)
        else:
            temp = po[neighbor]
        if temp>highestPO:
            highestPO=temp
    output[currentNode]=highestPO
    return highestPO


def test_highest_post_order():
    S = {'a': {'c': 'green', 'b': 'green'},
         'b': {'a': 'green', 'd': 'red'},
         'c': {'a': 'green', 'd': 'green'},
         'd': {'c': 'green', 'b': 'red', 'e': 'green'},
         'e': {'d': 'green', 'g': 'green', 'f': 'green'},
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'}
         }
    po = post_order(S, 'a')
    h = highest_post_order(S, 'a', po)
    print(h)
    assert h == {'a': 7, 'b': 5, 'c': 6, 'd': 5, 'e': 4, 'f': 3, 'g': 3}

#################


def bridge_edges(G, root):
    # use the four functions above
    # and then determine which edges in G are bridge edges
    # return them as a list of tuples ie: [(n1, n2), (n4, n5)]
    S=create_rooted_spanning_tree(G,root)
    po=post_order(S,root)
    nd=number_of_descendants(S,root)
    l=lowest_post_order(S,root,po)
    h=highest_post_order(S,root,po)
    marked={root}
    output=[]
    bridge_edges_rec(S,po,nd,l,h,marked,output,root)
    #h<po and l>po-nd
    return output

def bridge_edges_rec(S,po,nd,l,h,marked,output,currentNode):
    for neighbor in S[currentNode]:
        if neighbor not in marked:
            if S[currentNode][neighbor]=='green':
                marked.add(neighbor)
                if(h[neighbor]<=po[neighbor] and l[neighbor]>po[neighbor]-nd[neighbor]):
                    output.append((currentNode,neighbor))
                bridge_edges_rec(S,po,nd,l,h,marked,output,neighbor)
    return 0

def test_bridge_edges():
    G = {'a': {'c': 1, 'b': 1},
         'b': {'a': 1, 'd': 1},
         'c': {'a': 1, 'd': 1},
         'd': {'c': 1, 'b': 1, 'e': 1},
         'e': {'d': 1, 'g': 1, 'f': 1},
         'f': {'e': 1, 'g': 1},
         'g': {'e': 1, 'f': 1}
         }
    bridges = bridge_edges(G, 'a')
    print(bridges)
    assert bridges == [('d', 'e')]

test_bridge_edges()