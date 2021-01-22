import triangle.build_ballot_triangle as bt
import triangle.build_tss as tss


def get_diag_count(triangle):
    size = len(triangle)
    diag_count = []

    for i in range(size):
        sum = 0
        for j in range(i+1):
            sum = sum + triangle[i-j][j]
        diag_count.append(sum)

    return diag_count





def compare_diag_counts(tss_list, bt_list):
    tss_count_map = dict()
    bt_count_map = dict()

    for t in tss_list:
        diag_str = str(get_diag_count(t))

        if not diag_str in tss_count_map:
            tss_count_map[diag_str] = 0

        tss_count_map[diag_str] = tss_count_map[diag_str] + 1

        if diag_str == "[2, 3, 3, 1]" and t not in bt_list:
            print('begin tss')
            print_triangle(t)

    for t in bt_list:
        diag_str = str(get_diag_count(t))

        if not diag_str in bt_count_map:
            bt_count_map[diag_str] = 0

        bt_count_map[diag_str] = bt_count_map[diag_str] + 1

        if diag_str == "[2, 3, 3, 1]" and t not in tss_list:
            print('begin bt')
            print_triangle(t)

    print('tss - btt')
    count_set = set()
    for key in tss_count_map:
        print(key, tss_count_map[key] - bt_count_map[key], tss_count_map[key], bt_count_map[key])
        if not tss_count_map[key] == bt_count_map[key]:
            print('>>>>>>>>> FAIL')
        count_set.add(tss_count_map[key])

    print(count_set)


def print_triangle(t):
    for row in t:
        print(row)
    print('-------')


def shift(big_row_in, small_row_in):
    big_row = [x for x in big_row_in]
    small_row = [x for x in small_row_in]

    for idx in range(len(small_row)):
        print('handling index', idx)
        print('\t', big_row)
        print('\t', small_row)
        delta = 0
        if small_row[idx] == big_row[idx] -2:
            # need a change of -2 in big_row to be our witness
            if big_row[idx+1] == big_row[idx]:
                delta = 2
            else:
                delta = 1
        elif small_row[idx] < big_row[idx] -2:
            # changing by at least 2
            delta = big_row[idx] - small_row[idx] - 1
        else:
            # no change needed here
            delta = 0

        if delta > 0:
            print('change needed for index', idx)
            change_idx = idx
            change_delta = delta

            while (small_row[change_idx]+delta > small_row[change_idx-1] and change_idx > 0):
                print('could not change idx', change_idx, 'delta', delta, 'bigrow', big_row)
                change_idx = change_idx -1
                if big_row[change_idx] ==  big_row[change_idx+1]:
                    change_delta = 2
                else:
                    change_delta = 1

            print('final change_idx:', change_idx, change_delta)


            big_row, small_row =  do_shift(big_row, small_row, change_idx, change_delta)
        else:
            print('no change for index', idx)

    return big_row, small_row


def handle_row(triangle, row_idx):
    print_triangle(triangle)

    for idx in range(0,len(triangle[row_idx])):
        print('handling entry index', idx)
        print('\t', triangle[row_idx-1])
        print('\t', triangle[row_idx])
        diff = triangle[row_idx-1][idx] -  triangle[row_idx][idx]


        if diff > 1:
            # need to close the gap: what's the closest row that works?
            found_slack = False
            offset = 1
            delta = diff - 1
            print('delta is', delta)
            while not found_slack:
                print('row_idx', row_idx, 'idx', idx, 'offset', offset, 'offset row', row_idx-offset, 'offset col', idx+offset)
                print('want slack', delta, 'for', idx+offset, triangle[row_idx-offset], triangle[row_idx-offset][idx+offset])
                if  triangle[row_idx-offset][idx+offset] >= delta:
                    if delta > 1:
                        found_slack = True
                        print('aaaaa')
                    elif triangle[row_idx-offset][idx+offset - 1] > triangle[row_idx-offset][idx+offset]:
                        print('\t', triangle, row_idx-offset, idx+offset)
                        found_slack = True
                        print('bbbb')
                    elif triangle[row_idx-offset][idx+offset] >= 2:
                        #  found the delta = 2 to create gap
                        delta = 2
                        found_slack = True
                        print('ccccc')
                    else:
                        offset = offset + 1
                        print('ddddd')
                else:
                    offset = offset + 1
                    print('eeeee')

                if offset > row_idx:
                    # didn't find the slack we need!
                    raise IndexError('Did not find slack we need row_idx=', row_idx, 'idx=', idx, 'triangle', triangle )

            triangle = fix_gap(triangle, row_idx, idx, offset, delta)
        else:
            print('\tno change needed')

    return triangle




def fix_gap(triangle, row_idx, idx, offset, delta):
    print('fixing gap for row_idx', row_idx, 'idx', idx, 'offset', offset, 'delta', delta, triangle)

    change_idx = idx
    change_delta = delta
    big_row = triangle[row_idx - offset]
    small_row = triangle[row_idx]

    # look for an entry diagonally above that has blocks to spare
    while (small_row[change_idx] + delta > small_row[change_idx - 1] and change_idx > 0):
        print('could not change idx', change_idx, 'delta', delta, 'bigrow', big_row)
        change_idx = change_idx - 1
        if big_row[change_idx + offset] == big_row[change_idx + offset + 1]:
            change_delta = 2
        else:
            change_delta = 1

    print('final change_idx:', change_idx, change_delta)

    new_big_row, new_small_row = do_fix_gap(big_row, small_row, offset, change_idx, change_delta)

    triangle[row_idx-offset] = new_big_row
    triangle[row_idx] = new_small_row

    print('\tupdated', triangle)

    return triangle

def do_fix_gap(big_row, small_row, offset, change_idx,  change_delta):
    #big_value = big_row[change_idx +offset] - change_delta
    #print('big value', big_value, big_row)

    # move as much as possible until the end
    end_idx = len(small_row)

    for j in range(change_idx, end_idx):
        print(j, big_row, small_row)
        change = min(change_delta, big_row[j+offset], len(small_row) - j - small_row[j])
        big_row[j + offset] = big_row[j+offset] - change
        small_row[j] = small_row[j] + change
        print('j', j, 'change', change)


    # if big_value in big_row:
    #     end_idx = len(big_row) - big_row[::-1].index(big_value) -  offset
    #     print('end_idx', end_idx)
    #     #end_idx = big_row.index(big_value) -  offset
    # else:
    #     end_idx = len(small_row)
    #
    # # how much do we move now?
    # for j in range(change_idx, end_idx):
    #     print(j, big_row, small_row)
    #     change = big_row[j + offset] - big_value
    #     big_row[j +  offset] = big_value
    #     small_row[j] = small_row[j] + change
    #     print('j',j, 'change', change)

    return big_row, small_row


def do_shift(big_row, small_row, idx, delta):
    big_value = big_row[idx + 1] - delta
    if big_value in big_row:
        end_idx = big_row.index(big_value)
    else:
        end_idx = len(big_row)

    for j in range(idx + 1, end_idx):
        change = big_row[j] - big_value
        big_row[j] = big_value
        small_row[j - 1] = small_row[j - 1] + change

    return big_row, small_row


def map_tss_to_bt(tss_in):
    tss = [[x for x in row] for row in tss_in]

    # for i in reversed(range(len(tss) - 1)):
    #     print('i=', i)
    #     for j in range(i, len(tss) - 1):
    #         print('\tj=', j)
    #         big_row, small_row = shift(tss[j], tss[j + 1])
    #         tss[j] = big_row
    #         tss[j + 1] = small_row
    #     print(tss)

    for i in range(1, len(tss)):
        print('i=', i)
        for j in reversed(range(1,i+1)):
            tss = handle_row(tss, j)
        print(tss)

    return tss


n = 4



tss_list = tss.build_tss(n)
bt_list = bt.build_bt(n)



tss_str_list = set([str(t) for t in tss_list])
bt_str_list = set([str(t) for t in bt_list])


#temp = sorted([1, 2, 4, 132, 8, 266, 14, 16, 272, 24, 28, 32, 160, 164, 424, 48, 688, 436, 56, 1720, 712, 80, 2640, 1112, 96])
#print(temp)

#compare_diag_counts(tss_list, bt_list)

count = 0
print('>>>>>>>> tss only')
for t in tss_list:
    if t not in bt_list:
        count+=1
       # print_triangle(t)

# print('>>>>>>>> bt only')
# for t in bt_list:
#     if t not in tss_list:
#         print_triangle(t)

#print(2**(n*(n+1)/2) - count)

#print(count)


#compare_diag_counts(tss_list, bt_list)


#big_row = [2,2,2,1]
#small_row  = [1,0,0]

# big_row = [5,4,4,4,4,3,2,1,0]
# small_row  = [4,3,3,2,2,1,1,1]
# #small_row  = [4,4,4,2,2,1,1,1]
#
# new_big_row, new_small_row = shift(big_row, small_row)
#
#
# print('before')
# print(big_row)
# print(small_row)
# print('after')
# print(new_big_row)
# print(new_small_row)




# error_count = 0
#
# out_str_set = set()
#
# for t in tss_list:
#     out = map_tss_to_bt(t)
#     print('>>>>before')
#     print_triangle(t)
#     print('>>>>after')
#     print_triangle(out)
#
#     if not out in bt_list:
#         print('################## ERROR not in bt_list')
#         error_count = error_count + 1
#
#     if str(out) in out_str_set:
#         print('duplicate!', out)
#     else:
#         out_str_set.add(str(out))
#
# print('errors: ', error_count)
# print(len(out_str_set))


#
# #t = [[3, 2, 1], [1, 0], [0]]
# t = [[3, 2, 1],[1, 1],[1]]
t = [[3, 2, 1, 0], [1, 1, 0], [0, 0], [0]]
out = map_tss_to_bt(t)
#
#
print_triangle(t)
#
print_triangle(out)


#print(do_fix_gap([3,2,1,1], [1,0,0], 1, 0,  1))

