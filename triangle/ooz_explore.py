import stackset.build_stack_sets as bss



def fix_sst(sst):
    local_sst = [ row.copy() for row in sst]

    for row_idx in range(1,len(sst)):
        for col_idx in reversed(range(1,len(local_sst[row_idx]))):
            if local_sst[row_idx][col_idx] == 0:
                if local_sst[row_idx][col_idx-1] == 1 and local_sst[row_idx-1][col_idx-1] == 1:
                    # turn the 1 into a 0 in the same row
                    local_sst[row_idx][col_idx - 1] = 0


    #print('>>> before')
    #print_array(sst)
    #print('>>> after')
    #print_array(local_sst)

    return local_sst



def first_explore(n):
    #for n in range(2,7):
    #    ooz_list = build_ooz(n)
    #    print(len(ooz_list))


    #n=4
    sst_list = bss.build_stacks(n)

    ooz_list = bss.build_ooz(n)

    print('num sst', len(sst_list))
    print('num ooz', len(ooz_list))

    not_sst_list = []
    yes_sst_list = []
    for ooz in ooz_list:
        if not ooz in sst_list:
            not_sst_list.append(ooz)
        else:
            yes_sst_list.append(ooz)



    print('\tooz not sst:', len(not_sst_list))
    print('\tooz yes sst:', len(yes_sst_list))

    for ooz in not_sst_list:
        print_triangle(ooz)

    print('=====================')
    print('=====================')
    print('=====================')

    # count = 0
    # yes_ooz_list = []
    # for sst in sst_list:
    #     if not sst in ooz_list:
    #         count += 1
    #         #for row in sst:
    #         #    print(row)
    #         #print("-------")
    #     else:
    #         yes_ooz_list.append(sst)
    # print(count)
    #
    # print(len(yes_sst_list), len(yes_ooz_list))

    #for x in yes_sst_list:
    #    if not x in yes_ooz_list:
    #        for row in x:
    #            print(row)

def print_triangle(triangle):
    for row in triangle:
        print(row)
    print('-------')


def try_fix(n):
    sst_list = bss.build_stacks(n)

    ooz_list = bss.build_ooz(n)
    yes_ooz_list = []
    not_ooz_list = []
    count = 0
    for sst in sst_list:
        if not sst in ooz_list:
            count += 1
            not_ooz_list.append(sst)
            #for row in ooz:
            #    print(row)
            #print("-------")
        else:
            yes_ooz_list.append(sst)
    print('not ooz:', len(not_ooz_list))
    print('yes ooz:', len(yes_ooz_list))

#    print(len(sst_list) - count)

    fixed_list = []

    for sst in not_ooz_list:
        fixed = fix_sst(sst)

        if fixed in fixed_list:
            print('>>>>>>> already in fixed list')
            print_triangle(sst)
            print_triangle(fixed)
        elif fixed in yes_ooz_list:
            print('######### doubled up ooz/sst')
            print_triangle(sst)
            print_triangle(fixed)
        else:
            fixed_list.append(fix_sst(sst))

    print('num_fixed', len(fixed_list))

    for fixed in fixed_list:
        if not fixed in ooz_list:
            print('!!!!!!!!!! not ooz')
            print_triangle(fixed)


    print('=========== missing ooz')
    count = 0
    for ooz in ooz_list:
        if not ooz in fixed_list and not ooz in sst_list:
            print_triangle(ooz)
            count+=1

    print(count)

#try_fix(5)
first_explore(4)
