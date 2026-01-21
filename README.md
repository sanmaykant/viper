# Viper
Viper is a lightweight, custom interpreted programming language implemented in Python. It features a rich tokenization system supporting literals, arithmetic operations, comparisons, assignments, logical operators, keywords, punctuators, separators, and identifiers.

# Language Features

Viper supports modern programming constructs including:
Control Flow Keywords:

- `if`, `elif`, `else` for conditional statements
- `for`, `while` for loops
- `return` for function returns

## Data Types (Literals):

- Numbers (NUM)
- Strings (STRING)
- Booleans (True/true/TRUE, False/false/FALSE)

## Identifiers:

- Function definitions (FUNCDEF)
- Function calls (FUNCCALL)
- Built-in functions (INBUILTFUNC)
- Variables (VARIABLE)
- Data types (DATATYPE)

## Separators and Punctuators

```
( ) [ ] { } , ; .
```

## Token Families

```
LITERAL        (NUM, STRING, BOOL)
ARITHMETICOP   (+, -, *, /, **)
COMPOP         (<, >, <=, >=, ==, !=)
ASSIGNOP       (=, +=, -=, *=, /=, ^=)
LOGICALOP      (and, or, not)
KEYWORD        (if, for, while, return)
PUNCTUATOR     (;, .)
IDENTIFIER     (variables, functions)
SEPARATOR      ((), [], {}, ,)
```

# Getting started

```bash
git clone https://github.com/sanmaykant/viper.git
cd viper

python main.py your_program.vip
```

# Sample code

```
num factorial(num n) {
      if (n == 1) { return n }
      else { return n * factorial( n - 1 ) }
}

num sum(num n1, num n2) return n1 + n2

print('Hello world!')

num num1 = inputNum('Enter first number: ')
num num2 = inputNum('Enter first number: ')

print(factorial(sum(num1, num2)))
inputExpr()
```
