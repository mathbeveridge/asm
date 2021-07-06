import stackset.build_stack_set as bss



def build_ssb(size):
    if size == 1:
        sst_list = bss.build_stacks(size)
        return [ [s,] for s in sst_list]
    else:
        prev_list = [[sst,] for sst in bss.build_stacks(size)]

        for idx in reversed(range(1,size)):

            sst_list = bss.build_stacks(idx)

            new_list = []

            for sst in sst_list:
                for prev in prev_list:
                    if is_compatible(sst, prev[-1]):
                        new_list.append( [sst,] + prev)

            prev_list = new_list

        return new_list

def is_compatible(sst, prev_sst):
    n = len(sst)

    for idx in range(n):
        inv_sst_row = [1-x for x in sst[idx]]
        inv_prev_sst_row = [1 - x for x in prev_sst[idx]]

        new_count = 0
        prev_count = 0

        ones = [i for i, x in enumerate(inv_prev_sst_row) if x == 1]
        num_passed = 0
        for i in ones:
            if sum(inv_prev_sst_row[i:n + 1]) >= sum(inv_sst_row[i:n]):
                    num_passed += 1
        if num_passed < sum(inv_prev_sst_row):
            return False


    return True



def get_binary_lists(n):
    if n == 1:
        return [[1,], [0]]
    else:
        prev_list = get_binary_lists(n-1)
        new_list1 = [ [1,] + prev for prev in prev_list]
        new_list0 = [ [0,] + prev for prev in prev_list]
        return new_list1 + new_list0




ssb_list = build_ssb(2)

for ssb in ssb_list:
    print(ssb)
    print('-----')

print (len(ssb_list))

