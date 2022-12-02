# Tokenizer (Lexical Analyzer), Parser (Syntax Analyzer), and Executor for Self-Defined Python-esque EBNF



## You do NOT have permission to use this code OR EBNF for any schoolwork purposes under any circumstances. 

## You do NOT have permission to use this code OR EBNF for any commercial purposes without speaking to me to work out a deal.


This project tokenizes, parses, and executes code written in accordance with the below EBNF.

This project uses Python from the command line, and uses the treelib and graphviz libraries, which can be downloaded using pip. 

### To execute on Windows:

1) open command prompt
2) cd over to the folder where the files and test file are located
3) run the command "python lexicalAnalyzerPyV21.py XXX.xxx"

XXX.xxx should be a file written in the grammar of the following EBNF (this is essentially limited Python with endif, endwhile, and enddef statements, rather than indentation):

### EBNF:

#### OPERATOR PRECEDENCE / ASSIGNMENTS (EBNF):

\<assign\> --\> \<id\> (= | += | -= | *= | /= | %= | //= | ^= | **= | \<\<= | \>\>=) \<expr\> \n

\<expr\> --\> \<term\> {or \<term\>}

\<term\> --\> \<factor\> {and \<factor\>}

\<factor\> --\> [not] \<factor2\>

\<factor2\> --\> \<factor3\> {(== | \<= | \>= | != | \> | \< | is | is not | in | not in) \<factor3\>}

\<factor3\> --\> \<factor4\> {| \<factor4\>}

\<factor4\> --\> \<factor5\> {^ \<factor5\>}

\<factor5\> --\> \<factor6\> {& \<factor6\>}

\<factor6\> --\> \<factor7\> {(\<\< | \>\>) \<factor7\>}

\<factor7\> --\> \<factor8\> {(+ | -) \<factor8\>}

\<factor8\> --\> \<factor9\> {(* | / | // | %) \<factor9\>}

\<factor9\> --\> \<factor10\> {(+x | -x | ~x) \<factor10\>}

\<factor10\> --\> \<factor11\> {** \<factor11\>}

\<factor11\> --\> ( \<expr\> ) | \<parameter\>


#### Possible Method Parameters:

\<parameter\> --\> \<id\> |  \<int_literal\> | \<float\> | \<string_literal\> | \<boolean\>   


#### Method call:

\<method\> --\> \<method_id\>([\<parameter\> {, \<parameter\>}]) \n


#### WHILE (EBNF) WITH ENDWHILE: #only allowing no parentheses () \<expr\>

\<while\> --\> while \<expr\>: \n \<statement\> {\<statement\>} endwhile \n



#### Statement: 

\<statement\> --\> \<assign\> | \<if_statement\> | \<method\> | \<while\>

 
#### EBNF IF WITH ENDIF: 

\<if_statement\> --\> if \<expr\>: \n \<statement\> {\<statement\>} {elif \<expr\>: \n \<statement\>  {\<statement\>}} [else:\n \<statement\> {\<statement\>}] endif \n


#### Function definition EBNF:

\<define\> --\> def \<method_id\> ([\<id\> {, \<id\>}]): \n \<statement\> {\<statement\>} enddef \n


#### Nonterminal Resolutions:

\<id\> --\> IDENTIFIER

\<int_literal\> --\> INT_LITERAL

\<float\> --\> FLOAT

\<method_id\> --\> METHOD_IDENTIFIER

##### String Literal:

Only allow strings with double quotes: “ “, not ‘ ‘ or “”” “””, etc, for simplicity.

\<string_literal\> --\> “{STRING_LITERAL}”

##### Boolean:

\<boolean\> --\> True | False

### Small sample output for the command "works = True":

![image](https://user-images.githubusercontent.com/33675444/205215337-568235f7-ebfe-406c-b834-5100f7bc0f78.png)

### Larger Output:

#### Test file being analyzed:
[pythontest2.txt](https://github.com/aidan-le-beard/Syntax-Lexical-Analyzer-and-Executor-for-Self-Defined-Python-esque-EBNF/files/10095255/pythontest2.txt)

#### Parse tree of above sample file:
[Source.gv.pdf](https://github.com/aidan-le-beard/Syntax-Lexical-Analyzer-and-Executor-for-Self-Defined-Python-esque-EBNF/files/10095240/Source.gv.pdf)

#### Final command line output of above sample file:
![image](https://user-images.githubusercontent.com/33675444/205215675-6d7f16a8-fb2d-4afd-b029-21a39a2037e4.png)
