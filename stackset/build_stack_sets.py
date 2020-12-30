import itertools


def build_binary_lists(n):
    binary_lists = []
    if n == 1:
        return [[0], [1]]
    if n > 1:
        n_minus_one_lists = build_binary_lists(n-1)
        for old in n_minus_one_lists:
            new_list_zero = old + [0]
            new_list_one = old + [1]
            binary_lists += [new_list_one, new_list_zero]
    return binary_lists


def build_stacks(n):
    if n == 1:
        return [[[0]],[[1]]]
    if n > 1:
        old_stacks = build_stacks(n-1)
        next_layer_candidates = build_binary_lists(n)
        new_stacks = []
        for old_stack in old_stacks:
            last_layer = old_stack[len(old_stack)-1]
            ones = [i for i, x in enumerate(last_layer) if x == 1]
            for nl_candidate in next_layer_candidates:
                num_passed = 0
                for i in ones:
                    if sum(nl_candidate[i:n+1]) >= sum(last_layer[i:n]):
                        num_passed += 1
                if num_passed == sum(last_layer):
                    new_stack = old_stack + [nl_candidate]
                    new_stacks += [new_stack]
        return new_stacks

# build binary triangles that do not contain:
# 1
# 10
#
def build_ooz(n):
    if n == 1:
        return [[[0]],[[1]]]
    if n > 1:
        old_stacks = build_ooz(n-1)
        next_layer_candidates = build_binary_lists(n)
        new_stacks = []
        for old_stack in old_stacks:
            last_layer = old_stack[len(old_stack)-1]
            ones = [i for i, x in enumerate(last_layer) if x == 1]
            for nl_candidate in next_layer_candidates:
                is_good = True
                for idx in ones:
                    if nl_candidate[idx] == 1 and nl_candidate[idx+1] == 0:
                        is_good = False
                        break
                # TRACKING TO SEE IF ZEROS MOVING UP 2 ROWS HAD BOTTLENECK?
                # CODE ISN'T RIGHT AND ALL EXCLUDED WERE ACTUALLY GOOD
                #check_two_rows_above = False
                # if is_good:
                #     for idx in range(2, len(nl_candidate)):
                #         if nl_candidate[idx] == 1:
                #             check_two_rows_above = True
                #         if check_two_rows_above:
                #             if nl_candidate[idx] == 0 and old_stack[len(old_stack)-2][idx-2] == 1:
                #                 is_good = False
                #                 print('fail')
                #                 for row in old_stack:
                #                     print(row)
                #                 print(nl_candidate)
                #                 print('-----')
                #                 break
                if is_good:
                    new_stack = old_stack + [nl_candidate]
                    new_stacks += [new_stack]
        return new_stacks







def build_inverted_stacks(n):
    stacks = build_stacks(n)
    inv_stacks = [ invert(s) for s in stacks]

    return inv_stacks



def invert(stack):
    inv_stack = []
    for s in stack:
        ones = [1] * len(s)
        zip_list = zip(ones, s)
        t = []
        for x,y in zip_list:
            t.append(x-y)
        inv_stack.append(t)

    return inv_stack


def reflect(stack):
    n = len(stack)
    new_stack = []

    for i in range(1,n+1):
        new_stack.append([0]*i)

    for i in range(len(stack)):
        row = stack[i]
        for j in range(len(row)):
            new_stack[n-1-j][n-1-i] = stack[i][j]

    return new_stack

# swap rows and columns
def rotate(stack):
    n = len(stack)
    new_stack = [[0] * (n-k) for k in range(n)]
    for row_idx in range(n):
        for col_idx in range(len(stack[row_idx])):
            new_stack[col_idx][row_idx-col_idx] =  stack[row_idx][col_idx]
    return new_stack

#def reverse_rows(stack):
#    return [list(reversed(row)) for row in stack]




def last_index(my_list):
    return len(my_list) - my_list[::-1].index(1) - 1

def stack_to_perm(stack):
    new_stack = rotate(stack)
    perm = []
    n =  len(stack)+1
    elements =  list(range(1,n+1))
    for row in new_stack:
        if not 1 in row:
            idx = 0
        else:
            idx = len(row)- row.index(1)
        #print(idx, new_stack)
        perm.append(elements.pop(idx))
    perm.append(elements.pop())

    return perm


def get_triples(n):
    my_list = range(1,n+1)
    triple_list = []
    for t in itertools.combinations(my_list, 3):
        triple_list.append(t)
    return triple_list


#################
#
# The next method doesn't illuminate things.
#

def build_opp_stacks(n):
    if n == 1:
        return [[[0]],[[1]]]
    if n > 1:
        old_stacks = build_stacks(n-1)
        next_layer_candidates = build_binary_lists(n)
        new_stacks = []
        for old_stack in old_stacks:
            last_layer = old_stack[len(old_stack)-1]
            for nl_candidate in next_layer_candidates:
                num_passed = 0
                for i in range(len(last_layer)):
                    passed = True
                    if sum(nl_candidate[i:n+1]) > sum(last_layer[i:n]):
                        passed = False
                        break
                if passed:
                    new_stack = old_stack + [nl_candidate]
                    new_stacks += [new_stack]
        return new_stacks


# similar construction, but num ones in previous layer must be less than or equal
# to ones in last layer starting at 0 and ending at every i.
# See "Monotone Triangles and 312 Pattern Avoidance"
def build_gapless_gog_word_stacks(n):
    if n == 1:
        return [[[0]],[[1]]]
    if n > 1:
        old_stacks = build_gapless_gog_word_stacks(n-1)
        next_layer_candidates = build_binary_lists(n)
        new_stacks = []
        for old_stack in old_stacks:
            last_layer = old_stack[len(old_stack)-1]
            #print('last layer', last_layer)
            #ones = [i for i, x in enumerate(last_layer) if x == 1]
            for nl_candidate in next_layer_candidates:
                #print('candidate', nl_candidate)
                passed = True
                for i in range(len(last_layer)):
                    if sum(nl_candidate[0:i+1]) > sum(last_layer[0:i+1]):
                        passed = False
                        break
                if passed:
                    new_stack = old_stack + [nl_candidate]
                    new_stacks += [new_stack]
        return new_stacks

# not very illuminating...
def build_opp_gapless_gog_word_stacks(n):
    if n == 1:
        return [[[0]],[[1]]]
    if n > 1:
        old_stacks = build_gapless_gog_word_stacks(n-1)
        next_layer_candidates = build_binary_lists(n)
        new_stacks = []
        for old_stack in old_stacks:
            last_layer = old_stack[len(old_stack)-1]
            #print('last layer', last_layer)
            #ones = [i for i, x in enumerate(last_layer) if x == 1]
            for nl_candidate in next_layer_candidates:
                #print('candidate', nl_candidate)
                passed = True
                for i in range(len(last_layer)):
                    if sum(nl_candidate[0:i+1]) < sum(last_layer[0:i+1]):
                        passed = False
                        break
                if passed:
                    new_stack = old_stack + [nl_candidate]
                    new_stacks += [new_stack]
        return new_stacks

def build_plateaus(stacks, n):
    #stacks = build_stacks(n)
    plateaus = []
    for stack in stacks:
        plateau = []
        for row in stack:
            plat_row = []
            height = 0
            for x in reversed(row):
                height = height + x
                plat_row.append(height)
            plat_row.reverse()
            plateau.append(plat_row)
        plateaus.append(plateau)
    return plateaus


def switch(stack):
    return [ list(reversed(row)) for row in stack]


def pst_layer_list(n):
    if n == 1:
        return [[0,], [1,]]
    else:
        layer_list = []
        prev_list = pst_layer_list(n-1)
        for x in range(n+1):
            for prev_layer in prev_list:
                if x == prev_layer[0] or x == prev_layer[0]+1:
                    layer_list.append([x,] + prev_layer)
        return layer_list

# columns increase
def check_pst_col(prev_layer, layer):
    for idx in range(len(prev_layer)):
        if prev_layer[idx] > layer[idx]:
            return False
    return True

# pst rules:
# rows weakly decrease by at most 1
# columns increase
# a(i,j) <= i+j-1
# NOTE: this family is what Adam and Giselle call APATs. Cool.
def build_pst(n):
    if n == 1:
        return [[[0],],[[1],]]
    else:
        current_psts = []
        prev_psts = build_pst(n-1)
        #print(n)
        #for pp in prev_psts:
        #    print(pp)
        layer_list = pst_layer_list(n)
        for pst in prev_psts:
            prev_layer = pst[n-2]
            for layer in layer_list:
                if check_pst_col(prev_layer, layer):
                    current_psts.append(pst + [ layer,])
        return current_psts






