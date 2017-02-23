#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools

def tenner_csp_model_1(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 8.
       
       
       The input board is specified as a pair (n_grid, last_row). 
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid. 
       If a -1 is in the list it represents an empty cell. 
       Otherwise if a number between 0--9 is in the list then this represents a 
       pre-set board position. E.g., the board
    
       ---------------------  
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists
       
       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]
       
       
       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each 
       column.
    '''

    # initial CSP
    csp = CSP('tenner_csp')

    var_array = []

    n_grid = initial_tenner_board[0]
    last_row = initial_tenner_board[1]
    rows = len(n_grid)

    bin_tup = []
    for i in range(10):
        for j in range(10):
            if i != j:
                bin_tup += [(i, j)]

    for i in range(rows):
        var_array += [[]]
        for j in range(10):
            # check domain of cell i, j
            if n_grid[i][j] == -1:
                dom = list(range(10))
            else:
                dom = [n_grid[i][j]]

            # create variables
            var = Variable('v'+str(i)+str(j), dom)
            var_array[i] += [var]
            csp.add_var(var)

    # create binary constraints
    for i in range(rows):
        for j in range(10):
            # create constraints for neighbours of cell i,j that are >= i and one neighbour that is (i, j+1)
            print('---',i,j)
            for r in range(i, min(i+2, rows)):
                for c in range(max(0, j-1), 10):
                    if r == i and (c == j or c == j-1):
                        continue
                    if r == i:
                        scope = [var_array[i][j], var_array[r][c]]
                        print('ij', r, c)
                    elif r == i+1 and c > j+1:
                        break
                    else:
                        scope = [var_array[i][j], var_array[r][c]]
                        print('ij', r, c)

                    con = Constraint('c'+str(i)+str(j), scope)
                    con.add_satisfying_tuples(bin_tup)
                    csp.add_constraint(con)

    # create sum constraints
    for j in range(10):
        scope = []
        s = last_row[j]
        for i in range(rows):
            scope += [var_array[i][j]]
        con = Constraint('c'+str(j), scope)
        sum_tup = []
        for t in itertools.product(range(10), repeat=rows):
            if sum(t) == s:
                sum_tup += [t]

        con.add_satisfying_tuples(sum_tup)
        csp.add_constraint(con)

    print('done')
    return csp, var_array

##############################

def tenner_csp_model_2(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 8.

       The input board takes the same input format (a list of n length-10 lists
       specifying the board as tenner_csp_model_1.
    
       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0-9} if the
       board has a -1 at that position, and domain equal {i} if the board
       has a fixed number i at that cell.

       However, model_2 has different constraints. In particular,
       model_2 has a combination of n-nary 
       all-different constraints and binary not-equal constraints: all-different 
       constraints for the variables in each row, binary constraints for  
       contiguous cells (including diagonally contiguous cells), and n-nary sum 
       constraints for each column. 
       Each n-ary all-different constraint has more than two variables (some of 
       these variables will have a single value in their domain). 
       model_2 should create these all-different constraints between the relevant 
       variables.
    '''

    # initial CSP
    csp = CSP('tenner_csp')

    var_array = []

    n_grid = initial_tenner_board[0]
    last_row = initial_tenner_board[1]
    rows = len(n_grid)

    bin_tup = []
    for i in range(10):
        for j in range(10):
            if i != j:
                bin_tup += [(i, j)]

    for i in range(rows):
        var_array += [[]]
        for j in range(10):
            # check domain of cell i, j
            if n_grid[i][j] == -1:
                dom = list(range(10))
            else:
                dom = [n_grid[i][j]]

            # create variables
            var = Variable('v'+str(i)+str(j), dom)
            var_array[i] += [var]
            csp.add_var(var)

    # create binary constraints
    for i in range(rows):
        for j in range(10):
            # create constraints for neighbours of cell i,j that are >= i and one neighbour that is (i, j+1)
            print('---',i,j)
            for r in range(i, min(i+2, rows)):
                for c in range(max(0, j-1), min(j+2, 10)):
                    if r == i and (c == j or c == j-1):
                        continue

                    scope = [var_array[i][j], var_array[r][c]]
                    print('ij', r, c)

                    con = Constraint('c'+str(i)+str(j), scope)
                    con.add_satisfying_tuples(bin_tup)
                    csp.add_constraint(con)

    nary_tup = []
    for t in itertools.permutations(range(10)):
        nary_tup += [t]

    # create n-ary all-different constraints
    for i in range(rows):
        scope = []
        for j in range(10):
            scope += [var_array[i][j]]
        con = Constraint('cr'+str(i), scope)
        con.add_satisfying_tuples(nary_tup)
        csp.add_constraint(con)

    # create sum constraints
    for j in range(10):
        scope = []
        s = last_row[j]
        for i in range(rows):
            scope += [var_array[i][j]]
        con = Constraint('cc'+str(j), scope)
        sum_tup = []
        for t in itertools.product(range(10), repeat=rows):
            if sum(t) == s:
                sum_tup += [t]

        con.add_satisfying_tuples(sum_tup)
        csp.add_constraint(con)

    print('done')
    return csp, var_array
