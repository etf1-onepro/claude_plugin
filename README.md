# OnePro AI

Plugin oficial do [OnePro](https://etf1.com.br/onepro) para clientes de IA que
suportam plugins do Claude Code. Conecta a sua IA aos dados e motores de análise
do OnePro: ETFs BR e globais, ações, BDRs, FIIs, fundos, renda fixa, índices, e a
carteira do próprio assinante.

## Instalar

```
/plugin marketplace add https://etf1.com.br/claude/marketplace.json
/plugin install onepro@etf1
```

Na primeira chamada o Claude abre a autorização do OnePro no navegador. Faça
login e conceda o acesso; a conexão fica salva.

## Requisitos

Assinatura ativa do OnePro. O conector é um benefício do assinante: não há camada
gratuita.

## O que ele faz

18 tools `onepro_*` de consulta e de computação, entre elas:

- **Consulta**: buscar ativos, ficha, comparação, screener, composição
  (holdings), séries mensais.
- **Carteira do assinante**: listar portfólios salvos e detalhar pesos e
  implementações.
- **Motores**: análise de carteira, aba Comportamento, otimização (fronteira
  eficiente), plano de retirada (SWR/PWR), GBI, janelas móveis, Monte Carlo
  prospectivo.

Somente-leitura: nenhuma tool altera dados da conta. Os dados vêm de um
**snapshot mensal**: toda resposta traz `dataset_version`, e os motores raciocinam
em termos reais (R$ de hoje).

## Skills

O plugin traz duas skills junto:

- **`analise-com-lastro`** disciplina como a IA reporta o que buscou: janela
  sempre em datas, benchmark nomeado, dado do conector separado de conta
  derivada, meses estendidos por índice declarados como simulação, e quando o
  conector não tem o dado, a lacuna dita em vez de preenchida por estimativa.
- **`onepro-conectar`** cobre a verificação da conexão e o diagnóstico de falha:
  autorização, assinatura, cota e o que fazer com o erro que a tool devolveu.

Para testar a conexão: *"Liste meus portfólios do OnePro e confirme a versão dos
dados."*

## Estrutura

O plugin mora na raiz deste repositório:

```
.claude-plugin/plugin.json   manifesto
.mcp.json                    servidor MCP remoto
skills/                      skills empacotadas junto
```

O catálogo que aponta para cá é servido em
`https://etf1.com.br/claude/marketplace.json`, e mora no repositório do site.

## Suporte

https://etf1.com.br/onepro
