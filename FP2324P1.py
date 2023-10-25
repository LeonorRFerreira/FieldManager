def eh_territorio(arg):
    """Verifica se o argumento corresponde a um território valido.

    Args:
        arg (tuple): Um territorio representado como um tuplo de tuplos, onde cada tuplo
        contém valores inteiros representando as intersecoes.

    Returns:
        boolean: True se o argumento é um territorio valido, False caso contrario.

    """
    if not isinstance(arg, tuple):  # Verifica se o argumento é um tuplo
        return False
    if len(arg) < 1:  # Verifica se o argumento contém pelo menos 1 caminho vertical e 1 caminho horizontal
        return False
    if any(not isinstance(path, tuple) for path in arg):
        return False
    for path in arg:
        if any(not isinstance(val, int) or (val != 0 and val != 1) for val in
               path):  # Verifica se os valores dentro dos caminhos são inteiros (0 ou 1)
            return False

    num_tuplos = len(arg) # Verifica o número de tuplos dentro do tuplo maior
    if 1 <= num_tuplos <= 26: # Verifica que o número de tuplos não ultrapasa o alfabeto
        first_length = len(arg[0]) # Verifica o comprimento do primeiro tuplo
        for tuplo in arg: # Percorre os outros tuplos e compara os seus comprimentos
            if len(tuplo) != first_length: #Se o comprimento for difirente em algum tuplo
                return False

        return True

    return False

#----------------------------------------------------------------------------------------------------------------------#

def obtem_ultima_intersecao(t):
    """Obtem a intersecao no extremo superior direito do territorio.

    Args:
        t (tuple): Um território válido.

    Returns:
        tuple: A intersecao no formato ('Letra', Número).
    """
    ultimo_tuplo = t[-1]  # Encontra o último tuplo no território (o tuplo mais à direita)
    numero_de_valores = len(ultimo_tuplo)  # Calcula a quantidade de valores dentro do último tuplo
    letra = chr(ord('A') + len(t) - 1)  # Subtrai 1 do número de tuplos para mapear para a letra do alfabeto
    return (letra, numero_de_valores)

#----------------------------------------------------------------------------------------------------------------------#

def eh_intersecao(arg):
    """Verifica se o argumento corresponde a uma intersecao valida.

    Args:
        arg (tuple): Uma intersecao representada como um tuplo ('Letra', Numero).

    Returns:
        boolean: True se o argumento é uma interseção válida, False caso contrário.
    """
    return (isinstance(arg, tuple) and len(arg) == 2 and isinstance(arg[0], str) and len(arg[0]) == 1 and 'A' \
            <= arg[0] <= 'Z' and isinstance(arg[1], int) and 1 <= arg[1] <= 99)

#----------------------------------------------------------------------------------------------------------------------#
def eh_intersecao_valida(t, i):
    """Verifica se a interseção é válida dentro do território dado.

    Args:
        t (tuple): Um território válido.
        i (tuple): Uma interseção representada como ('Letra', Número).

    Returns:
        boolean: True se a interseção é válida no território, False caso contrário.
    """

    numero_de_valores = obtem_ultima_intersecao(t)[1]
    letra = obtem_ultima_intersecao(t)[0]
    if i[0] <= letra and i[1] <= numero_de_valores:
        return True
    return False

#----------------------------------------------------------------------------------------------------------------------#
def eh_intersecao_livre(t, i):
    """Verifica se a interseção é livre (não ocupada por montanhas).

    Args:
        t (tuple): Um território válido.
        i (tuple): Uma interseção representada como ('Letra', Número).

    Returns:
        boolean: True se a interseção é livre, False caso contrário.
    """
    coluna = ord(i[0]) - ord('A')
    linha = i[1] - 1

    if eh_intersecao_valida(t, i):
        return t[coluna][linha] == 0

    return False

#----------------------------------------------------------------------------------------------------------------------#

def obtem_intersecoes_adjacentes(territorio, intersecao):
    """Obtém as interseções válidas adjacentes a uma interseção dada.

    Args:
        territorio (tuple): Um território válido.
        intersecao (tuple): Uma interseção válida.

    Returns:
        tuple: Um tuplo contendo as interseções adjacentes válidas.
    """
    if not eh_territorio(territorio) or not eh_intersecao_valida(territorio, intersecao):
        return ()  # Retorna uma tupla vazia se o território ou a interseção não forem válidos.

    letra, numero = intersecao[0], intersecao[1]
    letra = ord(letra) - ord('A')  # Converter letra para valor numérico (A=0, B=1, C=2, ...)

    adjacentes = []

    # Verifique as quatro direções possíveis: acima, abaixo, esquerda e direita.
    direcoes = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    for direcao in direcoes:
        nova_letra = chr(ord('A') + letra + direcao[0])  # Converter de volta para letra
        novo_numero = numero + direcao[1]

        # Verifique se a nova interseção está dentro dos limites do território.
        if eh_intersecao((nova_letra,novo_numero)) and eh_intersecao_valida(territorio,(nova_letra,novo_numero)):
            adjacentes.append((nova_letra, novo_numero))

    adjacentes.sort(key=lambda x: x[1])
    return tuple(adjacentes)

#----------------------------------------------------------------------------------------------------------------------#

def ordena_intersecoes(tup):
    """Ordena um tuplo de interseções de acordo com a ordem de leitura do território.

    Args:
        tup (tuple): Um tuplo de interseções.

    Returns:
        tuple: Um tuplo que contem as interseções ordenadas.
    """
    return tuple(sorted(tup, key=lambda x: (x[1], x[0])))

#----------------------------------------------------------------------------------------------------------------------#

def territorio_para_str(t):
    """Converte um território em uma representação de cadeia de caracteres.

    Args:
        t (tuple): Um território válido.

    Raises:
        ValueError: Se o argumento não for válido.

    Returns:
        str: Uma representação do território como uma cadeia de caracteres.
    """
    if not isinstance(t, tuple) or not all(isinstance(row, tuple) and len(row) == len(t[0]) for row in t):
        raise ValueError('territorio_para_str: argumentos inválidos')  # Correção na mensagem de exceção

    largura = len(t)  # Inicializa a variável de largura do território
    altura = len(t[0])  # Inicializa a variável de altura do território
    linhas = []  # Cria uma lista de strings para cada linha do território

    for i in range(altura, 0, -1):
        if (i > 9):
            linha = f"{i} "
        else:
            linha = f" {i} "  # Número da linha com um espaço em branco.

        for j in range(largura):
            if t[j][i - 1] == 1:
                linha += "X "  # Representação de uma montanha
            else:
                linha += ". "  # Representação de um espaço vazio

        if (i > 9):
            linha += f"{i}"
        else:
            linha += f" {i}"

        linhas.append(linha)

    colunas = "   " + " ".join([chr(ord('A') + j) for j in range(largura)])
    linhas.insert(0, colunas)
    linhas.append(colunas)

    return "\n".join(linhas)
#----------------------------------------------------------------------------------------------------------------------#

def obtem_cadeia(t, i):
    """Obtem uma cadeia de intersecoes conectadas a uma intersecao especifica

    Args:
        t (tuple): Um território válido
        i (tuple): Uma interseção válida

    Raises:
        ValueError: Se os argumentos não forem validos

    Returns:
        tuple: Um tuplo de intersecoes ordenadas da cadeia
    """
    if not eh_territorio(t) or not eh_intersecao_valida(t, i):
        raise ValueError('obtem_cadeia: argumentos inválidos')

    visited = set()  # Conjunto para armazenar interseções visitadas

    stack = []  # Pilha para realizar umas busca em profundidade
    stack.append(i)

    target_value = t[ord(i[0]) - ord('A')][i[1] - 1]  # Valor da interseção inicial

    while stack:
        current = stack.pop()
        if current not in visited:
            visited.add(current)
            adjacentes = obtem_intersecoes_adjacentes(t, current)
            for adj in adjacentes:
                adj_value = t[ord(adj[0]) - ord('A')][adj[1] - 1]
                if adj_value == target_value:
                    stack.append(adj)

    return tuple(ordena_intersecoes(visited))

#----------------------------------------------------------------------------------------------------------------------#

def obtem_vale(t, i):
    """Obtém as interseções que formam um vale a partir de uma interseção com montanhas.

    Args:
        t (tuple): Um território válido.
        i (tuple): Uma interseção com montanhas.

    Raises:
        ValueError: Se os argumentos não forem válidos.

    Returns:
        tuple: Um tuplo de interseções que compõem o vale.
    """
    if not eh_territorio(t) or not eh_intersecao_valida(t, i) or eh_intersecao_livre(t, i):
        raise ValueError('obtem_vale: argumentos invalidos')  # Mensagem de exceção corrigida

    cadeia = obtem_cadeia(t, i)

    # Verifica se há alguma montanha adjacente à interseção inicial
    montanha_adjacente = False
    for adj in obtem_intersecoes_adjacentes(t, i):
        coluna = ord(adj[0]) - ord('A')
        linha = adj[1] - 1
        if t[coluna][linha] == 1:
            montanha_adjacente = True
            break

    # Se houver montanhas adjacentes, encontra todas as interseções adjacentes às montanhas
    if montanha_adjacente:
        montanhas_adjacentes = set()
        for i in cadeia:
            adjacentes = obtem_intersecoes_adjacentes(t, i)
            for adj in adjacentes:
                coluna = ord(adj[0]) - ord('A')
                linha = adj[1] - 1
                if t[coluna][linha] == 1:
                    montanhas_adjacentes.add(adj)

        # Encontra todas as interseções sem montanhas, adjacentes às montanhas encontradas
        intersecoes_vale = set()
        for montanha in montanhas_adjacentes:
            adjacentes = obtem_intersecoes_adjacentes(t, montanha)
            for adj in adjacentes:
                coluna = ord(adj[0]) - ord('A')
                linha = adj[1] - 1
                if t[coluna][linha] == 0:
                    intersecoes_vale.add(adj)

    # Se não houver montanhas adjacentes, encontra todas as interseções vazias adjacentes
    else:
        intersecoes_vale = set()
        for adj in obtem_intersecoes_adjacentes(t, i):
            coluna = ord(adj[0]) - ord('A')
            linha = adj[1] - 1
            if t[coluna][linha] == 0:
                intersecoes_vale.add(adj)

    return tuple(ordena_intersecoes(intersecoes_vale))
#----------------------------------------------------------------------------------------------------------------------#

def verifica_conexao(t, i1, i2):
    """Verifica se duas interseções estão conectadas no território.

    Args:
        t (tuple): Um território válido.
        i1 (tuple): Uma interseção válida.
        i2 (tuple): Uma interseção válida.

    Raises:
        ValueError: Se os argumentos não forem válidos.

    Returns:
        boolean: True se as interseções estiverem conectadas, False caso contrário.
    """
    if not eh_territorio(t) or not eh_intersecao_valida(t, i1) or not eh_intersecao_valida(t, i2):
        raise ValueError('verifica_conexao: argumentos invalidos')

    cadeia_i1 = obtem_cadeia(t, i1)
    return i2 in cadeia_i1
#----------------------------------------------------------------------------------------------------------------------#


def calcula_numero_montanhas(t):
    """Calcula o número de interseções ocupadas por montanhas no território.

    Args:
        t (tuple): Um território válido.

    Raises:
        ValueError: Se o argumento não for válido.

    Returns:
        int: O número de montanhas no território.
    """
    if not eh_territorio(t):
        raise ValueError('calcula_numero_montanhas: argumento inválido')

    num_montanhas = 0

    for coluna in t:
        for valor in coluna:
            if valor == 1:
                num_montanhas += 1

    return num_montanhas
#----------------------------------------------------------------------------------------------------------------------#


def calcula_numero_cadeias_montanhas(t):
    """Calcula o número de cadeias montanhosas no território.

    Args:
        t (tuple): Um território válido.

    Raises:
        ValueError: Se o argumento não for válido.

    Returns:
        int: O número de cadeias montanhosas no território.
    """
    if not eh_territorio(t):
        raise ValueError('calcula_numero_cadeias_montanhas: argumento invalido')

    cadeias_montanhas = []  # Lista para armazenar as cadeias de montanhas encontradas

    for coluna in range(len(t)):
        for linha in range(len(t[0])):
            if t[coluna][linha] == 1:
                intersecao = (chr(ord('A') + coluna), linha + 1)
                cadeia = obtem_cadeia(t, intersecao)

                # Verifica se a cadeia já foi contabilizada
                if not any(all(i in cadeia for i in cadeia_montanha) for cadeia_montanha in cadeias_montanhas):
                    cadeias_montanhas.append(cadeia)

    return len(cadeias_montanhas)

#----------------------------------------------------------------------------------------------------------------------#

def calcula_tamanho_vales(t):
    """Calcula o tamanho dos vales.

    Args:
        t (tuple): Um território valido

    Raises:
        ValueError: ValueError: Se o argumento não for valido

    Returns:
        int: o numero total de intersecoes diferentes que formam todos os vales do territorio
    """
    if not eh_territorio(t):
        raise ValueError('calcula_tamanho_vales: argumento inválido')

    intersecoes_vales = set()  # Conjunto para armazenar todas as interseções dos vales

    for coluna in range(len(t)):  # Percorre as colunas
        for linha in range(len(t[coluna])):  # Percorre as linhas
            if t[coluna][linha] == 0:  # Verifica a igualdade a 0
                intersecao = chr(ord('A') + coluna), linha + 1
                if eh_intersecao_valida(t, intersecao):  # Verifique se a interseção é válida
                    vale = obtem_vale(t, intersecao)
                    intersecoes_vales.update(vale)

    return len(intersecoes_vales)
