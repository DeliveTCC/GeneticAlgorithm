from random import randint
from City import Distance

class Individuals():
    def __init__(self, time_distances, cities, generation=0):
        self.time_distances = time_distances  # 2D array [[], []]
        self.cities = cities  # City list [City(), City()]
        self.generation = generation
        self.note_review = 0
        self.chromosome = []
        self.visited_cities = []
        self.travelled_distance = 0
        self.probability = 0

        # Cria cromossomos (não repete cidades)
        # Ex.: [0, 2, 3, 1] --> [A, C, D, B]
        cities_copy = self.cities.copy()
        for i in range(len(cities_copy)):
            cities_copy[i]._index = i
        
        names_aux = []
        while len(cities_copy) > 0:
            city = randint(0, len(cities_copy) - 1)
            
            if ((cities_copy[city].trip_type == "dest") & (cities_copy[city].detail in names_aux)
                | (cities_copy[city].trip_type == "orig")):
                
                names_aux.append(cities_copy[city].name)
                self.chromosome.append(cities_copy.pop(city)._index)
        
    # Avaliação de aptidão
    def fitness(self):
        sum_distance = 0
        current_city = self.chromosome[0]  # cidade de partida do cromossomo

        for i in range(len(self.chromosome)):
            d = Distance(self.cities)
            dest_city = self.chromosome[i]  # cidade atual no grafo
            distance = d.get_distance(current_city, dest_city)
            sum_distance += distance
            self.visited_cities.append(dest_city)  # adiciona cromossomo como cidade visitada
            current_city = dest_city

            # soma distância da última cidade para a primeira - caminho de volta
            if i == len(self.chromosome) - 1:
                sum_distance += d.get_distance(self.chromosome[len(self.chromosome) - 1], self.chromosome[0])

        self.travelled_distance = sum_distance

    """
    Alteração dos cromossomos para trazer diversidade nas gerações
    Sorteia um gene no cromossomo e realiza a troca, respeitando o critério de não conter genes duplicados.
    """

    def crossover(self, otherIndividual):
        genes_1 = self.chromosome
        genes_2 = otherIndividual.chromosome
        selected_gene = randint(0, len(genes_1) - 1)
        self.exchange_gene(selected_gene, genes_1, genes_2)
        exchanged_genes = []
        exchanged_genes.append(selected_gene)
        while True:
            duplicated_gene = self.get_duplicated_gene(genes_1, exchanged_genes)
            if (duplicated_gene == -1):
                break
            self.exchange_gene(duplicated_gene, genes_1, genes_2)
            exchanged_genes.append(duplicated_gene)

        childs = [
            Individuals(self.time_distances, self.cities, self.generation + 1),
            Individuals(self.time_distances, self.cities, self.generation + 1)
        ]

        childs[0].chromosome = genes_1
        childs[1].chromosome = genes_2

        return childs

    """
    Realiza combinação dos genes de um cromossomo
    """

    def exchange_gene(self, gene, genes_1, genes_2):
        tmp = genes_1[gene]
        genes_1[gene] = genes_2[gene]
        genes_2[gene] = tmp

    """
    Busca genes duplicados em um cromossomo
    """

    def get_duplicated_gene(self, genes, exchanged_genes):
        for gene in range(len(genes)):
            if gene in exchanged_genes:
                continue

            if len([g for g in genes if g == genes[gene]]) > 1:
                return gene

        return -1

    """
    Mutação
    Sorteia um intervalo de 1% a 100%, se corresponder a taxa de mutação altera os genes
    Respeita o critério de não existir genes duplicados
    """

    def mutate(self, mutationRate):
        # sorteia um intervalo de 1% a 100%
        if randint(1, 100) <= mutationRate:
            print("Realizando mutação no cromossomo %s" % self.chromosome)
            genes = self.chromosome
            gene_1 = randint(0, len(genes) - 1)
            gene_2 = randint(0, len(genes) - 1)
            tmp = genes[gene_1]
            genes[gene_1] = genes[gene_2]
            genes[gene_2] = tmp
            print("Valor após mutação: %s" % self.chromosome)
        return self