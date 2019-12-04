
# Algorithme Génétique 

Les algorithmes génétiques doivent etre utilisés si on se retrouve dans un des cas suivants :

- Le nombre de solutions potentielles doit etre très grand
- Il n'y a pas de methode exacte permettant d'obtenir une solution
- Une méthode presque optimale est acceptable
- On peut évaluer la qualité d'une solution potentielle.

## I- Vue d'ensemble du cycle d'algorithme génétique :

### 1 - Phases d'initialisation et de terminaison

    Lors de la phase d'initialisation, une première population est créé. On peut
    initiliaser leurs 'genes' aléatoirement, mais si on connait déjà la direction à
    prendre, on peut les initialiser dans ce sens et gagner du temps dans l'évolution.

    Il faut aussi définir un critère d'arret de l'évolution : ça peut etre un
    nombre de génération ou sur un score fitness minimal, ou encore "si pas de meilleure
    solution trouvée pendant X générations"

### 2 - Phase de sélection

    Il s'agit de déterminer quels individus méritent d'etre parent pour la prochaine
    génération. On les note avec une fonction de fitness qui leur attribut à chacun
    un score qui représente leur performance dans le problème donné.

    Une des solutions courantes est d'utiliser une roulette biaisée : plus un individu est adapté,
    et plus il aura une grande part sur la roue. Les individus suivants ont donc une part de plus
    en plus petite. Un tirage au sort indique alors quel est l'individu choisi.

    Statistiquement, ceux ayant les fitness les plus élevées auront le plus d'enfants, mais tous
    ont au moins une chance de se reproduire, meme si elle reste faible.

    La part de la roulette de chaque individu peut etre déterminée par le rang de celui-ci,
    le premier ayant toujours la meme part par rapport aux deuxième, ou par sa fitness. Dans
    ce dernier cas, les proportions changent à chaque génération et un individu bcp plus
    adapté que les autres de sa population aura bcp plus de descendants, pour transmettre
    rapidement ses genes.

    ((Mais parfois certains gènes en apparence mauvais peuvent aboutir une meilleure
    solution. Donc on peut sélectionner par exemple 90% de la meilleure moitié
    et prendre 10% des moins bons au pif.))


### 3 - Phase de reproduction avec mutation

    a) Crossover

    Pour chaque enfant de la génération N+1, on sélectionne 1 à N parents (en général 2)
    pour lesquelles on mélange leurs genes dans la fonction 'crossover'.

    Le crossover n'est pas automatique : on peut définir un taux de crossover (ex: + de 50%)
    qui entrainera un mélange des genes entre 2 parents. Le reste des individus pourront etre
    de simple clone de leurs parents. Tout dépendra de la rapidité de l'évolution.

    Le crossover en tant que tel va dépendre de comment on aura structuré nos genes. Si
    nos genes sont une simple liste de valeurs. On peut définir un point de coupure dans ce
    tableau : L'enfant prendra la 1ère partie du tableau des genes du parent 1 et la 2ème
    partie du tableau du parent 2 (discret). On peut aussi effectuer une moyenne (continu).

    Mais tout dépend de la structure de données de nos genes.

    b) Mutation

    Une fois le mélange effectué et attribuer aux enfants, on applique des mutations aléatoires
    aux enfants et dont le nombre dépend du taux de mutation choisi de l'algorithme.

    Celà consiste à choisir aléatoirement certains genes. La probabilité qu'un gene soit touché
    par une mutation s'appelle le taux de mutation. Si il est trop élevé, les bonnes solutions
    risquent de disparaitre. Il faut trouver le bon compromis. (Par défaut 5%).

    Cette mutation peut consister à remplacer un gene par une valeur aléatoire, mais en général
    la mutation suit une distribution normale (courbe en cloche) : On va modifier un peu la
    valeur.


### 4 - Phase de survie

    On remplace les parents par les enfants, et on reboucle sur le processus

## II - Convergence

    Il peut potentiellement mettre beaucoup de temps pour que la l'algorithme
    converge vers une solution en un temps acceptable.

    Pour celà, on peut jouer sur plusieurs facteurs :
    - Les opérateurs : Sélection, Mutation, Crossover, Survie
    - Les représentations : Gènes, Individus, Population
