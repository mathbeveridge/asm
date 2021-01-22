
# this code confirms that the permutation stack family (built from coin triangles)
# is the same as the 2nd Schroder family that Ian found.

col_dict = dict()
col_dict[1] =[[k, ] for k in range(0, 2)]

def get_column(size):
    if not size in col_dict:
        prev_list = get_column(size-1)
        new_list = []
        for idx in range(size+1):
            for prev in prev_list:
                if (idx == 0 and prev[0] ==0) or idx > prev[0]:
                    new_list.append([idx,] + prev)
        col_dict[size] = new_list

    return  col_dict[size]



# initialize the ocean dictionary
pst_dict = dict()
pst_dict[1] = [[[k, ],] for k in range(0,2)]

def get_permutation_stacks(size):
    if not size in pst_dict:
        prev_list = get_permutation_stacks(size-1)
        col_list = get_column(size)
        new_list = []

        for c in col_list:
            for p in prev_list:
                new_list.append([c,] + p)

        pst_dict[size] = new_list

    return pst_dict[size]



def get_block_totals():
    for size in range(2,6):
        stacks = get_permutation_stacks(size)

        totals = [[0 for j in range(len(stacks[0][i]))] for i in range(len(stacks[0]))]
        #print('totals', totals)

        for s in stacks:
            #print(s)
            for i in range(len(s)):
                for j in range(len(s[i])):
                    totals[i][j]+= s[i][j]


        print('size=', size)
        print('num triangles=', len(stacks))

        #print(totals)
        tot = 0
        for row in totals:
            tot+=sum(row)
        print('total blocks=', tot)
        for x in totals:
            print(x)
        print("----------")




cols = get_permutation_stacks(2)

#for c in cols:
#    print(c)

#print(len(cols))

get_block_totals()


