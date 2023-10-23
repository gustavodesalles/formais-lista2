class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.parent = None
        self.c1 = left
        self.c2 = right
        self.firstpos = set()
        self.lastpos = set()
        self.nullable = None

def regex_to_tree(expression):
    aux = expression[-1] == '*'
    expression = expression + '#'

    tree = parse(expression)
    if aux:
        end_node = Node('#', None, None)
        concat_end = Node('.', tree, end_node)
        tree.parent = concat_end
        end_node.parent = concat_end
        tree = concat_end

    nodos_folha = []
    numerar(tree, nodos_folha)
    
    for i in range(len(nodos_folha)):
        nodos_folha[i].firstpos.add(i + 1)
        nodos_folha[i].lastpos.add(i + 1)
    
    get_nullable(tree)
    root = find_root(tree)
    print("Yeah!")

def parse(expression):
    i = len(expression) - 1
    next = None

    while i >= 0: # a|b
        if expression[i] == "|":
            nodo = Node(expression[i], None, next)
            next.parent = nodo
        elif expression[i] == ")":
            sub_begin = i
            balance = 1
            while balance != 0:
                sub_begin -= 1
                if expression[sub_begin] == "(":
                    balance -= 1
                elif expression[sub_begin] == ")":
                    balance += 1
            nodo = parse(expression[sub_begin + 1:i])
            i = sub_begin      
        else:
            nodo = Node(expression[i], None, None)
        if next == None:
            next = nodo
        elif next.value == '*' or next.value == '|':
            nodo.parent = next
            next.c1 = nodo
            tmp = next
            next = Node('.', None, tmp)
        elif next.value == '.':
            nodo.parent = next
            next.c1 = nodo
            next = nodo
        else:
            tmp = next
            tmp_parent = next.parent
            if nodo.value.isalpha() or nodo.value == '#' or nodo.value == '*':
                concat = Node('.', nodo, tmp)
                nodo.parent = concat
                tmp.parent = concat
                concat.parent = tmp_parent
                if tmp_parent is not None:
                    tmp_parent.c1 = concat
            else:
                nodo.c2 = tmp
            next = nodo
        i -= 1
    
    while nodo.parent != None:
        nodo = nodo.parent
    return nodo

def numerar(node, node_list):
    if node is None:
        return
    
    numerar(node.c1, node_list)

    if (node.value.isalpha() or node.value == '#') and node.c1 is None and node.c2 is None:
        node_list.append(node)
    
    numerar(node.c2, node_list)

def get_nullable(n):
    if n is None:
        return
    get_nullable(n.c1)
    nullable(n)
    firstpos(n)
    lastpos(n)
    get_nullable(n.c2)

def nullable(n):
    if n.c1 != None and n.value == '*':
        n.nullable = True
        # return True
    elif n.c1 != None and n.c2 != None:
        if n.value == '.':
            n.nullable = nullable(n.c1) and nullable(n.c2)
            # return nullable(n.c1) and nullable(n.c2)
        elif n.value == '|':
            n.nullable = nullable(n.c1) or nullable(n.c2)
            # return nullable(n.c1) or nullable(n.c2)
    elif n.c1 == None and n.c2 == None:
        if n.value == '&':
            n.nullable = True
            # return True
        elif n.value.isalpha() or n.value == '#':
            n.nullable = False
            # return False
    return n.nullable

def firstpos(n):
    if n.c1 != None and n.value == '*':
        n.firstpos = firstpos(n.c1)
        # return firstpos(n.c1)
    elif n.c1 != None and n.c2 != None:
        if n.value == '.':
            if nullable(n.c1):
                n.firstpos = firstpos(n.c1).union(firstpos(n.c2))
                # return firstpos(n.c1).union(firstpos(n.c2))
            else:
                n.firstpos = firstpos(n.c1)
                # return firstpos(n.c1)
        elif n.value == '|':
            n.firstpos = firstpos(n.c1).union(firstpos(n.c2))
            # return firstpos(n.c1).union(firstpos(n.c2))
    elif n.c1 == None and n.c2 == None:
        if n.value == '&':
            return {}
        elif n.value.isalpha() or n.value == '#':
            return n.firstpos
    return n.firstpos

def lastpos(n):
    if n.c1 != None and n.value == '*':
        n.lastpos = lastpos(n.c1)
        # return lastpos(n.c1)
    elif n.c1 != None and n.c2 != None:
        if n.value == '.':
            if nullable(n.c2):
                n.lastpos = lastpos(n.c1).union(lastpos(n.c2))
                # return lastpos(n.c1).union(lastpos(n.c2))
            else:
                n.lastpos = lastpos(n.c2)
                # return lastpos(n.c2)
        elif n.value == '|':
            n.lastpos = lastpos(n.c1).union(lastpos(n.c2))
            # return lastpos(n.c1).union(lastpos(n.c2))
    elif n.c1 == None and n.c2 == None:
        if n.value == '&':
            return {}
        elif n.value.isalpha() or n.value == '#':
            return n.lastpos
    return n.lastpos

def find_root(tree):
    while tree.value == '.':
        tree = tree.c1
    return tree

regex_to_tree("aab*")
# parse("a*b")
# regex_to_tree("a*b")
# parse("ab")
# regex_to_tree("(a|b)*")