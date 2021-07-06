import triangle.build_ballot_triangle as bbt
import triangle.build_tss as btss
import triangle.array_util as util



def get_boosted_tss_rows(size):
    row_list = btss.get_row_list(size)

    boost_list = [ [x + idx for idx,x in enumerate(row)] for row in row_list]
    boost_list = [ [x for x in reversed(row)]  for row in boost_list]

    return boost_list

def get_boosted_tss_trapezoid(max_row_size, num_rows):
    trap_list  = [[ [ x for x in row],] for row in get_boosted_tss_rows(max_row_size)]

    for idx in range(num_rows-1):
        old_trap_list = util.clone_array(trap_list)
        trap_list = []
        row_list = get_boosted_tss_rows(max_row_size-1 - idx)
        for trap in old_trap_list:
            for row in row_list:
                trap_list.append( trap + [row,])

    return trap_list


def get_boosted_fbt_rows(size):
    row_list = [[size,], [size-1]]

    for idx in range(1, size):
        vals = range(size-1 - idx, size+1)
        old_row_list = row_list
        row_list = []
        for row in old_row_list:
            for k in vals:
                if k <= row[-1]:
                    row_list.append(row + [k,])

    return row_list


def get_boosted_fbt_trapezoid(max_row_size, num_rows):
    trap_list  = [[ row,] for row in get_boosted_fbt_rows(max_row_size)]

    for idx in range(num_rows-1):
        old_trap_list = util.clone_array(trap_list)
        trap_list = []
        row_list = get_boosted_fbt_rows(max_row_size-1 - idx)
        for trap in old_trap_list:
            for row in row_list:
                is_valid = True

                for k in range(max_row_size-1 - idx):
                    if row[k] > trap[-1][k] or row[k] > trap[-1][k+1]:
                        is_valid = False

                if is_valid:
                    trap_list.append( trap + [row,])

    return trap_list




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



                small_row[idx] = small_row[idx] - crossed_delta - 1
                big_row[idx] = big_row[idx] + crossed_delta + 1
            # elif diff == 0:
            #     # let's try this
            #     crossed_delta = crossed_delta - 1
            #     small_row[idx] = small_row[idx] - crossed_delta - 1
            #     big_row[idx] = big_row[idx] + crossed_delta + 1
            else:
                # diff < 0:
                # reset
                is_crossed = False
                is_level = False
                level_start_idx = size
                crossed_delta = 0
                #raise ValueError('Small row cannot jump from crossed to uncrossed')


        elif is_level:
            if not small_row[idx] == big_row[idx]:
                # paths no longer touch (and didn't cross)

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

                        end_idx = idx+1

                        # while small_row[end_idx]  == big_row[end_idx] and end_idx < col_max_idx:
                        #     end_idx += 1

                        # cannot share diagonal step
                        # change [2,1,1,1,0],[1,1,1,1,0] to [2,2,2,2,0],[1,0,0,0,0]
                        for k in range(level_start_idx, end_idx):
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
            #triangle = handle_row_with_col_max_v4(triangle, j, size-i)
            triangle = untangle(triangle, j, size-i)

            if debug and not prev == triangle:
                print('>>>>> i,j', i, j)
                util.print_array(triangle)
                prev = util.clone_array(triangle)



    return triangle


##### the states
ABOVE = 1
LEVEL = 0
CROSSED = -1

def untangle(triangle, row_idx, col_max_idx, debug=False):
    small_row = triangle[row_idx]
    big_row = triangle[row_idx-1]
    size = len(small_row)

    level_start_idx = size
    prev_state = ABOVE
    state = ABOVE
    crossed_delta = 0

    print('untangle', triangle, row_idx, col_max_idx)

    for idx in range(col_max_idx):

        print('handle column', idx)

        # note the previous state
        prev_state = state

        diff = small_row[idx] - big_row[idx]

        # update to the current state
        if diff < 0:
            state = ABOVE
            level_start_idx = size
            crossed_delta = 0
        elif diff == 0:
            if not prev_state == CROSSED:
                state = LEVEL
                if not prev_state == LEVEL:
                    level_start_idx = idx
        else:
            # diff > 0
            state = CROSSED

        # assert statements
        if prev_state == ABOVE:
            if state == LEVEL and idx > 0 and  small_row[idx-1] > small_row[idx]:
                    pass
                    print('Above to level at a diagonal TBD', idx, small_row)
                    ValueError('Above to level at a diagonal TBD')
            elif diff > 0:
                # transition directly from above to below
                pass
                #raise ValueError('Directly from above to below. TBD')

        if prev_state == LEVEL and state == CROSSED:
            if diff > 1:
                raise ValueError('TBD Level to unexpected diff' + str(diff))


        shares_diagonal = (state == LEVEL and small_row[level_start_idx] > small_row[idx])

        # handle the current state
        if state == CROSSED or shares_diagonal:

            post_end_idx = idx

            while post_end_idx < col_max_idx and small_row[post_end_idx] >= big_row[post_end_idx]:
                post_end_idx += 1

            orig_post_end_idx = post_end_idx


            # only need coda for changes that don't create a drop
            coda_start_idx = size
            coda_end_idx = size


            ##### must end with a drop step, so correct if necessary
            need_coda = False
            final_idx = post_end_idx-1
            final_diff = small_row[final_idx] - big_row[final_idx]
            if final_diff == 0 and big_row[final_idx+1] == big_row[final_idx]:
                print('HERE IS THE THING WE MUST FIX!!!!', final_idx)
                print(big_row)
                print(small_row)

                coda_height = small_row[final_idx]

                # not enough heights to create a drop
                if coda_height == 1:
                    # must end with  [x,1,1], [x,1] so we should just stop one early
                    # to create [x+1,1,1], [x-1,1]
                    post_end_idx = post_end_idx - 1
                else:
                    temp_idx = post_end_idx - 1

                    while temp_idx > 0 and big_row[temp_idx] == coda_height and small_row[temp_idx] == coda_height:
                        if small_row[temp_idx] < size - temp_idx + 1:
                            post_end_idx = temp_idx
                        temp_idx = temp_idx - 1


                if post_end_idx == orig_post_end_idx:
                    # still have a problem: no drop will be created
                    need_coda = True

                # else:
                #     # must create a downstep
                #     coda_end_idx = post_end_idx
                #     coda_start_idx = post_end_idx - 1
                #
                #     while coda_start_idx > 0 and big_row[coda_start_idx - 1] == coda_height:
                #         coda_start_idx = coda_start_idx -1
                #
                #     post_end_idx = coda_start_idx



            ##### DEAL WITH THE LEADING LEVEL STEPS
            if prev_state == LEVEL:
                if diff > 1:
                    raise ValueError('TBD Level to unexpected diff' + str(diff))

                # correct the level steps before this
                for k in range(level_start_idx, idx):
                    big_row[k] = big_row[k] + 1
                    small_row[k] = small_row[k] - 1

                level_start_idx = size

            #crossed_delta = diff

            post_big_height = big_row[post_end_idx]


            for k in range(idx, post_end_idx):
                #d = small_row[k]  - big_row[k]
                #crossed_delta = max(d, crossed_delta)
                print('just using diff')
                crossed_delta = small_row[k]  - big_row[k]

                if small_row[k] - crossed_delta - 1 < size - 1 - k:
                    raise ValueError('not enough to take!')

                small_row[k] = small_row[k] - crossed_delta - 1
                big_row[k] = big_row[k] + crossed_delta + 1


            if need_coda:
                if not big_row[post_end_idx] == big_row[post_end_idx-1] -1:
                    raise ValueError("We supposedly need coda. WTF?")
                else:
                    print("WE DO NEED CODA!")


                coda_end_idx = post_end_idx
                coda_start_idx = coda_end_idx - 1

                while coda_start_idx > 0 and small_row[coda_start_idx-1] == small_row[coda_start_idx]:
                    coda_start_idx = coda_start_idx - 1

                # hack???!!!!!
                if coda_end_idx - coda_start_idx > 1:
                    coda_start_idx = coda_start_idx + 1

                print('coda runs', coda_start_idx, coda_end_idx)

                for amt,k in enumerate(range(coda_start_idx, coda_end_idx)):
                    big_row[k] = big_row[k] + 1 + amt
                    small_row[k] = small_row[k] - 1 - amt

                coda_end_height = small_row[coda_end_idx-1]

                if coda_end_idx < size and coda_end_height < small_row[coda_end_idx]:
                    print('uh oh! problem to solve!')
                    print('\t', big_row)
                    print('\t', small_row)
                    extra_idx = coda_end_idx
                    while extra_idx < size and small_row[extra_idx] > coda_end_height:
                        extra_idx +=1

                    print('extra change', coda_end_idx, extra_idx)
                    for i in range(coda_end_idx, extra_idx):
                        diff = small_row[i] - coda_end_height + 1
                        small_row[i] = coda_end_height - 1
                        big_row[i] = big_row[i] + diff



            state = ABOVE
            crossed_delta = 0
            level_start_idx = size


        #    hack to fix this here? is there a way to detect this?
        elif state == LEVEL and  idx == col_max_idx-1 and small_row[idx] > big_row[idx+1]:
            # this is never allowed in a FBT
            if small_row[idx] - big_row[idx+1] > 1:
                pass
                #raise ValueError('TBD Big drop after level')

            for k in range(level_start_idx, idx+1):
                small_row[k] = small_row[k] - 1
                big_row[k] = big_row[k] + 1

            state = ABOVE
            level_start_idx = size


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

    print('distinct', len(combed_map))
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


def compare_two_rows(size, col_sums=()):

    # tss_list = get_boosted_tss(size)
    # fbt_list = get_boosted_fbt(size)
    #
    #
    #
    # tss_row_list = []
    #
    # for tss in tss_list:
    #     temp = [tss[0], tss[1]]
    #
    #     if not temp in tss_row_list:
    #         tss_row_list.append(temp)
    #
    # fbt_row_list = []
    #
    # for fbt in fbt_list:
    #     temp = [fbt[0], fbt[1]]
    #
    #     if not temp in fbt_row_list:
    #         fbt_row_list.append(temp)

    ###########

    # tss_row_list = [ [x[0], x[1]] for x in tss_list]
    # fbt_row_list = [ [x[0], x[1]] for x in fbt_list]

    #combed_row_list = [handle_row_with_col_max_v4(tss_rows, 1, size-1) for tss_rows in tss_row_list]

    #print(len(tss_row_list), len(fbt_row_list), len(combed_row_list))

    ###########

    tss_row_list2 = get_boosted_tss_trapezoid(size,2)
    fbt_row_list2 = get_boosted_fbt_trapezoid(size,2)

    tss_row_list = tss_row_list2
    fbt_row_list = fbt_row_list2


    fbt_match_list = [f for f in fbt_row_list if get_col_sums(f) == col_sums ]

    combed_map = dict()



    error_list = []
    comb_match_list = []

    for k,t in enumerate(tss_row_list):
        print(k, 'before')
        util.print_array(t)

        tt = util.clone_array(t)

        if k % 1000 == 0:
            print('processed', k)

        #print("HANDLING ROW WITH COL MAX")
        #b = handle_row_with_col_max_v4(tt, 1, size-1)
        b = untangle(tt, 1, size-1)

        key =  str(b)
        if not key in combed_map:
            combed_map[key]  = [ t, ]
        else:
            print('REPEAT!!!!', k)
            combed_map[key].append(t)
            print(key, 'mapped from', combed_map[key])

        print('after')
        util.print_array(b)

        if not b in fbt_row_list:
            print('ERROR NOT IN FBT LIST!', k)
            error_list.append([t,b])
            print(t, 'mapped to', b)
        else:
            if get_col_sums(b) == col_sums:
                    comb_match_list.append(b)

        #print('======================')

    print('num errors', len(error_list))
    for x in error_list:
        print(x[0], x[1], util.get_column_sums(x[0]))

    missing_count = 0
    print('missing')
    for b in fbt_row_list:
        if not str(b) in combed_map:
            missing_count += 1
            #print(b, util.get_column_sums(b))
    print(missing_count)


    rep_count = 0
    print('repeated')
    for k in combed_map:
        x = combed_map[k]
        if len(x) > 1:
            print(k)
            rep_count += 1
            for y in x:
                print('\t', y, util.get_column_sums(y))

    print('summary')
    print('tss=', len(tss_row_list), 'combed=', len(combed_map), 'fbt=', len(fbt_row_list), 'repeated=', rep_count, 'error=', len(error_list))

    # print('only tss 1')
    # for t in tss_row_list:
    #     if not t in tss_row_list2:
    #         print('\t', t)
    # print('only tss 2')
    # for t in tss_row_list2:
    #     if not t in tss_row_list:
    #         print('\t', t)
    #
    # print('only fbt 1')
    # for t in fbt_row_list:
    #     if not t in fbt_row_list2:
    #         print('\t', t)
    # print('only fbt 2')
    # for t in fbt_row_list2:
    #     if not t in fbt_row_list:
    #         print('\t', t)

    if not col_sums == ():
        print('missing fbt with col_sums', col_sums)
        for f in fbt_match_list:
            if not f in comb_match_list:
                print(f)



def get_col_sums(trapezoid):
    size = len(trapezoid[0])
    sums = [x for x in trapezoid[0]]


    for i in range(1, len(trapezoid)):
        for idx,val in enumerate(trapezoid[i]):
            sums[idx] = sums[idx] + val

    return tuple(sums)

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
# c = comb(t,debug=True)
# util.print_array(c)
# print(c)

#compare(4)


r2 = [[1, 0], [1]]

r3a = [[2, 1, 0], [2, 1]]
r3b = [[2, 1, 0], [2, 2]]
r3c = [[2, 1, 0], [1, 1]]
r3d = [[2, 1, 1], [2, 1]]

r4a = [[3, 2, 2, 1], [3, 3, 2]] # [4,4,3,1],[2,1,0] (or switch with next)
r4b = [[3, 2, 1, 1], [3, 3, 3]] # [4,4,4,1],[2,1,1]
r4c = [[3, 2, 1, 0], [2, 2, 2]]
r4d = [[3, 2, 1, 0], [3, 2, 2]] # [4,3,3,0],[2,1,0]
r4e = [[3, 2, 2, 1], [3, 2, 2]] # [4,3,3,1],[2,1,1]
r4f = [[3, 2, 1, 1], [2, 2, 1]] # [3,3,2,1],[2,1,0]
r4g = [[3, 2, 1, 1], [3, 2, 1]]
r4h = [[3, 2, 2, 1], [3, 2, 1]] # [4,2,2,2],[2,2,1]
r4i = [[3, 2, 2, 2], [3, 2, 2]]
r4j = [[3, 2, 2, 2], [3, 3, 2]] # [4,4,4,2],[2,1,0]
r4k = [[3, 2, 1, 0], [3, 2, 1]]
r4l = [[3, 3, 2, 2], [3, 3, 2]] # [4,4,4,2], [2,2,0]
r4m = [[4, 3, 2, 2], [3, 3, 2]] # [4,4,4,2], [3,3,1]

r5a = [[4, 3, 2, 1, 0], [3, 2, 2, 2]]
r5b = [[4, 3, 2, 2,2], [4, 3, 3, 2]]
r5c = [[4, 3, 3, 3, 2], [4, 4, 3, 2]]

r5d = [[4, 3, 3, 3, 3], [4, 4, 3, 2]]
r5e = [[4, 3, 3, 3, 3], [4, 4, 3, 3]]
r5f = [[4, 3, 3, 3, 3], [4, 4, 4, 3]]
r5g = [[4, 4, 3, 3, 3], [4, 4, 3, 3]]
r5h = [[5, 4, 3, 3, 3], [4, 4, 3, 3]]

rlong = [[3,3,2,2,2,1,1],[3,3,2,2,2,1]]

r = r4l
r_orig = util.clone_array(r)
#r = r3a
rr = util.clone_array(r)
s = len(r[0])
r_col_sum = get_col_sums(r)

util.print_array(r)


print('handle')
c_before = handle_row_with_col_max_v4(rr,1,s-1,True)


#c = comb(r)


#util.print_array(c_before)

print('untangle')

c = untangle(r,1,s-1,True)
util.print_array(c)

compare_two_rows(4, r_col_sum)

print(r_orig, 'orig')
print(r, 'comb')
#print(rr)

#compare(3)

# print('diag_sums')
# rows = get_boosted_fbt_trapezoid(5,2)
# for row in rows:
#     if get_col_sums(row) == (8,7,6,5,2):
#         for r in row:
#             print(r)
#         print('-------')


#trap_list = get_boosted_fbt_trapezoid(3,3)

#print(get_boosted_fbt_rows(2))


# bt_list = get_boosted_fbt(3)
#
# for b in bt_list:
#     if not b in trap_list:
#         print('missing', b)
#
#
# for b in trap_list:
#     print(b)
#
# print(len(trap_list))
#
# for r in get_boosted_fbt_rows(2):
#     print(r)


# fbt = get_boosted_fbt(3)
#
# print('BOOSTED FBT')
#
# for b in fbt:
#     util.print_array(b)


