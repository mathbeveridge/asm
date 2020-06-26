import triangle.gog_magog as gog_magog
import triangle.gog_pyramid as gog_pyramid






#print(gog_magog.max_gog(4))

#gp = gog_pyramid.GogPyramid(((4, 2, 1, 0),(3, 1, 1), (2, 1), (1,)))
#print(gp.pyramid)


#gp.print_gog()

#gp.print_layers()

#g = gog_magog.gog3[39]

hm = dict()

for g in gog_magog.gog3:

    pyr = gog_pyramid.GogPyramid(g)
    #pyr.print_gog()
    #pyr.print_layers_z()

    print(pyr.gog)
    #pyr.explode_columns()

    #print('after')

    #pyr.print_layers_z()

    layers = pyr.get_layers_z();

    st = str(layers[0])

    print(st)

    if not st in hm:
        hm[st] = 0

    hm[st] = hm[st] + 1

    print('*********')


for key in hm:
    print(key, hm[key])