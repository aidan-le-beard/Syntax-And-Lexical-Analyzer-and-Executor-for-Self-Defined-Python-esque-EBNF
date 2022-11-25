# Syntax-Lexical-Analyzer-and-Executor-for-Self-Defined-Python-esque-EBNF



# You do NOT have permission to use this code for any schoolwork purposes under any circumstances. You do NOT have permission to use this code for any commercial purposes without speaking to me to work out a deal.



This project uses Python from the command line, and uses the treelib and graphviz libraries, which can be downloaded using pip.

To run the project:

1) open command prompt
2) cd over to the folder where the files and test file are located
3) run the command "python lexicalAnalyzerPyV21.py XXX.py"

XXX.py should be a file written in the grammar of the following EBNF (this is essentially limited Python with endif, endwhile, and enddef statements, rather than indentation):

OPERATOR PRECEDENCE / ASSIGNMENTS (EBNF):

\<assign\> --\> \<id\> (= | += | -= | *= | /= | %= | //= | ^= | \*\*= | <<= | >>=) \<expr\> \n

\<expr\> --\> \<term\> {or \<term\>}

\<term\> --\> \<factor\> {and \<factor\>}

\<factor\> --\> [not] \<factor2\>

\<factor2\> --\> \<factor3\> {(== | \<= | \>= | != | \> | \< | is | is not | in | not in) \<factor3\>}

\<factor3\> --\> \<factor4\> { \<factor4\>}

\<factor4\> --\> \<factor5\> {^ \<factor5\>}

\<factor5\> --\> \<factor6\> {& \<factor6\>}

\<factor6\> --\> \<factor7\> {(\<\< | \>\>) \<factor7\>}

\<factor7\> --\> \<factor8\> {(+ | -) \<factor8\>}

\<factor8\> --\> \<factor9\> {(* | / | // | %) \<factor9\>}

\<factor9\> --\> \<factor10\> {(+x | -x | ~x) \<factor10\>}

\<factor10\> --\> \<factor11\> {** \<factor11\>}

\<factor11\> --\> ( \<expr\> ) | \<parameter\>


Possible Method Parameters:

\<parameter\> --\> \<id\> |  \<int_literal\> | \<FLOAT\> | \<string_literal\> | \<boolean\>   


Method call:

\<method\> --\> \<method_id\>([\<parameter\> {, \<parameter\>}]) \n


WHILE (EBNF) WITH ENDWHILE: #only allowing no parentheses () \<expr\>

\<while\> --\> while \<expr\>: \n \<statement\> \n {\<statement\> \n}  endwhile \n



Statement: 

\<statement\> --\> \<assign\> | \<if_statement\> | \<method\> | \<while\>

 
EBNF IF WITH ENDIF: 

\<if_statement\> --\> if \<expr\>: \n \<statement\> {\<statement\>} {elif \<expr\>: \n \<statement\>  {\<statement\>)} [else:\n \<statement\> {\<statement\>}] endif \n


Function definition EBNF:

\<define\> --\> def \<method_id\> ([\<id\> {, \<id\>}]): \n \<statement\> \n {\<statement\> \n} enddef \n


Nonterminal Resolutions:

\<id\> --\> IDENTIFIER

\<int_literal\> --\> INT_LITERAL

\<float\> --\> FLOAT

\<method_id\> --\> METHOD_IDENTIFIER

String Literal:

Only allow strings with double quotes: “ “, not ‘ ‘ or “”” “””, etc, for simplicity.

\<string_literal\> --\> “STRING_LITERAL {STRING_LITERAL}”

Boolean:

\<boolean\> --\> True | False
