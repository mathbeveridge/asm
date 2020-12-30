from stackset import build_stack_sets as build
from stackset import stack_set_stats as stats
from stackset import hook as hook
import math

import itertools



def count_ells_old(stack):
    size = len(stack)
    count = 0
    for i in range(size):
        for j in range(i):
            #print(i,j)
            if stack[i][j] == 0 and stack[i-1][j] == 1:
                count = count + 1
    return count

def count_ells(stack):
    return len(get_ells(stack))

# an ell is of the form [[a,b], [c,d], e] where a < c and b < d and e is the number of zeros
# the zero of the ell is at [c,d]
# there are only ones above the zero
# there may be zeros and then ones to the right of the zero.
def get_ells(stack):
    size = len(stack)
    ell_list = []
    for i in range(size):
        for j in range(i):
            #print(i,j)
            if stack[i][j] == 0 and stack[i-1][j] == 1:
                # ell will be of the form [a,j], [i,j], [i,b]


                #print('zero is at', i, j)

                a = i
                #print('\t a starts at', i)
                #print('\t\t stack[a-1][j]=', stack[a-1][j])
                while a > j and stack[a-1][j] == 1:
                    a = a - 1
                    #print('\t\ta is now', a)


                b = j
                num_zeros = 0
                #print('\t b starts at', j)

                # xxxab If I comment out this whole statement then
                # I get the right answer for n=5: 13052. But some of
                # the "hooks" that are generated aren't correct:
                # they become a single column.
                while stack[i][b] == 0:
                    b = b  + 1
                    num_zeros = num_zeros + 1
                    #print('\t\tb 0 is now', b)
                while b < i and stack[i][b+1] == 1:
                    b = b + 1
                    #print('\t\tb 1 is now', b)

                #print('\tb is', b)

                ell_list. append([[a,j], [i,b], num_zeros])


    #for s in stack:
    #    print(s)
    #print('-----')
    #for ell in ell_list:
    #    print('\t', ell)
    #print('##########')

    return ell_list

def check_nested(ell1, ell2):
    x = ell1
    y = ell2

    if x[0][0] < y[0][0] and x[0][1] < y[0][1] and x[1][0] > y[1][0] and x[1][1] > y[1][1]:
        return True
    elif x[0][0] > y[0][0] and x[0][1] > y[0][1] and x[1][0] < y[1][0] and x[1][1] < y[1][1]:
        return True
    else:
        return False

def explore_zeros_and_ells(n):

    #stacks = build.build_stacks(n)
    stacks = [ [ [1], [1, 0], [1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 1, 1]], ]
    zero_map = dict()
    total_zeros = 0
    total_nested = 0
    num_nested_three = 0
    for stack in stacks:
        for s in stack:
            print(s)

        size = len(stack)
        # num_ones = 0
        # for s in stack:
        #    num_ones = num_ones + s[0]

        # if num_ones < size+1:

        ells = get_ells(stack)

        for ell in  ells:
            print(ell)

        z = len(ells)

        if not z in zero_map:
            zero_map[z] = 0

        zero_map[z] = zero_map[z] + 1

        total_zeros = total_zeros + z

        nested_ells = []

        for pair in itertools.combinations(ells, 2):
            x = pair[0]  # (a,b)
            y = pair[1]  # (c,d)

            # xxxAB note! This method does not take into account overlapping zeros.
            # Use hook instead!
            if check_nested(x, y):
                nested_ells.append(pair)

        if len(nested_ells) > 3:
            for s in stack:
                print(s)
            for pair in nested_ells:
                print('\t', pair[0], pair[1])
            print('------')

        temp = len(nested_ells)

        if (temp > 2):
            print('changing', temp, 'to 1')
            temp = 1

        # total_nested = total_nested + len(nested_ells)
        total_nested = total_nested + temp


        # if z == 2:
        #    for x in stack:
        #        print(x)
        #    print('---------')

    print('total nested', total_nested)
    print('total zeros', total_zeros)
    total = total_zeros + total_nested
    print('total', total)
    for key in zero_map:
        print(key, 'zeros:', zero_map[key])


#### CURRENT IDEA: ONLY DISJOINT NESTINGS COUNT SEPARATELY.
#### ONCE PER LONGEST ELL


### 6/27 amazingly, # of ASM with A(1,k) =  1 equals # SST with k-1 0's in column 1
### this is a known theorem, as noted by Striker.
### the numbers of 1's followed by 0's in columns diverges from # of -1 in ASM for n > 5
### is there another structure that arises when the SST gets large enough?


def explore_zeros_and_hooks(n):

    stacks = build.build_stacks(n)
    #stacks = [[ [1], [1, 1], [1, 0, 1], [0, 1, 1, 1]],]

    #stacks = [ [ [1], [1, 0], [1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 1, 1]], ]
    #for s in stacks[0]:
    #    print(s)

    zero_map = dict()
    total_zeros = 0
    total_min_nested_hooks = 0
    total_correct_nest = 0
    compare_count = 0

    for stack in stacks:
        # print(stack)

        #size = len(stack)
        # num_ones = 0
        # for s in stack:
        #    num_ones = num_ones + s[0]

        # if num_ones < size+1:

        ells = get_ells(stack)



        z = len(ells)

        if not z in zero_map:
            zero_map[z] = 0

        zero_map[z] = zero_map[z] + 1
        total_zeros = total_zeros + z


        if len(ells) > 1:
            hooks = [ hook.Hook(ell[0], ell[1], ell[2]) for ell in ells]

            #for s in stack:
            #    print('\t\t', s)

            for pair in itertools.combinations(hooks, 2):
                if pair[0].update_comparison(pair[1]):
                    #print('comparable', pair[0].toString(), pair[1].toString())
                    compare_count = compare_count + 1


            for h in hooks:
                #print('minimal=', h.is_minimal())
                if h.is_minimal() and h.has_hooks_above():
                    print(h.toString(), len(h.hooks_below), 'above count', len(h.hooks_above))
                    # let's assume it's the height of this poset rather than the width of
                    # height 1.

                    height = h.get_height_above();



                    #total_min_nested_hooks  = total_min_nested_hooks + h.get_num_directly_above()
                    total_min_nested_hooks  = total_min_nested_hooks + 1
                    #total_min_nested_hooks  = total_min_nested_hooks + height
                    #total_min_nested_hooks = total_min_nested_hooks + height - h.get_num_directly_above()
                    if len(h.hooks_above) > 1:
                        for s in stack:
                            print(s)
                        print('>>>>>>>', h.toString(), 'nests', len(h.hooks_above))
                        print('\t\tand directly above =', h.get_num_directly_above())


        # if z == 2:
        #    for x in stack:
        #        print(x)
        #    print('---------')

    print('total min nested hooks', total_min_nested_hooks)
    print('total comparable hook pairs', compare_count)
    print('total zeros', total_zeros)
    total = total_zeros + total_min_nested_hooks
    print('total', total)
    for key in zero_map:
        print(key, 'zeros:', zero_map[key])



# permutations where biggest increase is k
def T(n,k):
    if k == 0:
        return 1
    else:
        return math.factorial(k)  * (k + 1) ** (n - k) - math.factorial(k - 1) * k ** (n - k + 1)

# the number we want
def S(n):
    return math.factorial(n) * n * (n-1) * (n-2) /36

# perm at least one more one in k than k-1
def U(n,k):
    return math.factorial(n)  * (k+1)

def V(n):
    u_list = [ [k, (n-k), U(n-1,k-1)] for k in range(1,n)]
    t_list = [ k * (n-k) *  U(n-1,k-1) for k in range(1,n+1)]
    print(u_list)
    print(t_list)
    print(S(n), n+1)
    return  S(n) * (n+1) +  sum(t_list)


def count_perm_and_triples(stacks, nn):

    triples = build.get_triples(nn + 1)

    for t in triples:
        print(t)

    print(len(stacks))

    count = 0
    for stack in stacks:
        # print(stack, '\t', build.rotate(stack))
        perm = build.stack_to_perm(stack)
        # print(stack, perm)
        for triple in triples:
            low = triple[0]
            mid = triple[1]
            high = triple[2]
            # print(triple)
            # print(perm.index(3), perm.index(2), perm.index(1))
            index_list = [perm.index(high), perm.index(mid), perm.index(low)]
            if index_list[0] < index_list[1] and index_list[1] < index_list[2]:
                count = count + 1
                short_list = [high]
                for i in range(index_list[0] + 1, len(perm)):
                    if perm[i] < high:
                        short_list.append(perm[i])
                heights = [len(short_list) - 1 - short_list.index(triple[k]) for k in reversed(range(3))]

                print('stack', stack, 'perm', perm, 'triple', triple, 'index', index_list, 'heights', heights)

    print(count)


def print_stack_list(stacks):
    for s in stacks:
        for row in s:
            print(row)
        print('-----')
    print('num stacks=', len(stacks))


def stack_to_tex(stack):
    ret_val = "\\begin{bmatrix}\n"
    for row in stack:
        ret_val = ret_val + ' & '.join(str(n) for n in row) + ' \\\\ \n'
    ret_val = ret_val + '\\end{bmatrix} \n \\\\ \n'

    return ret_val

def stack_list_to_tex(stacks):
    ret_val = ''
    for stack in stacks:
        ret_val = ret_val + stack_to_tex(stack)

    return ret_val


#m=4
#print('S', S(m+1))
#print('V', V(m))
#print(S(3)  * 4)

#print('----')
#for k in range(m):
#    print(k, m-k, U(m,k))


#for t in triangles:
#    print(t[0])
#    print(t[1])
#    print(t[2])
#    print('')

####################################################
# print(count_by_diagonal(2))
# print(count_by_diagonal(3))
# print(count_by_diagonal(4))
# print(count_by_diagonal(5))
#
#
# print(count_by_first_col(2))
# print(count_by_first_col(3))
# print(count_by_first_col(4))
# print(count_by_first_col(5))
#
#
# print(count_by_last_row(2))
# print(count_by_last_row(3))
# print(count_by_last_row(4))
# print(count_by_last_row(5))
#
#
#
# print('======== by column======')
# stacks = build.build_stacks(3)
# sorted_stacks = sort_by_col(stacks,0)
#
# for s in sorted_stacks:
#     print(len(s))
#     double_sorted = sort_by_col(s,1)
#     for t in double_sorted:
#         print('\t', len(t))
#
#
# print('======== by diagonal ======')
# stacks = build.build_stacks(3)
# sorted_stacks = sort_by_diag(stacks,3)
#
# for s in sorted_stacks:
#     print(len(s))
#     double_sorted = sort_by_diag(s,2)
#     for t in double_sorted:
#         print('\t', len(t))
#
#
#
# print('======== by diagonal then col ======')
# stacks = build.build_stacks(3)
# sorted_stacks = sort_by_col(stacks,0)
#
# for s in sorted_stacks:
#     print(len(s))
#     double_sorted = sort_by_diag(s,2)
#     for t in double_sorted:
#         print('\t', len(t))


#stacks = build.build_stacks(3)
#for k in range(3,7):
#    stacks = one_one_per_row_and_col(k)
#    print(k, len(stacks))

#nn=6
#kk=1
# kk=1: 14, 43, 142, 499 which is http://oeis.org/A005425
# kk=2: 35,226,1780,16462
#stacks = max_ones_per_col(nn,kk)
#print(nn, kk, len(stacks))
#for s in stacks:
#    for x in s:
#        print(x)
#    print('------')





# inv one one per column 2, 5, 16, 62, 283,1488
# inv one one per row and col 2, 5, 15, 52, 203, 877 Bell numbers!
# inv one one per row 2, 6, 24, 120, 720, 5040 Permutations

#stacks = cols_weak_decreasing(3)
#nn = 3
#stacks = build.build_stacks(nn)
#for s in stacks:
#    print(s)
#good_stacks = one_one_per_col_fixed(stacks, nn)
#for s in good_stacks:
#    for x in s:
#        print(x)
#    print('------')
#print('regular',len(stacks), len(good_stacks))

#stacks = build.build_inverted_stacks(nn)
#for s in stacks:
#    print(s)
#good_stacks = one_one_per_col_fixed(stacks, nn)
#print('inverted',len(stacks), len(good_stacks))



# diag weak incr: 2,6,24,120,720 this is (n+1)!
# diag weak decr: 2,5,14,42,132 this is Catalan
# semidiag weak decr: 2, 7, 34, 277, 2786
# semidiag weak incr: 2, 7, 30, 244, 2078
# one one per diag: 2, 5, 14, 41, 131, 439
# inverted one one per diag: 2, 5, 17, 70, 339
# one one per semidiag: 2, 7, 30, 157, 929
# inverted one one per semidiag: 2, 7, 32, 198, 1506
# one one per row and diag: 2,4,15,28,51
# one one per col and diag: 1,4,9,21,52,134 (w/o 134 A051292)
# inverted one one per col and diag 1,4,10,30,100,360
# inverted one one per row and diag 5,15,52,203 Bell numbers
# inverted one one per row, col, 2,3,5,8,13,21 Fibonacci
# inverted one one per row, col, diag 1,4,10,28,84,272 (almost A228403)
# inverted one one per diagonal 2,5,17,70,339, 1895
# exactly one per diagonal 2,4,9,22,57 MANY MATCHES. Need more terms
# exactly one per col 2,4,10,26,76 A000085 Self inverse permutations
# exactly one per row 2,5,14,42,132 Catalan (Robbie did at most 1)
# inverted exactly one per row 2,624,120,720 permutations
# inverted exactly one per diagonal 1,3,9,31,145
# inverted exactly one per col 1,2,5,15,57 MAYBE??? A334155
# inverted exactly one per row 2,624,120,720 permutations
# exactly one per col and diag weak incr 2,4,8,16,32
# exactly one per row and diag weak incr 1
# exactly one per col and diag weak decr 1
# exactly one per row and diag weak decr 2,3,4,5
# inverted exactly one per col and diag weak incr 1,2,2,3,4 Interesting... some sort of integer partition
# inverted exactly one per row and diag weak incr 1
# inverted exactly one per col and diag weak decr 1
# inverted exactly one per row and diag weak decr 2,4,8,16,32

# one per row, wol weak incr

#### HAVEN'T ADDED THESE

# weak incr col and one one per row 2,4,7,11,16,22   A000124
# weak incr col and exact one per row 1
# weak incr col and one one per diag  2,5,13,34,89,233  A001519
# weak incr col and exact one per diag  1,2,4,8,16,32

# weak dec col and one one per row 4,8,16,32,64
# weak dec col and exact one per row 2,4,16,32
# weak dec col and one one per diag  1,3,4,5,6
# weak dec col and exact one per diag  1


# invert is stackset 6, 28, 202, 2252
# reflect is stackset 6, 25, 149, 1259
# invert reflect is stackset 6, 26, 158, 1332





nn = 3
stacks = build.build_stacks(nn)
#stacks = build.build_inverted_stacks(nn)
#stacks0 = stats.one_one_per_col_fixed(stacks,nn)
#stacks0 = stats.one_one_per_row(stacks, nn)
#good_stacks = stats.one_one_per_diag(stacks,nn)
#good_stacks = stats.one_one_per_row(stacks0,nn)
#good_stacks = stats.cols_weak_decreasing(stacks,nn)
#good_stacks = stats.reflect_is_sst(stacks,nn)
#good_stacks = stats.invert_is_sst(stacks, nn)
#good_stacks = stats.has_num_zero_below_one(stacks, 1, nn)
#good_stacks = stacks


#print(len(good_stacks))




#stacks1 = stats.has_num_zero_below_one(stacks, 0, nn)
#print('----- n=', nn, 'total stacks=', len(stacks1))
#for k in range(nn):
#    good_stacks = stats.at_least_one_more_in_row(stacks1,k,nn)
    #if k > 0:
    #    good_stacks = stats.none_in_row(good_stacks, k - 1, nn)
#    print('>>>>>>>>>>>>>>row', k, 'num good', len(good_stacks))
#    print(U(nn,k))
    #for stack in good_stacks:
    #    for r in stack:
    #        print(r)
    #    print('----')



# stacks1 = stats.has_num_zero_below_one(stacks,1,nn)
# print('----- n=',  nn, 'total stacks=', len(stacks1))
# for k in range(1,nn):
#     count = 0
#     print('>>>>>>>>>> 1/0 in row', k)
#     for stack in stacks1:
#         if stack[k][0] == 0 and stack[k-1][0] == 1:
#             count = count + 1
#             for s in stack:
#                 print(s)
#             print('------')
#     print('count=', count)

#    good_stacks = stats.one_in_row(stacks1,k,nn)
#    if k > 0:
#        good_stacks = stats.none_in_row(good_stacks, k-1, nn)
#    print('row', k, 'num good', len(good_stacks))

#stacks = [[ [1], [1, 1], [1, 0, 1], [0, 0, 1, 1]],]



### Compare the stats of first SST column versus rest to ASM column deletion. Are they the same?

nn = 2
#stacks = build.build_stacks(nn)
#stacks = stats.cols_weak_increasing(stacks,nn)
#stacks = stats.rows_weak_decreasing(stacks,nn)
#for kk in range(nn+1):
#    good_stacks1 = stats.has_num_ones_in_last_diag(stacks,kk)
#    good_stacks2 = stats.has_num_ones_in_last_diag(stacks,nn-kk)
#    print(kk, 'ones=', len(good_stacks1), ' and ', (nn-kk), 'ones=', len(good_stacks2))

#print_stack_list(stacks)



#for nn in range(3,4):
#    print('size', nn)
    #stacks = build.build_opp_gapless_gog_word_stacks(nn)
    #stacks = build.build_opp_stacks(nn)
    #for s in stacks:
    #    for x in s:
    #        print(x)
    #    print('----')
    #print('num gapless', len(stacks))




def start_of_row_stats(nn):
    print(nn)
    my_set = set()
    stacks2 = build.build_stacks(nn)
    for s in stacks2:
        #for x in s:
        #    print(x)
        #print('----')
        key = 0
        for idx,row in enumerate(s):
            if 0 in row:
                val = row.index(0)+1
            else:
                val = 0
            key = 10**(idx) * val + key
        my_set.add(key)

    #for key in my_set:
    #    print(key)

    print('len key=',len(my_set))



    print('num sst', len(stacks2))

    # the non-permutations: more than one 1 in a row
    # bad_stacks = []
    # for s in stacks2:
    #     good = True
    #     for x in s:
    #         if sum(x) > 1:
    #             good = False
    #             break
    #     if good == False:
    #         bad_stacks.append(s)

    #for b in bad_stacks:
        #for x in b:
            #print(x)
        #print('----')
    #print(len(bad_stacks))

    #stacks3 = []
    #for s in stacks:
    #    if s in stacks2:
    #        stacks3.append(s)

    #print('in both: ', len(stacks3))
    #print('in sst only: ', len(stacks2) -  len(stacks3))
    print('--------')



ogog3 = [[[0], [0, 0], [0, 0, 0]], [[1], [0, 0], [0, 0, 0]], [[0], [0, 1], [0, 0, 0]], [[1], [0, 1], [0, 0, 0]], [[2], [0, 1], [0, 0, 0]], [[1], [1, 1], [0, 0, 0]], [[2], [1, 1], [0, 0, 0]], [[0], [0, 0], [0, 0, 1]], [[1], [0, 0], [0, 0, 1]], [[0], [0, 1], [0, 0, 1]], [[1], [0, 1], [0, 0, 1]], [[2], [0, 1], [0, 0, 1]], [[1], [1, 1], [0, 0, 1]], [[2], [1, 1], [0, 0, 1]], [[0], [0, 2], [0, 0, 1]], [[1], [0, 2], [0, 0, 1]], [[2], [0, 2], [0, 0, 1]], [[3], [0, 2], [0, 0, 1]], [[1], [1, 2], [0, 0, 1]], [[2], [1, 2], [0, 0, 1]], [[3], [1, 2], [0, 0, 1]], [[0], [0, 1], [0, 1, 1]], [[1], [0, 1], [0, 1, 1]], [[2], [0, 1], [0, 1, 1]], [[1], [1, 1], [0, 1, 1]], [[2], [1, 1], [0, 1, 1]], [[0], [0, 2], [0, 1, 1]], [[1], [0, 2], [0, 1, 1]], [[2], [0, 2], [0, 1, 1]], [[3], [0, 2], [0, 1, 1]], [[1], [1, 2], [0, 1, 1]], [[2], [1, 2], [0, 1, 1]], [[3], [1, 2], [0, 1, 1]], [[2], [2, 2], [0, 1, 1]], [[3], [2, 2], [0, 1, 1]], [[1], [1, 1], [1, 1, 1]], [[2], [1, 1], [1, 1, 1]], [[1], [1, 2], [1, 1, 1]], [[2], [1, 2], [1, 1, 1]], [[3], [1, 2], [1, 1, 1]], [[2], [2, 2], [1, 1, 1]], [[3], [2, 2], [1, 1, 1]]]


def flip_ogog_list(ogogs):
    return [flip_ogog(ogog) for ogog in ogogs]

def flip_ogog(ogog):
    print(ogog)
    size = len(ogog)
    ret_val = [[0] * k for k in range(1,size+1)]
    print(ret_val)
    for i in range(size):
        for j in range(i+1):
            print(i,j,'to', size-1+i-j, j)
            ret_val[i][j] = ogog[size-1+j-i][j]
    return ret_val


def compare_plateau_to_gog():
    for nn in range(4,5):
        sst = build.build_stacks(nn)
        stacks = build.build_plateaus(sst,nn)
        #print_stack_list(stacks)
        #stacks = stats.one_one_per_row(stacks, nn)
        #print(len(stacks))
        #print_stack_list(stacks)
        #print(stack_list_to_tex(stacks))

        #start_of_row_stats(nn)

        temp_list =[]
        # [ [a], [b,c], [d, e, f] ] to [ [d], [b, e], [a, c, f]]
        for stack in stacks:
            temp = [[ stack[2][0]], [stack[1][0], stack[2][1]],  [stack[0][0], stack[1][1], stack[2][2]]]
            temp_list.append(temp)

        # [ [a], [b,c], [d, e, f] ] to [ [d], [e, b], [f, c, a]]
        #for stack in stacks:
        #    temp = [[ stack[2][0]], [stack[2][1], stack[1][0]],  [stack[2][2], stack[1][1], stack[0][0]]]
        #    temp_list.append(temp)

        print_stack_list(stacks)

        #for temp,stack in zip(temp_list,sst):
        #    if temp not in ogog3:
        #        print('no', temp, stack)
        #    else:
        #        print('yes')

## this one didn't go anywhere
def compare_plateau_to_gog_two():
    for nn in range(3, 4):
        sst = build.build_stacks(nn)
        temp_list = []
        for stack in sst:
            temp = [[stack[2][0]], [stack[1][0], stack[2][1]], [stack[0][0], stack[1][1], stack[2][2]]]
            temp_list.append(temp)

        # print_stack_list(temp_list)

        plateau_stacks = build.build_plateaus(temp_list, nn)
        # print_stack_list(stacks)
        # stacks = stats.one_one_per_row(stacks, nn)
        # print(len(stacks))
        # print_stack_list(stacks)
        # print(stack_list_to_tex(stacks))

        # start_of_row_stats(nn)

        print_stack_list(temp_list)

        #for plateau, stack in zip(plateau_stacks, stacks):
        #    if plateau not in ogog3:
        #        print('no', plateau, stack)
        #    else:
        #        print('yes', plateau)

def compare_pst():
    pst = build.build_pst(3)
    #for x in pst:
    #    print(x)
    #print(len(pst))

    plat = build.build_plateaus(build.build_stacks(3), 3)
    print(len(plat))

    print('plateaus not pst are:')
    for p in plat:
        if p not in pst:
            print(p)

    flipped_ogogs = flip_ogog_list(ogog3)


    print('ogogs are')
    for ogog in ogog3:
        print(ogog)

    print('flipped ogogs not pst are:')
    for f in flipped_ogogs:
        if f not in pst:
            for row in f:
                print(f)

# pst_map = dict()
# ogog_map = dict()
#
# for p in pst:
#     count = 0
#     for row in p:
#         count = count + sum(row)
#     if count not in pst_map:
#         pst_map[count] = 1
#     else:
#         pst_map[count] = pst_map[count] + 1
#
# for g in ogog3:
#     count = 0
#     for row in g:
#         count = count + sum(row)
#     if count not in ogog_map:
#         ogog_map[count] = 1
#     else:
#         ogog_map[count] = ogog_map[count]+1
#
#
# for key in pst_map:
#     print(key, 'pst', pst_map[key], 'ogog', ogog_map[key])




#### What is the length of the last row?
# for nn in range(2,7):
#     stacks = build.build_stacks(nn)
#     stat_list = stats.last_row_len_stats(stacks, nn)
#     comp_stat_list = [stat_list[0]]
#     for idx in range(1,nn+1):
#         comp_stat_list.append(comp_stat_list[idx-1] + stat_list[idx])
#     print(nn, comp_stat_list, sum(stat_list))


# 0: 1
# 1: n
# 2: 	a(n) = (n+1)*(n+3)*(n+8)/6.
# 3:
#
# 0: 1
# 1: n+1
# 2: 	a(n) = (n-1)*n*(n+4)/6
# 3:
### How many permutations have more 1's in row i than in row i+1?
def more_ones_in_row(stacks, nn):
    perm_stacks = stats.cols_weak_increasing(stacks,nn)
    data = []

    print('got perms', len(perm_stacks))

    for i in range(nn):
        current_data = []
        print('--- row', i)
        for j in range(i,i+1):
            good_stacks = stats.at_least_one_more_in_row_after_col(perm_stacks,i,j,nn)
            print('row', i, 'col', j, 'num', len(good_stacks))
            current_data.append(len(good_stacks))
            # for gs in good_stacks:
            #     print('good')
            #     for g in gs:
            #         print('\t',g)
            #     print('******')
            # for p in perm_stacks:
            #     if p not in good_stacks:
            #         print('bad')
            #         for g in p:
            #             print('\t', g)
            #         print('******')
        data.append(current_data)
        print('------')

    for r in data:
        print(r)

#for idx,s in enumerate(good_stacks):
#    print(idx+1)
#    for x in s:
        #temp = []
        #temp = [xx for xx in reversed(x)]
        #print(temp)
#        print(x)
#    print('######')



#good_stacks2 = rows_weak_decreasing(nn)

#for s in good_stacks2:
#    for x in s:
#        print(x)
#    print('------')
#print(len(good_stacks2))

#13|2
#123
#1|23
#1|2|3
#12|3

#all_stacks = build.build_stacks(nn)
#for s in all_stacks:
#    for x in s:
#        print(x)
#    print('------')
#print(len(all_stacks))

#stacks2 = build.build_stacks(nn)
#good_stacks2 = one_one_per_col(stacks2,nn)
#print(len(good_stacks2))

##############
###### EXPLORE ZEROS AND HOOKS

# number of -1's in ASM is 1,20,434, 13052, 591708

#explore_zeros_and_ells(5) #5= 150, 13124

#explore_zeros_and_hooks(4)

nn = 3
stacks = build.build_stacks(nn)
#stacks = stats.has_num_zero_below_one(stacks,2,nn )

print_stack_list(stacks)

print(len(stacks))