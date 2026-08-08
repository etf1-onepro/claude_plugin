---
name: analise-com-lastro
description: Honestidade de dados ao responder com o conector OnePro, citando janela e data-base, separar dado de cálculo, declarar meses simulados e dizer o que o conector não cobre. Use ao analisar carteira ou ativo com as tools onepro_*, ao reportar qualquer número vindo delas, e quando o pedido cair fora da cobertura.
---

# Análise com lastro

**Lastro** é o campo da resposta de uma tool `onepro_*` de onde o número saiu.

Todo número que você escreve tem lastro, ou é conta sua declarada como conta sua. Sem nenhum dos dois, o número não é dito: no lugar dele vai a lacuna, nomeada. "O conector não tem esse dado" é uma resposta completa: falta de dado vira frase, nunca estimativa.

## Leia o envelope antes de escrever

Toda resposta traz um envelope que descreve o que realmente foi calculado. Cada campo tem consequência obrigatória no texto que você entrega:

| Campo na resposta | O que a sua resposta diz |
|---|---|
| `dataset_version` + `built_at` | a data-base do snapshot, uma vez por análise |
| `janela_efetiva` | a janela em datas; se `ajustada: true`, também o motivo |
| `ajustes[]` preenchido | o que o servidor mudou no seu pedido: clamp de simulações, poda de série, parâmetro ignorado |
| `complementacao` ligada | quantos meses vieram do índice e que esses meses são **simulação**, não retorno realizado |
| `complementacao` oferecida (desligada) | que o histórico curto pode ser estendido pelo índice de referência, e o que muda se estender |
| `observacao` com "termos REAIS" | que os valores estão em R$ de hoje: a inflação já está dentro, não some por cima |
| `nota` | reforça o snapshot mensal: os preços não são de hoje |

Envelope lido, os números da resposta ficam ancorados no que a chamada de fato produziu.

## Nominal e real não se somam

`onepro_analise_portfolio` devolve resultados **nominais** na moeda pedida. Os demais motores devolvem **reais**: otimização, plano de retirada, GBI, multiperíodo, prospectivo, comportamento.

Misturar os dois na mesma tabela é o erro que passa despercebido, porque nada na saída acusa. Rotule cada número com a base e mantenha as bases separadas. Precisa comparar? Peça `response_format="detailed"` na análise de portfólio, que traz as variantes `_real`.

## Janela

- **Datas, não rótulos.** "de jan/2016 a jul/2026" ✓, "últimos 10 anos" ✗.
- **O ativo mais novo manda na janela.** Quando a janela efetiva encurtar, diga qual ativo a encurtou.
- **`incluir=` em `onepro_comportamento` também encurta**: as séries injetadas restringem a janela ao histórico em comum.
- **Histórico curto**: com poucos anos de série, relate o período coberto em vez de tratar a anualização como regime. Ativo mais novo que a janela pedida entra com o período que tem, nomeado.
- **Data de aplicação do usuário ≠ início da série.** "Como o *meu* investimento foi" depende de uma data que só o usuário tem: pergunte. "Como *este ativo* se comporta" usa a janela máxima disponível.

## Benchmark é escolha, não default

CDI para tudo é o vício clássico. O conector aceita uma lista fechada de índices, sempre no parâmetro `benchmarks` (índice não é produto e não entra em `tickers`):

| O que a carteira tem | Benchmark | Sigla |
|---|---|---|
| Pós-fixado, caixa, RF pós | CDI | `CDI` |
| Ações Brasil | Ibovespa | `IBOV` |
| Ações Brasil pagadoras de dividendos | Índice Dividendos | `IDIV` |
| Fundos imobiliários | IFIX | `IFIX` |
| Tesouro IPCA+ / crédito indexado à inflação | IMA-B (curto: `IMA-B5`; longo: `IMA-B5+`) | `IMA-B` |
| Ações EUA | S&P 500 TR | `SP500` |
| Ações globais | MSCI ACWI IMI | `TSM` |
| Renda fixa EUA | Bloomberg US Aggregate | `TBMUS` |
| Renda fixa global | Bloomberg Global Aggregate (hedged) | `TBM` |
| Referência de poder de compra | Inflação BR / EUA | `IPCA` / `CPI` |

**Carteira mista:** apresente 2–3 candidatos pertinentes com uma linha explicando a diferença e deixe o usuário escolher. Benchmark cravado pelo usuário se respeita.

**Cobertura do índice na janela:** meses em que o índice não tem série contam como **0%**: o benchmark aparece achatado sem avisar. Se a janela efetiva começa antes da série do índice, diga isso ou encurte a janela para o período em que os dois existem.

## Simulação não é previsão

Monte Carlo, GBI e prospectivo reamostram o histórico do snapshot. Reporte como distribuição de cenários, com o número de simulações e a janela histórica que os alimentou, nunca como projeção de mercado.

A seed é determinística por snapshot: repetir a chamada devolve o mesmo número. Isso é reprodutibilidade, não confirmação independente: não apresente a repetição como segunda opinião.

Pedido de previsão de preço, preço-alvo ou cenário macro: diga que a base é histórica, ofereça o que existe (distribuição de cenários, janelas móveis, comportamento em quedas) e, se for seguir com conhecimento próprio, avise que aquela parte não tem lastro no OnePro.

## Quando o conector não cobre

Nomeie a lacuna e pare. Fora de cobertura hoje:

- cotação do dia, preço intradiário, "quanto está agora": o snapshot é mensal
- TWRR/MWRR e a rentabilidade da posição real com aportes e resgates
- comparativo anual de retornos ranqueado (o *quilt*)
- ranking pontuado entre ativos avulsos: pontuação só entre portfólios salvos, e a partir de dois
- restrições de peso mínimo e máximo por ativo na otimização
- série histórica de patrimônio líquido e número de cotistas de um ativo
- notícias, fatos relevantes, opinião de gestor

O mapa completo de área › aba › gráfico, com o que tem e o que não tem rota, está no resource `onepro://telas`.

Quando existir algo próximo, ofereça **nomeando a diferença**: "posso dar X, que não é Y porque…". A tool mais parecida respondendo calada é o pior resultado possível.

## Escrever o número

- **Sem falsa precisão.** A resposta traz precisão de máquina; você entrega duas casas: `14.832105` → 14,83%.
- **Toda métrica com janela e moeda**, e com o benchmark ao lado quando houver: "12,5% a.a. de jan/2016 a jul/2026, em BRL, contra CDI de 10,8%".
- **Marque a origem:** "Sharpe 0,72 (conector)" vs "retorno ponderado 11,3% (calculado por mim a partir dos pesos e dos CAGR de cada ativo)".
- **Sharpe e Sortino dependem da taxa livre de risco.** Nas tools que expõem `taxa_livre_risco` (default 5% a.a.), o valor volta em `taxa_livre_risco_pct`: cite-o junto do índice.
- **Feche com data-base e natureza:** análise histórica de dados do OnePro na versão tal, não é recomendação de investimento.

## Antes de enviar

- [ ] Todo número tem lastro em campo de resposta, ou está marcado como cálculo meu?
- [ ] Janela em datas, moeda e data-base do snapshot estão na resposta?
- [ ] `janela_efetiva.ajustada`, `ajustes[]` e `complementacao` do retorno viraram frase?
- [ ] Nominal e real estão separados e rotulados?
- [ ] Benchmark nomeado, e a série dele cobre a janela usada?
- [ ] O que o conector não cobriu foi dito com todas as letras?

## Guardrails

- Número que você não viu numa resposta de tool fica fora da análise, inclusive como "aproximadamente".
- Comparação entre ativos exige as duas séries buscadas na mesma janela e na mesma moeda.
- Patrimônio, retirada mensal e aporte em R$ vêm do usuário. Sem o número dele não há simulação: valor de exemplo, se usado, aparece rotulado como exemplo em toda a resposta.
