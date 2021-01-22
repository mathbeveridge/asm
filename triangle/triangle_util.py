



def print_triangle(triangle):
    for row in triangle:
        print(row)
    print('-----------')



def to_ytableau(triangle):
    tex_list = ['$\\begin{ytableau}']
    for row in triangle:
        tex_list.append(' & '.join(str(r) for r in row) + ' \\\\')
    tex_list.append('\\end{ytableau}$')

    return ' '.join(tex_list)


# returns [[0],[0,0],[0,0,0],...]
def get_all_zero(size):
    return [[0] * k for k in range(1,size+1)]