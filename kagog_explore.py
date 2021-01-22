import triangle.gog_magog as gog_magog



my_list = gog_magog.build_kagog(4)

for m in my_list:
    for row in m:
        print(row)
    print('--------')

print(len(my_list))