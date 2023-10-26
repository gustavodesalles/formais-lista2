class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.parent = None
        self.c1 = left
        self.c2 = right
        self.firstpos = set()
        self.lastpos = set()
        self.followpos = set()
        self.nullable = None
        self.number = None

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
        nodos_folha[i].number = i + 1
        nodos_folha[i].firstpos.add(i + 1)
        nodos_folha[i].lastpos.add(i + 1)
    
    get_nullable(tree)
    root = find_root(tree)

    for i in nodos_folha:
        followpos(tree, i)
    
    montar_automato(nodos_folha, root)

def parse(expression):
    i = len(expression) - 1
    next = None

    while i >= 0: 
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
                nodo.c2 = tmp # problema está aqui
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
            return set()
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
            return set()
        elif n.value.isalpha() or n.value == '#':
            return n.lastpos
    return n.lastpos

def find_root(tree):
    while tree.c1.value == '.':
        tree = tree.c1
    return tree

def followpos(tree, n):
    if tree is None:
        return
    
    if n.value == '#':
        return set()
    
    followpos(tree.c1, n)
    if tree.value == '.':
        # if tree.c1.lastpos.contains(n.number):
        if n.number in tree.c1.lastpos:
            n.followpos = n.followpos.union(tree.c2.firstpos)
    elif tree.value == '*':
        # if tree.lastpos.contains(n.number):
        if n.number in tree.lastpos:
            n.followpos = n.followpos.union(tree.firstpos)
    followpos(tree.c2, n)

def formatar_listas_estados(lista):
    lista_final = []
    for i in lista:
        lista_final.append('{' + formatar_set(i) + '}')
    return ",".join(lista_final)

def formatar_set(conjunto):
    return ",".join(map(str, sorted(list(conjunto))))

def formatar_transicoes(transicoes):
    transicoes_str = []
    lista_transicoes = list(transicoes)
    lista_transicoes = sorted(lista_transicoes, key=lambda x : formatar_set(x[0]))
    for i in lista_transicoes:
        aux = f"{{{formatar_set(i[0])}}},{i[1]},{{{formatar_set(i[2])}}}"
        transicoes_str.append(aux)
    return transicoes_str

def montar_automato(nodos_folha, root):
    estados = []
    alfabeto = set()
    estado_inicial = root.firstpos
    estados.append(estado_inicial)
    transicoes = []
    estados_finais = []

    for i in nodos_folha:
        if i.value != '&' and i.value != '#':
            alfabeto.add(i.value)
    
    for i in estados:
        for k in alfabeto:
            novo_estado = set()
            for j in i:
                if j == len(nodos_folha):
                    if i not in estados_finais:
                        estados_finais.append(i)
                if nodos_folha[j - 1].value == k:
                    novo_estado = novo_estado.union(nodos_folha[j - 1].followpos)
            if novo_estado not in estados and len(novo_estado) > 0:
                estados.append(novo_estado)
            if (i,k,novo_estado) not in transicoes and len(novo_estado) > 0:
                transicoes.append((i,k,novo_estado))
    
    transicoes_str = formatar_transicoes(transicoes)
    # print(f"{len(estados)}")
    # print(f"{formatar_set(estado_inicial)}")
    # print(f"{formatar_listas_estados(estados_finais)}")
    # print(f"{','.join(sorted(list(alfabeto)))}")
    # print(f"{';'.join(transicoes_str)}")
    print(f"{len(estados)};{{{formatar_set(estado_inicial)}}};{{{','.join({formatar_listas_estados(estados_finais)})}}};{{{','.join(sorted(list(alfabeto)))}}};{';'.join(transicoes_str)}")

# regex_to_tree("aab*")
# regex_to_tree("aa*(bb*aa*b)*")
regex_to_tree("(&|b)(ab)*(&|a)")
# parse("a*b")
# regex_to_tree("a*b")
# parse("ab")
# regex_to_tree("(a|b)*")