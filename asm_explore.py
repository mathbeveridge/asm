from asm import asm
from stackset import build_stack_sets as build

psm_list = asm.getPartialSums(4)
pst_list = asm.getPartialSumTriangles(4)

sst_list = build.build_stacks(3)

#print('missing from SST list')

for pst in psm_list:
    #if pst not in sst_list:
    for x in pst:
        print(x)
    print('-----')

#print('missing from PST list')

#for sst in sst_list:
#    if sst not in pst_list:
#        for x in sst:
#            print(x)
#        print('-----')



# print('mapping count')
# hash_map = dict()
#
# for matrix,triangle in zip(psm_list,pst_list):
#     key = str(triangle)
#     if not key in hash_map:
#         print('adding key', key)
#         #hash_map[key] = []
#         hash_map[key] = 0
#     #hash_map[key] = hash_map[key].append(matrix)
#     hash_map[key] = hash_map[key] + 1
#
#
# for key in hash_map:
#     if hash_map[key] > 1:
#         print(key, hash_map[key])