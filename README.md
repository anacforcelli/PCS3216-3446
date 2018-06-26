# Sistemas de Programação - PCS3216
## Projeto 2018

Daniel Nery Silva de Oliveira - 9349051

Professor João José Neto

27/06/2018

-------------

## Introdução

Esse projeto tem como objetivo a concepção, projeto, desenvolvimento e
implementação de um pequeno sistema para o desenvolvimento de programas em
linguagem simbólica absoluta, especificada a seguir e de uma Máquina Virtual
para interpretação desses programas.

A Máquina Virtual e os outros programas de alto nível foram desenvolvidos na
linguagem python.

## Especificação da Máquina Virtual

A Máquina Virtual consiste em 16 (0x0 a 0xF) bancos de 4096 bytes cada (0x000 a 0xFFF), além de um contador de instruções de 2 bytes, que contém o endereço da instrução atual; um registrador de instrução de 2 bytes, que contém a instrução atual e um acumulador de 1 byte, a disposição do programador. Tudo é inicilizado em 0.

```py
## FILE: system/VM.py 45:50
self.main_memory = [[c_uint8(0) for i in range(bank_size)] for j in range(banks)]
self._ri = c_uint16(0) # Registrador de Instrução
self._ci = c_uint16(0) # Contador de Instruções
self._acc = c_int8(0)  # Acumulador

self._cb = c_uint8(0)  # Banco atual
```

### Linguagem Simbólica

A Máquina Virtual foi projetada para entender uma linguagem de comandos
específica, em assembly, com os seguintes mnemônicos possíveis:

* `JP /xxx` - Salto Incondicional - salta incondicionalmente para o endereço xxx (em hexadecimal) no banco de memória atual

* `JZ /xxx` - Salto se Zero - salta para o endereço xxx (em hexadecimal) no banco de memória atual somente se o conteúdo do acumulador for 0x00

* `JN /xxx` - Salto se Negativo - salta para o endereço xxx (em hexadecimal) no banco de memória atual somente se o conteúdo do acumulador for negativo (0x80 a 0xFF)

* `CN /x  ` - Controle - o nibble x define o código da operação de controle:
    * `x = 0` - Halt Machine - Espera por interrupção externa (nesse caso, uma interrupção de teclado causada pelo pressionamento de ctrl e C)
    * `x = 2` - Indirect - Ativa o modo de endereçamento indireto
    * Outras instruções não foram implementadas e serão ignoradas

* `+  /xxx` - Soma - soma o conteúdo presente no endereço de memória xxx (em hexadecimal) do banco de memória atual no acumulador

* `-  /xxx` - Subtração - subtrai o conteúdo presente no endereço de memória xxx (em hexadecimal) do banco de memória atual do acumulador

* `*  /xxx` - Multiplicação - multiplica o conteúdo presente no endereço de memória xxx (em hexadecimal) do banco de memória atual com acumulador, salva o resultado no acumulador

* `/  /xxx` - Divisão - divide o conteúdo presente no acumulador com o do endereço de memória xxx (em hexadecimal) do banco de memória atual, salva o resultado no acumulador

* `LD /xxx` - Carregar da Memória - copia o conteúdo da memória do endereço xxx (em hexadecimal) do banco de memória atual para o acumulador

* `MM /xxx` - Mover para a Mamória - copia o conteúdo do acumulador para o endereço xxx (em hexadecimal) do banco de memória atual

* `SC /xxx` - Chamada de Subrotina - salva o conteúdo atual do contador de instruções em xxx e xxx+1 e desvia para xxx+2

* `OS /x  ` - Chamada de Sistema Operacional - o nibble x define a chamada:
    * `x = /0` - Mostra o estado atual (acumulador e contador de instruções) da Máquina Virtual na tela.
    * `x = /F` - Devolve o controle para o Interpretador de Comandos, encerrando a execução do programa
    * Outras instruções não foram implementadas e serão ignoradas

* `IO /x  ` - Entrada/Saída

Além disso, também é possível utilizar as seguintes pseudoinstruções:

* `@ /yxxx` - Endereço inicial do código seguinte - indica que as instruções a seguir devem ser guardas no banco y, a partir do endereço xxx

* `# /yxxx` - Fim do código e endereço inicial de execução - indica que o código a ser montado acabou e que ele deve ser executado a partir do endereço xxx do banco y

* `$ /xxx ` - Reserva de área de memória - reserva bytes de memória vazios

* `K /xx  ` - Preenche memória com byte constante - preenche a memória naquela posição com o byte xx

### Formato do Arquivo Objeto

## Programas de Alto Nível
### Interface de Linha de Comando

Todo o sistema pode ser iniciado executando o script `main.py` presente na raiz desse projeto (como com `python main.py` - Python 3 necessário). Ao executá-lo o interpretador de comandos será inicializado e o login será necessário:

> Pela primeira vez é necessário instalar os pacotes adicionais do python, com
> `pip install -r requirements.txt`

```
Welcome! (l)ogin or (r)egister
login >> _
```

Basta digitar `l` ou `login` para fazer o login ou `r` | `register` para registrar um novo usuário, o usuário 'user' com a senha 'user' já está criado. Usuários e suas senhas são guardados no arquivo `system/passwd`, com as senhas criptografadas.

Após o login, será exibido `[usuario] [pasta atual] >>` e comandos podem ser executados

```
Welcome! (l)ogin or (r)egister
login >> l
User: user
Password: ****
user users/user >> _
```

Os comandos possiveis são:

* `$DIR`: Mostra os arquivos na pasta
* `$RUN`: Executa um arquivo OBJ
* `$ASM`: Monta um arquivo ASM
* `$DEL`: Marca um arquivo para remoção
* `$LOGOUT`: Volta para o login
* `$END`: Encerra o interpretador

> É possível mostrar outputs de debug de todos os programas inicializando o sistema
> com a flag -d: `python main.py -d`

### Montador

O montador pode ser chamado com o comando `$ASM <nome_do_arquivo.asm>`, ele gera o
código objeto do arquivo asm, além de um arquivo de lista e um arquivo com a tabela de
labels, para que possam ser consultados.

Exemplo:

* Arquivo original: `teste.asm`
* Lista: `teste.lst`
* Labels: `teste.asm.labels`
* Objeto: `teste.obj.X`, x vai de 0 ao numero de arquivos objetos necessários, esse arquivo está codificado em ASCII e pode ser lido, também é criado `teste.obj.bin.X`, para ser usado pelo loader.

```
user users\user >> $DIR
teste.asm

user users\user >> $ASM teste.asm

user users\user >> $DIR
teste.asm
teste.asm.labels
teste.lst
teste.obj.0
teste.obj.1
teste.obj.2
teste.obj.bin.0
teste.obj.bin.1
teste.obj.bin.2

user users\user >>
```

### Máquina Virtual

## Programas de Baixo Nível

Os programas a seguir já foram previamente implementados na linguagem
simbólica e transformados em código objeto absoluto e são carregados na
memória da máquina virtual assim que ela é inicializada, estando disponíveis
na interface de linha de comando.

### Loader

O loader foi escrito na própria linguagem simbólica especificada acima e montado pelo
assembler também especificado acima, seu código-fonte é o seguinte:

```arm
; loader.asm
        @   /0000
INIT    IO  /1        ; Get Data from device
        MM  IADDR     ; Save first byte of initial address
        IO  /1
        MM  IADDR+1   ; Save second byte of initial address
        IO  /1
        MM  SIZE      ; Save size

LOOP    IO  /1        ; Read byte from file
        CN  /2        ; Activate Indirect Mode
        MM  IADDR     ; Indirect move to current address

        LD  IADDR+1   ; Get current address
        +   ONE       ; Sum 1
        MM  IADDR+1   ; Put it back

        LD  SIZE      ; Get size
        -   ONE       ; Subtract 1
        MM  SIZE      ; Put it back

        JZ  END       ; Finish if size = 0
        JP  LOOP

END     OS  /F        ; End Program

IADDR   K   0
        K   0
SIZE    K   0
ONE     K   1
        # INIT
```

E esses são seu arquivos de lista e tabela de labels:

```
loader.lst LIST FILE
---------------------
ADDRESS   OBJECT    LINE   SOURCE
                       1   @ /0000
   0000       C1       2   INIT IO /1 ; Get Data from device
   0001     901E       3   MM IADDR ; Save first byte of initial address
   0003       C1       4   IO /1
   0004     901F       5   MM IADDR+1 ; Save second byte of initial address
   0006       C1       6   IO /1
   0007     9020       7   MM SIZE ; Save size
   0009       C1       9   LOOP IO /1 ; Read byte from file
   000A       32      10   CN /2 ; Activate Indirect Mode
   000B     901E      11   MM IADDR ; Indirect move to current address
   000D     801F      13   LD IADDR+1 ; Get current address
   000F     4021      14   + ONE ; Sum 1
   0011     901F      15   MM IADDR+1 ; Put it back
   0013     8020      17   LD SIZE ; Get size
   0015     5021      18   - ONE ; Subtract 1
   0017     9020      19   MM SIZE ; Put it back
   0019     101D      21   JZ END ; Finish if size = 0
   001B        9      22   JP LOOP
   001D       BF      24   END OS /F ; End Program
   001E        0      26   IADDR K 0
   001F        0      27   K 0
   0020        0      28   SIZE K 0
   0021        1      29   ONE K 1
                      30   # INIT
```


```
loader.asm.labels LABEL TABLE FILE
----------------------------------
LABEL           VALUE
INIT             0000
IADDR            001E
SIZE             0020
LOOP             0009
ONE              0021
END              001D
```

Para invocar o loader, basta rodar o comando `$RUN <nome_do_arquivo.obj> [step]`, não
se deve colocar os números .X após .obj, isso é tratado automaticamente pela VM e
todos eles serão carregados pelo loader.

> A opção `step` pode ser usada para executar uma instrução de cada vez, sendo necessário
> apertar enter para continuar, porém ela só útil se o debug estiver ativado

### Dumper

## Testes

## Diagramas

## Arquivos
