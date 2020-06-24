from stackset import build_stack_sets as build
from stackset import stack_set_stats as stats


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

nn = 4
#stacks = build.build_stacks(nn)
stacks = build.build_inverted_stacks(nn)
#stacks0 = stats.one_one_per_col_fixed(stacks,nn)
stacks0 = stats.one_one_per_row(stacks, nn)
#good_stacks = stats.one_one_per_diag(stacks0,nn)
#good_stacks = stats.one_one_per_row(stacks0,nn)
#good_stacks = stats.cols_weak_decreasing(stacks,nn)
#good_stacks = stats.reflect_is_sst(stacks,nn)
good_stacks = stacks0
#good_stacks = stats.invert_is_sst(stacks, nn)


#for idx,s in enumerate(good_stacks):
#    print(idx+1)
#    for x in s:
        #temp = []
        #temp = [xx for xx in reversed(x)]
        #print(temp)
#        print(x)
#    print('######')
print(len(good_stacks))


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



