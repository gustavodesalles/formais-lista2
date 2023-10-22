class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.parent = None
        self.c1 = left
        self.c2 = right

def regex_to_tree(expression):
    expression = expression + '#'

    parse(expression)

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
            nodo = parse(expression[sub_begin:i])
            i -= sub_begin      
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
            next = Node('.', nodo, tmp)
            nodo.parent = next
            next.parent = tmp.parent
            next = nodo
            # tmp = next.parent
            # concat = Node('.', None, next)
            # tmp.c2 = concat
            # next.parent = concat
            # nodo.parent = tmp
            # next = tmp
            # tmp.parent = next
            # next.c1 = tmp
            # nodo.parent = tmp
            # next = tmp
        i -= 1
    return nodo

parse("aba*")