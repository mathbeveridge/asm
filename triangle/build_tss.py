

# these triangles have shape
# xxx
# xx
# x
#
# and rules:
# rows weak decr by at most 1

def get_row_list(size):
    if size ==  1:
        return [ [0,], [1,]]
    else:
        previous_list = get_row_list(size-1)
        row_list = []
        for k in range(size+1):
            for prev_row in previous_list:
                if k >= prev_row[0] and k <= prev_row[0] +1:
                    row_list.append( [k,]  + prev_row.copy())

        return row_list


##### be careful! you should really clone everything.
def build_tss(size):
    if size == 1:
        return [ [[0,],], [[1,],]]
    else:
        previous_list =  build_tss(size-1)
        row_list =  get_row_list(size)

        tss_list = []


        count = 0

        for prev in previous_list:
            for row in row_list:
                tss = [ p.copy() for p in prev]
                tss.insert(0,row)
                tss_list.append(tss)
            count = count + 1

            if count % 1000 == 0:
                print('tss count', count)

    return tss_list


def transpose(triangle):
    size = len(triangle)
    new_triangle = [ [0] * (size - idx) for idx in range(size)]

    #print(triangle)

    for i in range(size):
        for j in range(size-i):
            #print(i,j)
            new_triangle[j][i] = triangle[i][j]

    return new_triangle

def transpose_list(triangle_list):
    return [ transpose(triangle) for triangle in triangle_list]


#tss_list = build_tss(3)
#for tss in tss_list:
#    print(tss)
#print(len(tss_list))
