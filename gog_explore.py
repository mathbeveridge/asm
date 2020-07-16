import triangle.build_gog as build_gog

for n in range(2,6):
    gogs = build_gog.build_gog(n)
    print(len(gogs))