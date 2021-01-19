from cell import Cell
from random import randint

class CLA :

    def __init__(self, max_cell , penalty , reward):
        self._size = max_cell
        self.penalty = penalty
        self.reward = reward
        self.cells = []
        #self.cur_adj_mat = [[0 for i in range(max_cell)]for j in range(max_cell)]
        for i in range(max_cell) :
            self.cells.append(Cell(max_cell , penalty , reward))

    def update(self, next_adjacency_matrix):

        for it in range(1):

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

    def predict(self , mat):
        missing_link = []
        non_existent_link = []
        for i in range(self._size):
            for j in range(i + 1, self._size):
                #print(self.cells[i].LAs[j].probability[1])
                if mat[i][j] == 1:
                    missing_link.append((i, j))
                else:
                    non_existent_link.append((i, j))

        #print(len(missing_link))
        if len(missing_link) == 0 or len(non_existent_link) == 0:
            return 0
        greater = 0
        total_test = 10000
        equal = 0
        for i in range(total_test) :
            idx_m = randint(0, len(missing_link) - 1)
            idx_n = randint(0, len(non_existent_link) - 1)

            score_m = self.cells[missing_link[idx_m][0]].LAs[missing_link[idx_m][1]].probability[1]
            score_n = self.cells[non_existent_link[idx_n][0]].LAs[non_existent_link[idx_n][1]].probability[1]
            if score_m > score_n :
                greater += 1
            elif score_m == score_n :
                equal += 1

        return self.__AUC(total_test , greater , equal)