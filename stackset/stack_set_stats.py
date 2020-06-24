from stackset import build_stack_sets as build


def cols_weak_decreasing(stacks, n):
    #stacks = build.build_stacks(n)
    good_stacks = stacks.copy()
    for stack in stacks:
        for i in range(n-1):
            for j in range(i+1):
                if stack[i][j] < stack[i+1][j]:
                    if stack in good_stacks:
                        good_stacks.remove(stack)
    return good_stacks

def cols_weak_increasing(stacks,n):
    #stacks = build.build_stacks(n)
    good_stacks = stacks.copy()
    for stack in stacks:
        for i in range(n-1):
            for j in range(i+1):
                if stack[i][j] > stack[i+1][j]:
                    if stack in good_stacks:
                        good_stacks.remove(stack)
    return good_stacks

def rows_weak_decreasing(n):
    stacks = build.build_stacks(n)
    good_stacks = stacks.copy()
    for stack in stacks:
        for i in range(n):
            for j in range(i):
                if stack[i][j] < stack[i][j+1]:
                    if stack in good_stacks:
                        good_stacks.remove(stack)
                        break
    return good_stacks


def diag_weak_increasing(stacks,n):
    #stacks = build.build_stacks(n)
    good_stacks = stacks.copy()
    for stack in stacks:
        for i in range(n-1):
            for j in range(n-i-1):
                if stack[i+j][j] > stack[i+j+1][j+1]:
                    if stack in good_stacks:
                        good_stacks.remove(stack)
    return good_stacks

def diag_weak_decreasing(stacks, n):
    #stacks = build.build_stacks(n)
    good_stacks = stacks.copy()
    for stack in stacks:
        for i in range(n-1):
            for j in range(n-i-1):
                if stack[i+j][j] < stack[i+j+1][j+1]:
                    if stack in good_stacks:
                        good_stacks.remove(stack)
    return good_stacks


def semidiag_weak_increasing(n):
    stacks = build.build_stacks(n)
    good_stacks = stacks.copy()
    for stack in stacks:
        print(stack)
        #start on col 1
        for i in range(1,n):
            for j in range(int(i/2)):
                print(n,i,j)
                print('\t', j,j, '>', j-1, j+1)
                if stack[i-j][j] > stack[i-j-1][j+1]:
                    if stack in good_stacks:
                        good_stacks.remove(stack)
                        break
                print('***')
        print('####')
        # start on row n
        for i in range(n):
            for j in range(int((n-1-i)/2)):
                print(n,i,j)
                if stack[n-1-j][j] > stack[n-1-j-1][j+1]:
                    if stack in good_stacks:
                        good_stacks.remove(stack)
                        break
        print('-----')
    return good_stacks

def semidiag_weak_decreasing(n):
    stacks = build.build_stacks(n)
    good_stacks = stacks.copy()
    for stack in stacks:
        print(stack)
        for i in range(1,n):
            for j in range(int(i/2)):
                print(n,i,j)
                print('\t', j,j, '<', j-1, j+1)
                if stack[i-j][j] < stack[i-j-1][j+1]:
                    if stack in good_stacks:
                        good_stacks.remove(stack)
                        break
                print('***')
        print('####')
        # start on row n
        for i in range(n):
            for j in range(int((n-1-i)/2)):
                print(n,i,j)
                if stack[n-1-j][j] < stack[n-1-j-1][j+1]:
                    if stack in good_stacks:
                        good_stacks.remove(stack)
                        break
        print('-----')
    return good_stacks

def semidiag_weak_decreasing_old(n):
    stacks = build.build_stacks(n)
    good_stacks = stacks.copy()
    for stack in stacks:
        print(stack)
        #start on col 1
        for i in range(1,n):
            for j in range(int(i/2)):
                print(n,i,j)
                print('\t', j,j, '<', j-1, j+1)
                if stack[i-j][j] < stack[i-j-1][j+1]:
                    if stack in good_stacks:
                        good_stacks.remove(stack)
                        break
                print('***')
        print('####')
        # start on row n
        for i in range(n):
            for j in range(int((n-1-i)/2)):
                print(n,i,j)
                if stack[n-1-j][j] < stack[n-1-j-1][j+1]:
                    if stack in good_stacks:
                        good_stacks.remove(stack)
                        break
        print('-----')
    return good_stacks


def rows_weak_increasing(n):
    stacks = build.build_stacks(n)
    good_stacks = stacks.copy()
    for stack in stacks:
        for i in range(n):
            for j in range(i):
                if stack[i][j] > stack[i][j+1]:
                    if stack in good_stacks:
                        good_stacks.remove(stack)
                        break
    return good_stacks


def one_one_per_col_broken(stacks, n):
    #stacks = build.build_stacks(n)
    good_stacks = stacks.copy()
    for stack in stacks:
        for i in range(n):
            num_ones = 0
            for j in range(i+1):
                if stack[i][j] == 1:
                        num_ones += 1
            if num_ones > 1:
                if stack in good_stacks:
                    good_stacks.remove(stack)
    return good_stacks

def one_one_per_col_fixed(stacks,n):
    print("starting");
    #stacks = build.build_stacks(n)
    #print("built stacks for", n, len(stacks));
    good_stacks = stacks.copy()
    for index,stack in enumerate(stacks):
        if index % 1000 == 0:
        	print('col processing stack', index)
        for i in range(n):
            num_ones = 0
            for j in range(i,n):
                if stack[j][i] == 1:
                        num_ones += 1
            #### CHANGE BACK!
            if num_ones > 1:
            #if not num_ones == 1:
                if stack in good_stacks:
                    good_stacks.remove(stack)
                    break
    return good_stacks

def max_ones_per_col(n,k):
    print("starting");
    stacks = build.build_stacks(n)
    print("built stacks for", n, len(stacks));
    good_stacks = stacks.copy()
    for index,stack in enumerate(stacks):
        if index % 1000 == 0:
        	print('col processing stack', index)
        for i in range(n):
            num_ones = 0
            for j in range(i,n):
                if stack[j][i] == 1:
                        num_ones += 1
            if num_ones > k:
                if stack in good_stacks:
                    good_stacks.remove(stack)
                    break
    return good_stacks


def one_one_per_row(stacks,n):
    good_stacks = stacks.copy()
    for index,stack in enumerate(stacks):
        if index % 1000 == 0:
        	print('row processing stack', index)
        for x in stack:
            ##### CHANGE BACK
            if sum(x) > 1:
            #if not sum(x) == 1:
                good_stacks.remove(stack)
                break
    return good_stacks

def one_one_per_row_and_col(stacks,n):
    temp_stacks = one_one_per_col_fixed(stacks,n)
    good_stacks = temp_stacks.copy()
    for index,stack in enumerate(temp_stacks):
        if index % 1000 == 0:
        	print('row processing stack', index)
        for x in stack:
            if sum(x) > 1:
                good_stacks.remove(stack)
                break
    return good_stacks

def one_one_per_diag(stacks, n):
    flip_stacks = []

    # turn diagonals into columns
    for stack in stacks:
        temp = []
        for s in stack:
            temp.append([x for x in reversed(s)])
        flip_stacks.append(temp)

    stack_list = one_one_per_col_fixed(flip_stacks,n)

    # turn columns back into diagonals
    ret_val = []
    for stack in stack_list:
        temp = []
        for s in stack:
            temp.append([x for x in reversed(s)])
        ret_val.append(temp)

    return ret_val


def one_one_per_diag_old(stacks, n):
    good_stacks = stacks.copy()
    for index,stack in enumerate(stacks):
        if index % 1000 == 0:
            print(index)
        for i in range(n):
            num_ones = 0
            for j in range(n-i):
                if stack[i+j][j] > 0:
                    num_ones += 1
                if num_ones > 1:
                    if stack in good_stacks:
                        good_stacks.remove(stack)
                        break
    return good_stacks

def one_one_per_semidiag(stacks, n):
    #stacks1 = [ stacks[len(stacks)-1]]
    good_stacks = stacks.copy()
    for stack in stacks:
        #print('handling:',stack)
        #start on col 1
        for i in range(n):
            num_ones = 0
            #print('start col diag', i)
            for j in range(int(i/2)+1):
                #print(n,i-j,j)
                if stack[i-j][j] == 1:
                    num_ones += 1
            if num_ones > 1:
                print('\tcol fail', stack)
                good_stacks.remove(stack)
                break
                #print('done col diag')
        print('####')
        # start on row n
        if num_ones <= 1:
            for i in range(n+1):
                #print('start row diag', i)
                num_ones = 0
                for j in range(int((n+1-i)/2)):
                    print(n,n-1-j,j+i, '<---', stack[n-1-j][j+i])
                    if stack[n-1-j][j+i] == 1:
                        num_ones = num_ones + 1
                        print('bad!!!')
                    print(num_ones)
                if num_ones > 1:
                    print('\trow fail', stack)
                    good_stacks.remove(stack)
                    break
                #print('done row diag')
            print('-----')
    return good_stacks

def count_by_diagonal(n):
    num_ones_list = [0] * (n+1)
    stacks = build.build_stacks(n)
    for stack in stacks:
        num_ones = count_ones_in_diag(stack, n)
        num_ones_list[num_ones] = num_ones_list[num_ones] +1
    return num_ones_list


def count_by_first_col(n):
    num_ones_list = [0] * (n+1)
    stacks = build.build_stacks(n)
    for stack in stacks:
        #num_ones = sum(stack[i][0] for i in range(n))
        num_ones = count_ones_in_col(stack, 0)
        num_ones_list[num_ones] = num_ones_list[num_ones] +1
    return num_ones_list


def count_by_last_row(n):
    num_ones_list = [0] * (n+1)
    stacks = build.build_stacks(n)
    for stack in stacks:
        num_ones = sum(stack[n-1][i] for i in range(n))
        num_ones_list[num_ones] = num_ones_list[num_ones] +1
    return num_ones_list


def count_ones_in_diag(stack,diag_num):
    return sum(stack[i][i] for i in range(diag_num))

def count_ones_in_col(stack,col_num):
    return sum(stack[i][col_num] for i in range(col_num, len(stack)))


def sort_by_diag(stack_list, diag_num):
    my_list = []
    for i in (range(diag_num+1)):
        my_list.append([])
    for stack in stack_list:
        num_ones  = count_ones_in_diag(stack,diag_num)
        my_list[num_ones].append(stack)
    return my_list


def sort_by_col(stack_list, col_num):
    my_list = []
    for i in (range(len(stack_list[0])-col_num+1)):
        my_list.append([])
    for stack in stack_list:
        num_ones  = count_ones_in_col(stack,col_num)
        my_list[num_ones].append(stack)
    return my_list


######

def transform_stacks(n):
    stacks = build.build_stacks(n)
    return [ transform_stack(stack) for stack in stacks]


### just write for n=3
def transform_stack(stack):
    triangle = [[stack[0][0] + stack[1][0] + stack[2][0],],
                [ stack[1][1] + stack[2][1],stack[1][0] + stack[2][0],],
                [stack[2][2],stack[2][1],stack[2][0],],];

    return triangle


gog3 = [[[0, 0, 0], [0, 0], [0,]], [[0, 0, 1], [0, 0], [0,]], [[0, 1, 0], [0,
   0], [0,]], [[0, 1, 1], [0, 1], [0,]], [[0, 2, 1], [0, 0], [0,]], [[0,
   2, 1], [0, 1], [0,]], [[1, 0, 0], [0, 0], [0,]], [[1, 0, 1], [0,
   0], [0,]], [[1, 1, 0], [1, 0], [0,]], [[1, 1, 1], [1, 1], [1,]], [[1,
   2, 1], [1, 0], [0,]], [[1, 2, 1], [1, 1], [1,]], [[2, 1, 0], [0,
   0], [0,]], [[2, 1, 1], [0, 1], [0,]], [[2, 1, 0], [1, 0], [0,]], [[2,
   1, 1], [1, 1], [1,]], [[2, 2, 1], [2, 1], [0,]], [[2, 2, 1], [2,
   1], [1,]], [[3, 2, 1], [0, 0], [0,]], [[3, 2, 1], [0, 1], [0,]], [[3,
   2, 1], [1, 0], [0,]], [[3, 2, 1], [1, 1], [1,]], [[3, 2, 1], [2,
   1], [0,]], [[3, 2, 1], [2, 1], [1,]], [[0, 1, 1], [0, 0], [0,]], [[1,
   1, 1], [1, 0], [0,]], [[2, 1, 1], [1, 1], [0,]], [[3, 2, 1], [1,
   1], [0,]], [[2, 2, 1], [1, 1], [1,]], [[2, 2, 1], [0, 1], [0,]], [[1,
   2, 1], [0, 0], [0,]], [[1, 1, 0], [0, 0], [0,]], [[1, 1, 1], [0,
   1], [0,]], [[1, 2, 1], [0, 1], [0,]], [[1, 2, 1], [1, 1], [0,]], [[1,
   1, 1], [1, 1], [0,]], [[1, 1, 1], [0, 0], [0,]], [[2, 2, 1], [1,
   0], [0,]], [[2, 2, 1], [0, 0], [0,]], [[2, 1, 1], [0, 0], [0,]], [[2,
   1, 1], [1, 0], [0,]], [[2, 2, 1], [1, 1], [0,]]]


def get_gog3():
    ret_val = []
    for g in gog3:
        triangle = [[g[0][0],],
                    [g[1][0], g[0][1]],
                    [g[2][0], g[1][1],g[0][2]]]
        ret_val.append(triangle)

    return ret_val


def count_blocks(triangle):
    count = 0
    for t in triangle:
        count = count + sum(t)
    return count

##########

def stack_and_gog():

	stack_triangles = transform_stacks(3)
	gog_triangles = get_gog3()

	gog_blocks = [0] * 11
	stack_blocks = [0] * 11


	count = 0
	for t in stack_triangles:
		if t not in gog_triangles:
			count = count+1
			print(t[0])
			print(t[1])
			print(t[2])
			print('')
		c = count_blocks(t)
		stack_blocks[c] = stack_blocks[c]+1

	print('stack not gog  count is', count)


	count = 0
	for t in gog_triangles:
		if t not in stack_triangles:
			count = count+1

		print(t[0])
		print(t[1])
		print(t[2])
		print('')
		c = count_blocks(t)
		gog_blocks[c] = gog_blocks[c]+1

	print('gog not stack count is', count)


	print('sta blocks', stack_blocks)
	print('gog blocks', gog_blocks)






def reflect_is_sst(stacks,n):
    sst = build.build_stacks(n)
    good_stacks = []
    for stack in stacks:
        reflect_stack = build.reflect(stack)
        if reflect_stack in sst:
            good_stacks.append(reflect_stack)

    return good_stacks

def invert_is_sst(stacks,n):
    good_stacks = []
    sst = build.build_stacks(n)
    for stack in stacks:
         inv_stack = build.invert(stack)
         if inv_stack in sst:
            good_stacks.append(inv_stack)
    return good_stacks


