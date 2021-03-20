class City():
    def __init__(self, name, trip_type, detail, distances):
        self.name = name
        self.trip_type = trip_type
        self.detail = detail
        self.distances = distances

    def getName(self):
        return self.name

    def getDistances(self):
        return self.distances


class Cities():
    def __init__(self, cities=[]):
        self.cities = cities

    def chromose_to_cities(self, chromosome):
        cities = []
        for i in range(len(chromosome)):
            cities.append(self.get_city(chromosome[i]).name)
        return cities

    def get_city_distances(self, index):
        return self.get_city(index).distances

    def get_cities(self):
        return self.cities

    def get_city(self, index):
        return self.cities[index]

    def set_cities(self, cities={},
                        #  distances=[[]]
                         ):
        self.cities = []
        for k, v in cities.items():
            self.cities.append(City(name=k, trip_type=v[0], detail=v[1], distances=v[2]
                                    # distances[i]
                                    )
                                )

    def get_total_cities(self):
        return len(self.cities)

class Distance:
    def __init__(self, cities):
        self.cities = cities

    def get_distance(self, fromCity: int, toCity: int):
        city1 = self.cities[fromCity]
        total_distance = city1.distances[toCity]
        return total_distance
