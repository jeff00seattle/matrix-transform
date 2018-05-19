# matrix-transform
DocuSign's Coding Challenge

**Version Friday, 2018 May 18, 17:30 PST**

## Requirements:

+ Write a method or function in your programming language of choice.
+ It MUST accept a two-dimensional matrix of characters and a "search" character.
+ Wherever the "search" character is found, the entire row and column MUST be replaced with that character.
+ Method/function MUST transform its input, not return a new matrix.
+ Method/function MUST NOT produce any other output (e.g. returns, printing to STDOUT)
+ Method/function SHOULD strive for optimal performance. There is a solution with O(n*m) run time and O(C) additional memory, assuming a rectangular matrix with n rows and m columns.

Sample input matrix:

```
A M X C V
B R C K N
F J L O P
D S K Z Q
```

Input matrix after transformation (searching for 'C'):

```
C C C C C
C C C C C
F J C C P
D S C C Q
```

## Implementation

The following code is writtine Python 3.5.4

```bash
$ python3 --version
Python 3.5.4
```

Created two classes:

+ ```class MatrixTransformA``` -- Transform rows and columns based upon matching target character.
+ ```class JaggedMatrixGenerator``` -- Generate a Jagged Matrix and fill it with random characters as defined by available string sequences.

## Operation

### Usage

```bash
$ python3 matrix_transform_A.py --help

Usage: matrix_transform_A.py
        [-v | --verbose]
        [-h | --help]
        --matrix string
        --target string
        --case-insensitive
        --sequence ['ascii_letters', 'ascii_lowercase', 'ascii_uppercase', 'digits', 'hexdigits', 'octdigits', 'printable', 'punctuation', 'whitespace']
    --matrix: Strigified 2-D Jagged Array, If not provided then random is generated.
    --target: Target matrix transformation with specific character [Required]
    --case-insensitive: Be case-insensitive when targeting specific character, Default: False
    --sequence: If random matrix is generated this uses this sequence, Default: 'ascii_uppercase'
```

### Example

#### Generate randomly-filled Jagged Matrix with ASCII Upper-case Characters, Target 'C' with case-sensitivity.

```bash
$ python3 matrix_transform_A.py \
  --target 'C'

2018-05-18 17:22:32,357 MatrixTransformation INFO     Original JaggedMatrixGenerator:

0 : ['Z', 'J', 'A', 'H', 'X']
1 : ['F', 'K', 'A', 'D']
2 : ['N', 'S', 'Y', 'W', 'N', 'P', 'G']
3 : ['Q', 'S', 'S', 'P', 'V', 'J']
4 : ['C', 'X', 'H', 'M', 'E', 'V']
5 : ['G', 'U', 'Q', 'U', 'N', 'I']
6 : ['Q', 'X', 'V', 'O', 'Z']


2018-05-18 17:22:32,358 MatrixTransformation INFO     rows:    7: [False, False, False, False, True, False, False]
2018-05-18 17:22:32,359 MatrixTransformation INFO     columns: 7: [True, False, False, False, False, False, False]
2018-05-18 17:22:32,359 MatrixTransformation INFO     Transformed JaggedMatrixGenerator:

0 : ['C', 'J', 'A', 'H', 'X']
1 : ['C', 'K', 'A', 'D']
2 : ['C', 'S', 'Y', 'W', 'N', 'P', 'G']
3 : ['C', 'S', 'S', 'P', 'V', 'J']
4 : ['C', 'C', 'C', 'C', 'C', 'C']
5 : ['C', 'U', 'Q', 'U', 'N', 'I']
6 : ['C', 'X', 'V', 'O', 'Z']
```

#### Generate randomly-filled Jagged Matrix with ASCII Characters (both Upper-case and Lower-case), Target 'C' with case-sensitivity.

```bash
$ python3 matrix_transform_A.py \
  --target 'C' \
  --sequence ascii_letters

2018-05-18 17:23:25,761 MatrixTransformation INFO     Original JaggedMatrixGenerator:

0 : ['K', 't', 'H', 'y']
1 : ['O', 'r', 'R', 'c', 'h']
2 : ['k', 'q', 'I', 'y', 'n', 'z', 'o', 'D']
3 : ['M', 'J', 'A', 'W', 'y']
4 : ['m', 'O', 'o', 'n', 'D', 'Z', 'c', 'g']
5 : ['E', 'f', 'h', 'C', 'd', 'C', 'w']
6 : ['I', 'x', 'p', 'Y', 'H', 'J']


2018-05-18 17:23:25,761 MatrixTransformation INFO     rows:    7: [False, False, False, False, False, True, False]
2018-05-18 17:23:25,762 MatrixTransformation INFO     columns: 8: [False, False, False, True, False, True, False, False]
2018-05-18 17:23:25,762 MatrixTransformation INFO     Transformed JaggedMatrixGenerator:

0 : ['K', 't', 'H', 'C']
1 : ['O', 'r', 'R', 'C', 'h']
2 : ['k', 'q', 'I', 'C', 'n', 'C', 'o', 'D']
3 : ['M', 'J', 'A', 'C', 'y']
4 : ['m', 'O', 'o', 'C', 'D', 'C', 'c', 'g']
5 : ['C', 'C', 'C', 'C', 'C', 'C', 'C']
6 : ['I', 'x', 'p', 'C', 'H', 'C']
```

#### Generate randomly-filled Jagged Matrix with ASCII Characters (both Upper-case and Lower-case), Target 'C' without case-sensitivity.

```bash
$ python3 matrix_transform_A.py \
  --target 'C' \
  --sequence ascii_letters \
  --case-insensitive

2018-05-18 17:24:48,465 MatrixTransformation INFO     Original JaggedMatrixGenerator:

0 : ['z', 'I', 'f', 'd']
1 : ['G', 'g', 'q', 'u', 'i', 'e']
2 : ['u', 'A', 'u', 'W', 'l', 'm']
3 : ['y', 'h', 'a', 'k', 'g', 'l']
4 : ['d', 'Y', 'b', 'c', 's']
5 : ['b', 'q', 'E', 'u', 'i']
6 : ['R', 'z', 'p', 'J', 'I', 'B']
7 : ['K', 'V', 'J', 'c', 'm']


2018-05-18 17:24:48,465 MatrixTransformation INFO     rows:    8: [False, False, False, False, True, False, False, True]
2018-05-18 17:24:48,465 MatrixTransformation INFO     columns: 6: [False, False, False, True, False, False]
2018-05-18 17:24:48,466 MatrixTransformation INFO     Transformed JaggedMatrixGenerator:

0 : ['z', 'I', 'f', 'C']
1 : ['G', 'g', 'q', 'C', 'i', 'e']
2 : ['u', 'A', 'u', 'C', 'l', 'm']
3 : ['y', 'h', 'a', 'C', 'g', 'l']
4 : ['C', 'C', 'C', 'C', 'C']
5 : ['b', 'q', 'E', 'C', 'i']
6 : ['R', 'z', 'p', 'C', 'I', 'B']
7 : ['C', 'C', 'C', 'C', 'C']
```
