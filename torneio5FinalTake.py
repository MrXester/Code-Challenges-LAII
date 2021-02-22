'''

Neste torneio pretende-se que implemente uma função para validar o mapa
de um arquipélago.

O mapa (rectangular e quadriculado) é constituído por um conjunto de ilhas 
e por mar, sendo representado por uma lista de strings onde o caracter '.' 
representa uma quadrícula de terra (parte de uma ilha) e o caracter '#' 
uma quadrícula de mar. Uma ilha é um conjunto de quadrículas de terra 
acessíveis entre si. É possível aceder de uma quadrícula a outra se forem 
vizinhas na horizontal ou na vertical. As ilhas podem também ter quadrículas 
com um digito, digito esse que representa uma quadrícula de terra mas também a 
dimensão da ilha (em quadrículas).

Uma ilha está bem representada no mapa se contem exactamente um digito com a
sua dimensão correcta. Um mapa está correcto se todas as ilhas estão bem
representadas e se apenas existe um mar (todas as quadrículas de mar são
acessíveis entre si).

A função deve devolver um tuplo com a seguinte informação (por esta ordem):
- Número de ilhas bem representadas
- Número de ilhas mal representadas
- Um booleano que indica se existe apenas um mar.
- O número mínimo de caracteres que seria preciso alterar para que o mapa
  estivesse correcto.

Note que se não existirem ilhas mal representadas e existir apenas um mar este
último número deverá ser 0. Nos testes a realizar este número, quando não 0,
será tipicamente bastante pequeno.

'''

def mapa(m):
	if m and m[0]: #Difere o resultado para um mapa vazio ou não vazio
		return analise(m) #Retorna o valor relativo à análise de um mapa não vazio
	return (0,0,True,0) #caso "default"

#######################################

#Realiza a análise de um mapa m, não vazio
def analise(m):
	ext = (len(m),len(m[0])) #Calcula as extremidades do mapa para cálculos futuros  
	r = grafos(m,ext) #Calcula um tuplo com as informações: (número de ilhas válidas, número de ilhas invalidas, booleana indicando se o mar é único, booleana se o mapa é válido)
	if r[3]: #Se o mapa for válido não calcula qualquer alteração
		return (r[0],r[1],r[2],0) 

	for x in range(ext[0]):
		m[x] = list(m[x]) #Transforma m em uma lista de listas de caracteres  
	
	return (r[0],r[1],r[2],editsMap(m,ext)) #retorna o valor esperado de checagem e o número de alterações para corrigir o mapa

#######################################

#Retorna True sse o mapa é válido
def validaMapa(m,ext):
	return grafos(m,ext)[3]

#Retorna True sse a ilha está bem definida, i.e. apresenta somente um dígito que represeta seu tamanho correto
def validaIlha(size,digs):
	if(len(digs) > 1) or size not in digs.values():
		return False
	return True


#######################################

#Dado um mapa (mapF) e suas extremidades(ext um par com (numero de linhas,numero de colunas)) Calculaum tuplo0 com:
#(número de ilhas válidas, número de ilhas invalidas, booleana indicando se o mar é único, booleana se o mapa é válido
def grafos(mapF,ext):
	vis = set() #Posições já visitadas pelo algoritmo
	sea = 0 #Número de mares representados pelo mapa 
	numValLand = 0 #Número de ilhas válidas
	numInvalLand = 0 #Número de ilhas inválidas

	for x in range(ext[0]):
		for y in range(ext[1]): #Percorre todas as posições do mapa pelo menos 1 vez
			
			if (x,y) not in vis:  #Verifica se a posição já não foi calculada e utilizada no contexto de outra ilha ou mar 
				ref = mapF[x][y] 
				(p,n) = grafoPos(mapF,(x,y),vis,ref,ext) #Calcula as informações a cerca de um grafo(ilha ou mar) apresentado por uma posição, tomando em conta o char que a representa
				
				if ref == "#":
					sea += 1 #Incrementa o número de mares se a posição representar um mar e n tiver sido utilizada em outro contexto

				else:
					if validaIlha(p,n): #Realiza a validação de uma ilha pelas informações passadas por seu grafo incrementando a seguir a devida variavel consoante sua validação
						numValLand += 1

					else:
						numInvalLand += 1

	seaBool = (sea <= 1)
	valid = ((numInvalLand == 0) and seaBool)

	return (numValLand,numInvalLand,seaBool,valid)

#######################################

#Dada uma posição, um mapa, uma referência relativa ao char que ocupa tal posição e as extremidades do mapa calcula a partir de um grafo:
# O tamanho da ilha ou mar referenciado e os digitos que podem representar seu tamanho em uma lista
def grafoPos(mapF,pos,vis,ref,ext): ####vis é opcional, demarca as posições utilizadas no grafo atual, impedindo a geração de grafos repetidos, em determinados contextos
	auxVis = vis.copy() #referência de visitados interna da função
	size = 0 #tamanho do grafo gerado pela posição
	digs = {} #posição dos digitos no grafo gerada pela posição
	
	queue = [pos] #Inicia uma queue c a posição desejada 
	neighbours = [(0,1),(1,0),(-1,0),(0,-1)]
	
	while queue: #Enquanto houverem elementos na queue continua a "construção" do grafo
		use = False
		(x,y) = queue.pop(0)

		if (x,y) not in auxVis: #só procede à construção se a posição não tiver sido visitada anteriormente
			auxVis.add((x,y))

			if ref == mapF[x][y] or ref != "#" and mapF[x][y] != "#": #verificações a cera de chars para a formação do grafo
				if mapF[x][y].isdigit():
					digs[(x,y)] = int(mapF[x][y])
				size += 1
				use = True

			if use: # Se a posição foi utilizada procede à acrescentar elementos na queue e adicionar a posição ao set de posições que pertencem a um grafo
				vis.add((x,y))
				for (u,v) in neighbours:
					u += x
					v += y
					if (u,v) not in auxVis:
						if u in range(ext[0]) and v in range(ext[1]):
								queue.append((u,v))

	return (size,digs)


#######################################

#Dado um mapa e suas extremidades calcula o número mínimo de alterações para tornar o mapa válido
def editsMap(m,ext):
	depth = 0 #Número de alterações necessárias para tornar o mapa válido em cada iteração
	found = False #Indicação se um mapa válido foi encontrado
	while not found:
		depth += 1 #incrementa o número de alterações para executar a correção
		found = depthSearch(m,ext,depth,(0,0)) #Testa se com dado número de alterações é possivel validar um mapa
		
	return depth

#######################################

#Dado um mapa, suas extremidades, uma posição inicial, e um número máximo de alterações tenta tornar um mapa válido
def depthSearch(m,ext,maxDepth,pos):
	if maxDepth == 0: #se não há mais alterações a serem feitas retorna se o mapa é ou não válido
		return validaMapa(m,ext)

	(x,y) = pos #verifica se a posição inicial para se realizar o processo é válida ou precisa ser processada
	if y >= ext[1]:
		y = 0;
		x +=1
		if x >= ext[0] :
			return False
	
	# realiza o processo de decisões a cerca de alterações
	original = m[x][y]
	for t in extensions(m,(x,y),original,ext):
		m[x][y] = t
		if depthSearch(m,ext,maxDepth-1,(x,y+1)): #faz a busca para cada alteração subtraindo uma alteração para a procura seguinte
			return True
		m[x][y] = original

	r = depthSearch(m,ext,maxDepth,(x,y+1)) #faz a busca a partir de uma nova posição inicial para realizar alterações
	return r

#######################################

#Retorna a lista de possíveis carateres a serem inseridos na posição a ser alterada
#Para reduzir o custo da realização de testes a função leva em conta se a posição pode ser alterada para um char e, se puder escolhe somente o que representa o tamanho da ilha a qual a posição faz parte
#A lista resultante possui sempre length <= 3
def extensions(m,pos,original,ext):
	r = [".","#"]
	
	#Calcula as possibilidades de dígitos a partir do tamanho da ilha que seria gerada c a posição indicada
	m[pos[0]][pos[1]] = "."
	(p,n) = grafoPos(m,pos,set(),".",ext)
	m[pos[0]][pos[1]] = original
	
	if ((len(n) == 0) or ((len(n) == 1) and original.isdigit())):
		if(p in range(1,10)):
			r.append(str(p))

	#Remove o valor inicial da lista de possibilidades
	if not original.isdigit():
		r.remove(original)

	return r







