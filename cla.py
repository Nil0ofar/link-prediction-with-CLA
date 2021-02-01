from cell import Cell
from random import randint

class CLA :

    def __init__(self, max_cell , penalty , reward , iteration):
        self._size = max_cell
        self.penalty = penalty
        self.reward = reward
        self.iteration = iteration
        self.cells = []
        self.cur_adj_mat = [[0 for i in range(max_cell)]for j in range(max_cell)]
        for i in range(max_cell):
            self.cells.append(Cell(max_cell, penalty, reward, i))

    def update(self, next_adjacency_matrix):

        for it in range(self.iteration):

            for i in range(self._size):
                self.cells[i].update_genome(next_adjacency_matrix[i])

            for i in range(self._size):
                self.cells[i].update_chosen_neighbor(next_adjacency_matrix)

            for i in range(self._size):
                self.cells[i].update_by_reinforcement_signal()

        for i in range(self._size):
            self.cells[i].neighbor.clear()
            for j in range(self._size):
                if next_adjacency_matrix[i][j] == 1:
                    self.cells[i].neighbor.append(self.cells[j])

    def __AUC(self, total, greater, equal):
        #print(greater, equal, total)
        return (greater + 0.5 * equal) / total

    def __get_score(self, pair):
        return (self.cells[pair[0]].LAs[pair[1]].probability[1] + self.cells[pair[1]].LAs[pair[0]].probability[1]) / 2

    def predict(self, mat):
        missing_link = []
        non_existent_link = []
        for i in range(self._size):
            for j in range(i + 1, self._size):
                #print(self.cells[i].LAs[j].probability[1])
                if self.cells[i].LAs[j].probability[0] > 0.5 or self.cells[j].LAs[i].probability[0] > 0.5: #non-observed
                    if mat[i][j] == 1: #missing
                        missing_link.append((i, j))
                    else: #non-existent
                        non_existent_link.append((i, j))

        #print(len(missing_link))
        if len(missing_link) == 0 or len(non_existent_link) == 0:
            return 0
        greater = 0
        total_test = 1000
        equal = 0
        for i in range(total_test) :
            idx_m = randint(0, len(missing_link) - 1)
            idx_n = randint(0, len(non_existent_link) - 1)

            score_m = self.__get_score(missing_link[idx_m])
            score_n = self.__get_score(non_existent_link[idx_n])
            if score_m > score_n:
                greater += 1
            elif score_m == score_n:
                equal += 1
        print(total_test, greater, equal)
        return self.__AUC(total_test, greater, equal)