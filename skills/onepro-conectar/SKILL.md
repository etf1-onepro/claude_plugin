---
name: onepro-conectar
description: Verificar e diagnosticar a conexão com o conector OnePro, com smoke test após instalar, leitura do erro que a tool devolveu, e o que fazer em falha de autorização, assinatura inativa, cota estourada ou carteira vazia. Use quando uma tool onepro_* falhar, quando o usuário disser que o plugin não está funcionando, e logo após instalar o plugin.
---

# Conectar ao OnePro

O conector é um servidor MCP remoto sobre HTTP. O cliente negocia a autorização
sozinho no navegador na primeira chamada: **não existe token para colar, chave
de API para pedir ou arquivo de credencial para editar.** Se você se pegar
pedindo segredo ao usuário, o diagnóstico já saiu do trilho.

## Smoke test

Uma chamada resolve, porque exercita autorização, cota e dados de conta ao mesmo
tempo:

```
onepro_meus_portfolios
```

Passou: relate o `dataset_version` da resposta e siga para o que o usuário
queria. Não invente uma bateria de testes por tool: as 18 compartilham o mesmo
transporte e a mesma sessão.

Sem portfólio salvo, a resposta vem vazia **e isso é sucesso**: a conexão
funcionou, a conta é que não tem carteira montada. Use `onepro_conexao_status`
quando quiser separar as duas coisas sem depender de a conta ter dados.

## Se esta skill carregou, o plugin está instalado

Esta skill vem dentro do plugin: você só está lendo isto porque ele carregou.
Logo, **"plugin não instalado" está descartado como causa**, e nenhuma tool
`onepro_*` à vista significa que falta o connector, que é peça separada da
instalação em todo cliente.

- **claude.ai e Claude Desktop**: o OnePro entra como connector, em Customize →
  Connectors. Precisa estar autorizado, o login abre no navegador, e precisa
  estar **ligado naquela conversa**, no seletor de ferramentas. Connector
  desligado na conversa não expõe tool nenhuma, com o plugin instalado do mesmo
  jeito.
- **Claude Code**: `/mcp` lista o servidor `onepro` e o estado da autorização.

Comando de barra para gerenciar plugin (`/plugin ...`) só existe no Claude Code.
No claude.ai a instalação é por menu, Customize → Plugins. Mandar o usuário
digitar um comando que o cliente dele não tem trava a conversa em vez de
resolver.

## O erro já traz a correção

Toda falha do conector volta com a instrução do que fazer. Leia e siga:
**repetir a mesma chamada não é diagnóstico**, e em erro de cota a repetição
gasta o saldo que você está tentando preservar.

| Sintoma | O que é | O que fazer |
|---|---|---|
| Nenhuma tool `onepro_*` existe | Connector fora do ar nesta sessão, não plugin faltando | Siga a seção acima: autorize e ligue o connector no cliente em que o usuário está |
| Tools existem, primeira chamada trava | Autorização pendente no navegador | Peça ao usuário para concluir o login e a permissão na aba aberta; a sessão fica salva depois disso |
| Erro de autorização recorrente | Sessão expirada ou permissão revogada | Refazer a autorização pelo cliente, nunca contornar pedindo credencial |
| Acesso negado com login válido | Assinatura inativa | O conector é benefício de assinante e não tem camada gratuita: encaminhe para https://etf1.com.br/onepro |
| Erro de cota | Limite de uso atingido | O erro diz quando tentar de novo; `onepro_conexao_status` mostra o saldo. Espere o tempo informado |
| Resposta vazia sem erro | Conta sem aquele dado | Conexão OK: diga que a conta não tem o item, não trate como falha |
| Tool que você esperava não existe | Fora da cobertura do conector | Confira `onepro://telas` e nomeie a lacuna |

## Limite do seu diagnóstico

Você enxerga o que a resposta da tool devolveu, e só. Estado do servidor,
latência de rede e saúde da infraestrutura do OnePro não estão ao seu alcance:
não os apresente como causa.

Esgotada a tabela acima com a falha de pé, a conclusão honesta é nomear o que
foi tentado, colar o erro literal que voltou e encaminhar para
https://etf1.com.br/onepro. Palpite de causa raiz sem lastro manda o usuário
mexer em coisa certa.

## Guardrails

- Não peça token, senha, chave de API nem cookie de sessão em nenhuma hipótese.
- Não sugira editar `.mcp.json`, trocar a URL do servidor ou apontar para outro
  endpoint: a URL é a mesma para todos os assinantes.
- Falha de conexão não vira análise por conhecimento próprio: sem dado do
  conector, diga que não há dado em vez de responder de memória.
