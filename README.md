# Linguagem de Programação Criptografada por Cifra de César

Este repositório contém a minha própria linguagem de programação, criada como um projeto da disciplina Lógica da Computação do Insper, no curso de Engenharia de Computação.

Escolhi fazer uma linguagem inspirada no C, uma vez que construí um compilador para a linguagem, facilitando assim a transposição para essa nova linguagem. Porém, em minha linguagem, todos os tokens são criptografados em Cifra de César, um método muito simples e antigo de criptografia.

---

Para saber mais:

- [Apresentação em PDF](https://github.com/williamars/my-programming-language/blob/main/presentation/presentation.pdf)

O compilador utilizado foi baseado em um construído para a linguagem C, feito por mim mesmo como outra implementação da matéria Lógica da Computação [1]: 
- [Compilador](https://github.com/williamars/my-programming-language/blob/main/compiler-discipline/main-compiler.py)


---

# Criptografia de César
- É uma técnica de criptografia bem simples, na qual cada letra é substituída por outra. Por exemplo, caso o A seja substituído por G, o B seria pelo H, C pelo I, e assim por diante.
- Nome porque Júlio César, um político romano, utilizava essa estratégia para se
comunicar com seus militares

## Inspiração
- Conexão de aprendizados: Tecnologias Hacker e Lógica da Computação, duas disciplinas do Insper


## Etapas de Construção
- EBNF
- Flex e Bison
- Compilador

## Teste

```cmd
git clone https://github.com/williamars/my-programming-language
cd my-programming-language
python main.py example/example-01.cr
```

Os comandos acima testarão com o exemplo `example-01.cr`, porém pode-se colocar qualquer arquivo que quiser programado corretamente na linguagem!

## Referências

[1] https://github.com/williamars/compilador-logica-computacao

[2] https://marciapsilva.github.io/cifra-de-cesar/