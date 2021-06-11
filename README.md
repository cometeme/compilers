# compilers 编译原理 - 简单类 C 编译器

本项目实现了一个简单的类 C 编译器，能够分析简单类 C 语言风格的程序代码。如声明语句、赋值语句、表达式、if while 控制语句等，进行语法分析并生成相应的中间代码（三地址代码）。

提供了一个命令行交互程序，可以输出词法分析、语法分析、语义分析及中间代码生成过程中的各种表格以及数据集合。

输入文法文件可以根据需要进行修改，同时也可以添加自定义的语义动作，从而能够让程序分析不同的语言。

## 运行说明

运行说明（**需要确保 python 版本为 3.7**）：

1. 进入项目文件夹

（初次使用需要创建一个空的 output 目录）

2. 安装 rich 库（若没有安装）

```shell
pip install rich
```

3. 运行`main.py`程序

```shell
python main.py
```

### 操作说明

运行`main.py`后，命令行中会生成引导菜单（如下所示）：

```shell
---------------------------------------------------
Enter a number to show detail, or enter 'q' to quit

0 - Grammar
1 - Input Code
2 - Scanner States
3 - SLR States
4 - Token Table
5 - Symbol Table
6 - First Set
7 - Follow Set
8 - Closure Set
9 - SLR Table (Action/Goto Table)
10 - Output Code
---------------------------------------------------
```

下面对各个选项进行说明：

| 选项 |                        功能                        |
| :--: | :------------------------------------------------: |
|  0   |                   输出给定的文法                   |
|  1   |                 输出给定的程序输入                 |
|  2   |                 输出词法分析的结果                 |
|  3   | 输出SLR语法分析过程（包含分析栈以及移入/归约动作） |
|  4   |                   输出 Token 串表                    |
|  5   |                     输出符号表                     |
|  6   |                   输出 First 集合                    |
|  7   |                   输出 Follow 集合                   |
|  8   |                     输出项集族                     |
|  9   |        输出 SLR 分析表（包括 action 和 goto 表）         |
|  10  |                 输出生成的中间代码                 |
|  q   |                      退出程序                      |


## 工程文件说明

项目整体目录结构如下：

```shell
.
├── Grammar.py
├── SLR_Automata.py
├── SLR_Table.py
├── Scanner.py
├── Symbol_Table.py
├── Token.py
├── action_table.json
├── format.sh
├── goto_table.json
├── input
│   ├── grammar.txt
│   ├── grammar_assign.txt
│   ├── grammar_control.txt
│   ├── grammar_define.txt
│   ├── grammar_expression.txt
│   ├── grammar_raw.txt
│   ├── input.txt
│   ├── input_assign.txt
│   ├── input_control.txt
│   ├── input_define.txt
│   ├── input_expression.txt
│   ├── input_raw.txt
│   └── input_scanner.txt
├── main.py
├── output
│   ├── closure_set.txt
│   ├── code.csv
│   ├── first_set.txt
│   ├── follow_set.txt
│   ├── grammar.txt
│   ├── scanner_states.csv
│   ├── slr_states.csv
│   ├── slr_table.csv
│   ├── symbol_table.csv
│   └── token_table.csv
├── test_grammar.py
└── test_scanner.py
```

### 语法文件

|  文件/文件夹  |                        说明                        |
| :-----------: | :------------------------------------------------: |
| input 文件夹  |           程序输入（文法、待分析的程序）           |
| output 文件夹 | 词法、语法、中间代码生成时产生的所有集合以及表结构 |



### 词法分析相关

|   文件/文件夹   |       说明       |
| :-------------: | :--------------: |
|   Scanner.py    | 词法分析器的实现 |
| test_scanner.py |  词法分析器测试  |
|    Token.py     |    Token 相关     |
| Symbol_Table.py |    符号表相关    |

### 语法分析/中间代码生成相关

|   文件/文件夹   |                        说明                        |
| :-------------: | :------------------------------------------------: |
|  SLR_Table.py   |           SLR 语法分析表以及辅助函数生成            |
| SLR_Automata.py | SLR 语法分析的实现 + 中间代码生成部分语义动作的实现 |
|   Grammar.py    |                  语法分析总控程序                  |
| test_grammar.py |                   语法分析器测试                   |

### 主控函数

| 文件/文件夹 |        说明        |
| :---------: | :----------------: |
|   main.py   | 程序入口与控制逻辑 |
