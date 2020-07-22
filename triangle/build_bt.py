

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
                if (row_ok):
                    for i in range(len(prev_row)):
                        if row[i+1] - prev_row[i]   > 1:
                            row_ok =  False
                            break


                if row_ok:
                    bt = [ p.copy() for p in prev]
                    bt.insert(0,row)
                    bt_list.append(bt)
    return bt_list


#bt_list = build_bt(3)
#for bt in bt_list:
#    print(bt)
#print(len(bt_list))