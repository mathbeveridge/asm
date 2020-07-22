from stackset import build_stack_sets as build

def factor_one_zero_per_row(stack):
    #print('handling stack', stack)
    size = len(stack)
    zero_count_list = [sum(row) for row in stack]

    if sum(zero_count_list) == size * (size+1)/2:
        # all ones stack : we know how the factorization works from here
        # so let's stop the recursion early.
        return [row.copy() for row in stack]
    else:
        zero_index = []
        for row in stack:
            if 0 in row:
                zero_index.append(row.index(0))
            else:
                zero_index.append(-1)

        factor_stack = [ [1,] * k for k in range(1, size+1)]
        next_stack = [ [x for x in row] for row in stack]

        for idx in range(len(stack)):
            if zero_index[idx] >= 0:
                # zero out to the left of the rightmost zero
                factor_stack[idx][zero_index[idx]] = 0
                # turn the factored zero into a one for recursion
                next_stack[idx][zero_index[idx]] = 1

        #print('stack', stack, 'factor stack', factor_stack, 'next stack', next_stack)

        factor_list = [ factor_stack] + factor_one_zero_per_row(next_stack)
        return factor_list



def try_one_zero_per_row_factor():

    ### really does factor so that each permutation appears at least once in the list.
    stacks = build.build_stacks(3)

    first_dict = dict()

    for s in stacks:
        print(s)
        factor_list = factor_one_zero_per_row(s)
        print('\t', factor_list )

        if len(factor_list) > 1:
            key = str(factor_list[0])
        else:
            key = str(factor_list[0])

        if not key in first_dict:
            first_dict[key] = 1
        else:
            first_dict[key] = first_dict[key] + 1

    total = 0
    for key in first_dict:
        print(key, first_dict[key])
        total = total + first_dict[key]

    print(total)
    print(len(first_dict))



def row_col_swap(stack):
    #print('swap this', stack)
    size = len(stack)
    swap_stack = [[0,] * size  for k in range(size)]
    #print('swap this', stack, 'into', swap_stack)
    for i in range(size):
        for j in range(i+1):
            #print('moving', i,j, 'to', j, i)
            swap_stack[j][i] = stack[i][j]
            #print('\tss=', swap_stack)
    return swap_stack



def factor_weakly_incr_row(square):
    size = len(square)

    if size == 1:
        return( [ square,])
    else:
        factor_square = [[0,] * size  for k in range(size)]
        # reduce size of next square later
        next_square = [row.copy() for row in square]
        for i in range(size):
            if 1 in square[i]:
                j = square[i].index(1)
                next_square[i][j] = 0
                for k in range(j,size):
                    factor_square[i][k]=1

        del next_square[-1]
        for row in next_square:
            del row[0]

        return [ factor_square] + factor_weakly_incr_row(next_square)


def print_triangle(triangle):
    for row in triangle:
        print(row)
    print('----')

def print_factor_list(factor_list):
    for x in factor_list:
        for y in x:
            print(y)
        print('----')
    print('======')


stacks = build.build_stacks(3)

my_dict = dict()

for stack in stacks:
    squares = [row_col_swap(stack)  for stack in stacks]

for square in squares:
    print('******Start*********')
    print('triangle')
    print_triangle(square)
    factor_list = factor_weakly_incr_row(square)
    print('factor list')
    print_factor_list(factor_list)
    print('******End*********')
    key = str(factor_list[0])

    if key in my_dict:
        my_dict[key] = my_dict[key]+1
        print('updating key')
    else:
        my_dict[key] = 1
        print('adding key')

for key in my_dict:
    print(my_dict[key], key)

print(len(stacks))


#try_one_zero_per_row_factor()