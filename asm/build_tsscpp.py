



n = 3

tsscpp = [[0] * (2*n) for x in range(2*n)]



tri = [[6,6,6],[6,6,5],[6,5,5]]


for i in range(n):
    for j in range(n):
        tsscpp[i][j] = tri[i][j]
        tsscpp[2*n-1-i][2*n-1-j] = 2*n - tri[i][j]

# for i in range(0,n):
#     for j in range(n,2*n):
#         for k in range(n,2*n):
#             #tsscpp[i][j] = n
#             if tsscpp[2*n -1-k][2*n -1 - j] < 2*n + 1 - i:
#                 tsscpp[i][j] = k

for i in range(n, 2*n):
    for j in range(n, 2*n - (i-n)):
        print(i,j, 'leads to' ,str(i-n), str(j))
        tsscpp[i-n][j] = n + tsscpp[i][j]

for i in range(n-1):
    for j in range(n, 2*n -1 -i):
        print('i,j', i, j, 'maps to', str(n-1-i), str(3*n-1-j))
        tsscpp[n-1-i][3*n-1-j] = 2*n - tsscpp[i][j]


for i in range(n):
    for j in range(n):
        tsscpp[n+i][j] = tsscpp[i][n+j]

for row in tsscpp:
    print(row)
