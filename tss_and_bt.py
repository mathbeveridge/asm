import triangle.build_tss as build_tss
import triangle.build_bt  as build_bt




def print_triangle(triangle):
    for row in triangle:
        print(row)
    print('-----')


def print_triangle_list(triangle_list):
    for t in triangle_list:
        print_triangle(t)
    print(len(triangle_list))

# in this implementation, we find a row entry that decreases by more than one
# we then find a nonzero entry in its diagonal and do a +1/-1 swap
# we propagate this in the fixing row for each entry equal to the one we changed
#
#  it fails for n=3. We get 2 doubles in the transformed and 1 that was already a bt + tss.
def fix_row(triangle, idx):
    row_length = len(triangle[idx])
    for k in range(1,len(triangle[idx])):
        while triangle[idx][k-1] - triangle[idx][k] > 1:
            offset = -1
            for j in range(1,k+1):
                if triangle[idx+j][k-j] > 0:
                    # we found it!
                    offset = j
                    break

            if (offset < 0):
                raise Exception('fix row failed! idx=' + str(idx) + ' triangle=' + str(triangle))

            # fixing row entry k, but we may have to subtract from
            # entries to the right of the fixing value
            base_value = triangle[idx+offset][k-offset]

            for j in range(k, row_length):
                if triangle[idx+offset][j-offset] == base_value:
                    triangle[idx][j] = triangle[idx][j] + 1
                    triangle[idx + offset][j - offset] = triangle[idx + offset][j - offset] - 1
                else:
                    # let's quit this look early
                    break
            #print(idx,k,triangle)

    # no need to return anything





n=3

tss_list = build_tss.build_tss(n)
bt_list = build_bt.build_bt(n)

tss_only_list  = []
bt_only_list  = []

print('tss only:')
for tss in tss_list:
    if  not tss in bt_list:
        tss_only_list.append(tss)

print('total=', len(tss_only_list))
print('=============================')

print('bt only:')
for bt in bt_list:
    if  not bt in tss_list:
        bt_only_list.append(bt)
        #print_triangle(bt)

print('total=', len(bt_only_list))
print('=============================')


temp_list = [ [ [2, 0, 0], [1, 1], [0] ], ]

transformed_set = set()

for bt in bt_only_list:
    triangle = [ row.copy() for row  in bt]
    for i in range(len(triangle)):
        #print('fixing row', i, 'for', triangle)
        fix_row(triangle, i)
    #print_triangle(triangle)
    if not triangle in tss_only_list:
        print('transform failed!')
        if triangle in tss_list:
            print('\ttriangle is both tss and bt')
        print_triangle(bt)
        print_triangle(triangle)
        print('#########')
    else:
        if not str(triangle) in transformed_set:
            transformed_set.add(str(triangle))
        else:
            print('transform double:')

            print_triangle(bt)
            print_triangle(triangle)
            print('*************************')


print(len(tss_only_list), 'tss only')
print(len(transformed_set),'transformed')

print('did not create these tss:')

for tss in tss_only_list:
    if str(tss) not in transformed_set:
        print_triangle(tss)