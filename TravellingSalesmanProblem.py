import random
from typing import List
import constants


class TravellingSalesmanProblem:
    cities: List[str] = []
    distances: List = []

    @staticmethod
    def init():
        TravellingSalesmanProblem.cities = ["Paris", "Lyon", "Marseille", "Nantes", "Bordeaux", "Toulouse", "Lille"]

        TravellingSalesmanProblem.distances.append([0, 462, 772, 379, 546, 678, 215])  # Paris
        TravellingSalesmanProblem.distances.append([462, 0, 326, 598, 842, 506, 664])  # Lyon
        TravellingSalesmanProblem.distances.append([772, 326, 0, 909, 555, 407, 1005])  # Marseille
        TravellingSalesmanProblem.distances.append([379, 598, 909, 0, 338, 540, 584])  # Nantes
        TravellingSalesmanProblem.distances.append([546, 842, 555, 338, 0, 250, 792])  # Bordeaux
        TravellingSalesmanProblem.distances.append([678, 506, 407, 540, 250, 0, 926])  # Toulouse
        TravellingSalesmanProblem.distances.append([215, 664, 1005, 584, 792, 926, 0])  # Lille

    @staticmethod
    def get_distance(city1: int, city2: int) -> int:
        return TravellingSalesmanProblem.distances[city1][city2]

    @staticmethod
    def get_city(city_index: int) -> str:
        return TravellingSalesmanProblem.cities[city_index]

    @staticmethod
    def get_cities_index() -> List[int]:
        return [i for i in range(len(TravellingSalesmanProblem.cities))]


class Gene:
    city_index: int = None

    def __init__(self, *args, **kwargs):
        if 'gene' in kwargs:
            gene = kwargs.get('gene')
            self.city_index = gene.city_index
        elif 'city_index' in kwargs:
            city_index = kwargs.get('city_index')
            self.city_index = city_index

    def get_distance(self, gene):
        return TravellingSalesmanProblem.get_distance(self.city_index, gene.city_index)

    def __str__(self):
        return TravellingSalesmanProblem.get_city(self.city_index)

    def mutate(self) -> None:
        raise NotImplementedError("You must implemente this")


class Individual:

    def __init__(self, *args, **kwargs):
        self.fitness: float = None
        self.genome: List[Gene] = []

        if len(kwargs) == 0:
            available_indexes = TravellingSalesmanProblem.get_cities_index()
            while len(available_indexes) != 0:
                index = random.randrange(len(available_indexes))
                self.genome.append(Gene(city_index=available_indexes[index]))
                del available_indexes[index]

        elif 'parent' in kwargs:
            parent = kwargs.get('parent')
            for gene in parent.genome:
                self.genome.append(Gene(gene))
            self.mutate()

        elif 'parent1' in kwargs and 'parent2' in kwargs:
            parent1 = kwargs.get('parent1')
            parent2 = kwargs.get('parent2')
            cut_point = random.randrange(len(parent1.genome))
            for i in range(cut_point):
                self.genome.append(Gene(parent1.genome[i]))
            for gene in parent2.genome:
                if gene not in self.genome:
                    self.genome.append(Gene(gene))
            self.mutate()

    def mutate(self) -> None:
        if random.random() < constants.mutation_rate:
            index1 = random.randrange(len(self.genome))
            gene = self.genome[index1]
            self.genome.remove(gene)
            index2 = random.randrange(len(self.genome))
            self.genome.insert(index2, gene)

    def evaluate(self) -> float:
        total_km = 0
        former_gene = None
        gene: Gene
        for gene in self.genome:
            if former_gene is not None:
                total_km = total_km + gene.get_distance(former_gene)
            former_gene = gene
        total_km = total_km + former_gene.get_distance(self.genome[0])
        self.fitness = total_km
        return self.fitness

    def __str__(self) -> str:
        gen = "(" + str(self.fitness) + ")"
        genome_str = ""
        for gene in self.genome:
            genome_str = genome_str + " - " + str(gene)
        return gen + " " + genome_str


class IndividualFactory:
    """ Cette classe sert à instancier des individus selon un nombre de parent :
        Si aucun parent : caractéristiques aléatoires
        Si 1 parent : c'est un clone du parent
        Si 2 parents : Il prend la moitié des caractéristiques de chaque coté
    """

    @staticmethod
    def init() -> None:
        TravellingSalesmanProblem.init()

    @staticmethod
    def create_individual(*args, **kwargs) -> Individual:
        if len(kwargs) == 0:
            ind = Individual()
            return ind
        elif 'parent' in kwargs:
            return Individual(kwargs.get('parent'))
        elif 'parent1' in kwargs and 'parent2' in kwargs:
            return Individual(kwargs.get('parent1'), kwargs.get('parent2'))


class EvolutionnaryProcess:
    population: List[Individual] = []
    nb_generation: int = 0
    best_fitness: float = None
    problem_name: str = ""

    def __init__(self):
        """À l'initialisation, on se contente de créer un nombre défini d'indivius
        et de les ajouter à la liste de la population"""
        IndividualFactory.init()
        for i in range(constants.nb_individual + 1):
            self.population.append(IndividualFactory.create_individual())

    def survival(self, new_generation: List[Individual]) -> None:
        """L'étape de survie consiste à remplacer l'ancienne génération par la nouvelle"""
        self.population = new_generation

    def selection(self) -> Individual:
        """L'étape de sélection consiste à prendre au hasard 2 individus de la population
        et de ne garder que celui qui a la meilleure fitness"""
        index1: int = random.randrange(constants.nb_individual)
        index2: int = random.randrange(constants.nb_individual)
        if self.population[index1].fitness <= self.population[index2].fitness:
            return self.population[index1]
        else:
            return self.population[index2]

    def run(self):
        """ Le processus d'évolution va perdurer jusqu'à ce que 2 conditions soient remplis :
                - avoir atteint le nb max de génération défini en constante
                - que la meilleure fitness est atteint un certain seuil
            On initialise le 1er individu de la population comme étant le meilleur
            On va ensuite parcourir chaque individu, l'évaluer et calculer sa fitness et la comparer à celle du meilleur
            Si elle meilleur, c'est l'individu courant qui devient le meilleur individu
            Suite à ça, on affiche le meilleur individu de la population
            Et on initialise la prochaine génération avec au moins cet individu
            Enfin, on génère la prochaine génération en prenant en compte un taux de crossover :
            càd que 60% de la pop aura 2 parents, et le reste sera un clone
            Puis on remplace l'ancienne génération par la nouvelle et on recommence
        """
        self.best_fitness = constants.min_fitness + 1

        while self.nb_generation < constants.nb_max_generations and self.best_fitness > constants.min_fitness:
            best_individual: Individual = self.population[0]
            for individual in self.population:
                individual.evaluate()
                if individual.fitness < best_individual.fitness:
                    best_individual = individual

            print(str(self.nb_generation) + " -> " + best_individual.__str__())
            self.best_fitness = best_individual.fitness

            new_population: List[Individual] = [best_individual]

            for i in range(constants.nb_individual + 1):
                if random.random() < constants.crossover_rate:
                    # Avec crossover, donc 2 parents
                    parent1: Individual = self.selection()
                    parent2: Individual = self.selection()
                    new_population.append(IndividualFactory.create_individual(parent1, parent2))
                else:
                    parent: Individual = self.selection()
                    new_population.append(IndividualFactory.create_individual(parent))

            self.survival(new_population)
            self.nb_generation = self.nb_generation + 1


def main():
    syst = EvolutionnaryProcess()
    syst.run()


if __name__ == '__main__':
    main()
