# Robô Entregador de Medicamentos em Hospital

## Descrição do Projeto

Este projeto implementa um agente inteligente baseado em busca para realizar entregas de medicamentos em um hospital representado por uma grade bidimensional.

O robô inicia em uma posição inicial (farmácia) e deve visitar todas as salas que possuem pedidos, minimizando o custo total de movimentação.

A solução utiliza a arquitetura **Ambiente – Agente – Programa de Agente**, conforme o modelo apresentado no livro *Artificial Intelligence: A Modern Approach (Russell & Norvig)* e no repositório **aima-python**.

# 1. Modelagem Formal do Problema

## 1.1 Representação dos Estados

Cada estado é representado por:

state = (posicao_robo, entregas_pendentes)

Onde:

* posicao_robo: tupla (x, y) indicando a posição atual do robô.
* entregas_pendentes: frozenset contendo as posições que ainda precisam de entrega.

Exemplo:

((2, 1), frozenset({(0,3), (4,4)}))

Uso de frozenset é necessário para permitir hashing e comparação eficiente, conforme esperado pelas estruturas do AIMA.

**Mapeamento no código:**
`DeliveryProblem(Problem)`

## 1.2 Estado Inicial

O estado inicial é definido como:

(posicao_inicial, todas_as_entregas)

Exemplo:

((0,0), frozenset({(1,2), (3,4), (4,1)}))

## 1.3 Conjunto de Ações

Ações possíveis em cada estado:

* `UP`
* `DOWN`
* `LEFT`
* `RIGHT`

Cada ação move o robô uma célula dentro dos limites da grade.

Se o robô entrar em uma posição que contém uma entrega pendente, a entrega é realizada automaticamente.

**Mapeamento no código:**
`actions(self, state)`

## 1.4 Modelo de Transição — result(s, a)

A função de transição:

* Calcula a nova posição do robô
* Remove a entrega se houver
* Retorna o novo estado

Formalmente:

result((pos, entregas), ação) =
    (nova_pos, entregas - {nova_pos})  se nova_pos ∈ entregas
    (nova_pos, entregas)              caso contrário

**Mapeamento no código:**
`result(self, state, action)`

## 1.5 Teste de Objetivo — goal_test

O objetivo é alcançado quando não há entregas pendentes.

goal_test(state) = True se len(entregas_pendentes) == 0

**Mapeamento no código:**
`goal_test(self, state)`

## 1.6 Custo de Caminho — path_cost

Cada movimento tem custo unitário:

path_cost(c, s, a, s') = c + 1

**Mapeamento no código:**
path_cost(self, c, state1, action, state2)`

## 1.7 Heurística

Foi utilizada a menor distância de Manhattan entre o robô e uma entrega pendente:

h(n) = min(|x - dx| + |y - dy|)

### Intuição

Estima o menor número de movimentos necessários para alcançar a próxima entrega.

### Propriedades

* **Admissível**: nunca superestima o custo real.
* **Consistente**: a variação entre estados vizinhos é no máximo o custo da ação.

**Mapeamento no código:**
`h(self, node)`

# 2. Classificação do Ambiente

Segundo os critérios do AIMA:

* **Determinístico**: ações sempre produzem o mesmo resultado.
* **Totalmente observável**: o agente conhece sua posição e todas as entregas restantes.
* **Estático**: o ambiente não muda enquanto o agente decide.
* **Discreto**: estados, ações e tempo são discretos.
* **Agente único**: apenas um agente atua no ambiente.

# 3. Arquitetura do Sistema

## Ambiente

Classe: `HospitalEnvironment`

Responsável por:

* Manter o estado do mundo
* Executar ações
* Fornecer percepções
* Exibir o estado via `render()`

## Agente

Classe: `DeliveryAgent`

Representa o robô inserido no ambiente.

## Programa de Agente

Classe: `DeliveryAgentProgram`

Funcionamento:

1. Recebe a percepção do ambiente
2. Formula um problema (`DeliveryProblem`)
3. Executa o algoritmo A*
4. Obtém um plano (sequência de ações)
5. Executa uma ação por passo

A busca é executada **dentro do programa do agente**, conforme o modelo **SimpleProblemSolvingAgentProgram** do AIMA.

# 4. Algoritmos de Busca

## Utilizado

* **A*** (A-Star)

### Justificativa

O problema possui múltiplas entregas, aumentando o espaço de estados. O A* utiliza heurística para guiar a busca calculando a distância até o próximo e até o fim das entregas, reduzindo significativamente o número de estados explorados mantendo a solução ótima.

## Utilizados na fase de teste

* **BFS**: não utiliza heurística,explora muitos estados.
* **DFS**: pode encontrar soluções não ótimas.
* **Uniform Cost Search**: garante otimalidade, mas é menos eficiente que A* sem heurística.

# 5. Testes

Foram implementados testes automatizados com **pytest**, verificando:

* Funcionamento do `goal_test`
* Atualização correta de estados em `result`
* Validade da heurística
* Capacidade do A* encontrar solução
* Funcionamento básico do agente

## 6. Estrutura do Projeto

```
projectGrupo6/
│
├── env/
│   └── hospital_environment.py
│
├── agents/
│   └── delivery_agent.py
│
├── problems/
│   └── delivery_problem.py
│
├── tests/
│   ├── test_agent.py
│   └── test_problem.py
│
├── main.py
└── README.md
```

# 7. Como Executar o Sistema

## Pré-requisitos

- Python 3.9 ou superior
- pip instalado


## 1 Instalar dependências

O projeto utiliza o repositório oficial do AIMA (`aima3`).

Execute no terminal:

```bash
pip install aima3
```


## 2 Executar o sistema

No diretório raiz do projeto (onde está o arquivo `main.py`), execute:

```bash
python main.py
```


## 3 O que acontecerá na execução

- O ambiente hospitalar será inicializado (grade 10x10).
- O agente inteligente será inserido no ambiente.
- O algoritmo A* será utilizado para planejar as entregas.
- A simulação será exibida passo a passo no terminal.
- O ambiente será renderizado a cada iteração, mostrando:
  - `R` → Robô
  - `D` → Entregas
  - `=` → Paredes
  - `.` → Espaço livre

A execução termina automaticamente quando todas as entregas forem concluídas ou quando o número máximo de passos for atingido.
