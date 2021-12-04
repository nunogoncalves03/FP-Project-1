# Projeto 1 - Buggy Data Base (BDB)
# Nuno Gonçalves - nunomrgoncalves@tecnico.ulisboa.pt (ist1103392) - 29/10/2021

def corrigir_palavra(palavra):
    '''
    corrigir_palavra: cad. carateres -> cad. carateres
    Esta função recebe uma palavra (potencialmente modificada por um surto de
    letras) e devolve essa mesma palavra corrigida, removendo os pares
    minúscula/maiúscula adjacentes da mesma letra.
    '''
    palavra_corrigida = False
    while not palavra_corrigida:
        palavra_corrigida = True
        for indice in range(0, len(palavra) - 1):
            if abs(ord(palavra[indice]) - ord(palavra[indice + 1])) == 32:
                palavra = palavra[:indice] + palavra[indice + 2:]
                palavra_corrigida = False  
                break
    return palavra


def eh_anagrama(palavra_1, palavra_2):   
    '''
    eh_anagrama: cad. carateres X cad. carateres -> booleano
    Esta função recebe duas palavras e devolve True se uma é anagrama da outra
    (palavras constituídas pelas mesmas letras).
    '''
    # Ignorar diferenças entre maiúsculas e minúsculas
    palavra_1 = palavra_1.lower()
    palavra_2 = palavra_2.lower()       
    if len(palavra_1) != len(palavra_2):
        return False        
    for caractere in palavra_1:
        if palavra_1.count(caractere) != palavra_2.count(caractere):
            return False    
    return True


def corrigir_doc(texto):
    '''
    corrigir_doc: cad. carateres -> cad. carateres
    Esta função recebe um texto com erros da documentação da BDB e devolve esse
    mesmo texto filtrado com as palavras corrigidas e os anagramas retirados,
    ficando apenas a sua primeira ocorrência. Gera um ValueError caso o texto
    não seja válido.
    '''
    def validar_texto(texto):
        '''
        validar_texto: cad. carateres -> booleano
        Esta função recebe um texto e devolve True se o mesmo apenas tiver
        carateres válidos.
        '''        
        if type(texto) != str or texto == '':
            return False        
        for indice, caractere in enumerate(texto):
            if caractere not in 'abcdefghijklmnopqrstuvwxyz \
            ABCDEFGHIJKLMNOPQRSTUVWXYZ' or (caractere == ' ' and \
                                            texto[indice + 1] == caractere):
                return False                          
        return True  
    
    
    if not validar_texto(texto):
        raise ValueError('corrigir_doc: argumento invalido')    
    lista_palavras = texto.split()
    lista_palavras_corrigidas = list()
    for palavra in lista_palavras:
        lista_palavras_corrigidas.append(corrigir_palavra(palavra))        
    # O "break_duplo" permite sair de ambos os ciclos contados
    texto_sem_anagramas = False
    while not texto_sem_anagramas:
        texto_sem_anagramas = True
        break_duplo = False
        for indice_1, palavra in enumerate(lista_palavras_corrigidas):
            for indice_2 in range(indice_1 + 1, len(lista_palavras_corrigidas)):
                if eh_anagrama(palavra, lista_palavras_corrigidas[indice_2]) \
            and palavra.lower() != lista_palavras_corrigidas[indice_2].lower():
                    del lista_palavras_corrigidas[indice_2]
                    texto_sem_anagramas = False
                    break_duplo = True
                    break                
            if break_duplo:
                break
    return " ".join(lista_palavras_corrigidas)


def obter_posicao(direcao, posicao_atual):
    '''
    obter_posicao: cad. carateres X inteiro -> inteiro
    Esta função recebe a direção de um movimento ('C', 'B', 'E' ou 'D') e a
    posição atual (1, 2, 3, 4, 5, 6, 7, 8 ou 9); e devolve a posição após o
    movimento.
    '''    
    if direcao == 'C':        
        if posicao_atual in (1, 2, 3):            
            return posicao_atual        
        return posicao_atual - 3    
    elif direcao == 'B':        
        if posicao_atual in (7, 8, 9):
            return posicao_atual         
        return posicao_atual + 3       
    elif direcao == 'E':        
        if posicao_atual in (1, 4, 7):
            return posicao_atual           
        return posicao_atual - 1        
    elif direcao == 'D':        
        if posicao_atual in (3, 6, 9):
            return posicao_atual        
        return posicao_atual + 1
    

def obter_digito(movimentos, posicao_inicial):
    '''
    obter_digito: cad. carateres X inteiro -> inteiro
    Esta função recebe uma sequência de um ou mais movimentos e a
    posição inicial; e devolve o dígito a marcar após finalizar todos os
    movimentos.
    '''
    digito = posicao_inicial    
    for movimento in movimentos:
        digito = obter_posicao(movimento, digito)        
    return digito


def obter_pin(tuplo):    
    '''
    obter_pin: tuplo -> tuplo
    Esta função recebe um tuplo contendo entre 4 e 10 sequências de movimentos e
    devolve o tuplo de inteiros que contêm o pin codificado de acordo com o
    tuplo de movimentos. Gera um ValueError caso o tuplo de movimentos não seja
    válido. 
    '''
    def validar_tuplo(tuplo):
        '''
        validar_tuplo: tuplo -> booleano
        Esta função recebe um tuplo de movimentos e devolve True se o mesmo
        apenas tiver movimentos válidos.
        '''        
        if type(tuplo) != tuple or len(tuplo) > 10 or len(tuplo) < 4:
            return False
        for sequencia_movimentos in tuplo:
            if type(sequencia_movimentos) != str or sequencia_movimentos == '':
                return False            
            for caractere in sequencia_movimentos:
                if caractere not in 'CBED':
                    return False        
        return True    
    

    if not validar_tuplo(tuplo):
        raise ValueError('obter_pin: argumento invalido')    
    posicao_atual = 5
    pin = ()    
    for sequencia_movimentos in tuplo:
        posicao_atual = obter_digito(sequencia_movimentos, posicao_atual)
        pin += (posicao_atual,)    
    return pin


def eh_entrada(entrada):
    '''
    eh_entrada: universal -> booleano
    Esta função recebe um argumento de qualquer tipo e devolve True se o mesmo
    corresponder a uma entrada da BDB.
    '''    
    if type(entrada) != tuple or len(entrada) != 3:
        return False
    if type(entrada[0]) != str or type(entrada[1]) != str or \
       type(entrada[2]) != tuple or entrada[0] == '' or entrada[1] == '':
        return False
    if entrada[0][0] == '-' or entrada[0][-1] == '-':
        return False    
    for indice, letra in enumerate(entrada[0]):
        if letra not in 'abcdefghijklmnopqrstuvwxyz-':
            return False                
        if letra == '-' and (entrada[0][indice - 1] == '-' or \
                             entrada[0][indice + 1] == '-'):
            return False
    if len(entrada[1]) != 7 or entrada[1][0] != '[' or \
       entrada[1][-1] != ']':
        return False    
    for indice in range(1, 6):
        if entrada[1][indice] not in 'abcdefghijklmnopqrstuvwxyz':
            return False
    if len(entrada[2]) < 2:
        return False    
    for numero in entrada[2]:
        if type(numero) != int or numero <= 0:
            return False     
    return True


def validar_cifra(cifra, sequencia_controlo):    
    '''
    validar_cifra: cad. carateres X cad. carateres -> booleano
    Esta função recebe uma cifra e uma sequência de controlo; e devolve True se
    a sequência de controlo for coerente com a cifra.
    '''    
    dicionario_ocorrencias = dict()
    lista_ocorrencias = list()    
    for letra in cifra:
        if letra != '-':
            dicionario_ocorrencias[letra] = cifra.count(letra)        
    for letra in cifra:
        if letra in dicionario_ocorrencias and [cifra.count(letra), letra] \
                                                 not in lista_ocorrencias:
            lista_ocorrencias += [[cifra.count(letra), letra]]  
    # Ordenar a lista por ordem decrescente de ocorrências
    lista_ocorrencias = sorted(lista_ocorrencias, reverse=True)
    # Aplicação do "Bubble Sort" para ordenar alfabeticamente os elementos da
    # lista com o mesmo número de ocorrências
    ordem_correta = False
    while not ordem_correta:
        ordem_correta = True
        for indice in range(0, len(lista_ocorrencias) - 1):
            if lista_ocorrencias[indice][0] == lista_ocorrencias[indice + 1][0]\
            and lista_ocorrencias[indice][1] > lista_ocorrencias[indice + 1][1]:
                lista_ocorrencias[indice], lista_ocorrencias[indice + 1] \
                = lista_ocorrencias[indice + 1], lista_ocorrencias[indice]
                ordem_correta = False
                break
    sequencia_controlo = sequencia_controlo[1:6]
    sequencia_final = ''
    for indice in range(0, 5):
        sequencia_final += lista_ocorrencias[indice][1]    
    return sequencia_final == sequencia_controlo


def filtrar_bdb(lista):    
    '''
    filtrar_bdb: lista -> lista
    Esta função recebe uma lista contendo uma ou mais entradas da BDB e devolve
    apenas a lista contendo as entradas em que a sequência de controlo não é
    coerente com a cifra correspondente, na mesma ordem da lista original. Gera
    um ValueError caso a lista não seja válida. 
    '''    
    def validar_lista_entradas(lista):
        '''
        validar_lista_entradas: lista -> booleano
        Esta função recebe uma lista de entradas da BDB e devolve True se estas
        forem válidas.
        '''          
        if type(lista) != list or len(lista) == 0:
            return False        
        for entrada in lista:
            if not eh_entrada(entrada):
                return False        
        return True
    

    if not validar_lista_entradas(lista):
        raise ValueError('filtrar_bdb: argumento invalido')    
    cifras_incoerentes = False
    while not cifras_incoerentes:
        cifras_incoerentes = True
        for indice in range(0, len(lista)):
            if validar_cifra(lista[indice][0], lista[indice][1]):
                del lista[indice]
                cifras_incoerentes = False
                break    
    return lista


def obter_num_seguranca(tuplo):    
    '''
    obter_num_seguranca: tuplo -> inteiro
    Esta função recebe um tuplo de números inteiros e devolve o número de
    segurança (menor diferença positiva entre qualquer par de números).
    '''
    #Uma das hipóteses: a menor diferença corresponde aos dois primeiros números
    menor_diferenca = abs(tuplo[0] - tuplo[1])
    for indice_1, numero in enumerate(tuplo):
        for indice_2 in range(indice_1 + 1, len(tuplo)):
            if abs(numero - tuplo[indice_2]) < menor_diferenca:
                menor_diferenca = abs(numero - tuplo[indice_2])                
    return menor_diferenca


def decifrar_texto(cifra, numero_seguranca): 
    '''
    decifrar_texto: cad. carateres X inteiro -> cad. carateres
    Esta função recebe uma cifra e um número de segurança; e devolve o texto
    decifrado.
    '''        
    caracteres = 'abcdefghijklmnopqrstuvwxyz'
    texto = ''    
    for indice, letra in enumerate(cifra):        
        if letra == '-':
            texto += ' '
        else:
            # A posição está entre 0 e 25 (len(caracteres) = 26)
            posicao = caracteres.find(letra)          
            if indice % 2 == 0:
                texto += caracteres[(posicao + numero_seguranca + 1) % 26]
            else:
                texto += caracteres[(posicao + numero_seguranca - 1) % 26]    
    return texto


def decifrar_bdb(lista):    
    '''
    decifrar_bdb: lista -> lista
    Esta função recebe uma lista contendo uma ou mais entradas da BDB e devolve
    uma lista de igual tamanho, contendo o texto das entradas decifradas na
    mesma ordem. Gera um ValueError caso a lista não seja válida.
    '''    
    def validar_lista(lista):
        '''
        validar_lista: lista -> booleano
        Esta função recebe uma lista de entradas da BDB e devolve True se estas
        forem válidas.
        '''        
        if type(lista) != list or len(lista) == 0:
            return False        
        for entrada in lista:
            if not eh_entrada(entrada):
                return False            
        return True    
    

    if not validar_lista(lista):
        raise ValueError('decifrar_bdb: argumento invalido')    
    lista_texto_decifrado = list()
    for entrada in lista:
        lista_texto_decifrado += [decifrar_texto(entrada[0], \
                                            obter_num_seguranca(entrada[2]))]    
    return lista_texto_decifrado


def eh_utilizador(dicionario):  
    '''
    eh_utilizador: universal -> booleano
    Esta função recebe um argumento de qualquer tipo e devolve True se o mesmo
    corresponder a um dicionário contendo a informação de utilizador relevante
    da BDB (nome, senha e regra individual).
    '''     
    if type(dicionario) != dict or len(dicionario) != 3:
        return False    
    for chave in dicionario:
        if chave not in ('name', 'pass', 'rule'):
            return False        
    if type(dicionario['name']) != str or len(dicionario['name']) == 0:
        return False
    if type(dicionario['pass']) != str or len(dicionario['pass']) == 0:
        return False
    if type(dicionario['rule']) != dict or len(dicionario['rule']) != 2:
        return False
    for chave in dicionario['rule']:
        if chave not in ('vals', 'char'):
            return False    
    if type(dicionario['rule']['vals']) != tuple or \
       len(dicionario['rule']['vals']) != 2:
        return False        
    for numero in dicionario['rule']['vals']:
        if type(numero) != int or numero <= 0 or \
           dicionario['rule']['vals'][0] > dicionario['rule']['vals'][1]:
            return False
    if type(dicionario['rule']['char']) != str or \
       len(dicionario['rule']['char']) != 1 or \
       dicionario['rule']['char'] not in 'abcdefghijklmnopqrstuvwxyz':
        return False        
    return True


def eh_senha_valida(senha, regra_individual):
    '''
    eh_senha_valida: cad. carateres X dicionário -> booleano
    Esta função recebe uma senha e um dicionário contendo a regra individual de
    criação da senha; e devolve True se a senha cumprir todas as regras de
    definição (gerais e individual).
    '''
    numero_vogais = 0    
    for caractere in senha:
        if caractere in 'aeiou':
            numero_vogais += 1
    if numero_vogais < 3:
        return False
    caracteres_consecutivos = False
    for indice in range(0, len(senha) - 1):
        if senha[indice] == senha[indice + 1]:
            caracteres_consecutivos = True    
    if not caracteres_consecutivos:
        return False
    if not (regra_individual['vals'][0] <= \
        senha.count(regra_individual['char']) <= regra_individual['vals'][1]):
        return False    
    return True


def filtrar_senhas(lista):
    '''
    filtrar_senhas: lista -> lista
    Esta função recebe uma lista contendo um ou mais dicionários correspondentes
    às entradas da BDB e devolve a lista ordenada alfabeticamente com os nomes
    dos utilizadores com senhas erradas. Gera um ValueError caso a lista não
    seja válida.
    '''    
    def validar_lista(lista):
        '''
        validar_lista: lista -> booleano
        Esta função recebe uma lista de entradas da BDB e devolve True se estas
        forem válidas.
        '''        
        if type(lista) != list or len(lista) == 0:
            return False        
        for dicionario in lista:
            if not eh_utilizador(dicionario):
                return False            
        return True    
    

    if not validar_lista(lista):
        raise ValueError('filtrar_senhas: argumento invalido')    
    utilizadores_senhas_erradas = list()
    for dicionario in lista:
        if not eh_senha_valida(dicionario['pass'], dicionario['rule']):
            utilizadores_senhas_erradas += [dicionario['name']]    
    return sorted(utilizadores_senhas_erradas)  