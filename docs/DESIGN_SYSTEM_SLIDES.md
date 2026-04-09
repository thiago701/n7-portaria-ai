# n7-portaria-ai — Design System dos Slides

Diretriz oficial de identidade visual para TODAS as apresentações do projeto.
Toda aula, palestra ou material em slides DEVE seguir este padrão.

---

## Paleta de Cores (extraída da Aula 01)

```javascript
const COLORS = {
  // ── Backgrounds ─────────────────────────────
  darkBg:     "172A45",  // Fundo escuro principal (slides título, código, conclusão)
  darkerBg:   "0F1D30",  // Fundo extra-escuro (barras/linhas em slides dark)
  lightBg:    "EDF2F7",  // Fundo claro (slides de conteúdo, agenda)
  lighterBg:  "F7FAFC",  // Fundo claro alternativo (slides com cards)
  white:      "FFFFFF",  // Cards, textos em fundo escuro

  // ── Texto ───────────────────────────────────
  textDark:   "1A202C",  // Texto principal em fundos claros
  textMuted:  "A0AEC0",  // Texto secundário, subtítulos, descrições
  textSlate:  "8BA3C0",  // Texto terciário, rodapés, captions
  textBorder: "CBD5E0",  // Bordas sutis, divisórias

  // ── Accent principal ────────────────────────
  teal:       "38B2AC",  // COR DE DESTAQUE — a mais usada!
                         // Badges, palavras destacadas, títulos teal, subtítulos
  tealDark:   "2C9A94",  // Variante escura do teal (borda do badge)

  // ── Accent secundários (uso com moderação) ──
  orange:     "E8734A",  // Números de agenda, iniciais de destaque
  blue:       "3B82F6",  // Cards, ícones, iniciais
  purple:     "8B5CF6",  // Cards, ícones, iniciais
  red:        "E05252",  // Alertas, destaque de erro, iniciais

  // ── Código ──────────────────────────────────
  codeBg:     "1E293B",  // Fundo dos blocos de código
};
```

### Regras de Uso de Cor

1. **Teal `38B2AC` é o protagonista.** Usado para: badges, palavras-chave, subtítulos,
   numeração em fundo escuro, barras inferiores, checkmarks.
2. **Orange, blue, purple, red** são coadjuvantes — usados para diferenciar items em
   listas, cards ou iniciais. Nunca como cor dominante.
3. **Fundo escuro (`172A45`)** para: slide título, slides com código, tabelas, prática, conclusão.
4. **Fundo claro (`EDF2F7` ou `F7FAFC`)** para: agenda, cards de features, estrutura de pastas.
5. **Nunca verde puro (`2ECC71`) ou navy puro (`1E2761`).** O verde do projeto é teal.

---

## Tipografia

| Elemento | Fonte | Tamanho | Peso | Cor |
|----------|-------|---------|------|-----|
| Título principal | Calibri | 42-48pt | Bold | `FFFFFF` (escuro) ou `1A202C` (claro) |
| Subtítulo / destaque | Calibri | 28-32pt | Bold | `38B2AC` (teal) |
| Corpo de texto | Calibri | 14-15pt | Regular | `FFFFFF` ou `1A202C` |
| Texto secundário | Calibri | 11-13pt | Regular | `A0AEC0` ou `8BA3C0` |
| Código / terminal | Consolas | 11-14pt | Regular | `FFFFFF` em fundo `1E293B` |
| Rodapé | Calibri | 9-10pt | Regular | `8BA3C0` |

### Regras de Tipografia

1. **Apenas Calibri + Consolas.** Nenhuma outra fonte.
2. **Títulos são GRANDES** (42pt+) e alinhados à esquerda.
3. **Última palavra do título** pode ser destacada em teal (`38B2AC`).
4. **Corpo alinhado à esquerda.** Centro apenas para banners e rodapés.

---

## Layouts dos Slides (10 templates)

### 1. TÍTULO (dark bg)
```
┌─────────────────────────────────────┐
│ [badge teal] AULA XX | FASE X      │  bg: 172A45
│                                     │
│ Título Grande em                    │  Calibri 48pt bold white
│ Várias Linhas                       │
│                                     │
│   Subtítulo descritivo              │  Calibri 15pt A0AEC0
│                                     │
│ DD de Mês de AAAA • n7 Tech • ...   │  Calibri 11pt 8BA3C0
└─────────────────────────────────────┘
```
- Badge: retângulo arredondado bg `38B2AC`, borda `2C9A94`, texto `FFFFFF` 10pt bold
- Título: última palavra em teal

### 2. AGENDA (split dark/light)
```
┌────────┬────────────────────────────┐
│ DARK   │  LIGHT bg (EDF2F7)         │
│ 172A45 │                            │
│        │  01  Item da agenda        │  teal number + dark text
│ Título │  ──────────────────        │  divisória CBD5E0
│ grande │  02  Item da agenda        │
│ white  │  ──────────────────        │
│        │  03  Item da agenda        │
│ desc   │  ...                       │
│ muted  │                            │
│        │                            │
│ [badge]│                            │
└────────┴────────────────────────────┘
```
- Painel esquerdo: ~28% da largura
- Badge "n7-portaria-ai" no canto inferior esquerdo

### 3. CARDS EM GRID (light bg)
```
┌─────────────────────────────────────┐
│ Título                              │  bg: F7FAFC
│ Subtítulo muted                     │
│                                     │
│ ┌─card──┐ ┌─card──┐ ┌─card──┐     │  Cards brancos com borda
│ │▌Letra │ │▌Letra │ │▌Letra │     │  sutil e barra lateral
│ │ Nome  │ │ Nome  │ │ Nome  │     │  colorida no topo
│ │ desc  │ │ desc  │ │ desc  │     │
│ └───────┘ └───────┘ └───────┘     │
│                                     │
│ ┌──── Banner teal 38B2AC ────────┐ │  Banner inferior
│ │  Texto resumo                   │ │  opcional
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```
- Cards: bg white, borda `CBD5E0`, barra top/lateral com accent color
- Iniciais grandes em accent color (orange/blue/purple/red/teal)

### 4. LINHAS HORIZONTAIS (dark bg)
```
┌─────────────────────────────────────┐
│ Título Grande                       │  bg: 172A45
│ Subtítulo italic muted              │
│                                     │
│ ┌─ bar ─────────────────────────┐  │  bar: 1E293B ou 0F1D30
│ │ 01  Label teal  →  Resultado  │  │
│ └───────────────────────────────┘  │
│ ┌─ bar ─────────────────────────┐  │
│ │ 02  Label teal  →  Resultado  │  │
│ └───────────────────────────────┘  │
│ ...                                 │
│                                     │
│ rodapé: n7-portaria-ai • ...        │
└─────────────────────────────────────┘
```
- Barras alternando `1E293B` e transparente
- Números em teal, labels em teal bold, resultados em teal
- Setas "→" em `A0AEC0`

### 5. SPLIT COM CÓDIGO (dark left / light right)
```
┌────────┬────────────────────────────┐
│ DARK   │  LIGHT                     │
│        │                            │
│ Título │  01 ┌─code─────────┐      │  Blocos de código
│ grande │     │ comando       │      │  bg: 1E293B
│        │     └───────────────┘      │  borda: 38B2AC
│ teal   │     Descrição              │
│ sub    │                            │
│        │  02 ┌─code─────────┐      │
│ desc   │     │ comando       │      │
│ muted  │     └───────────────┘      │
│        │     Descrição              │
│ [badge]│                            │
└────────┴────────────────────────────┘
```

### 6. SPLIT COM CARDS (dark left / light right)
```
┌────────┬────────────────────────────┐
│ DARK   │  LIGHT                     │
│        │                            │
│ Título │  ┌─card────────────┐      │  Cards com barra lateral
│ grande │  │▌ Título code     │      │  colorida (accent)
│        │  │  Descrição       │      │
│ tree   │  └──────────────────┘      │
│ code   │                            │
│ mono   │  ┌─card────────────┐      │
│ teal   │  │▌ Título code     │      │
│        │  │  Descrição       │      │
│ [badge]│  └──────────────────┘      │
└────────┴────────────────────────────┘
```

### 7. TABELA (dark bg)
```
┌─────────────────────────────────────┐
│ Título                              │  bg: 172A45
│ Subtítulo muted                     │
│                                     │
│  Coluna    Coluna    Coluna         │  Header: 38B2AC text
│ ┌────────────────────────────────┐ │
│ │ dado     dado      dado        │ │  Rows alternando bg
│ ├────────────────────────────────┤ │
│ │ dado     dado      dado        │ │
│ └────────────────────────────────┘ │
│                                     │
│ Dica/CTA em teal                    │
└─────────────────────────────────────┘
```

### 8. PRÁTICA (dark bg)
```
┌─────────────────────────────────────┐
│                                     │  bg: 172A45
│ Hora da                             │  48pt bold white
│ Prática!                            │
│                                     │
│ Subtítulo teal                      │
│                                     │
│  1  Passo descrição                 │  Números muted, texto white
│  2  Passo descrição                 │
│  3  Passo descrição                 │
│  ...                                │
└─────────────────────────────────────┘
```

### 9. CONCLUSÃO (dark bg)
```
┌─────────────────────────────────────┐
│                                     │  bg: 172A45
│ Parabéns pelo                       │  48pt bold white
│ momento incrível!                   │  última linha em teal
│                                     │
│ ┌─ box ─────────────────────────┐  │  Box com borda teal
│ │ O que aprendemos hoje:  teal  │  │
│ │ ✓  Item 1                     │  │
│ │ ✓  Item 2                     │  │
│ │ ✓  Item 3                     │  │
│ └───────────────────────────────┘  │
│                                     │
│ Próxima aula: Título em teal        │
│                                     │
│ ┌── Banner 38B2AC ──────────────┐  │
│ │  Mensagem motivacional         │  │
│ └────────────────────────────────┘  │
└─────────────────────────────────────┘
```

### 10. COMPARAÇÃO LADO A LADO (dark ou light)
Para slides de mapeamento (ex: SQL → Python).

---

## Elementos Recorrentes

### Badge "n7-portaria-ai"
- Posição: canto inferior esquerdo (x: 0.4, y: bottomEdge - 0.55)
- Tamanho: ~1.3" × 0.35"
- Background: `38B2AC`, borda `2C9A94`, border-radius
- Texto: "n7-portaria-ai" em 9pt Calibri bold white

### Badge de Aula (slide título)
- Posição: topo esquerdo (x: 0.5, y: 0.3)
- Texto: "AULA XX  |  FASE X — NOME" em 10pt Calibri bold white
- Background: `38B2AC`, borda `2C9A94`

### Rodapé (slides dark com contexto)
- Texto: "n7-portaria-ai  •  Neural Tech  •  Aula XX  •  2026"
- Cor: `8BA3C0`, 9pt, alinhado à esquerda
- Posição: bottom-left com margem 0.5"

### Divisórias horizontais
- Cor: `CBD5E0` ou `8BA3C0` com 0.5pt
- Em slides claros: separam items de agenda ou sections

### Barras de destaque em cards (light bg)
- 4px de largura, alinhada ao topo ou à esquerda do card
- Cores: variam entre orange, blue, purple, red, teal
- Nunca duas barras da mesma cor seguidas

---

## Regras Gerais

1. **Layout:** 16:9 (prs.layout = "LAYOUT_WIDE" → 13.3" × 7.5")
2. **Margens mínimas:** 0.5" em todos os lados
3. **Espaçamento entre blocos:** 0.3"–0.5"
4. **Alternância dark/light:** Intercalar para manter ritmo visual.
   Padrão típico: Dark (título) → Split/Light → Dark → Light → Dark (prática) → Dark (conclusão)
5. **Sem emojis.** Usar cores e formas geométricas em vez de emojis.
6. **Sem linhas sob títulos.** Usar espaço em branco ou mudança de cor de fundo.
7. **Consistência absoluta:** Todos os slides de todas as aulas devem parecer da mesma apresentação.

---

## Estrutura Padrão de uma Aula (10-15 slides)

| # | Tipo | Background | Conteúdo |
|---|------|-----------|----------|
| 1 | Título | Dark | Badge + título grande + subtítulo |
| 2 | Agenda | Split | O que vamos fazer hoje (6 items) |
| 3-4 | Conteúdo | Light | Cards, grids, explicações visuais |
| 5-6 | Conteúdo | Dark | Tabelas, comparações, código |
| 7-8 | Conteúdo | Split/Light | Estruturas, detalhes |
| 9 | Prática | Dark | Hora da prática + passos |
| 10 | Conclusão | Dark | Parabéns + checklist + próxima aula |

---

*Última atualização: 09/04/2026*
*Baseado na identidade visual estabelecida na Aula 01.*
