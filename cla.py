from cell import Cell
from random import randint


class CLA:

    def __init__(self, max_cell, penalty, reward, iteration):
        self._size = max_cell
        self.penalty = penalty
        self.reward = reward
        self.iteration = iteration
        self.cells = []
        for i in range(max_cell):
            self.cells.append(Cell(max_cell, penalty, reward, i))

    def update(self, next_adjacency_matrix):

        for it in range(self.iteration):
            self.__update_genome_of_cells(next_adjacency_matrix)
            self.__update_chosen_neighbor_of_cells(next_adjacency_matrix)
            self.__update_cells_by_reinforcement_signal(next_adjacency_matrix)
        self.__update_neighbor_of_cells(next_adjacency_matrix)

    def __update_genome_of_cells(self, next_adjacency_matrix):
        for i in range(self._size):
            self.cells[i].update_genome(next_adjacency_matrix)

    def __update_chosen_neighbor_of_cells(self, next_adjacency_matrix):
        for i in range(self._size):
            self.cells[i].update_chosen_neighbor(next_adjacency_matrix)

    def __update_cells_by_reinforcement_signal(self, next_adjacency_matrix):
        for i in range(self._size):
            self.cells[i].update_by_reinforcement_signal()

    def __update_neighbor_of_cells(self, next_adjacency_matrix):
        for i in range(self._size):
            self.cells[i].neighbor = []
            for j in next_adjacency_matrix[i]:
                self.cells[i].neighbor.append(self.cells[j])
            # print(self.cells[i].neighbor)

    def __calculate_AUC(self, missing_link, non_existent_link):
        greater = 0
        total_test = 1000
        equal = 0
        for i in range(total_test):
            idx_m = randint(0, len(missing_link) - 1)
            idx_n = randint(0, len(non_existent_link) - 1)

            score_m = self.__get_score(missing_link[idx_m])
            score_n = self.__get_score(non_existent_link[idx_n])

            if score_m > score_n:
                greater += 1
            elif score_m == score_n:
                equal += 1
        print(total_test, greater, equal)
        return (greater + 0.5 * equal) / total_test

    def __get_score(self, pair):
        return max(self.cells[pair[0]].LAs[pair[1]].probability[1], self.cells[pair[1]].LAs[pair[0]].probability[1])

    def get_AUC(self, mat):
        missing_link = []
        non_existent_link = []

        self.__find_missing_link(mat, missing_link)
        self.__find_non_existent_link(mat, non_existent_link)

        # print(len(missing_link))
        if len(missing_link) == 0 or len(non_existent_link) == 0:
            return 0

        return self.__calculate_AUC(missing_link,non_existent_link)

    def __find_missing_link(self, mat, missing_link):
        for i in range(self._size):
            for j in mat[i]:
                if self.cells[i].LAs[j].probability[0] > 0.5 and self.cells[j].LAs[i].probability[0] > 0.5:# non-observed
                    missing_link.append((i, j))

    def __find_non_existent_link(self, mat, non_existent_link):
        for i in range(self._size):
            idx = 0
            for j in range(self._size):
                if idx < len(mat[i]) and j >= mat[i][idx]:
                    idx += 1
                    j -= 1
                    continue
                if self.cells[i].LAs[j].probability[0] > 0.5 and self.cells[j].LAs[i].probability[0] > 0.5:  # non-observed
                    non_existent_link.append((i, j))