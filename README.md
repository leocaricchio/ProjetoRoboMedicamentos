**1-Modelagem Formal do Problema**

Projeto: Robô Entregador de Medicamentos em Hospital

**Descrição Geral**

Um robô autônomo deve entregar medicamentos a diferentes quartos em um hospital representado como uma grade bidimensional.
O robô inicia na farmácia e deve visitar todas as posições que possuem pedidos, minimizando o custo total de movimentação.

**1.1-Representação dos Estados**

Cada estado é representado por:

**state = (posicao_robo, entregas_pendentes)**

Onde:

posicao_robo = tupla (x, y) indicando a posição atual do robô na grade

entregas_pendentes = conjunto imutável (frozenset) contendo as posições que ainda precisam de entrega

Exemplo:
((2, 1), frozenset({(0,3), (4,4)}))

Significa:

Robô na posição (2,1)

Entregas restantes em (0,3) e (4,4)

*o conjunto precisa ser frozenset devido às especificações do AIMA

Mapeamento para o código:

**HospitalDeliveryProblem(Problem)**

**1.2-Estado Inicial**

O estado inicial é definido como:

**(posicao_inicial, todas_as_entregas)**

Onde:

posicao_inicial = posição da farmácia (ex: (0,0))

todas_as_entregas = frozenset com todas as posições de entrega

Exemplo:
((0,0), frozenset({(1,2), (3,4), (4,1)}))

**3. Conjunto de Ações**

Em cada estado, o agente pode executar quatro ações de movimento:
UP
DOWN
LEFT
RIGHT

Cada ação move o robô uma célula na grade, respeitando os limites do ambiente e buscando a melhor rota para zerar as entregas pendentes.

*Se o robô entrar em uma posição que pertence a entregas_pendentes, a entrega é realizada automaticamente.

Mapeamento no código:

**actions(self, state)**

**1.4-Modelo de Transição —result(s, a)**

A função de transição:

Calcula a nova posição do robô com base na ação

Verifica se a nova posição contém uma entrega pendente(Se sim, remove essa posição do conjunto de entregas)

Retorna o novo estado

**result((pos, entregas), ação) =
    (nova_pos, entregas - {nova_pos})  se nova_pos ∈ entregas
    (nova_pos, entregas)              caso contrário**

Mapeamento no código :

**result(self, state, action)**

**1.5-Teste de Objetivo — goal_test**

O objetivo é alcançado quando:

entregas_pendentes está vazio

**goal_test(state) = True  se len(entregas_pendentes) == 0**

Mapeamento no código:

**goal_test(self, state)**

**6. Custo de Caminho — path_cost**

Cada movimento tem custo unitário:

custo = 1 por ação

**path_cost(c, s, a, s') = c + 1**

Mapeamento no código:

**path_cost(self, c, state1, action, state2)**

**7. Heurística**

Utilizamos a distância de Manhattan para definir qual a melhor rota possível

Inicialmente,é feita uma soma da distância do robô até cada entrega pendente e depois soma o custo total.

**Distância Manhattan:**

**∣x1−x2∣+∣y1−y2∣**

*(x1,y1) representam o estado atual

Propriedades:

Admissível: não superestima o custo real.

Consistente: baseada na distância Manhattan com custo de movimento unitário

Mapeamento no código:

**h(self, node)**


