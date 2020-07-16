import triangle.gog_magog as gog_magog



def build_magog(n):
    magog_list = gog_magog.build_magog(n)
    for m in magog_list:
        m.reverse()

    return magog_list