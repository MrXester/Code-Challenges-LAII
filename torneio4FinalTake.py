'''

Neste torneio pretende-se que implemente um programa que ajude um arquiteto a
planear os prédios a construir num bairro.

Um bairro de dimensão N é uma matriz quadrada com N x N lotes de iguais dimensões.
Em cada lote deve ser construído um prédio. As alturas dos prédios variam entre 
1 e N, sendo que em cada linha e coluna do bairro as alturas dos prédios devem ser
todas diferentes. Alguns lotes podem já ter um prédio previamente construído.

Para além destas retrições, o arquiteto tem que respeitar algumas regras de 
visibilidade: para cada coluna e para cada linha podem ser indicados quantos
prédios devem ser visíveis em cada uma das direcções.

Considere por exemplo o seguinte esquema para um bairro de dimensão N = 4.

    3 . . 1
    v v v v
. > . . . . < .
. > . 4 . . < 2
. > . . . . < .
1 > . . . 3 < .
    ^ ^ ^ ^
    . . 2 .

Dois dos lotes deste bairro já têm prédios constuídos (de alturas 4 e 3). Na primeira
coluna só podem estar visíveis 3 prédios quando olhando de Norte para Sul. Na terceira
coluna só podem estar visíveis 2 prédios quando olhando de Sul para Norte. Na quarta 
coluna só pode estar visível um prédio quando olhando de Norte para Sul. Na segunda
linha só podem estar visíveis 2 prédios quando olhando de Este para Oeste. Finalmente,
na quarta linha só pode estar visível um prédio quando olhando de Oeste para Este.

O programa deve calcular um possível projeto para o bairro, nomeadamente as alturas dos
prédios a construir em cada lote, que respeite todas as restrições dadas. Só serão dados
problemas onde tal é possível. Pode existir mais do que um projeto que satisfaz todas as
restrições, podendo neste caso ser devolvido qualquer um deles.

A função a implementar recebe 5 parâmetros:
- m é uma matriz quadrada (representada por uma lista de listas) que descreve quais os 
  prédios já existentes. Se um lote estiver vazio a lista irá conter um None na posição 
  respectiva.
- t é uma lista com as restrições de visibilidade para as colunas, quando olhando de Norte
  para Sul. Se não existir restrição para uma determinada coluna existirá um None na
  posição respectiva.
- b é uma lista com as restrições de visibilidade para as colunas, quando olhando de Sul
  para Norte. Se não existir restrição para uma determinada coluna existirá um None na
  posição respectiva.
- l é uma lista com as restrições de visibilidade para as linhas, quando olhando de Oeste
  para Este. Se não existir restrição para uma determinada linha existirá um None na
  posição respectiva.
- r é uma lista com as restrições de visibilidade para as linhas, quando olhando de Este
  para Oeste. Se não existir restrição para uma determinada linha existirá um None na
  posição respectiva.

A função deverá devolver uma matriz quadrada (representada por uma lista de listas) com as 
alturas projetadas para todos os lotes.

'''

def projeto(m,t,b,l,r):
	v = (t,b,l,r) #Cria um tuplo com as listas de restrições de visibilidade;
	n = len(m)
	preload(n,m,v) #Posiciona na matriz os prédios de escolha imediata,i.e., os prédios mais altos em linhas ou colunas cuja a restrição de visibilidade seja 1;
	mC = colunas(m,n) #Cria uma matriz equivalente á matriz original, mas que agrupa as posições por colunas ao invés de linhas;
	fill(n,m,mC,v,(0,0)) #Inicia o processo de preenchimento da matriz;
	return m

###########################################################################################################################################

#Processa a matriz inicial posicionando os prédios de tamanho n nas extremidades das colunas e linhas cuja restrição de visibilidade seja 1,
#removendo, a seguir, a restrição, para evitar reverificar a linha ou coluna na direção indicada;
#Por exemplo:
'''
    . . 1 .						. . . .
    v v v v     				v v v v
. > . . . . < .				. > . . 4 . < .
. > . . . . < 1		===>>	. > . . . 4 < .
. > . . . . < .				. > . . . . < .
1 > . . . . < .				. > 4 . . . < .
    ^ ^ ^ ^						^ ^ ^ ^
    1 . . .						. . . .

'''
#Recebe como argumento a ordem da matriz, a própria matriz por referência, e um tuplo com a lista de visibilidades também por referência;
def preload(n,m,v):
	for h in range(0,4):
		listView = v[h]
		
		for x in range(0,n):
			view = listView[x]
			#Percorre a lista das restrições procurando uma cujo valor seja 1;
			if view and view == 1: 
				#Faz as devidas alterações na matriz e ás restrições;
				if h == 0:
					m[0][x] = n

				elif h == 1:
					m[n-1][x] = n

				elif h == 2:
					m[x][0] = n

				elif h == 3:
					m[x][n-1] = n

				listView[x] = None		
	pass

#O(4*n) tendo q percorre 4 listas de n elementos;

###########################################################################################################################################

#Percorre a matriz original criando a lista das colunas; a matriz "transposta", utilizada para verificações de visibilidade a seguir;
#Exemplo:
'''

| 3 1 2 |
| 2 3 1 |  == [[3,1,2],[2,3,1],[1,2,3]] =>> [[3,2,1],[1,3,2],[2,1,3]]
| 1 2 3 |

'''
#Recebe a matriz e sua respectiva ordem;
def colunas(m,n):
	mC = []
	for x in range(0,n):
		mC.append([lines[x] for lines in m])
	return mC

#O(n^2) percorre toda a matriz;
###########################################################################################################################################

#Determina os valores que uma dada posição na matriz pode assumir tendo em conta não repetir valores por linha e coluna, e 
#um pequeno algoritmo de filtragem, para saber se vale a pena posicionar um valor em determinada posição tendo em conta restrições de visibilidade;

#Recebe a matriz, sua transposta e sua ordem, seguidas pela posição a ser analisada e um tuplo com as restrições de visibilidade; 
def extensions(m,mC,n,pos,v):
	(y,x) = pos
	base = set(range(1,n+1)) #Coloca todas as possibilidades em um set e começa a filtrá-las;
	line = set(m[y]) 
	row = set(mC[x]) 
	base = base.difference(line.union(row)) #Possibilidades sem repetições em linha ou coluna;   
	base = [b for b in base if validaPos(n,v[0][x],mC,x,b) and validaPos(n,v[2][y],m,y,b)] #Processo de "filtro" a partir da análise das restrições de visibilidades em linha e coluna
	#Filtra tendo em conta restrições em T e L, sendo feita a validação para B e R posteriormente no código
	return base


###########################################################################################################################################

#Determina a viabilidade de se colocar um dado valor em uma posição na matriz, para isso, o algoritmo se foca em analisar a "lista" em que o elemento está sendo inserido,
'''
Para o exemplo, se queremos analisar a inserção do elemento X na linha 3:
    . . . .						
    v v v v     				
. > . . . . < .		o algoritmo realiza a analise por		
. > . . . . < .					===>>	   					2 [2,1,X,None]
. > . . . . < .				
2 > 2 1 X . < 2				
    ^ ^ ^ ^						
    . . . .

Analogamente para a coluna 3 no exemplo:
    . . . 3						
    v v v v     				
. > . . . 2 < .		o algoritmo realiza a analise por		
. > . . . 1 < .					===>>	   					3 [2,1,X,None]
. > . . . X < .				
. > . . . . < .				
    ^ ^ ^ ^						
    . . . 1


Dado o Input apresentado, (3,[2,1,X,None]), o algoritmo então leva em conta comparações acerca do elemento X com o resto da lista onde está sendo inserido,
inicialmente verifica quantos elementos já são visíveis na linha antes da inserção de X, em seguida:

1- Verifica se o elemento X é maior que os demais elementos da lista, i.e., se é visível na linha de prédios. Se esta condição é satisfeita, verifica:
	2- Incrementa o numero de predios visiveis;
	3- Calcula o número de prédios maiores do que X. (i.e. que poderão vir a serem visíveis posteriormente);
	4- Se o número de prédios visíveis for maior que a restrição o valor é invalidado;
	5- Se o número de prédios visíveis é igual à restrição e X não é o maior dos prédios, o valor é invalidado;
	6- Se o número de prédios visíveis difere da restrição por y, verifica se o número de prédios maiores que X é maior ou igual a y, se não invalida o valor;

'''
#Recebe o tamanho do maior prédio possível, a restrição de visibilidade dos prédios na lista analisada, a matriz de onde vem a linha, o indice da linha na matriz e o valor a ser testado;
def validaPos(n,metaL,m,i,val):
	lista = m[i] #Extrai da matriz a lista de teste; 
	
	if metaL: #Verifica se é necessário fazer validação sobre restrição de visibilidade (i.e. restrição != None);
		maxL = -1
		auxMetaL = metaL
		#Encontra o maior dos prédios na lista e o número de prédios visíveis até então;
		for num in lista:
			if not num:
				break

			if num > maxL:
				maxL = num
				auxMetaL -= 1


		if val > maxL: #Verificação (1);
			auxMetaL -= 1 #Verificação (2);
			nexL = n - val #Verificação (3);
			if (auxMetaL < 0):#Verificação (4);
				return False
			
			if (auxMetaL == 0 and nexL > 0): #Verificação (5);
				return False

			if (nexL < auxMetaL): #Verificação (6);
				return False

	return True

#Ressalta-se que esta validação garante a integridade apenas para os eixos T e L, a verificação para as demais restrições é feita em outra etapa do código;

##########################################################################################################################################

#Realiza a validação de uma linha ou coluna para os eixos de B e R, tomando um input muito semelhante ao apresentado na ultima função;
#Recebe a lista equivalente á linha ou coluna a ser validada, o tamanho da lista e a restrição de visibilidade almejada;
#Nesta função a linha ou coluna ja deve estar completa e só é validada;

def validaLista(n,lista,auxMetaR):
	if auxMetaR: #Verifica se é necessário fazer validação sobre restrição de visibilidade (i.e. restrição != None);
		maxL = -1
		metaL = auxMetaR
		#Encontra o maior dos prédios na lista e o número de prédios visíveis até então;
		for y in range(1,n+1):
			x = lista[n-y]	
			if x > maxL:
				maxL = x
				metaL -= 1

		#Verifica se a contagem de prédios visíveis é compatível com a restrição; 
		if metaL != 0:
			return False
		
	return True

###########################################################################################################################################

#Preenche uma matriz m de ordem n, e sua transposta (mC) a partir da posição passada;
def fill(n,m,mC,v,lstPos):
	(y,x) = lstPos
	val = False

	if(x == n): #Se a posição passada excede o tamanho da linha reinicia-se a partir da linha seguinte;
		y +=1
		x = 0

	if (y < n): #Se a linha passada ja não corresponde a uma linha da matriz, a matriz está preenchida;
		# A partir deste ponto inicia-se o BackTracking, cada avanço é validado através da função validaPos() para eixos L e T, 
		#e assim que uma linha e coluna é preenchida é testada utilizando-se da função validaLista() para os eixos B e R;
		# Se uma validação não funciona o processo volta e avança para a próxima tentativa;
		if not m[y][x]: 
			#Realiza o processo seguinte somente se a posição a preencher não está preeenchida;
			for ext in extensions(m,mC,n,(y,x),v): #Realiza a próxima etapa para todas as opções possiveis para a posição marcada até que se preencha a matriz nos moldes requisitados 
				m[y][x] = ext
				mC[x][y] = ext
				
				aux = True
				if (x == (n-1)): # verificação caso a linha seja preenchida;
					aux = validaLista(n,m[y],v[3][y])

				if aux and (y == (n-1)): # verificação caso a coluna seja preenchida;
					aux = validaLista(n,mC[x],v[1][x])

				if aux:
					(val,r) = fill(n,m,mC,v,(y,x+1))
					if val:
						return (val,r)
				
				m[y][x] = None
				mC[x][y] = None

		elif (x == (n-1)): # verificação caso a linha seja preenchida;
			if validaLista(n,m[y],v[3][y]):
				return fill(n,m,mC,v,(y,x+1))

		elif (y == (n-1)): # verificação caso a coluna seja preenchida;
			if validaLista(n,mC[x],v[1][x]):
				return fill(n,m,mC,v,(y,x+1))

		else:
			return fill(n,m,mC,v,(y,x+1))

	else:
		val = True
			
	return (val,m)


###########################################################################################################################################





'''
Lógica para diminuição do backtracking
x [(------ m = max -------) (t?) -- -- --]

Hmax = n

L = predios visiveis a esquerda

nexL = possiveis predios visiveis na proxima iteração

x = restrição de visibilidade


{
	L = (t > m)? ((L + 1) | (L))
	nexL = (t > m)? (nexL(t) | nextL(m))  

	(t)? = 
	(L > x)? ((False)| _)
	(L == x & nexL != 0)? ((False)| _)
	(L < x & nexL < x - L)? ((False)| True)
}




nextL(p) = Hmax - Hp 

(Hmax - H = predios maiores que o predio H)

'''

