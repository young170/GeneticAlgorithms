import random
import argparse

class KnapsackGeneticAlgorithm:
    def __init__(self, max_weight, items, population_size, mutation_rate, generations, tournament_size):
        self.MAX_WEIGHT = max_weight
        self.items = items
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.tournament_size = tournament_size

    # init 0-1 knapsack
    def initialize_population(self):
        return [random.choices([0, 1], k=len(self.items)) for _ in range(self.population_size)]
    
    # calculate the fitness of an individual (total value)
    def fitness(self, individual):
        total_weight = sum(item["weight"] for i, item in enumerate(self.items) if individual[i] == 1)
        total_value = sum(item["value"] for i, item in enumerate(self.items) if individual[i] == 1)
        
        if total_weight > self.MAX_WEIGHT:
            return 0 # weight limit exceeded
        else:
            return total_value

    # tournament selection
    def tournament_selection(self, population):
        selected = []

        for _ in range(len(population)):
            tournament = random.sample(population, self.tournament_size)
            winner = max(tournament, key=self.fitness)
            selected.append(winner)

        return selected

    # one-point crossover with backcross breeding
    def one_point_crossover_with_backcross(self, parent1, parent2):
        crossover_point = random.randint(1, len(parent1) - 1)

        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]

        # fitness of parents and children
        parent1_fitness = self.fitness(parent1)
        parent2_fitness = self.fitness(parent2)
        child1_fitness = self.fitness(child1)
        child2_fitness = self.fitness(child2)

        # a loss in fitness battled by backcross breeding
        if child1_fitness < parent1_fitness:
            crossover_point = random.randint(1, len(parent1) - 1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
        if child2_fitness < parent2_fitness:
            crossover_point = random.randint(1, len(parent1) - 1)
            child2 = parent2[:crossover_point] + parent1[crossover_point:]

        return child1, child2

    # bit flip mutation
    def mutate(self, individual):
        mutated_individual = individual[:]

        for i in range(len(mutated_individual)):
            if random.random() < self.mutation_rate:
                mutated_individual[i] = mutated_individual[i] % 1

        return mutated_individual

    def run_genetic_algorithm(self):
        population = self.initialize_population()

        for generation in range(self.generations):
            selected = self.tournament_selection(population)
            next_generation = []

            while len(next_generation) < self.population_size:
                parent1, parent2 = random.sample(selected, 2)

                # crossover of winners
                child1, child2 = self.one_point_crossover_with_backcross(parent1, parent2)
                
                # Mutation
                # Because crossover across the winners already occured to obtain a maximum, mutation causes a loss
                # Mutating the parent causes similar result with same reasons
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                
                next_generation.extend([child1, child2])

            population = next_generation
            
        best_solution = max(population, key=self.fitness)
        best_value = self.fitness(best_solution)
        print("Best solution:", best_solution)
        print("Total value:", best_value)

if __name__ == "__main__":
    MAX_WEIGHT = 1000
    items = [
    {"weight": 10, "value": 60},
    {"weight": 20, "value": 100},
    {"weight": 30, "value": 120},
    {"weight": 5, "value": 30},
    {"weight": 15, "value": 50},
    {"weight": 25, "value": 70},
    {"weight": 35, "value": 80},
    {"weight": 7, "value": 45},
    {"weight": 12, "value": 90},
    {"weight": 22, "value": 110},
    {"weight": 40, "value": 130},
    {"weight": 50, "value": 140},
    {"weight": 60, "value": 150},
    {"weight": 55, "value": 160},
    {"weight": 18, "value": 70},
    {"weight": 28, "value": 90},
    {"weight": 38, "value": 110},
    {"weight": 9, "value": 40},
    {"weight": 31, "value": 80},
    {"weight": 42, "value": 120}
]

    parser = argparse.ArgumentParser(description="GA parameters")
    parser.add_argument('-p', '--population', type=int, default=100, help='Size of population')
    parser.add_argument('-m', '--mutation', type=float, default=0.1, help='Rate of mutation')
    parser.add_argument('-g', '--generation', type=int, default=100, help='Number of generations')
    parser.add_argument('-t', '--tournament', type=int, default=10, help='Size of tournament')

    args = parser.parse_args()

    knapsack_ga = KnapsackGeneticAlgorithm(MAX_WEIGHT, items, args.population, args.mutation, args.generation, args.tournament)
    knapsack_ga.run_genetic_algorithm()
