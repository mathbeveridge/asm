from stackset import build_stack_sets as build
from stackset import stack_set_stats as stats
from stackset import hook as hook

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

# an ell is of the form [[a,b], [c,d]] where a < c and b < d
# the zero of the ell is at [c,d]
# there are only ones above the zero
# there may be zeros and then ones to the right of the zero.
# BUT FOR NOW I don't allow any zeros to the right.
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
                #print('\t b starts at', j)
                while stack[i][b] == 0:
                    b = b  + 1
                    #print('\t\tb 0 is now', b)
                while b < i and stack[i][b+1] == 1:
                    b = b + 1
                    #print('\t\tb 1 is now', b)

                #print('\tb is', b)

                ell_list. append([[a,j], [i,b]])


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

    stacks = build.build_stacks(n)
    #stacks = [ [ [1], [1, 0], [1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 1, 1]], ]
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
            hooks = [ hook.Hook(ell[0], ell[1]) for ell in ells]

            for s in stack:
                print('\t\t', s)

            for pair in itertools.combinations(hooks, 2):
                if pair[0].update_comparison(pair[1]):
                    print('comparable', pair[0].toString(), pair[1].toString())
                    compare_count = compare_count + 1


            for h in hooks:
                if h.is_minimal() and h.has_hooks_above():
                    total_min_nested_hooks  = total_min_nested_hooks + h.get_num_directly_above()
                    if len(h.hooks_above) > 1:
                        print('>>>>>>>', h.toString(), 'nests', len(h.hooks_above))
                        print('\t\tand directly above =', h.get_num_directly_above())


        # if z == 2:
        #    for x in stack:
        #        print(x)
        #    print('---------')

    print('total min nested hooks', total_min_nested_hooks)
    print('total comparable hooks', compare_count)
    print('total zeros', total_zeros)
    total = total_zeros + total_min_nested_hooks
    print('total', total)
    for key in zero_map:
        print(key, 'zeros:', zero_map[key])




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

#nn = 5
#stacks = build.build_stacks(nn)
#stacks = build.build_inverted_stacks(nn)
#stacks0 = stats.one_one_per_col_fixed(stacks,nn)
#stacks0 = stats.one_one_per_row(stacks, nn)
#good_stacks = stats.one_one_per_diag(stacks,nn)
#good_stacks = stats.one_one_per_row(stacks0,nn)
#good_stacks = stats.cols_weak_decreasing(stacks,nn)
#good_stacks = stats.reflect_is_sst(stacks,nn)
#good_stacks = stacks
#good_stacks = stats.invert_is_sst(stacks, nn)


# number of -1's in ASM is 1,20,434, 13052, 591708

#explore_zeros_and_ells(4) #5= 150, 13124

explore_zeros_and_hooks(4)


#stacks = [[ [1], [1, 1], [1, 0, 1], [0, 0, 1, 1]],]



### Compare the stats of first SST column versus rest to ASM column deletion. Are they the same?

#kk = 3
#good_stacks1 = stats.has_num_ones_in_first_col(stacks,kk)
#good_stacks2 = stats.has_num_ones_in_first_col(stacks,nn-kk)
#print(kk, 'ones=', len(good_stacks1), ' and ', (nn-kk), 'ones=', len(good_stacks2))


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

