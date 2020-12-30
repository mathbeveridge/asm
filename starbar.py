import triangle.build_gog  as build_gog
import triangle.build_magog as build_magog
import triangle.gog_magog as gog_magog
import stackset.build_stack_sets as build_stack_sets




def print_triangle(triangle):
    for r in triangle:
        print(r)
    print('-------')


def get_gog_starbar(n):
    gog_list = build_gog.build_gog(n)
    gog_list = build_gog.reflect_list(gog_list)

    return [triangle_to_starbar(gog, n)  for gog in gog_list]


def get_magog_starbar(n):
    magog_list = build_magog(n)





def triangle_to_starbar(triangle, size):

    starbar = []

    for idx,row in enumerate(triangle):
        row = list_to_starbar(row, idx+1)
        for k in range(size-1-idx):
            row.insert(0,2)
            row.append(2)

        starbar.append(row)



    return starbar

def list_to_starbar(list, size):
    starbar = []


    for i in range(size+1):
        for j in range(list.count(i)):
            starbar.append(0);

        if (i < size):
            starbar.append(1)

    return starbar



def get_sst_starbar(n):
    sst_list = build_stack_sets.build_stacks(n)

    return [sst_to_starbar(sst) for sst in sst_list]

def sst_to_starbar(sst):
    sb = []

    for row in sst:
        sb_row = [0]  * row.count(0)

        for entry in row:
            sb_row.append(1)
            if entry == 1:
                sb_row.append(0)

        sb.append(sb_row)
    return sb


def get_magog_starbar(n):
    magog_list = build_magog.build_magog(n)

    diag_magog_list = [ orient_diag(m) for m in magog_list]

    sb_list = [ triangle_to_starbar(magog, n) for magog in diag_magog_list ]

    return sb_list


def orient_diag(magog):
    n = len(magog)


    new_magog = [ [0] * i for i in range(1, n+1) ]


    for i in range(n):
        for j in range(i+1):
            new_magog[i][j] = magog[n-1-i+j][j]


    return new_magog


# in this mapping we find a gog violation
# a 0 in row start_row that is more than one before the same 0 in row k+1
# starting at that 0's index, we shift start_row down.
# we remove the 1 in start_row+1 and shift the rest  up
# we append a 1 onto the  second row.
def map_msb(magog_sb, start_row):


    size = len(magog_sb)

    if start_row < 0:
        start_row = size - start_row

    ret_val = [ [ x for x in row] for row in magog_sb]


    penult_idx = start_row
    ult_idx = start_row + 1

    penult_row = magog_sb[penult_idx].copy()

    ult_row = magog_sb[ult_idx].copy()

    indices_penult = [i for i, d in enumerate(penult_row) if d == 0]
    indices_ult = [i for i, d in enumerate(ult_row) if d == 0]


    #print(indices_penult)
    #print(indices_ult)

    for k in range(len(indices_penult)):
        idx_pen = indices_penult[k]
        idx_ult = indices_ult[k+1]

        if  idx_pen < idx_ult - 1:
            #print('found a gap')
            # there is a gap. let's fix it
            temp_penult_row = penult_row[0:idx_pen]
            temp_penult_row = temp_penult_row + ult_row[idx_pen +1:]
            temp_penult_row.append(2)

            temp_ult_row = ult_row[0:idx_pen]
            temp_ult_row = temp_ult_row + penult_row[idx_pen:]
            temp_ult_row[size + 1 +  start_row] = 1

            #print('before')
            #print(penult_row)
            #print(ult_row)
            #print('after')
            #print(temp_penult_row)
            #print(temp_ult_row)

            ret_val[ult_idx] = temp_ult_row
            ret_val[penult_idx] = temp_penult_row

            #print('returning', ret_val, magog_sb,  str(ret_val == magog_sb))

            # just fix first one we find for now
            break


    #if not str(ret_val)  == str(magog_sb):
    #    ret_val = map_msb(ret_val, start_row)

    return ret_val


# ignore duplicates
def clip_to_bottom(triangle_lsit):
    dict = {}
    for triangle in triangle_lsit:
        val = [ triangle[-2], triangle[-1] ]
        dict[str(val)] = val


    return list(dict.values())


def test_sb_magog_map(n):
    for n in range(n,n+1):
        gog_sb_list = get_gog_starbar(n)
        magog_sb_list = get_magog_starbar(n)

        gog_sb_list = clip_to_bottom(gog_sb_list)
        magog_sb_list = clip_to_bottom(magog_sb_list)


        gog_str_set = set()

        for gog in gog_sb_list:
            gog_str_set.add(str(gog))

        magog_str_set = set()

        for magog in magog_sb_list:
            magog_str_set.add(str(magog))




        mapped_list = []

        for x in magog_sb_list:
            print('magog sb')
            for r in x:
                print(r)
            print('------')
            mapped_sb = map_msb(x, len(x)-2)

            if not str(mapped_sb) == str(x):

                print('different', x, mapped_sb)

                if not mapped_sb in mapped_list:
                    mapped_list.append(mapped_sb)

                if str(mapped_sb) in gog_str_set:
                    print('\tfound in gog sb')
                else:
                    print('\tERROR not in gog sb')

                print('----')

        print(len(gog_sb_list))


        count = 0
        for msb in magog_sb_list:
            if not msb in gog_sb_list:
                count+=1
        print('# magog not gog is', count)

        print('# mapped is', len(mapped_list))


def test_multirow_map(n):

    for n in range(n,n+1):
        gog_sb_list = get_gog_starbar(n)
        magog_sb_list = get_magog_starbar(n)

        gog_str_list = [str(g) for g in gog_sb_list]
        magog_str_list = [str(mg) for mg in magog_sb_list]

        both_str_list =  []
        gog_only_str_list = []


        print('MAGOG ONLY===================')
        for m in magog_sb_list:
            if str(m) not in gog_str_list:
                for row in m:
                   print(row)
                print('------')



        print('GOG ONLY===================')
        for g in gog_sb_list:
            if str(g) not in magog_str_list:
                for row in g:
                   print(row)
                print('------')
                gog_only_str_list.append(str(g))
            else:
                both_str_list.append(str(g))


        fail_count =  0

        print('TRY THE MAPPING===================')
        for m in magog_sb_list:
            if not str(m) in both_str_list:
                mapped = m
                mapped = map_msb(mapped,n-3)
                #mapped = map_msb(mapped,n-3)



                if str(mapped) in gog_only_str_list:
                    print('success after 1 map')
                else:
                    #print('\tmagog ', m)
                    #print('\tbefore', mapped)

                    mapped = map_msb(mapped, n - 2)

                    #print('\tafter ', mapped)

                    if str(mapped) in gog_only_str_list:
                        print('success after 2 maps')
                    else:
                        print('>>>>>>>>>>>>>>>fail after 2 attempts<<<<<<<<<<<<<')
                        fail_count+=1
                        for row in m:
                            print(row)
                        print('--------')
                        for row in mapped:
                            print(row)
                        print('--------')
                        print(gog_only_str_list[10])

        print('num fails=', fail_count)

#test_sb_magog_map(5)

#test_multirow_map(3)




#foo = [[2, 2, 0, 1, 2, 2], [2, 0, 1, 1, 0, 2], [0, 1, 1, 0, 0, 1]]

foo = [[2, 2, 0, 1, 2, 2],[2, 0, 1, 1, 0, 2],[0, 1, 0, 1, 1, 0]]

foo = [[2, 2, 1, 0, 2, 2], [2, 0, 1, 0, 1, 2], [0, 1, 0, 1, 1, 0]]

gogsb_str_list = [str(gog) for gog in get_gog_starbar(3)]

print_triangle(foo)

foo_mapped  = map_msb(foo, 0)
print_triangle(foo_mapped)


foo_mapped = map_msb(foo_mapped,1)
print_triangle(foo_mapped)

print(str(foo_mapped) in gogsb_str_list)

