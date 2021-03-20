from City import Cities
from Individuals import Individuals
from random import random

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

    """
    Seleciona pais com base na roleta viciada
    As cidades com menores distâncias são as que possuem maior chances de ser sorteadas
    Distância e probabilidade são inversamente proporcionais (quanto menor a distância, maior a chance)
    """

    def select_parents(self, sum_travelled_distances):
        total_coefficient = 0
        parent = -1  # nenhum indivíduo sorteado
        sum = 0
        i = 0

        # criamos um coeficiente baseado na probabilidade do indivíduo ser selecionado e somamos
        for index in range(len(self.population)):
            total_coefficient += (1 / self.population[index].travelled_distance)

        # geramos as probabilidades
        for i_ in range(len(self.population)):
            coefficient = (1 / self.population[i_].travelled_distance)
            self.population[i_].probability = (coefficient / total_coefficient)

        sortedValue = random()  # sorteamos um número da roleta (0 - 1) --> 0% a 100%

        self.sort_population()
        while i < len(self.population) and sum < sortedValue:
            sum += self.population[i].probability
            parent += 1
            i += 1
        return parent

    def resolve(self, mutationRate, generations, time_distances, cities):
        self.init_population(time_distances, cities)
        for individual in self.population:
            individual.fitness()

        self.sort_population()

        for generation in range(generations):
            sum_travelled_distance = self.sum_travelled_distance()
            newPopulation = []

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
                print("Generation: %s New population: %s - Travelled Distance: %s" %
                      (generation, individual.chromosome, individual.travelled_distance))

            # ordena população para melhor solução estar na primeira posição
            self.sort_population()

            best = self.population[0]
            self.best_individual(best)

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
            "generations":2,
            'cities':{"a":["orig", "c", [0, 1, 2, 5]],
                    "b":["orig", "d", [1, 0, 4, 5]],
                    "c":["dest", "a", [2, 4, 0, 6]],
                    "d":["dest", "b", [5, 5, 6, 0]],
                    },
        }

    if event:
        population_size = int(event['populationSize'])
        mutation_rate = int(event["mutationRate"])
        generations = int(event["generations"])
        body_cities = event['cities']

    try:
        c = Cities()
        if body_cities:
            c.set_cities(body_cities)
        else:
            c.test()  # carrega cidades para testes

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