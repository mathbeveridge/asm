import triangle.build_ballot_triangle as bbt
import triangle.build_tss as btss
import triangle.array_util as util



def boost(triangle):
    boosted = [[x + idx for idx,x in enumerate(row)] for row in triangle]

    boosted = [[ x for x in reversed(row)] for row in boosted]

    return boosted


def get_boosted_tss(size):
    tss_list = btss.build_tss(size)

    boosted_list  = [boost(t) for t in tss_list]

    return boosted_list

def get_boosted_fbt(size):
    bt_list = bbt.build_bt(size)

    boosted_list  = [boost(util.flip_triangle2(t)) for t in bt_list]

    return boosted_list



# Works for n=3
def handle_row_with_col_max_v1(triangle, row_idx, col_max_idx, debug=False):
    big_row = triangle[row_idx-1]
    small_row = triangle[row_idx]
    size = len(small_row)

    if debug:
        print('handling row,col_max', small_row, col_max_idx)

    level_start_idx = size
    is_crossed = False
    is_level = False

    for idx in range(col_max_idx):
        if debug:
            print('handling idx', idx)

        if is_crossed:
            # we are crossed, so we must update both paths until
            # we are no longer crossed
            diff = small_row[idx] - big_row[idx]
            if diff >= 0 :
                small_row[idx] = small_row[idx] - diff - 1
                big_row[idx] = big_row[idx] + diff + 1
            elif diff < 0:
                # reset
                is_crossed = False
                is_level = False
                level_start_idx = size
            else:
                raise ValueError('Small row cannot jump from crossed to uncrossed')

        elif is_level:
            if not small_row[idx] == big_row[idx]:
                # paths no longer touch (and didn't cross)

                # did we share any diagonals before diverging?
                if small_row[level_start_idx] > small_row[idx-1]:
                    # handle all the level steps up to this one
                    for k in range(level_start_idx, idx):
                        small_row[k] = small_row[k] - 1
                        big_row[k] = big_row[k] + 1

                is_level = False
                level_start_idx = size
            elif idx == col_max_idx-1:
                if small_row[level_start_idx] > small_row[idx]:
                    # handle all the level steps up to this one
                    # ZZZZZZZZZ
                    if big_row[idx+1] == big_row[idx]:
                        end_idx = idx
                    else:
                        end_idx = idx+1
                    for k in range(level_start_idx, end_idx):
                        small_row[k] = small_row[k] - 1
                        big_row[k] = big_row[k] + 1

                    is_level = False
                    level_start_idx = size


        elif small_row[idx] == big_row[idx]:
            # paths touch  (and were not already crossing)
            # if they transition to crossing, we must update back
            # to where they first touched
            is_level = True
            level_start_idx = idx

        if debug:
            print('checking ', idx, small_row)


        if is_level:
            if idx == col_max_idx-1:
                if small_row[idx] > big_row[idx+1]:
                    #crosses after small row ends
                    #if idx == 0 or big_row[idx-1] - small_row[idx-1] == 1:
                    is_crossed = True
                # shares_next_diag = False
            else:

                #shares_next_diag = False

                if small_row[idx + 1] > big_row[idx + 1]:
                    # crosses at the next step
                    is_crossed = True
                elif small_row[idx + 1] == big_row[idx +1] and small_row[idx +1] < small_row[idx]:
                    # cannot share diagonal step
                    pass
                    #shares_next_diag = True

            if is_crossed:
                if not small_row[idx] - 1 == big_row[idx+1]:
                    print('>>>>>>>>WARNING: Small row is more than one below big row!!!')

                # handle all the level steps up to this one
                for k in range(level_start_idx, idx+1):
                    small_row[k] = small_row[k] - 1
                    big_row[k] = big_row[k] + 1

                is_level = False
                level_start_idx = size


    return triangle



# comb from fbt to tss
# fails on n=4 need to fix how to handle [[2,1,1],[2,1],[1]]
# don't go direct
## oops! added crossed delta
def handle_row_with_col_max_v2(triangle, row_idx, col_max_idx, debug=False):
    big_row = triangle[row_idx-1]
    small_row = triangle[row_idx]
    size = len(small_row)

    if debug:
        print('handling row,col_max', small_row, col_max_idx)


    level_start_idx = size
    is_crossed = False
    crossed_delta = 0
    is_level = False

    for idx in range(col_max_idx):
        if debug:
            print('handling idx', idx)

        if is_crossed:
            # we are crossed, so we must update both paths until
            # we are no longer crossed
            diff = small_row[idx] - big_row[idx]
            if diff >= 0 :
                # delta must weakly increase
                crossed_delta = max(crossed_delta, diff)
                small_row[idx] = small_row[idx] - crossed_delta - 1
                big_row[idx] = big_row[idx] + crossed_delta + 1
            elif diff < 0:
                # reset
                is_crossed = False
                crossed_delta = 0
                is_level = False
                level_start_idx = size
            else:
                raise ValueError('Small row cannot jump from crossed to uncrossed')

        elif is_level:
            if not small_row[idx] == big_row[idx]:
                # paths no longer touch (and didn't cross)

                # did we share any diagonals before diverging?
                # CHANGE: added delta!
                if small_row[level_start_idx] > small_row[idx-1]:
                    # handle all the level steps up to this one
                    for k in range(level_start_idx, idx):
                        delta = small_row[level_start_idx] - small_row[k]
                        small_row[k] = small_row[k] - 1 - delta
                        big_row[k] = big_row[k] + 1 + delta

                    # will this break n=3????
                    small_row[idx] = small_row[idx] - 1 - delta
                    big_row[idx] = big_row[idx] + 1 + delta

                is_level = False
                level_start_idx = size
            elif idx == col_max_idx-1:
                if small_row[level_start_idx] > small_row[idx]:
                    # handle all the level steps up to this one
                    # ZZZZZZZZZ
                    if big_row[idx+1] == big_row[idx]:
                        end_idx = idx
                    else:
                        end_idx = idx+1
                    for k in range(level_start_idx, end_idx):
                        small_row[k] = small_row[k] - 1
                        big_row[k] = big_row[k] + 1

                    is_level = False
                    level_start_idx = size


        elif small_row[idx] == big_row[idx]:
            # paths touch  (and were not already crossing)
            # if they transition to crossing, we must update back
            # to where they first touched
            is_level = True
            level_start_idx = idx

        if debug:
            print('checking ', idx, small_row)


        if is_level:
            if idx == col_max_idx-1:
                if small_row[idx] > big_row[idx+1]:
                    #crosses after small row ends
                    #if idx == 0 or big_row[idx-1] - small_row[idx-1] == 1:
                    is_crossed = True
                # shares_next_diag = False
            else:

                #shares_next_diag = False

                if small_row[idx + 1] > big_row[idx + 1]:
                    # crosses at the next step
                    is_crossed = True
                    crossed_delta = 0
                elif small_row[idx + 1] == big_row[idx +1] and small_row[idx +1] < small_row[idx]:
                    # cannot share diagonal step
                    pass
                    #shares_next_diag = True

            if is_crossed:
                if not small_row[idx] - 1 == big_row[idx+1]:
                    print('WARNING: Small row is more than one below big row!!!')

                # handle all the level steps up to this one
                for k in range(level_start_idx, idx+1):
                    small_row[k] = small_row[k] - 1
                    big_row[k] = big_row[k] + 1

                is_level = False
                level_start_idx = size


    return triangle


# comb from fbt to tss
# this is a failed attempt to handle [2,0],[1] "properly." Ugh
def handle_row_with_col_max_v3(triangle, row_idx, col_max_idx, debug=False):
    big_row = triangle[row_idx-1]
    small_row = triangle[row_idx]
    size = len(small_row)

    if debug:
        print('handling row,col_max', small_row, col_max_idx)


    level_start_idx = size
    is_crossed = False
    is_level = False

    for idx in range(col_max_idx):
        if debug:
            print('handling idx', idx)

        if is_crossed:
            # we are crossed, so we must update both paths until
            # we are no longer crossed
            diff = small_row[idx] - big_row[idx]
            if diff >= 0 :
                small_row[idx] = small_row[idx] - diff - 1
                big_row[idx] = big_row[idx] + diff + 1
            elif diff < 0:
                # reset
                is_crossed = False
                is_level = False
                level_start_idx = size
            else:
                raise ValueError('Small row cannot jump from crossed to uncrossed')

        elif is_level:
            if not small_row[idx] == big_row[idx]:
                # paths no longer touch (and didn't cross)

                # did we share any diagonals before diverging?
                # CHANGE: added delta!
                if small_row[level_start_idx] > small_row[idx-1]:
                    # handle all the level steps up to this one

                    # new change: only do diagonal
                    start_idx = idx - 1
                    while start_idx > 1 and small_row[start_idx-1] > small_row[start_idx]:
                        start_idx = start_idx - 1

                    for k in range(start_idx, idx):
                        delta = small_row[start_idx] - small_row[k]
                        small_row[k] = small_row[k] - 1 - delta
                        big_row[k] = big_row[k] + 1 + delta

                    # will this break n=3???? nope!
                    small_row[idx] = small_row[idx] - 1 - delta
                    big_row[idx] = big_row[idx] + 1 + delta

                is_level = False
                level_start_idx = size
            elif idx == col_max_idx-1:
                if small_row[level_start_idx] > small_row[idx]:
                    # handle all the level steps up to this one
                    if big_row[idx+1] < big_row[idx]:
                        small_row[idx] = small_row[idx] - 1
                        big_row[idx] = big_row[idx] + 1

                    # new code for n=4
                    # process in reverse until the end of the diagonal

#                    for k in range(level_start_idx, idx):
#                        small_row[k] = small_row[k] - 1
#                        big_row[k] = big_row[k] + 1

                    is_level = False
                    level_start_idx = size


        elif small_row[idx] == big_row[idx]:
            # paths touch  (and were not already crossing)
            # if they transition to crossing, we must update back
            # to where they first touched
            is_level = True
            level_start_idx = idx

        if debug:
            print('checking ', idx, small_row)


        if is_level:
            if idx == col_max_idx-1:
                # HACK ALERT: Seeing if we can get col 1 working
                if col_max_idx > 1:
                    if small_row[idx] > big_row[idx+1]:
                        #crosses after small row ends
                        #if idx == 0 or big_row[idx-1] - small_row[idx-1] == 1:
                        is_crossed = True

                # shares_next_diag = False
            else:

                #shares_next_diag = False

                if small_row[idx + 1] > big_row[idx + 1]:
                    # crosses at the next step
                    is_crossed = True
                elif small_row[idx + 1] == big_row[idx +1] and small_row[idx +1] < small_row[idx]:
                    # cannot share diagonal step
                    pass
                    #shares_next_diag = True

            if is_crossed:
                if not small_row[idx] - 1 == big_row[idx+1]:
                    raise ValueError('Small row is more than one below big row!!!')

                # handle all the level steps up to this one
                for k in range(level_start_idx, idx+1):
                    small_row[k] = small_row[k] - 1
                    big_row[k] = big_row[k] + 1

                is_level = False
                level_start_idx = size

    # HACK to fix in column 1
    # probably need to deal with other columns too
    if col_max_idx == 1:
        if small_row[0] > big_row[1]:
            diff = small_row[0] - big_row[1]
            small_row[0] = small_row[0] - diff

            # spread diff among rows above
            for k in reversed(range(0, row_idx)):
                if k == 0:
                    temp = len(triangle)
                else:
                    temp = triangle[k-1][0] -1
                temp = max(0, temp - triangle[k][0])
                delta = min(temp, diff)
                triangle[k][0] = triangle[k][0] + delta
                diff  = diff - delta
                if diff == 0:
                    break

            if not diff == 0:
                raise ValueError('diff is not zero!!!')




    return triangle






# comb from fbt to tss
# adapted from v2 to try to address errors for n=4
# don't go direct
def handle_row_with_col_max_v4(triangle, row_idx, col_max_idx, debug=False):
    big_row = triangle[row_idx-1]
    small_row = triangle[row_idx]
    size = len(small_row)

    if debug:
        print('handling row,col_max', small_row, col_max_idx)


    level_start_idx = size
    is_crossed = False
    is_level = False
    crossed_delta = 0

    for idx in range(col_max_idx):
        if debug:
            print('handling idx', idx)

        if is_crossed:
            # we are crossed, so we must update both paths until
            # we are no longer crossed
            diff = small_row[idx] - big_row[idx]
            if diff >= 0 :
                if diff < crossed_delta:
                    print(">>>>>>>>>>> diff less than crossed_delta", diff, crossed_delta)
                crossed_delta = max(crossed_delta, diff)
                small_row[idx] = small_row[idx] - diff - 1
                big_row[idx] = big_row[idx] + diff + 1
            elif diff < 0:
                # reset
                is_crossed = False
                is_level = False
                level_start_idx = size
                crossed_delta = 0
            else:
                raise ValueError('Small row cannot jump from crossed to uncrossed')

        elif is_level:
            if not small_row[idx] == big_row[idx]:
                # paths no longer touch (and didn't cross)

                # did we share any diagonals before diverging?
                # CHANGE: added delta!

                # DON'T THINK WE NEED THIS
                # if small_row[level_start_idx] > small_row[idx-1]:
                #     # handle all the level steps up to this one
                #     for k in range(level_start_idx, idx):
                #         delta = small_row[level_start_idx] - small_row[k]
                #         small_row[k] = small_row[k] - 1 - delta
                #         big_row[k] = big_row[k] + 1 + delta
                #
                #     # will this break n=3????
                #     small_row[idx] = small_row[idx] - 1 - delta
                #     big_row[idx] = big_row[idx] + 1 + delta

                is_level = False
                level_start_idx = size
            elif idx == col_max_idx-1:
                if small_row[level_start_idx] > small_row[idx]:
                    #raise ValueError("I think this should never happen")
                    # handle all the level steps up to this one
                    # ZZZZZZZZZ
                    if big_row[idx+1] == big_row[idx]:
                        end_idx = idx
                    else:
                        end_idx = idx+1
                    for k in range(level_start_idx, end_idx):
                        small_row[k] = small_row[k] - 1
                        big_row[k] = big_row[k] + 1

                    is_level = False
                    level_start_idx = size


        elif small_row[idx] == big_row[idx]:
            # paths touch  (and were not already crossing)
            # if they transition to crossing, we must update back
            # to where they first touched
            is_level = True
            level_start_idx = idx

        elif small_row[idx] > big_row[idx]:
            # went immediately to crossing without being level!
            is_crossed = True
            # copied from above. need to clean up the logic
            crossed_delta = small_row[idx] - big_row[idx]
            small_row[idx] = small_row[idx] - crossed_delta - 1
            big_row[idx] = big_row[idx] + crossed_delta + 1



        if debug:
            print('checking ', idx, small_row)


        if is_level:
            if idx == col_max_idx-1:
                if small_row[idx] > big_row[idx+1]:
                    #crosses after small row ends
                    #if idx == 0 or big_row[idx-1] - small_row[idx-1] == 1:
                    is_crossed = True
                    crossed_delta = 0

            else:
                if small_row[idx + 1] > big_row[idx + 1]:
                    # crosses at the next step
                    is_crossed = True
                    crossed_delta = 0

                elif level_start_idx < idx:
                    if small_row[idx - 1] > small_row[idx]:
                        # shared diagonal that we must correct
                        if small_row[idx+1] < small_row[idx] -1:
                            raise ValueError('Diagonal shared step drops more than one!')
                        # probably want to subtract delta :)

                        # cannot share diagonal step
                        # change [2,1,1,1,0],[1,1,1,1,0] to [2,2,2,2,0],[1,0,0,0,0]
                        for k in range(level_start_idx, idx):
                            small_row[k] = small_row[k] - 1
                            big_row[k] = big_row[k] + 1

                        level_start_idx = idx
            if idx > 0:
                if small_row[idx] == big_row[idx]:
                    # still have a diagonal step!
                    # what if this is a diagonal shared after a drop?
                    if small_row[idx-1] > small_row[idx]:
                        print('got to here!')


            if is_crossed:
                if not crossed_delta == 0:
                    raise ValueError("crossed_delta is not zero")
                if small_row[idx] - 1 == big_row[idx+1]:
                    # handle all the level steps up to this one
                    for k in range(level_start_idx, idx+1):
                        small_row[k] = small_row[k] - 1
                        big_row[k] = big_row[k] + 1
                elif small_row[idx] - 2 == big_row[idx+1]:
                    print('got to my hack here')
                    # HACK! let's get it working
                    # really need to rething this argument.
                    # it's gonna fail.
                    for k in range(level_start_idx, idx+1):
                        small_row[k] = small_row[k] - 1
                        big_row[k] = big_row[k] + 1

                    small_row[k] =  small_row[k] - 1
                    smaller_row = triangle[row_idx+1]
                    smaller_row[k] = smaller_row[k] + 1

                else:
                    raise ValueError('WARNING: Small row is more than two below big row!!!')

                is_level = False
                level_start_idx = size


    return triangle




def comb(tss,debug=False):

    size = len(tss)

    triangle = util.clone_array(tss)

    if debug:
        prev = util.clone_array(tss)
        print("COMBING")
        util.print_array(triangle)

    for i in range(1, size):
        if debug:
            print('dealing with row ', i)
        for j in reversed(range(1, i+1)):
            if debug:
                print('\thandling row ', j)
            triangle = handle_row_with_col_max_v4(triangle, j, size-i)

            if debug and not prev == triangle:
                print('>>>>> i,j', i, j)
                util.print_array(triangle)
                prev = util.clone_array(triangle)



    return triangle



def compare(size):


    tss_list = get_boosted_tss(size)
    fbt_list = get_boosted_fbt(size)

    combed_map = dict()



    error_list = []

    for k,t in enumerate(tss_list):
        print(k, 'before')
        util.print_array(t)

        if k % 1000 == 0:
            print('processed', k)

        b = comb(t)

        key =  str(b)
        if not key in combed_map:
            combed_map[key]  = [ t, ]
        else:
            print('REPEAT!!!!', k)
            combed_map[key].append(t)
            print(key, 'mapped from', combed_map[key])

        print('after')
        util.print_array(b)

        if not b in fbt_list:
            print('ERROR NOT IN FBT LIST!', k)
            error_list.append([t,b])
            print(t, 'mapped to', b)

        #print('======================')

    print('num errors', len(error_list))
    for x in error_list:
        print(x[0], x[1], util.get_column_sums(x[0]))


    print('missing')
    for b in fbt_list:
        if not str(b) in combed_map:
            print(b, util.get_column_sums(b))

    print('repeated')
    for k in combed_map:
        x = combed_map[k]
        if len(x) > 1:
            print(k)
            for y in x:
                print('\t', y, util.get_column_sums(y))

    # print('FTB ONLY')
    #
    # for b in fbt_list:
    #     if not b in tss_list:
    #         print(b)
    #
    # print('TSS ONLY')
    #
    # for t in tss_list:
    #     if not t in fbt_list:
    #         print(t)


t_list = get_boosted_tss(3)

#t  = [[2, 1, 1], [2, 2], [0]]
t = [[3, 2, 1, 1], [2, 2, 1], [1, 0], [0]]

bad_tss = [[[2, 2, 1], [2, 2], [0]], [[2, 1, 0], [1, 0], [1]],
           [[2, 1, 1], [1, 0], [1]],
           [[2, 2, 1], [2, 2], [1]], [ [3, 1, 1], [1, 1], [0]],
           [[3, 2, 1], [1, 0], [1]], [[2, 1, 1], [2, 1], [1]] ]


missing_fbt = [[[3,3,1], [1, 1], [0]], [[2, 1, 0], [1, 0], [1]],
           [[3, 1, 1], [1, 0], [0]],
           [[3, 3, 1], [1, 1], [1]], [ [3, 1, 1], [1, 1], [0]],
           [[3, 2, 1], [2, 0], [1]], [[3, 1, 1], [1, 1], [1]] ]


bad_tss = [[[2, 1, 1], [2, 1], [0]], ]

missing_fbt = [[[3, 1, 1], [1, 1], [0]]]


#t = t_list[16]
#t = t_list[17]
#t = t_list[18]

fail_list = []

for k in range(0):
    t = bad_tss[k]
    c = comb(t, True)
    b = missing_fbt[k]

    util.print_array(c)
    util.print_array(b)

    if not c == b:
        fail_list.append(k)

print('failures', fail_list)

t3a = [[2,1,1],[2,1],[1]]
t3b = [[2, 1, 0], [2, 1], [1]]
t3c = [[2, 1, 0], [2, 1], [0]]
t3d = [[2, 1, 0], [1, 1], [1]]
t3e = [[2, 1, 0], [2, 1], [1]]

tx = [[3, 2, 2, 1], [3, 2, 1], [1, 0], [0]]
tx = [[3, 2, 2, 2], [3, 2, 2], [1, 0], [0]] # maps to [[4, 2, 2, 2], [2, 2, 2], [1, 0], [0]]
t53= [[3, 2, 2, 2], [3, 2, 1], [1, 0], [0]]
t5a = [[3, 3, 3, 2], [3, 3, 2], [1, 0], [0]] # maps to [[3, 3, 3, 2], [3, 3, 2], [1, 0], [0]]
t5b = [[3, 2, 1, 1], [2, 2, 1], [2, 2], [0]] # maps to [[4, 4, 1, 1], [2, 1, 1], [1, 1]
t5c = [[3, 2, 2, 1], [3, 2, 1], [2, 2], [0]] # maps to [[4, 4, 2, 1], [3, 1, 1], [1, 1], [0]]
t5d = [[3, 2, 2, 2], [3, 3, 2], [1, 0], [0]]  # maps to [[4, 4, 4, 2], [2, 1, 0], [1, 0], [0]] [7, 5, 4, 2]

t = tx
c = comb(t,debug=True)
util.print_array(c)
print(c)

compare(3)


# fbt = get_boosted_fbt(3)
#
# print('BOOSTED FBT')
#
# for b in fbt:
#     util.print_array(b)