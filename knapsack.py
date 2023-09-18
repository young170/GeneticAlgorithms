import random
import argparse

MAX_WEIGHT = 50
items = [
    {"weight": 10, "value": 60},
    {"weight": 20, "value": 100},
    {"weight": 30, "value": 120},
    {"weight": 5, "value": 30},
    {"weight": 15, "value": 50}
]

parser = argparse.ArgumentParser(description="GA parameters")
parser.add_argument('-p', '--population', type=int, default=100, help='Size of population')
parser.add_argument('-m', '--mutation', type=float, default=0.1, help='Rate of mutation')
parser.add_argument('-g', '--generation', type=int, default=100, help='Number of generations')
parser.add_argument('-t', '--tournament', type=int, default=10, help='Size of tournament')

args = parser.parse_args()

population_size = args.population
mutation_rate = args.mutation
generations = args.generation
tournament_size = args.tournament

def initialize_population():
    return [random.choices([0, 1], k=len(items)) for _ in range(population_size)]

# Calculate the fitness of an individual (total value)
def fitness(individual):
    total_weight = sum(item["weight"] for i, item in enumerate(items) if individual[i] == 1)
    total_value = sum(item["value"] for i, item in enumerate(items) if individual[i] == 1)
    
    if total_weight > MAX_WEIGHT:
        return 0  # Penalize solutions that exceed the weight limit
    else:
        return total_value

# Perform tournament selection
def tournament_selection(population, tournament_size):
    selected = []
    for _ in range(len(population)):
        tournament = random.sample(population, tournament_size)
        winner = max(tournament, key=fitness)
        selected.append(winner)
    return selected

# Perform one-point crossover with backcross breeding
def one_point_crossover_with_backcross(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]

    # Calculate fitness for children and parents
    parent1_fitness = fitness(parent1)
    parent2_fitness = fitness(parent2)
    child1_fitness = fitness(child1)
    child2_fitness = fitness(child2)

    # Check if children have lower fitness than parents
    if child1_fitness < parent1_fitness:
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
    if child2_fitness < parent2_fitness:
        crossover_point = random.randint(1, len(parent1) - 1)
        child2 = parent2[:crossover_point] + parent1[crossover_point:]

    return child1, child2

# Perform mutation
def mutate(individual):
    mutated_individual = individual[:]
    for i in range(len(mutated_individual)):
        if random.random() < mutation_rate:
            mutated_individual[i] = mutated_individual[i] % 1  # Flip the bit
    return mutated_individual



# __Entry__
population = initialize_population()
for generation in range(generations):
    selected = tournament_selection(population, tournament_size)
    next_generation = []
    
    while len(next_generation) < population_size:
        parent1, parent2 = random.sample(selected, 2)
        child1, child2 = one_point_crossover_with_backcross(parent1, parent2)
        child1 = mutate(child1)
        child2 = mutate(child2)
        next_generation.extend([child1, child2])
    
    population = next_generation

# Find the best solution in the final population
best_solution = max(population, key=fitness)
best_value = fitness(best_solution)
print("Best solution:", best_solution)
print("Total value:", best_value)
