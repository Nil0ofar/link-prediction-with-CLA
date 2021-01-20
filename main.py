from cla import CLA
node_num = 900
step_num = 6
reward = 0.04
penalty = 0.01
iteration = 1

cla = CLA(node_num , reward , penalty , iteration)

for idx in range(0 ,step_num) :
    f = open("{}.txt".format(idx), 'r')
    mat = [[0 for i in range(node_num)]for j in range(node_num)]
    for line in f:
        x, y = map(int, line.split(' '))
        mat[x][y] = mat[y][x] = 1

    cla.update(mat)
    print("AUC : " + str(cla.predict(mat)))



