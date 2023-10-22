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
    expression = expression + '#'

    tree = parse(expression)
    nodos_folha = []
    numerar(tree, nodos_folha)
    
    for i in range(len(nodos_folha)):
        nodos_folha[i].firstpos.add(i + 1)
        nodos_folha[i].lastpos.add(i + 1)

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
            if nodo.value.isalpha():
                concat = Node('.', nodo, tmp)
                nodo.parent = concat
                tmp.parent = concat
                concat.parent = tmp_parent
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

regex_to_tree("ab(a|b)*")
# parse("a|b")