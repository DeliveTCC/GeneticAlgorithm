from City import Cities
from Individuals import Individuals
from random import choices
import numpy as np

class GeneticAlgorithm():
    def __init__(self, population_size=20, cities=[]):
        self.populationSize = population_size
        self.population = []
        self.generation = 0
        self.best_solution: 0
        self.cities = cities

    # time_distances será um array 2D
    # cities será [City("A", [0, 10]), City("B", [10, 0])]
    def init_population(self, time_distances, cities):
        for i in range(self.populationSize):
            self.population.append(Individuals(time_distances, cities))

        self.best_solution = self.population[0]

    # orderna a população pelo atributo travelled_distance ascendentemente
    def sort_population(self):
        self.population = sorted(self.population,
                                 key=lambda population: population.travelled_distance,
                                 reverse=False)

    # caso encontre um indivíduo com menor distância o marcamos como melhor solução
    def best_individual(self, individual):
        if individual.travelled_distance < self.best_solution.travelled_distance:
            self.best_solution = individual

    """
    Soma distância percorrida por cada indivíduo da população
    """

    def sum_travelled_distance(self):
        sum = 0
        for individual in self.population:
            sum += individual.travelled_distance
        return sum

    def select_parents(self, sum_travelled_distances):
        """
        Este método seleciona pais com base na roleta viciada onde,
        sendo a escolha aleatória, indivíduos com as menores distâncias percorridas
        possuem maior probabilidade de serem escolhidos.

        Os pesos são inversamente proporcionais à distância percorrida
        weight = 1-(travelled_distance / total_travelled_distance)
        Sendo:
            total_travelled_distance: a soma de todas as travelled_distance da população
        """
        parent = -1  # nenhum indivíduo sorteado
        total_travelled_distance = 0

        for index in range(len(self.population)):
            distance = self.population[index].travelled_distance
            if distance != np.inf:
                total_travelled_distance += distance

        weights = [(1-(p.travelled_distance/total_travelled_distance)) if p.travelled_distance!=np.inf else 0 for p in self.population]
        
        parent = choices(range(len(self.population)), weights, k=1)
        
        return parent[0]

    def resolve(self, mutationRate, generations, time_distances, cities):
        self.init_population(time_distances, cities)
        for individual in self.population:
            individual.fitness()

        self.sort_population()

        generation = 0
        # for generation in range(generations):
        while generation < generations:
            if (generation == (generations-1)) & (self.best_solution.travelled_distance == np.inf):
                generations += 1
                
            sum_travelled_distance = self.sum_travelled_distance()
            newPopulation = []
            print("\n")

            for i in range(0, self.populationSize, 2):
                # seleciona dois indivíduos para reprodução - cai na roleta
                parent1 = self.select_parents(sum_travelled_distance)
                parent2 = self.select_parents(sum_travelled_distance)

                # cria os filhos a partir de dois pais
                childs = self.population[parent1].crossover(self.population[parent2])

                newPopulation.append(childs[0].mutate(mutationRate))
                newPopulation.append(childs[1].mutate(mutationRate))

            # sobrescreve antiga população eliminando os pais
            self.population = list(newPopulation)

            for individual in self.population:
                individual.fitness()
                # Uncomment do debug
                # print(f"Generation: {generation} New population: {individual.chromosome} - Travelled Distance: {individual.travelled_distance}")
                print(f"Generation: {generation} - Travelled Distance: {individual.travelled_distance}")

            # ordena população para melhor solução estar na primeira posição
            self.sort_population()

            best = self.population[0]
            self.best_individual(best)
            
            generation += 1

        print("\nMelhor solução -> G: %s - Distância percorrida: %s - Cromossomo: %s" % (
            self.best_solution.generation,
            self.best_solution.travelled_distance,
            self.best_solution.visited_cities
        ))

        return [
            self.best_solution.generation,
            self.best_solution.travelled_distance,
            self.best_solution.visited_cities
        ]

def run(event=None, test=False):
    """
    event example:
    event = {
        'populationSize':20,
        "mutationRate":1,
        "generations":2,
        'cities':{"a":["orig", "c", [0, 1, 2, 5]],
                  "b":["orig", "d", [1, 0, 4, 5]],
                  "c":["dest", "a", [2, 4, 0, 6]],
                  "d":["dest", "b", [5, 5, 6, 0]],
                },
    }
    """
    if test:
        event = {
            'populationSize':20,
            "mutationRate":1,
            "generations":1000,
            'matrix':{'a':["deliveryMan", None, [0, 1, 3, 7, None]],
                    "b":["collect", "c", [1, 0, 2, 4, 5]],
                    "c":["collect", "d", [3, 2, 0, 5, None]],
                    "d":["delivery", "a", [7, 4, None, 0, 6]],
                    "e":["delivery", "b", [None, 5, 5, 6, 0]],
                    },
        }
        # event = {
        #     'populationSize':20,
        #     "mutationRate":1,
        #     "generations":3000,
        #     'matrix':{'a':["dman", "b", [0, 1, 3, 7, None]],
        #               "b":["orig", "c", [1, 0, 2, 4, 5]],
        #               "c":["orig", "d", [3, 2, 0, 5, None]],
        #               "d":["dest", "a", [7, 4, None, 0, 6]],
        #               "e":["dest", "b", [None, 5, 5, 6, 0]],
        #             },
        # }
    
    if event:
        population_size = int(event['populationSize'])
        mutation_rate = int(event["mutationRate"])
        generations = int(event["generations"])
        body_cities = event['matrix']

    try:
        c = Cities()
        if body_cities:
            c.set_cities(body_cities)

        cities_list = c.get_cities()

        time_distances = []
        for city in cities_list:
            print("Distâncias da cidade: %s\n******" % city.name)
            time_distances.append(city.distances)
            print(city.distances)
            for index, distance in enumerate(city.distances):
                print("De %s --> %s = %s" % (city.name, cities_list[index].name, distance))

        ga = GeneticAlgorithm(population_size)
        result = ga.resolve(mutation_rate, generations, time_distances, cities_list)

        to_return = {
            'generation': result[0],
            'travelled_distance': result[1],
            'chromosome': result[2],
            'cities': c.chromose_to_cities(result[2])
        }
        print(to_return)
        return to_return

    except ImportError:
        print(ImportError)

if __name__ == "__main__":
    run(test=True)