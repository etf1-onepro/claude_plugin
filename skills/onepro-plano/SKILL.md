---
name: onepro-plano
description: Dúvida de como fazer algo no OnePro vira rota até a tool que responde, antes de gastar chamada, e vira plano quando o caminho tem mais de um passo. Use quando o usuário perguntar como faz, onde vê ou como gera um gráfico no OnePro, e quando ele não souber qual análise responde o que ele quer.
---

# Plano antes da chamada

**Rota** é o caminho do que o usuário pediu até a chamada que responde, com os
parâmetros preenchidos. **Plano** é a rota escrita antes de executar, quando ela
passa de um passo.

Chamada dada gasta cota e pode responder com precisão total a pergunta errada.
Trace a rota primeiro.

## Por onde o pedido entrou

| O que chegou | O que você faz |
|---|---|
| "como faço", "onde vejo", "para que serve" | rota, sem executar nada |
| Pedido fechado, com ativos, janela e moeda ditos | plano curto, e executa |
| Pedido aberto, um relatório ou um estudo sem parâmetro | um round de perguntas, depois o plano |

Pedido fechado não vira entrevista: a rota já está no pedido, monte e execute.
Vale inclusive quando o usuário chamou esta skill pelo nome, porque chamar pelo
nome pede o plano, não o interrogatório.

## Achar a rota

O catálogo não se decora, se consulta, e ele cresce sem avisar:

- **`onepro://telas`** traz o mapa de área, aba e gráfico do app, e a lista do
  que não tem rota. Primeira parada de "onde vejo".
- **`onepro_localizar_grafico`** recebe o gráfico citado pelo nome e devolve a
  tool com os parâmetros, ou a tela em que ele mora.
- **`onepro_buscar_ativos`** resolve nome em ticker, e é o passo 1 de quase todo
  plano. Índice sai por aqui também, com `classe="indice"`.
- A **description de cada tool** lista os parâmetros que ela aceita. Leia antes
  de prometer um parâmetro no plano.

Uma ambiguidade merece ficar decorada porque os nomes são quase iguais:
**"Janelas Móveis"** é o gráfico da aba Comportamento para uma carteira
(`onepro_comportamento`) e também da área Comparativo para várias linhas
(`onepro_analise_portfolio`), ambos com `visao="janelas_moveis"`.
`onepro_multiperiodo` é outra tela: resume CAGR real, percentis e extremos em
várias durações. Nunca entregue Multi Período como se fosse o gráfico chamado
"Janelas Móveis".

Toda pergunta sai com uma rota ou com a lacuna nomeada, e nomear a lacuna é
assunto de `analise-com-lastro`.

## O round

Pergunte o que muda o plano, e nada além disso. Todas as perguntas de uma vez,
numeradas, cada uma já com a sua recomendação na frente:

```
❓ **P1** - **<título da pergunta>**: <a pergunta, com as opções quando houver>

➡️ <a sua recomendação>
```

"Pode ir" fecha o round inteiro pelas recomendações. Um segundo round existe
quando uma resposta abriu uma decisão nova que muda os passos, e só.

Fato é trabalho seu, decisão é do usuário. O que costuma mudar o plano:

- **Quais ativos.** Nome ambíguo você resolve na busca, não na pergunta.
- **Janela e moeda**, quando o pedido não trouxe.
- **Carteira salva ou linhas montadas na conversa**, que são caminhos
  diferentes e chegam a números diferentes.
- **Valores em R$**, patrimônio, aporte e retirada, que só o usuário tem e sem
  os quais o motor não roda.
- **O que ele quer ver no fim**, uma tabela, uma comparação, uma distribuição de
  cenários.

## O plano

Numerado, um passo por chamada, cada passo com a tool e os parâmetros que vão
nela. A última linha diz o que o usuário vai receber.

```
1. onepro_buscar_ativos(query="bova", classe="etf") para fixar o ticker
2. onepro_analise_portfolio(carteiras=[...], benchmarks=["IBOV"], moeda="BRL")
3. onepro_multiperiodo(...) para as janelas móveis de 5 anos
Você vai receber uma tabela de retorno e risco na janela comum, com o IBOV ao lado.
```

Pronto quando:

- todo pedaço do pedido aparece em algum passo, ou está nomeado como lacuna
- cada passo traz parâmetro preenchido, não parâmetro descrito
- passo que depende de outro diz de qual depende e do que precisa dele
- a última linha descreve o entregável em uma frase

Aprovado o plano, execute na ordem. Passo que volta diferente do previsto muda o
plano na hora, e a mudança vira frase para o usuário antes de você seguir.

## Depois do plano

- Executado o plano, escrever os números é assunto de `analise-com-lastro`.
- Passo que falhou em conexão, autorização, assinatura ou cota é assunto de
  `onepro-conectar`.

## Guardrails

- Pedido explícito para não executar nenhuma tool se respeita literalmente:
  não leia resource nem chame o localizador. Descreva essa chamada de navegação
  como próximo passo da rota.
- O número entra no texto depois da chamada que o trouxe. O plano promete a
  busca, e o resultado dela aparece só quando ela volta.
- Pergunta ao usuário é para decisão dele. O que você consegue buscar, busque.
- Plano longo se entrega inteiro antes de rodar o primeiro passo, para o usuário
  cortar o que não quer enquanto cortar ainda é grátis.
