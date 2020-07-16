import triangle.build_gog as build_gog
import triangle.build_magog as build_magog


for n in range(1,4):
    magogs = build_magog.build_magog(n)
    gogs = build_gog.build_gog(n)

    flipped_gogs = build_gog.reflect_list(gogs)

    both_list = []
    both_count = 0

    for magog in magogs:
        if magog in flipped_gogs:
            both_count = both_count + 1
            both_list.append(magog)

    for b in both_list:
        for row in b:
            print(row)
        print('-----')
    print(n, both_count)
    print('========')



#gogs = build_gog.build_gog(4)
#for g in gogs:
#    f = build_gog.reflect(g)
#    for row in f:
#        print(row)
#    print('----')