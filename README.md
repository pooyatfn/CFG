# CFG Simplifier

## Introduction
In formal language theory, a **context-free grammar (CFG)** is a set of recursive rules used to generate patterns of strings. CFGs can describe a wide range of languages, including regular languages. However, some productions in CFGs may be redundant or unnecessary. Simplifying CFGs involves removing these extraneous elements while preserving the language they generate.

## Key Concepts

### 1. Context-Free Grammar (CFG)
- A CFG consists of:
  - **Terminal symbols**: Basic elements (e.g., letters, digits).
  - **Nonterminal symbols**: Variables representing language constructs.
  - **Production rules**: Specify how nonterminals can be replaced by other symbols.
  - **Start symbol**: The initial nonterminal from which we derive strings.

### 2. Simplification Steps

#### a. Removal of Null Productions
- **Null productions**: Productions of the form `A → ε` (where ε represents an empty string).
- Find nullable variables (variables that can derive ε).
- Construct a new grammar by adding all combinations of productions with nullable variables replaced by ε.
- Remove all original ε-productions except for the start symbol.

#### b. Removal of Unit Productions
- **Unit productions**: Productions of the form `A → B`, where `A` and `B` are nonterminals.
- Procedure:
  1. Replace `A → B` with `A → x` whenever `B → x` occurs in the grammar (where `x` can be a terminal or empty).
  2. Delete the original `A → B` production.
  3. Repeat until all unit productions are removed.

#### c. Removal of Useless Productions
- **Useless productions**: Productions that cannot participate in deriving any valid string.
- Identify and remove:
  - Nonterminals that never lead to terminal strings.
  - Productions involving these nonterminals.

## Example CFG
Consider the following CFG:
```
S → ABaC
A → BC
B → b | ε
C → D | ε
D → d
```

### Simplification Steps
1. **Null Productions**:
   - Remove `B | C → ε`.
   - add all states to which variable derives B or C to.
   - Modified grammar:
     ```
     S → ABaC |Aa | aC | Ba | AaC | BaC | a | ABa
     A → C | B | BC
     B → b
     C → D
     D → d
     ```

2. **Unit Productions**:
   - Remove `A → B`, `A → C`, and `C → D`.
   - Add `A → d | b` and `C → d`(since `B → b`, `C → D` and `D → d`).
   - Modified grammar:
     ```
     S → ABaC | Aa | aC | Ba | AaC | BaC | a | ABa
     A → d | BC | b
     B → b
     C → d
     D → d
     ```

3. **Useless Productions**:
   - Remove `D → d` (unreachable production).
   - Final grammar:
     ```
     S → ABaC | Aa | aC | Ba | AaC | BaC | a | ABa
     A → d | BC | b
     B → b
     C → d
     ```
