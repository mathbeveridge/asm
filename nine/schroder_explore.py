import nine.sandwich as sw
import nine.schroder_path as sp

from itertools import chain, combinations


def powerset(seq):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    #s = list(iterable)
    #return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
    if len(seq) <= 0:
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]]+item
            yield item



sp_map = dict()

def get_sp(size):
    if not size in sp_map:
        sand_list = sw.get_row(size)
        sp_list = [sp.SchroderPath(x) for x in sand_list]

        sp_map[size] = sp_list

    return sp_map[size]


sp_avoiding_map = dict()

def get_sp_avoiding_patterns(size, pattern_combo):
    pc_str = str(pattern_combo)
    if not pc_str in sp_avoiding_map:
        sp_avoiding_map[pc_str] = dict()

    avoid_map = sp_avoiding_map[pc_str]

    if not size in avoid_map:
        s_list = get_sp(size)

        pca_list = []

        for s in s_list:

            is_valid = True

            for p in pattern_combo:

                if s.has_pattern(p):
                    is_valid = False
                    break

            if is_valid:
                pca_list.append(s)

        avoid_map[size] = pca_list

    return avoid_map[size]


def are_disjoint(sp1, sp2):
    if sp1.get_size() > sp2.get_size():
        big_sp = sp1
        small_sp = sp2
    else:
        big_sp = sp2
        small_sp = sp1

    big_height_list = get_height_list(big_sp)
    small_height_list = get_height_list(small_sp)

    for x in range(len(small_height_list)):
        if max(small_height_list[x]) >= min(big_height_list[x]):
            return False

    return True



def are_noncrossing(sp1, sp2):
    if sp1.get_size() > sp2.get_size():
        big_sp = sp1
        small_sp = sp2
    else:
        big_sp = sp2
        small_sp = sp1

    big_height_list = get_height_list(big_sp)
    small_height_list = get_height_list(small_sp)

    for x in range(len(small_height_list)):
        if max(small_height_list[x]) > min(big_height_list[x]):
            return False

    return True


def are_osculating(sp1, sp2):
    if sp1.get_size() > sp2.get_size():
        big_sp = sp1
        small_sp = sp2
    else:
        big_sp = sp2
        small_sp = sp1

    big_height_list = get_height_list(big_sp)
    small_height_list = get_height_list(small_sp)

    for x in range(len(small_height_list)):
        if max(small_height_list[x]) > min(big_height_list[x]):
            return False
        elif max(small_height_list[x]) == min(big_height_list[x]):
            if max(small_height_list[x-1]) == min(big_height_list[x-1]):
                return False

    return True







def get_height_list(sp):
    height_list = [ [] for _ in range(sp.get_size()+1) ]
    for p in sp.get_path():
        height_list[p[0]].append(p[1])

    return height_list


###########

def disjoint_avoiding_pattern_summary(max_size):
    pattern_combo_list = [x for x in  powerset(sw.pattern_list)]

    disjoint_count_map = dict()

    for pc in pattern_combo_list:
        disjoint_count_map[str(pc)] = disjoint_avoiding_pattern_count(max_size, pc)

    #for key in disjoint_count_map:
    #    print(key, disjoint_count_map[key])

    # let's organize by the count
    seq_map = dict()

    for pc in disjoint_count_map:
        seq = disjoint_count_map[pc]
        seq_key = str(seq)

        if not seq_key in seq_map:
            seq_map[seq_key] = [pc,]
        else:
            seq_map[seq_key].append(pc)

    for s in seq_map:
        print(s, seq_map[s])


###########

def noncrossing_avoiding_pattern_summary(max_size):
    pattern_combo_list = [x for x in  powerset(sw.pattern_list)]

    count_map = dict()

    for pc in pattern_combo_list:
        count_map[str(pc)] = noncrossing_avoiding_pattern_count(max_size, pc, True)

    #for key in disjoint_count_map:
    #    print(key, disjoint_count_map[key])

    # let's organize by the count
    seq_map = dict()

    for pc in count_map:
        seq = count_map[pc]
        seq_key = str(seq)

        if not seq_key in seq_map:
            seq_map[seq_key] = [pc,]
        else:
            seq_map[seq_key].append(pc)

    for s in seq_map:
        print(seq_map[s])


def disjoint_avoiding_pattern_count(max_size, pattern_combo):
    return noncrossing_avoiding_pattern_count(max_size, pattern_combo, False)

def noncrossing_avoiding_pattern_count(max_size, pattern_combo, can_touch):

    sp_map = dict()

    sp1_list = get_sp_avoiding_patterns(1,pattern_combo)

    #initialize sp_map
    for sp in sp1_list:
        sp_map[str(sp)] = 1


    for size in range(2,max_size+1):
        big_list = get_sp_avoiding_patterns(size, pattern_combo)
        small_list = get_sp_avoiding_patterns(size-1, pattern_combo)

        for b in big_list:
            big_count = 0
            for s in small_list:
                if not can_touch:
                    if are_disjoint(b,s):
                        big_count += sp_map[str(s)]
                        print('compatible', b, s, b.get_hdv(), s.get_hdv())
                else:
                    if are_noncrossing(b,s):
                        big_count += sp_map[str(s)]
                        #print('compatible', b, s)

            sp_map[str(b)] = big_count


    final_count_list = []

    for n in range(1,max_size+1):

        final_list = get_sp_avoiding_patterns(n, pattern_combo)

        final_count = 0

        for sp in final_list:
            final_count += sp_map[str(sp)]

        final_count_list.append(final_count)

    print(pattern_combo, 'final count', final_count_list)

    return final_count_list




def disjoint_count():

    sp_map = dict()

    sp1_list = get_sp(1)

    #initialize sp_map
    for sp in sp1_list:
        sp_map[str(sp)] = 1


    max_size = 4

    for size in range(2,max_size+1):
        big_list = get_sp(size)
        small_list = get_sp(size-1)

        for b in big_list:
            big_count = 0
            for s in small_list:
                if are_disjoint(b,s):
                    big_count += sp_map[str(s)]

            sp_map[str(b)] = big_count


    final_list = get_sp(max_size)

    final_count = 0

    for sp in final_list:
        final_count += sp_map[str(sp)]

    print('final count', final_count)

############

def pattern_avoiding_count():
    pattern_count_map = dict()

    pattern_combo_list = [x for x in  powerset(sw.pattern_list)]

    for pc in pattern_combo_list:
        pattern_count_map[str(pc)] = []


    for size in range(1,9):

        s_list = get_sp(size)

        for pc in pattern_combo_list:

            count = 0

            for s in s_list:

                is_valid = True

                for p in pc:

                    if s.has_pattern(p):
                        is_valid = False
                        break

                if is_valid:
                    count += 1

            #print('update', size, pc)
            pattern_count_map[str(pc)].append(count)


    print('********')

    # let's organize by the count
    seq_map = dict()

    for pc in pattern_count_map:
        seq = pattern_count_map[pc]
        seq_key = str(seq)

        if not seq_key in seq_map:
            seq_map[seq_key] = [pc,]
        else:
            seq_map[seq_key].append(pc)



    for s in seq_map:
        print(seq_map[s])

####
#disjoint_avoiding_pattern_count(7, ['HV'])
#noncrossing_avoiding_pattern_count(7, ['HH', 'HD', 'DV', 'VD', 'VV', 'DH'], True)
#noncrossing_avoiding_pattern_count(7, ['HH', 'HD', 'DV', 'VD','VV'], True)
# noncrossing_avoiding_pattern_count(7, ['HH', 'HD', 'DV', 'VD', 'VV'], True)
# noncrossing_avoiding_pattern_count(7, ['HH', 'HD', 'DV', 'VD', 'DH'], True)
# noncrossing_avoiding_pattern_count(7, ['HH', 'HD', 'DV', 'VD'], True)
# noncrossing_avoiding_pattern_count(7, ['HH', 'HD', 'DV'], True)
# noncrossing_avoiding_pattern_count(7, ['HH', 'HD', 'DH'], True)
# noncrossing_avoiding_pattern_count(7, ['HH', 'HD' ], True)
# noncrossing_avoiding_pattern_count(7, ['HH',  ], True)
# noncrossing_avoiding_pattern_count(7, ['DH'  ], True)
# noncrossing_avoiding_pattern_count(7, ['HD'  ], True)

disjoint_avoiding_pattern_count(5, ['HH', 'DH'])

#pattern_avoiding_count()

#noncrossing_avoiding_pattern_summary(6)