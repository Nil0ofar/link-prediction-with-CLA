from basic_structure import LA , Genome

class Cell:
    def __init__(self , sz , penalty , reward):
        self._size = sz
        self.penaly = penalty
        self.reward = reward
        self.LAs = []
        self.neighbor = []
        self.chosen_neighbor = []
        for i in range(sz) :
            self.LAs.append(LA())

        self.genome = Genome([0 for i in range(sz)])

    def update_genome(self , goal):
        temp = []
        for l in self.LAs:
            temp.append(l.get_action())
        new_genome = Genome(temp)

        if self.genome.fitness(goal) < new_genome.fitness(goal):
            self.genome = new_genome

    def update_chosen_neighbor(self, goal):
        self.chosen_neighbor.clear()
        for other in self.neighbor:
            if other.genome.fitness(goal) > self.genome.fitness(goal):
                self.chosen_neighbor.append(other)

    def __update(self, idx, choice, punish):


        if punish:
            self.LAs[idx].probability[choice] = (1 - self.penalty) * self.LAs[idx].probability[choice]
        else:
            self.LAs[idx].probability[choice] += self.reward * (1 - self.LAs[idx].probability[choice])

        self.LAs[idx].probability[1 - choice] = 1 - self.LAs[idx].probability[choice]

        #print(idx, choice, punish, self.LAs[idx].probability[0])



    def update_by_reinforcement_signal(self):
        for idx in range(self._size):
            one = 0
            zero = 0

            for ne in self.chosen_neighbor :
                if ne[idx] == 0:
                    zero += 1
                else:
                    one += 1

            if self.genome.gene[idx] == 0:
                self.__update(idx, 0, one > zero)
            else :
                self.__update(idx, 1, zero > one)

