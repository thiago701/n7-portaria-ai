# Aula 03 — Revisao sobre Mapeamento de Dominio

**Data:** 17 de abril de 2026
**Duracao:** 2 horas
**Pre-requisito:** Leitura do Ebook "Do SQL para o Python — Mapeando o Dominio com Calma e Clareza"

---

## Por que esta Aula?

Voce ja leu o ebook, ja viu os conceitos. Mas sabemos que quando a gente
le algo novo, e normal precisar revisitar mais de uma vez — principalmente
conceitos que envolvem dois "idiomas" ao mesmo tempo (SQL e Python).

Entao hoje a aula e diferente: **nada de teoria nova**.
Vamos JOGAR para fixar o que voce ja aprendeu!

---

## O que Vamos Fazer Hoje

### Portaria Quest — O Jogo do Mapeamento

Um jogo interativo com 4 fases, cada uma praticando um conceito
do ebook de forma leve e divertida:

**Fase 1 — Jogo da Memoria**
Encontre os pares: conceitos SQL com seus equivalentes Python.
Ex: "TEXT NOT NULL" casa com "str"

**Fase 2 — Tradutor de Tipos**
Escolha a traducao Python correta para cada tipo SQL.
Cronometro amigavel — sem pressa!

**Fase 3 — Monte a Classe**
Dado um CREATE TABLE real do nosso projeto, ordene os campos
na classe Python corretamente (obrigatorios primeiro!).

**Fase 4 — Quiz do Porteiro**
Perguntas sobre os conceitos do ebook. Cada acerto e uma
"entrada autorizada" no condominio!

---

## Os 5 Conceitos que o Jogo Reforça

Estes sao os mesmos 5 pontos do ebook — a "mochila" que voce
precisa carregar:

1. **Cada tabela vira uma classe** — nome com letra maiuscula
2. **Cada coluna vira um atributo** — com tipo declarado
3. **Use @dataclass** — a etiqueta magica que faz o trabalho chato
4. **Campos NULL viram Optional** — Optional[tipo] = None
5. **Obrigatorios vem primeiro** — depois os opcionais

---

## Como Jogar

1. Abra o arquivo `exercicio/portaria-quest.html` no navegador
2. Clique em "Iniciar Jogo"
3. Complete as 4 fases no seu ritmo
4. Ao final, veja sua pontuacao e as conquistas desbloqueadas

**Dica:** Nao precisa acertar tudo de primeira! O jogo permite
tentar novamente quantas vezes quiser. O objetivo e APRENDER,
nao competir.

---

## Estrutura da Aula

```
aula-03/
    README.md                           <-- Este arquivo
    material-complementar.md            <-- Dicas e resumo do ebook
    exercicio/
        portaria-quest.html             <-- O JOGO! Abra no navegador
        INSTRUCOES.md                   <-- Como jogar (passo a passo)
```

---

## Dicas para Aproveitar

1. **Jogue com calma.** Nao tem cronometro apertado. Va no seu ritmo.
2. **Erre sem medo.** Cada erro mostra a resposta certa — e assim que se aprende!
3. **Se lembrar do ebook, otimo.** Se nao lembrar, o jogo ensina de novo.
4. **Divirta-se!** Programar pode (e deve!) ser divertido.

---

## Ao Final da Aula

Voce vai conseguir:

- [ ] Associar tipos SQL com tipos Python sem consultar tabela
- [ ] Saber a ordem dos campos em um @dataclass (obrigatorios primeiro)
- [ ] Reconhecer quando usar Optional e quando nao
- [ ] Olhar um CREATE TABLE e "enxergar" a classe Python
- [ ] Se sentir mais confiante para criar models sozinho!

---

## Proximos Passos

Na **Aula 04**, vamos colocar a mao no codigo de verdade: construir
models novos no projeto usando tudo que praticamos hoje.
Voce vai ver que, depois do jogo, tudo faz muito mais sentido!

Vamos jogar?