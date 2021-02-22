'''

Neste torneio pretende-se que implemente uma função que processa uma mensagem.

A mensagem é constituída por vários blocos de letras separados por ';'.

Cada bloco é recebido num formato comprimido: um número seguido de uma 
sequência entre parêntesis significa que essa sequência é repetida o número
de vezes indicado.

A função deve começar por descomprimir os blocos e filtrar os blocos vazios.

Depois deve filtrar os blocos que concordam com um padrão que também é parâmetro
da função processa. Um bloco concorda com um padrão se for possível obtê-lo a partir
do padrão substituindo cada caracter '?' por uma letra e cada caracter '*' por um
número arbitrário de letras. Por exemplo, 'aabxaxb' concorda com o padrão 'a*?b',
enquanto que 'ab' já não.

Depois de filtrar a função deve introduzir redundância na mensagem, repetindo 
alguns blocos. Deve escolher os blocos a repetir por forma a maximizar o 
número total de caracteres da mensagem, mas garantindo que nunca repete dois
blocos consecutivos.

Finalmente a função deve voltar a comprimir os blocos resultantes, com o cuidado
de comprimir o máximo possível.

'''

def processa(mensagem,padrao): 
	mensagem = mensagem.replace(" ","") #limpa os espaços da mensagem
	blocos = [descomprime(list(x),")") for x in mensagem.split(';') if x] #Cria a lista dos blocos de palavras ja descomprimidos e não vazios
	preCompress = {} #dicionário utilizado na pre-compressão do código
	aux = [(comprime2(x,preCompress),len(x)) for x in blocos if filtraPalavra(x,padrao)] #cria uma lista com palavras já filtradas, em pares (palavra comprimida, tamanho total da palavra)
	aux = redundancia(aux) #aplica a redundancia na lista de palavras
	r = ";".join(aux) #reune a lista de palavras novamente com ";"
	return r

########################################################################################

def descomprime(palavra,final):
#Descomprime uma palavra, toma a palavra no argumento, e um char final a ser buscado pela função (opcional)
#Tempo linear, n = tamanho da palavra, O(n) 
	r = ""
	acc = ""
	#acumula no resultado char a char percorrendo a palavra
	while palavra:
		#o pop e a passagem da palavra por referencia garante que cada char é lido uma única vez
		i = palavra.pop(0)
		#se encontrar o char final especificado a função para a execução
		if i == final:
			break
		#se o próximo char for numérico, é acumulado em um acumulador e não no resultado
		elif i.isnumeric():
			acc += i
		#se o char encontrado é o inicio de uma sequencia comprimida, a descomprime e multiplica pelo acumulador até então feito
		elif i == "(":
			r += int(acc) * descomprime(palavra,")")
			acc = ""
		#se o char for "comum" é acumulado no resultado e o acumulador numérico é esvaziado (tratava-se de um numero perdido na string)
		else:
			acc = ""
			r += i
	return r





##############################################################################



def filtraPalavra(palavra,padrao):
#Retorna um boolean indicando se a palavra está ou não de acordo com o padrão
#A função consiste em procurar na palavra todos os padrões que estejam entre * e garantir que comece e termine com o inicio e fim do padrão
#não confirmado, a função gira em torno da complexidade O(n*(n+m))
	r = False
	final = []
	#verifica se o padrão não é vazio
	if padrao:
		#determina os padrões entre "*", i.e., padrões que precisam simplesmente aparecer na string em qualquer posição
		padroes = padrao.split("*")
		aux = list(palavra)
		#determina o inicio obrigatorio da palavra
		inicio = list(padroes.pop(0))
		
		if padroes:
			#determina o final obrigatório da palavra, se existir
			final = list(padroes.pop())
		
		#verifica se a palavra inicia-se com o início obrigatório
		if verificaPadrao(aux,inicio):
			aux = aux[len(inicio):]
			r = True
			#busca por todos os padrões na palavra
			while padroes:
				(aux,m) = procuraPadrao(aux,list(padroes.pop(0)))
				r = (r and m) #se um padrão não é encontrado o resultado é Falso
			if r and final:
				#verifica se a palavra termina com o final obrigatório
				r = verificaPadrao(aux[-(len(final)):],final)
	return r




def verificaPadrao(palavra,padrao):
#Verifica se a palavra possui o inicio igual a um dado padrão
	auxPad = padrao.copy()
	auxPal = palavra.copy()
	r = True
	#Só verifica enquanto o padrão e a palavra não são vazios
	while auxPad and auxPal:
		p = auxPad.pop(0)
		i = auxPal.pop(0)
		if p != "?" and p != i:
			r = False

	if not auxPad and r:
		return True

	return False


def procuraPadrao(palavra,padrao):
#Complexidade normalmente é o tamanho do padrão * tamanho da palavra
#Procura o padrão na string e retorna a string sem o trecho onde o padrão não foi encontrado 
	r = verificaPadrao(palavra,padrao)
	while not r and palavra:
		palavra.pop(0)
		r = verificaPadrao(palavra,padrao)

	return (palavra[len(padrao):],r)


###########################################################################


def particiona2(palavra):
#Cria um dicionário com todas as partições da palavra em um dicionário
#O dicionário é constituido por: [tamanho da partição]: lista de partição possíveis com esse tamanho
	lgth = len(palavra)
	r = {}
	for x in range(1,lgth+1):
		r[x] = [palavra[y:y+x] for y in range(0,lgth) if(len(palavra[y:y+x]) == x)]
	return r





def blocosPossiveis(palavra):
#Verifica todas as repetições de partições que apareçam na palavra
	dic = particiona2(palavra)
	possBlocks = []
	#Para cada elemento no dicionário é verificado se o mesmo elemento encontra-se repetido na posição seguinte
	for charLen in dic:
		lgth = len(dic[charLen])
		#A posição na lista é equivalente ao ponto onde o padrão se iniciou
		for pos in range(lgth):
			indx = pos + charLen
			numberOfMatchs = 1
			while (indx < lgth) and dic[charLen][indx] == dic[charLen][pos]:
				indx += charLen
				numberOfMatchs +=1
			#Verifica se "vale a pena" comprimir os blocos encontrados
			if (numberOfMatchs > 1) and ((charLen*numberOfMatchs) > len(str(numberOfMatchs)) + 2 + charLen):
				possBlocks.append((dic[charLen][pos],numberOfMatchs,pos))
	return possBlocks


def comprime2(palavra,dic):
#Busca todos os blocos possíveis de repetições e cria sua devida possibilidade de compressão
#usa um dicionário de compressões para poupar execuções
	if palavra not in dic: 
		r = palavra

		for (bloco,qnt,pos) in blocosPossiveis(palavra):
			aux = comprime2(palavra[:pos],dic) + str(qnt) +"(" + comprime2(bloco,dic) + ")" + comprime2(palavra[(qnt*len(bloco)+pos):],dic)
			#acumula sempre a melhor compressão até o momento
			r = min(r,aux,key = lambda t: len(t))
		dic[palavra] = r	
	return dic[palavra]

###########################################################################

def redundancia(listaPalavras):   #tempo linear, 4*tamanho da lista de palavras
#Cria a lista com os indices da lista de palavras que devem ser duplicados para maximizar a length  
	l = len(listaPalavras)
	dicValues = {} 
	dicSets = {}
	maiorResult = (0,0)
	#Acumula em dois dicionários a melhor lista de duplicados e o tamanho obtido para cada índice da lista de palavras
	for x in range(1,l+1):
		lenT = 0
		posA = (l-x)
		copiaSeguinte = l
		
		for i in dicValues:
			if (i-posA) > 1:
				(lenT,copiaSeguinte) = max((dicValues[i],i) , (lenT,copiaSeguinte), key = lambda t: t[0])

				
		lenT += listaPalavras[posA][1]
		setCpy = (dicSets.get(copiaSeguinte,set())).copy()
		setCpy.add(posA)
		dicValues[posA] = lenT
		dicSets[posA] = setCpy
		
		maiorResult = max(maiorResult,(lenT,posA), key = lambda t: t[0])

		if (posA + 4) in dicValues:      
			del dicValues[posA + 4]
			del dicSets[posA + 4]

	setCpy = dicSets.get(maiorResult[1], set())
	#duplica as palavras consoante a lista de indices a serem duplicados
	r = duplicaPalavras(listaPalavras,setCpy)
	return r



def duplicaPalavras(listaPalavras,listaCpy):
	print(listaCpy)
	r= []
	i = 0
	for (x,_) in listaPalavras:
		r.append(x)
		if i in listaCpy:
			r.append(x)
		i += 1
	return r
