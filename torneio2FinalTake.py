'''

Neste problema pretende-se calcular a rota que um carteiro deve fazer para
entregar encomendas num bairro.

O carteiro quer tentar aliviar peso o mais depressa possível, pelo que tenta
sempre ir primeiro (pelo caminho mais rápido) ao maior prédio do bairro,
continuando depois as entregas pela ordem de tamanhos. 

O mapa do bairro é dado por uma lista de blocos rectangulares 2D, dados pelas
coordenadas do canto inferior esquerdo e superior direito, sendo que quaisquer
dois ou mais blocos que se toquem (ou intersectem) pertencem ao mesmo prédio.
Se existirem dois prédios com o mesmo tamanho, o carteiro visita primeiro o que 
começou a ser definido primeiro no mapa.

O carteiro pode deixar as encomendas de um prédio em qualquer posição que lhe
seja adjacente. Se houver duas posições de um prédio à mesma distância mais
curta, o carteiro dá  prioridade à que estiver mais à esquerda, e, em caso
de empate neste critério, então escolhe a que estiver mais para baixo.

Se um prédio não for acessível então é ignorado, passando o carteiro ao
próximo.

A função a implementar recebe o ponto onde o carteiro começa a visita e o mapa
do bairro. Deve devolver a sequência de pontos onde terá que deixar as encomendas,
intercalada pela respectiva distância.

'''


def rota(inicio,blocos):
	ext = (0,0,0,0)
	edificios = {} #[etiqueta do edificio] = (tamanho, set de pontos de entrega); 
	usados = set() #set de pontos usados pelos edificios;
	(ext,edificios) = defineEdificios(inicio,blocos,usados) #define o dicionário dos edificios e as extremidades do mapa;
	r = caminhosGrafo(inicio,edificios,usados,ext) #define os caminhos para o resultado;

	return r



#Função que define as extremidades do mapa entre as extremidades atuais e um novo retângulo adicionado; 
#Recebe uma lista com 4 componentes equivalente a um tuplo de retangulo 2D (canto inferior esquerdo,canto superior direito);
#Recebe um tuplo de retangulo 2D (canto inferior esquerdo,canto superior direito);
#--optamos usar uma lista para realizar o "set" das componentes por referência;

def defineExt(ext,tupl):
	(x,y,u,v) = tupl
	ext[0] = min(x-1,ext[0])
	ext[1] = min(y-1,ext[1])
	ext[2] = max(u+1,ext[2])
	ext[3] = max(v+1,ext[3])
	pass



#Função que demarca os edifícios e seus pontos de entrega, através da criação de um grafo não ligado, aproveita-se do tempo de execução para determinar as extremidades do mapa; 
#Recebe o ponto inicial do carteiro como referencia para extremidades do mapa;
#Recebe a lista de blocos do mapa;
#Recebe a referência de um set de pontos usados pelos edificios (inicialmente estará vazio), sendo preenchido durante a execução;
#***O dicionário resultante, apresenta os edifícios com etiquetas ordenadas por ordem de aparição na lista de blocos, i.e., o edificio 1 começou a ser definido antes do edifício 2;

def defineEdificios(inicio,blocos,usados):
	
	#Inicialização de variáveis;
	r = {}
	i = 0
	todos = []
	queue = []
	vecs = [(0,1),(0,-1),(1,0),(-1,0)]
	(x,y) = inicio
	ext = [x,y,x,y]

	#Define todos os pontos que pertençam a edifícios, i.e., todos os pontos que pertençam ao grafo;
	#Como percorre toda a lista de blocos, calcula as extremidades;
	for (x,y,u,v) in blocos:
		defineExt(ext,(x,y,u,v))
		for p in range(x,u+1):
			for q in range(y,v+1):
				if (p,q) not in todos:
					todos.append((p,q))

	#Define as componentes ligadas do grafo;
	while todos:
		(x,y) = todos[0]
		auxSet = set()
		auxSum = 0 
		queue = [(x,y)]
		
		while queue:
			(x,y) = queue.pop()
			if (x,y) not in usados:
				usados.add((x,y))
				todos.remove((x,y))
				auxSum += 1
				
				for (u,v) in vecs:
					if (x+u,y+v) in todos:
						queue.append((x+u,y+v))

					#Se o ponto adjacente não faz parte de um edifício, é adicionado como um ponto de entrega do edificio atual;
					elif (x+u,y+v) not in usados:
						
						auxSet.add((x+u,y+v))

		r[i] = (auxSum,auxSet)
		i += 1
		 
	return (ext,r)



#Define o caminho mais curto entre uma posição e um conjunto de posições, o caminho mais curto até o ponto mais próximo pertencente ao conjunto;
#Recebe o tuplo com os extremos do mapa retangular (canto inferior esquerdo,canto superior direito);
#Recebe o conjunto de pontos que pertençam a um edifício;
#Recebe a posição inicial;
#Recebe um conjunto de posições finais;
#Utiliza-se de uma "adaptação" da técnica de breadth first;

def caminho(ext,usados,posI,posF):
	queue = []
	if posI not in usados and posI not in posF:
		queue = [(posI,0)]

	vecs = [(-1,0),(0,-1),(0,1),(1,0)]
	visitados = {(posI,0)}
	
	while queue:
		queue.sort(key = lambda t : (t[1],t[0]))
		(x,y),soma = queue.pop(0)
		o = range(ext[0],ext[2]+1)
		l = range(ext[1],ext[3]+1)

		for (u,v) in vecs:
			u += x
			v += y
			
			if (u,v) not in usados and (u,v) not in visitados:
				visitados.add((u,v))
				if u in o and v in l:
						if (u,v) in posF:
							return ((u,v),(soma+1))

						queue.append(((u,v),soma+1))

	#Se o caminho não é encontrado, retorna uma posição qualquer e uma distância negativa
	return ((0,0),-1)



#Define todos os caminhos mais curtos necessários para realizar todas as entregas;
#Recebe o ponto inicial;
#Recebe o dicionário de edifícios([etiqueta do edificio] = (tamanho, set de pontos de entrega));
#Recebe o set de pontos pertencentes a edifícios;
#Recebe o tuplo com os extremos do mapa retangular (canto inferior esquerdo,canto superior direito);

def caminhosGrafo(inicio,edificios,usados,ext):
	#Inicia por criar a rota do carteiro, i.e. definir a ordem pela qual visita os edifícios;
	r = [inicio]
	rota = list(edificios.keys())
	rota.sort(key = lambda t: (-edificios[t][0],t)) #A key é um fator de ordenação por "***" apresentado na função defineEdificios; 
	pos = inicio

	#Para cada edifício, invoca a função caminho para descobriar a distância até o opnto adjacente mais próximo;
	for x in rota:
		(nex,custo) = caminho(ext,usados,pos,edificios[x][1])
		if custo >= 0:
			pos = nex
			r.append(custo)
			r.append(nex)

	return r