
# BALLOT TRIANGLES
# these triangles have shape
# xxx
# xx
# x
#
# and rules:
# col decr by at most 1 (can increase too)
# row weak decr
# NE diag decr at most 1


def get_row_list(size):
    if size ==  1:
        return [ [0,], [1,]]
    else:
        previous_list = get_row_list(size-1)
        row_list = []
        for k in range(size+1):
            for prev_row in previous_list:
                if k >= prev_row[0]:
                    row_list.append( [k,]  + prev_row.copy())

        return row_list


##### be careful! you should really clone everything.

def build_bt(size):
    if size == 1:
        return [ [[0,],], [[1,],]]
    else:
        previous_list =  build_bt(size-1)
        row_list =  get_row_list(size)

        bt_list = []

        count = 0

        for prev in previous_list:
            prev_row = prev[0]

            for row in row_list:
                row_ok = True

                #  check col decrease by at most 1 (note: can increase)
                for i in range(len(prev_row)):
                    if row[i] - prev_row[i]  > 1:
                        row_ok =  False
                        break

                # do we need to check the diag, or is it forced?
                # if (row_ok):
                #     for i in range(len(prev_row)):
                #         if row[i+1] - prev_row[i]   > 1:
                #             row_ok =  False
                #             break


                if row_ok:
                    bt = [ p.copy() for p in prev]
                    bt.insert(0,row)
                    bt_list.append(bt)

                    count = count + 1

                    #if count % 1000 == 0:
                    #    print('bt count', count)
    return bt_list


def is_row_gog(bt):
    is_good = True
    for row in bt:
        for idx in range(len(row)-1):
            if row[idx+1] - row[idx] > 1:
                is_good = False
                break
        if not is_good:
            break
    return is_good


def get_block_totals():
    for size in range(2,6):
        stacks = build_bt(size)

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





bt_list = build_bt(5)
for bt in bt_list:
   print(bt)
print(len(bt_list))


get_block_totals()