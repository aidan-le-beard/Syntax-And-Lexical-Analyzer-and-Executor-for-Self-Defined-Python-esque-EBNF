from treelib import Tree # using treelib library to create a tree
from graphviz import Source # graphviz creates the parse tree visualization

def execution(parseTreePassed):
    global parseTree
    parseTree = parseTreePassed
    
    print("\nBegin Execution:\n\nParse tree visualization using treelib library:\n")
    
    # Display the created parseTree
    parseTree.show()
    
    # Convert the treelib parseTree to graphViz format for prettier printing:  
    # treelib's provided to_graphviz() method doesn't maintain node order, so I'll do it myself with this method
    # scalable pre-order traversal
    digraph = 'digraph tree {\n'
    # for node in pre-order traversal order (treelib uses pre-order for DEPTH search)
    for node in parseTree.expand_tree(mode=Tree.DEPTH, sorting=False):
        tag = parseTree[node].tag
        # graphViz generates an error: """ if the lexeme is '"', so make it '\"'
        if tag == '"':
            tag = '\\"'
        # this many backslashes gets graphviz to display '\n' correctly for some reason
        if tag == '\\n':
            tag = '\\\\n'
        digraph += '"' + str(node) + '" [label="' + tag + '", shape=circle]\n'
        # don't add a parent/child relationship for the root, as it has no parent
        if str(parseTree.ancestor(node)) != 'None':
            digraph += '"' + str(parseTree.ancestor(node)) + '" -> "' + node + '"\n'
    digraph += " }"
    print("Graphviz tree:\n\n" + digraph)
    
    # create and open an image using graphViz and our graphviz tree visualization we've created:
    visualizeDigraph = Source(digraph)
    visualizeDigraph.view()

    # iterate through our parse tree and create an executable object
    executableCode = ''
    # i = 0 # for old unscalable pre-order traversal
    indent = '    '
    indents = 0
    global lastLexeme
    lastLexeme = '' # keep track of newlines for indents
    # scalable pre-order traversal of parseTree (treelib uses pre-order for DEPTH-first search)
    for node in parseTree.expand_tree(mode=Tree.DEPTH, sorting=False):
        # don't include multiple newlines in a row
        if lastLexeme == '\n' and parseTree[node].tag == '\\n':
            continue
        
        # for executable code don't include 'Start', '<>' tags, or enddef/endif/endwhile
        # we want to allow '<' though, so allow it if its length == 1
        if (parseTree[node].tag[0] == '<' and len(parseTree[node].tag) == 1) or (parseTree[node].tag != 'Start' and parseTree[node].tag[0] != '<' and parseTree[node].tag != 'enddef' and parseTree[node].tag != 'endif' and parseTree[node].tag != 'endwhile' and parseTree[node].tag != 'EOF'):
            if parseTree[node].tag == 'elif' or parseTree[node].tag == 'else':
                indents -= 1
            
            j = 0
            while j < indents:
                if lastLexeme == '\n':
                    executableCode += indent
                j += 1
                
            # we previously changed our NEWLINE lexeme to \\n for printing, 
            # change it back to \n for executing code
            if parseTree[node].tag == '\\n':
                executableCode += '\n'
                lastLexeme = '\n'
            else:
                executableCode += parseTree[node].tag + ' '
                lastLexeme = parseTree[node].tag
                
            if parseTree[node].tag == 'if' or parseTree[node].tag == 'elif' or parseTree[node].tag == 'else' or parseTree[node].tag == 'def' or parseTree[node].tag == 'while':
                indents += 1
        if parseTree[node].tag == 'endif' or parseTree[node].tag == 'endwhile' or parseTree[node].tag == 'enddef':  
            indents -= 1
    
    # print our Code that has been tokenized, parsed for errors, and now read from a 
    # Parse Tree to a string using a pre-order traversal
    print("\nTokenized, parsed, error checked, and tree iterated/re-formatted executable code:\n\n" + executableCode)
    print("Result of compiling and executing the code:\n")
    
    # execute our code. exec() seems to change the scope (exec is inside of a function, while
    # our test file is not?), so passing globals(), globals() enables the code to run correctly
    exec(compile(executableCode, '', 'exec'), globals(), globals()) 