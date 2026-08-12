# OnePro AI

Plugin oficial do [OnePro](https://etf1.com.br/onepro) para clientes de IA que
suportam plugins do Claude Code. Conecta a sua IA aos dados e motores de análise
do OnePro: ETFs BR e globais, ações, BDRs, FIIs, fundos, renda fixa, índices, e a
carteira do próprio assinante.

## Instalar

No **claude.ai**, em Personalizar → Plugins, adicione o marketplace por
repositório do GitHub:

```
etf1-onepro/claude_plugin
```

Instale o **OnePro AI**, clique em **Gerenciar**, abra a aba **Conectores** e,
na linha do `onepro`, clique em **Instalar** e depois em **Vincular**. É esse
conector que traz as tools, e é nele que a autorização do OnePro abre. Ele vem
dentro do plugin: não há nada para adicionar em Configurações → Conectores.

No **Claude Code**, no terminal ou na IDE:

```
/plugin marketplace add https://etf1.com.br/claude/marketplace.json
/plugin install onepro@etf1
```

Aqui o servidor MCP entra junto com o plugin, sem passo de conector à parte.

Os dois caminhos instalam o mesmo `onepro@etf1`. A autorização do OnePro abre no
navegador quando o cliente precisa dela, o que costuma ser na primeira chamada
de uma tool. Faça login e conceda o acesso; a conexão fica salva. Não existe
token para colar nem chave de API para pedir.

No Claude Code, depois de instalar, **ligue o auto-update** do marketplace
`etf1`:

```
/plugin  →  aba Marketplaces  →  etf1  →  Enable auto-update
```

Esse passo é necessário: marketplaces de terceiros vêm com auto-update desligado
por padrão. Sem ele o plugin fica parado na versão que você instalou, e skills
novas e correções não chegam.

## Atualizações

Com o auto-update ligado, o Claude Code checa por versões novas depois que a
sessão inicia, com um atraso de até dez minutos. A sessão em andamento continua
usando a versão que carregou; quando houver atualização, ele avisa para rodar
`/reload-plugins`, ou a versão nova entra sozinha na próxima vez que você abrir
o Claude.

Para atualizar na hora, sem esperar o ciclo automático:

```
/plugin marketplace update etf1
/plugin update onepro@etf1
/reload-plugins
```

## Requisitos

Assinatura ativa do OnePro. O conector é um benefício do assinante: não há camada
gratuita.

## O que ele faz

19 tools `onepro_*` de consulta e de computação, entre elas:

- **Consulta**: buscar ativos, ficha, comparação, screener, composição
  (holdings), séries mensais.
- **Navegação**: o gráfico citado pelo nome ("aquele de janelas móveis") vira a
  tool com os parâmetros, ou a tela do app onde ele mora.
- **Carteira do assinante**: listar portfólios salvos e detalhar pesos e
  implementações.
- **Motores**: análise de carteira, aba Comportamento, otimização (fronteira
  eficiente), plano de retirada (SWR/PWR), GBI, janelas móveis, Monte Carlo
  prospectivo.

Somente-leitura: nenhuma tool altera dados da conta. As chamadas ainda consomem
a cota do assinante e ficam registradas para segurança e auditoria. Os dados vêm
de um **snapshot mensal**: toda resposta traz `dataset_version`. Os motores de
planejamento e simulação usam termos reais (R$ de hoje); a análise comparativa
declara na própria resposta quando entrega base nominal, real ou ambas.

## Skills

O plugin traz três skills junto:

- **`onepro-plano`** responde à dúvida de caminho: como eu faço isso no OnePro,
  onde fica aquele gráfico, qual análise responde o que eu quero. Nessas
  perguntas ela entra sozinha. Para planejar um relatório antes de rodar,
  chame-a pelo nome com `/onepro:onepro-plano`: ela faz de uma vez as perguntas que
  mudam o resultado, cada uma já com a recomendação dela, e devolve o plano de
  chamadas para você aprovar ou cortar enquanto cortar ainda não gastou consulta.
- **`analise-com-lastro`** disciplina como a IA reporta o que buscou: janela
  sempre em datas, benchmark nomeado, dado do conector separado de conta
  derivada, meses estendidos por índice declarados como simulação, e quando o
  conector não tem o dado, a lacuna dita em vez de preenchida por estimativa.
- **`onepro-conectar`** cobre a verificação da conexão e o diagnóstico de falha:
  autorização, assinatura, cota e o que fazer com o erro que a tool devolveu.

Para testar a conexão: *"Liste meus portfólios do OnePro e confirme a versão dos
dados."*

## Estrutura

O plugin mora na raiz deste repositório, e o repositório também é o marketplace:

```
.claude-plugin/marketplace.json   catálogo, aponta para a própria raiz
.claude-plugin/plugin.json        manifesto
.mcp.json                         servidor MCP remoto
skills/                           skills empacotadas junto
```

O mesmo catálogo é servido em `https://etf1.com.br/claude/marketplace.json`, para
quem adiciona por URL. Essa cópia mora no repositório do site e aponta para cá
por fonte remota, porque caminho relativo só resolve contra um clone.

## Suporte

https://etf1.com.br/onepro
