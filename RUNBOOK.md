# RUNBOOK — Fluxo OpenSpec

Ordem dos comandos para levar uma mudança do zero até o arquivamento.
Documentado a partir do fluxo real executado no change `add-cadastro-cliente`.

## Visão geral

```
init  →  propose  →  apply  →  sync  →  archive
 (1x)     (novo)     (código)  (specs)   (fim)
```

O trabalho é feito por **slash commands** (`/opsx:*`), que orquestram o agente.
Os comandos `openspec` da CLI são as consultas de estado por trás deles — úteis
para inspecionar ou automatizar sem o agente.

---

## 0. Setup (uma vez por projeto)

```bash
openspec init
```

Cria a estrutura `openspec/` com `specs/` (specs principais) e `changes/`
(mudanças em andamento).

Layout resultante:

```
openspec/
├── specs/                  # specs principais (fonte da verdade, permanente)
│   └── <capability>/spec.md
└── changes/                # mudanças ativas
    ├── <change-name>/
    │   ├── proposal.md
    │   ├── specs/<capability>/spec.md   # delta spec
    │   ├── design.md
    │   └── tasks.md
    └── archive/            # mudanças concluídas
        └── YYYY-MM-DD-<change-name>/
```

---

## 1. Propor a mudança

```
/opsx:propose <descrição da mudança>
```

Gera, em ordem (schema `spec-driven`), os quatro artefatos de planejamento:

| Artefato | Arquivo | Conteúdo |
|---|---|---|
| `proposal` | `proposal.md` | Por quê, o que muda, capabilities afetadas |
| `specs` | `specs/<cap>/spec.md` | Delta spec: requisitos + cenários (WHEN/THEN) |
| `design` | `design.md` | Decisões técnicas, alternativas rejeitadas, riscos |
| `tasks` | `tasks.md` | Checklist de implementação `- [ ]` |

Cada artefato depende do anterior — `tasks` só é liberado depois de `specs` e
`design`.

**Inspecionar:**

```bash
openspec list --json                                  # mudanças ativas
openspec status --change "<name>" --json              # status dos artefatos
openspec show <name>                                  # exibir a mudança
openspec validate <name>                              # validar formato
```

---

## 2. Implementar

```
/opsx:apply <change-name>
```

Lê os artefatos de contexto, implementa as tasks em ordem e marca cada uma como
`- [x]` em `tasks.md` conforme conclui.

**Inspecionar:**

```bash
openspec instructions apply --change "<name>" --json
```

Retorna `contextFiles`, `progress` (total/complete/remaining), a lista de tasks
e um `state`:

- `blocked` — falta algum artefato de planejamento; volte ao passo 1
- `ready` — pode implementar
- `all_done` — tudo pronto, siga para o passo 3

**Regra:** só marque `- [x]` quando o comportamento especificado estiver
totalmente implementado. Se uma task exigir escopo além do spec, pare e
levante a questão em vez de reduzir silenciosamente.

---

## 3. Sincronizar specs

```
/opsx:sync <change-name>
```

Faz o merge do **delta spec** (`changes/<name>/specs/<cap>/spec.md`) no
**spec principal** (`specs/<cap>/spec.md`).

Operações do delta e o que cada uma faz no spec principal:

| Header no delta | Ação |
|---|---|
| `## ADDED Requirements` | adiciona o requisito |
| `## MODIFIED Requirements` | substitui o requisito (bloco completo, com todos os cenários) |
| `## REMOVED Requirements` | remove o bloco do requisito |
| `## RENAMED Requirements` | renomeia via `FROM:` / `TO:` |

O spec principal **nunca** contém headers de delta — tudo vive sob um único
`## Requirements`. O `## Purpose` do delta só é usado quando a capability é nova.

**Validar depois:**

```bash
openspec validate --specs
```

Este passo é separado do archive de propósito: as specs podem ser sincronizadas
antes de a implementação terminar, se fizer sentido.

---

## 4. Arquivar

```
/opsx:archive <change-name>
```

Verificações antes de mover:

1. todos os artefatos com status `done` ou `skipped`
2. todas as tasks marcadas `- [x]`
3. delta specs já sincronizados (senão, oferece sincronizar inline)

Depois move o diretório:

```bash
openspec/changes/<name>  →  openspec/changes/archive/YYYY-MM-DD-<name>
```

Avisos (artefatos ou tasks incompletos) não bloqueiam o archive — apenas pedem
confirmação.

Existe também a versão pura da CLI:

```bash
openspec archive <change-name>
```

---

## Comandos de consulta (qualquer momento)

```bash
openspec list                          # mudanças ativas
openspec list --specs                  # specs principais
openspec view                          # dashboard interativo
openspec show <item>                   # exibir change ou spec
openspec validate <item>               # validar um item
openspec validate --specs              # validar todas as specs principais
openspec status --change "<n>" --json  # status detalhado de artefatos
openspec doctor                        # saúde do root resolvido
openspec context                       # contexto de trabalho
openspec schemas                       # schemas de workflow disponíveis
```

### Flag `--store`

Se o trabalho vive em um *store* (repo OpenSpec standalone registrado na
máquina), descubra os ids e passe a flag em todos os comandos que leem ou
escrevem specs e changes:

```bash
openspec store list --json
openspec status --change "<name>" --json --store "<id>"
```

Uma vez escolhido, `--store <id>` é *sticky* para todo o fluxo. Sem store, os
comandos agem no `openspec/` local mais próximo.

---

## Exemplo completo — `add-cadastro-cliente`

```bash
# 1. propor (via slash command)
/opsx:propose adicionar cadastro de clientes com CRUD em Flask
# → proposal.md, specs/cliente/spec.md, design.md, tasks.md (9 tasks)

# 2. implementar
/opsx:apply add-cadastro-cliente
# → app.py, requirements.txt, test_app.py
# → 9/9 tasks marcadas, 12 testes passando

# 3. sincronizar specs
/opsx:sync add-cadastro-cliente
# → cria openspec/specs/cliente/spec.md (5 requisitos, 12 cenários)
openspec validate --specs        # ✓ spec/cliente

# 4. arquivar
/opsx:archive add-cadastro-cliente
# → openspec/changes/archive/2026-09-06-add-cadastro-cliente/
```

---

## Comandos auxiliares

| Comando | Quando usar |
|---|---|
| `/opsx:explore` | investigar specs e changes existentes antes de propor |
| `/opsx:update` | revisar artefatos de uma change já criada |

Se a implementação revelar um problema de design, pare o `apply`, atualize
`design.md` ou o delta spec via `/opsx:update`, e retome — o fluxo não é
travado por fase.
