import triangle.build_magog as build
import triangle.gog_magog as gog_magog


def get_magog(n):
    magog_list = build.build_magog(n)
    #for m in magog_list:
    #    m.reverse();
    return magog_list


# gog words avoiding 321
def row_increase_at_most_one(magog_list, n):
    good_magog = magog_list.copy()

    for m in magog_list:
        for row in m:
            for i in range(0,len(row)-1):
                if row[i] < row[i+1] -1:
                    good_magog.remove(m)
                    break
            if not m in good_magog:
                break

    return(good_magog)


# A005157 totally symmetric plane partitions that fit in an n X n X n box
#5, 16, 66, 352, 2431, 21760
def diag_incr_at_most(magog_list, n, k):
    good_magog = magog_list.copy()

    for m in magog_list:
        #print(m)
        for i in range(len(m)-1):
            for j in range(0,i+1):
                #print(i,j)
                if m[i][j] < m[i+1][j+1] - 1:
                    good_magog.remove(m)
                    break
            if not m in good_magog:
                break
    return(good_magog)



for n in range(2,5):
    magog_list = get_magog(n)
    magog_list = diag_incr_at_most(magog_list,n,1)
for m in magog_list:
    for x in m:
        print(x)
    print('-----')
print(len(magog_list))


