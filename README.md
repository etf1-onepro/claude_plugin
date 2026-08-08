# OnePro AI: marketplace de plugins

Catálogo oficial do [OnePro](https://etf1.com.br) para clientes de IA que
suportam plugins do Claude Code.

## Instalar

```
/plugin marketplace add https://etf1.com.br/claude/marketplace.json
/plugin install onepro@etf1
```

Alternativa, direto por este repositório:

```
/plugin marketplace add etf1-onepro/claude_plugin
/plugin install onepro@etf1
```

## Plugins

| Plugin | O que entrega |
|---|---|
| [`onepro`](plugins/onepro) | Conector OnePro AI: dados e motores de análise de investimentos do assinante |

## Estrutura

```
.claude-plugin/marketplace.json   catálogo
plugins/onepro/                   o plugin
```

O `marketplace.json` é servido também em
`https://etf1.com.br/claude/marketplace.json`. As duas cópias precisam ser
idênticas.

Cada plugin é referenciado por `git-subdir` apontando para a sua subpasta neste
repositório, e não por caminho relativo, que não resolve quando o marketplace é
adicionado por URL.
