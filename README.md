# O paradoxo do dinheiro infinito

Simulação de Monte Carlo do **paradoxo de São Petersburgo**: um jogo de cara ou coroa cujo
valor esperado é **infinito** — e que, ainda assim, ninguém pagaria R$ 50 para jogar.
Este repositório contém o simulador, os resultados brutos de **500 milhões de jogadas**
e um dashboard interativo que visualiza tudo.

## O jogo

1. Uma moeda honesta é lançada até sair **coroa**.
2. O prêmio começa em **R$ 1** e **dobra a cada cara** consecutiva.
3. Uma jogada encerrada na rodada *k* paga **R$ 2^(k−1)**, com probabilidade **1/2^k**.

O valor esperado do prêmio é a soma de infinitas parcelas iguais a ½:

```
E = ½·1 + ¼·2 + ⅛·4 + 1/16·8 + …  =  ½ + ½ + ½ + …  →  ∞
```

Se o valor esperado é infinito, qualquer preço de entrada deveria valer a pena.
O paradoxo (Nicolas Bernoulli, 1713; Daniel Bernoulli, 1738) é que ninguém aceita
pagar mais que alguns poucos reais — e a simulação mostra por quê: **quase todo o
valor esperado mora em prêmios que quase nunca acontecem**.

## Metodologia

### O simulador

Dois scripts em Python puro (sem dependências externas), ambos com o mesmo núcleo
(`simular_jogada()`): sorteia `random.random() <= 0.5` até sair coroa, dobrando o prêmio
a cada cara. "Rodadas" = número de caras + 1.

- [`inifit_simulation.py`](inifit_simulation.py) — versão mínima de demonstração
  (300 jogadas, saída apenas no console).
- [`stop_on_win.py`](stop_on_win.py) — a análise completa. Para `N` jogadas, registra:
  - **Agregados**: prêmio médio, maior/menor prêmio, média de rodadas, total de caras e coroas;
  - **Distribuição de rodadas**: quantas jogadas terminaram em cada rodada *k*;
  - **Resultado por preço de entrada**: para cada preço de R$ 5 a R$ 50 (passo 5),
    o saldo acumulado ao final (`prêmio total − preço × N`);
  - **Pontos de saída com lucro**: cada momento em que o saldo acumulado de um preço
    de entrada **cruzou de negativo para positivo** — a jogada, as rodadas da jogada
    que virou o saldo e o lucro naquele instante (até 50 pontos listados por preço).

  O resultado é impresso e salvo em `resultados/simulacao_<N>_jogadas-<timestamp>.txt`.

### Escala e agregação

A análise principal soma **5 execuções independentes de 100 milhões de jogadas**
(500 milhões no total), feitas em 5 de julho de 2026. Os agregados combinados são
recomputados de forma exata a partir das distribuições de rodadas de cada arquivo
(prêmio total = Σ contagem × 2^(k−1)), e cruzados contra os saldos por preço de
entrada de cada arquivo (a identidade `saldo = prêmio total − preço × N` confere
em todas as execuções).

### Auditabilidade

Princípio do projeto: **todo número do dashboard é conferível abrindo os arquivos
de `resultados/`**. A tabela de execuções do dashboard lista o nome de cada arquivo;
a distribuição, os saldos por preço e os 169 pontos de saída com lucro vêm literalmente
das seções correspondentes dos 5 arquivos de 100 milhões (verificado: cada contador
"ficou positivo Nx" bate com os pontos listados — nada foi truncado pelo limite de 50).

## Como rodar localmente

Requisitos: **Python 3.8+** (somente biblioteca padrão) e um navegador.

```bash
# demonstração rápida (300 jogadas, só console)
python3 inifit_simulation.py

# análise completa — o argumento é o número de jogadas (padrão: 500)
python3 stop_on_win.py 100000
python3 stop_on_win.py 100000000   # ~minutos, dependendo da máquina
```

Cada execução de `stop_on_win.py` grava um novo arquivo em [`resultados/`](resultados/).

**Dashboard**: abra [`main.html`](main.html)
diretamente no navegador (duplo clique). É um arquivo autocontido — os dados das
5 execuções de 100 milhões estão embutidos nele — com modo claro/escuro, tooltips
em todos os gráficos e um botão "Ver tabela" em cada card com os dados completos.

## Resultados obtidos (500 milhões de jogadas)

### Os números centrais

| Métrica | Valor |
|---|---|
| Jogadas simuladas | 500.000.000 (5 × 100 mi) |
| Prêmio médio observado | **R$ 14,89** (teórico: ∞) |
| Maior prêmio | **R$ 536.870.912** (30 rodadas — 29 caras seguidas, 1 vez em 500 mi) |
| Jogadas que pagam até R$ 4 | 87,5% (encerradas em até 3 rodadas) |
| Média de rodadas por jogada | 2,00 (teórico: E = 2) |

A distribuição observada segue a teórica (n/2^k) com precisão por 30 rodadas —
oito ordens de grandeza de decaimento geométrico.

### A média não converge

Cada execução de 100 milhões de jogadas termina com uma média diferente — e quem
manda é o maior prêmio que cada uma teve a sorte de ver:

| Execução (arquivo `…20260705_HHMMSS.txt`) | Prêmio médio | Maior prêmio | Rodada máx. |
|---|---|---|---|
| 125547 | R$ 12,76 | R$ 16.777.216 | 25 |
| 125812 | R$ 13,37 | R$ 33.554.432 | 26 |
| 125827 | R$ 16,84 | R$ 268.435.456 | 29 |
| 125835 | R$ 13,82 | R$ 134.217.728 | 28 |
| 125838 | R$ 17,65 | R$ 536.870.912 | 30 |

Sozinha, a jogada de R$ 536,9 mi responde por **R$ 5,37** da média da execução 125838 —
sem ela, a média cairia de R$ 17,65 para R$ 12,28. Em teoria, a média típica cresce
cerca de R$ 0,50 a cada duplicação do número de jogadas (~log₂(n)/2), sem nunca convergir.

### Quanto vale pagar para jogar?

O resultado médio por jogada é `prêmio médio − preço`; o equilíbrio empírico ficou em
**R$ 14,89**:

| Preço de entrada | Resultado médio/jogada | Saldo virou positivo (nas 5 execuções) |
|---|---|---|
| R$ 5 | +R$ 9,89 | 34× |
| R$ 10 | +R$ 4,89 | 49× |
| R$ 15 | −R$ 0,11 | 42× |
| R$ 20 | −R$ 5,11 | 25× |
| R$ 25 | −R$ 10,11 | 11× |
| R$ 30 | −R$ 15,11 | 3× |
| R$ 35 | −R$ 20,11 | 2× |
| R$ 40 | −R$ 25,11 | 2× |
| R$ 45 | −R$ 30,11 | 1× |
| R$ 50 | −R$ 35,11 | **0×** |

A R$ 50 por jogada, o saldo **nunca** ficou positivo — nem por um instante, em
nenhuma das cinco execuções.

### E se o jogador parasse no primeiro lucro?

Estatísticas dos pontos de "parou com lucro" (169 momentos em 500 milhões de jogadas):

| Preço | Chances de sair | Execuções com saída | 1ª saída (mediana) | Lucro mediano | Maior lucro |
|---|---|---|---|---|---|
| R$ 5 | 34 | 5 de 5 | jogada 7 | R$ 34 | R$ 866 |
| R$ 10 | 49 | 5 de 5 | jogada 1.970 | R$ 1.821 | R$ 7.883.663 |
| R$ 15 | 42 | 5 de 5 | jogada 1.970 | R$ 4.007,50 | R$ 363.957.811 |
| R$ 20 | 25 | 4 de 5 | jogada 3.691 | R$ 93.707 | R$ 88.782.523 |
| R$ 25 | 11 | 3 de 5 | jogada 7.368 | R$ 31.827 | R$ 62.443.238 |
| R$ 30 | 3 | 3 de 5 | jogada 7.368 | R$ 118.647 | R$ 36.103.953 |
| R$ 35 | 2 | 2 de 5 | jogada 2.637.613 | R$ 4.923.237,50 | R$ 9.764.668 |
| R$ 40 | 2 | 1 de 5 | jogada 7.368 | R$ 27.194 | R$ 44.967 |
| R$ 45 | 1 | 1 de 5 | jogada 7.368 | R$ 8.127 | R$ 8.127 |
| R$ 50 | 0 | 0 de 5 | — | — | — |

O padrão é o paradoxo de novo: entradas baratas saem no lucro **cedo, com frequência
e ganhando trocados**; entradas caras dependem de um mega-prêmio — as saídas dos preços
altos se alinham nos mesmos momentos (o mesmo prêmio raro empurra vários preços para o
azul de uma vez). E o lucro *médio* ao sair é inflado pelos mega-prêmios (a R$ 15:
mediana R$ 4 mil vs. média R$ 19,3 mi). Parar no lucro não muda o valor esperado do
jogo — só escolhe o momento de encerrar a história.

## Estrutura do repositório

```
├── README.md
├── inifit_simulation.py            # demo mínima (console)
├── stop_on_win.py                  # simulador completo (gera resultados/)
├── paradoxo-sao-petersburgo.html   # dashboard interativo (autocontido)
└── resultados/                     # saídas brutas, com timestamp
    ├── simulacao_100.000_jogadas-*.txt        (5 execuções)
    ├── simulacao_10.000.000_jogadas-*.txt     (5 execuções)
    └── simulacao_100.000.000_jogadas-*.txt    (5 execuções — base do dashboard)
```

Cada arquivo de resultado tem quatro seções: **resultado final** (agregados),
**distribuição de rodadas por jogada**, **resultado por preço de entrada** e a lista
de pontos em que cada preço **parou com lucro**.

## Notas e limitações

- **Reprodutibilidade**: os scripts não fixam semente (`random.seed`), então cada
  execução produz números diferentes — é proposital: a variância entre execuções é
  parte do que a análise mostra. Para reproduzir uma execução exata, fixe a semente.
- **Dashboard estático**: os dados estão embutidos no HTML. Gerar novos arquivos em
  `resultados/` **não** atualiza o dashboard automaticamente — os agregados precisam
  ser re-extraídos dos novos arquivos e re-injetados no HTML.
- **Limite de 50 pontos**: `stop_on_win.py` lista no máximo 50 pontos de saída com
  lucro por preço de entrada. Nas execuções de 100 milhões nenhum preço passou de 50
  (máximo observado: 38), então nada foi truncado; em execuções muito maiores isso
  pode deixar de valer (o contador "ficou positivo Nx" continua exato).
- **Precisão**: os prêmios são potências de 2 exatas (inteiros), então os totais e
  médias recomputados a partir das distribuições não têm erro de ponto flutuante
  relevante.

## Referência rápida da teoria

- P(encerrar na rodada k) = 1/2^k · prêmio = 2^(k−1) → cada rodada contribui ½ ao
  valor esperado → E[prêmio] = ∞; E[rodadas] = 2.
- Com *n* jogadas, o maior prêmio típico é ~n (2^log₂(n)), e a média amostral típica
  cresce ~log₂(n)/2 — em 100 milhões de jogadas, ≈ R$ 13–14, coerente com o observado
  (R$ 12,76–17,65).
- A resolução clássica do paradoxo (Daniel Bernoulli, 1738) troca valor esperado por
  utilidade esperada (utilidade logarítmica); a resolução moderna aponta a banca
  finita: se o cassino só pode pagar até B, o jogo truncado vale ~log₂(B)/2 + 1.
