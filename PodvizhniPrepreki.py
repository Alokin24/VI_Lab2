
#Starter kod
import bisect


"""
Дефинирање на класа за структурата на проблемот кој ќе го решаваме со пребарување.
Класата Problem е апстрактна класа од која правиме наследување за дефинирање на основните 
карактеристики на секој проблем што сакаме да го решиме
"""


class Problem:
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def successor(self, state):
        """За дадена состојба, врати речник од парови {акција : состојба}
        достапни од оваа состојба. Ако има многу следбеници, употребете
        итератор кој би ги генерирал следбениците еден по еден, наместо да
        ги генерирате сите одеднаш.

        :param state: дадена состојба
        :return:  речник од парови {акција : состојба} достапни од оваа
                  состојба
        :rtype: dict
        """
        raise NotImplementedError

    def actions(self, state):
        """За дадена состојба state, врати листа од сите акции што може да
        се применат над таа состојба

        :param state: дадена состојба
        :return: листа на акции
        :rtype: list
        """
        return self.successor(state).keys()

    def result(self, state, action):
        """За дадена состојба state и акција action, врати ја состојбата
        што се добива со примена на акцијата над состојбата

        :param state: дадена состојба
        :param action: дадена акција
        :return: резултантна состојба
        """
        possible = self.successor(state)
        return possible[action]


    def goal_test(self, state):
        """Врати True ако state е целна состојба. Даденава имплементација
        на методот директно ја споредува state со self.goal, како што е
        специфицирана во конструкторот. Имплементирајте го овој метод ако
        проверката со една целна состојба self.goal не е доволна.

        :param state: дадена состојба
        :return: дали дадената состојба е целна состојба
        :rtype: bool
        """
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Врати ја цената на решавачкиот пат кој пристигнува во состојбата
        state2 од состојбата state1 преку акцијата action, претпоставувајќи
        дека цената на патот до состојбата state1 е c. Ако проблемот е таков
        што патот не е важен, оваа функција ќе ја разгледува само состојбата
        state2. Ако патот е важен, ќе ја разгледува цената c и можеби и
        state1 и action. Даденава имплементација му доделува цена 1 на секој
        чекор од патот.

        :param c: цена на патот до состојбата state1
        :param state1: дадена моментална состојба
        :param action: акција која треба да се изврши
        :param state2: состојба во која треба да се стигне
        :return: цена на патот по извршување на акцијата
        :rtype: float
        """
        return c + 1

    def value(self):
        """За проблеми на оптимизација, секоја состојба си има вредност. 
        Hill-climbing и сличните алгоритми се обидуваат да ја максимизираат
        оваа вредност.

        :return: вредност на состојба
        :rtype: float
        """
        raise NotImplementedError


"""
Дефинирање на класата за структурата на јазел од пребарување.
Класата Node не се наследува
"""


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Креирај јазол од пребарувачкото дрво, добиен од parent со примена
        на акцијата action

        :param state: моментална состојба (current state)
        :param parent: родителска состојба (parent state)
        :param action: акција (action)
        :param path_cost: цена на патот (path cost)
        """
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0  # search depth
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node %s>" % (self.state,)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """Излистај ги јазлите достапни во еден чекор од овој јазол.

        :param problem: даден проблем
        :return: листа на достапни јазли во еден чекор
        :rtype: list(Node)
        """
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """Дете јазел

        :param problem: даден проблем
        :param action: дадена акција
        :return: достапен јазел според дадената акција
        :rtype: Node
        """
        next_state = problem.result(self.state, action)
        return Node(next_state, self, action,
                    problem.path_cost(self.path_cost, self.state,
                                      action, next_state))

    def solution(self):
        """Врати ја секвенцата од акции за да се стигне од коренот до овој јазол.

        :return: секвенцата од акции
        :rtype: list
        """
        return [node.action for node in self.path()[1:]]

    def solve(self):
        """Врати ја секвенцата од состојби за да се стигне од коренот до овој јазол.

        :return: листа од состојби
        :rtype: list
        """
        # changed to -1
        return [node.state for node in self.path()[-1]]

    def path(self):
        """Врати ја листата од јазли што го формираат патот од коренот до овој јазол.

        :return: листа од јазли од патот
        :rtype: list(Node)
        """
        x, result = self, []
        while x:
            result.append(x)
            x = x.parent
        result.reverse()
        return result

    """Сакаме редицата од јазли кај breadth_first_search или 
    astar_search да не содржи состојби - дупликати, па јазлите што
    содржат иста состојба ги третираме како исти. [Проблем: ова може
    да не биде пожелно во други ситуации.]"""

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)


"""
Дефинирање на помошни структури за чување на листата на генерирани, но непроверени јазли
"""


class Queue:
    """Queue е апстрактна класа / интерфејс. Постојат 3 типа:
        Stack(): Last In First Out Queue (стек).
        FIFOQueue(): First In First Out Queue (редица).
        PriorityQueue(order, f): Queue во сортиран редослед (подразбирливо,од најмалиот кон
                                 најголемиот јазол).
    """

    def __init__(self):
        raise NotImplementedError

    def append(self, item):
        """Додади го елементот item во редицата

        :param item: даден елемент
        :return: None
        """
        raise NotImplementedError

    def extend(self, items):
        """Додади ги елементите items во редицата

        :param items: дадени елементи
        :return: None
        """
        raise NotImplementedError

    def pop(self):
        """Врати го првиот елемент од редицата

        :return: прв елемент
        """
        raise NotImplementedError

    def __len__(self):
        """Врати го бројот на елементи во редицата

        :return: број на елементи во редицата
        :rtype: int
        """
        raise NotImplementedError

    def __contains__(self, item):
        """Проверка дали редицата го содржи елементот item

        :param item: даден елемент
        :return: дали queue го содржи item
        :rtype: bool
        """
        raise NotImplementedError


class Stack(Queue):
    """Last-In-First-Out Queue."""

    def __init__(self):
        self.data = []

    def append(self, item):
        self.data.append(item)

    def extend(self, items):
        self.data.extend(items)

    def pop(self):
        return self.data.pop()

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return item in self.data


class FIFOQueue(Queue):
    """First-In-First-Out Queue."""

    def __init__(self):
        self.data = []

    def append(self, item):
        self.data.append(item)

    def extend(self, items):
        self.data.extend(items)

    def pop(self):
        return self.data.pop(0)

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return item in self.data


class PriorityQueue(Queue):
    """Редица во која прво се враќа минималниот (или максималниот) елемент
    (како што е определено со f и order). Оваа структура се користи кај
    информирано пребарување"""
    """"""

    def __init__(self, order=min, f=lambda x: x):
        """
        :param order: функција за подредување, ако order е min, се враќа елементот
                      со минимална f(x); ако order е max, тогаш се враќа елементот
                      со максимална f(x).
        :param f: функција f(x)
        """
        assert order in [min, max]
        self.data = []
        self.order = order
        self.f = f

    def append(self, item):
        bisect.insort_right(self.data, (self.f(item), item))

    def extend(self, items):
        for item in items:
            bisect.insort_right(self.data, (self.f(item), item))

    def pop(self):
        if self.order == min:
            return self.data.pop(0)[1]
        return self.data.pop()[1]

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return any(item == pair[1] for pair in self.data)

    def __getitem__(self, key):
        for _, item in self.data:
            if item == key:
                return item

    def __delitem__(self, key):
        for i, (value, item) in enumerate(self.data):
            if item == key:
                self.data.pop(i)

import sys


"""
Неинформирано пребарување во рамки на дрво.
Во рамки на дрвото не разрешуваме јамки.
"""


def tree_search(problem, fringe):
    """ Пребарувај низ следбениците на даден проблем за да најдеш цел.

    :param problem: даден проблем
    :param fringe:  празна редица (queue)
    :return: Node
    """
    fringe.append(Node(problem.initial))
    while fringe:
        node = fringe.pop()
        # print(node.state)
        if problem.goal_test(node.state):
            return node
        fringe.extend(node.expand(problem))
    return None


def breadth_first_tree_search(problem):
    """Експандирај го прво најплиткиот јазол во пребарувачкото дрво.

    :param problem: даден проблем
    :return: Node
    """
    return tree_search(problem, FIFOQueue())


def depth_first_tree_search(problem):
    """Експандирај го прво најдлабокиот јазол во пребарувачкото дрво.

    :param problem:даден проблем
    :return: Node
    """
    return tree_search(problem, Stack())


"""
Неинформирано пребарување во рамки на граф
Основната разлика е во тоа што овде не дозволуваме јамки, 
т.е. повторување на состојби
"""


def graph_search(problem, fringe):
    """Пребарувај низ следбениците на даден проблем за да најдеш цел.
     Ако до дадена состојба стигнат два пата, употреби го најдобриот пат.

    :param problem: даден проблем
    :param fringe: празна редица (queue)
    :return: Node
    """
    closed = set()
    fringe.append(Node(problem.initial))
    while fringe:
        node = fringe.pop()
        if problem.goal_test(node.state):
            return node
        # if node.state not in closed:
        #     closed.add(node.state)
        #     fringe.extend(node.expand(problem))

        # fix na bug so navrakanje na ist state
        # se sluchuva zaradi drugi memoriski adresi, a isti vrednosti na objektite od tipot Prepreka
        # bez razlika shto imaat isti vrednosti, python gi sporeduva memoriski adresi
        # mozhno e reshenie i so implementacija na funkcijata __eq__()
        state = (node.state[0], (node.state[1].preprekaX1, node.state[1].preprekaY1), (node.state[2].preprekaX1, node.state[2].preprekaY1), (node.state[3].preprekaX1, node.state[3].preprekaY1))

        if state not in closed:
            closed.add(state)
            fringe.extend(node.expand(problem))

    return None


def breadth_first_graph_search(problem):
    """Експандирај го прво најплиткиот јазол во пребарувачкиот граф.

    :param problem: даден проблем
    :return: Node
    """
    return graph_search(problem, FIFOQueue())


def depth_first_graph_search(problem):
    """Експандирај го прво најдлабокиот јазол во пребарувачкиот граф.

    :param problem: даден проблем
    :return: Node
    """
    return graph_search(problem, Stack())


def depth_limited_search(problem, limit=50):
    def recursive_dls(node, problem, limit):
        """Помошна функција за depth limited"""
        cutoff_occurred = False
        if problem.goal_test(node.state):
            return node
        elif node.depth == limit:
            return 'cutoff'
        else:
            for successor in node.expand(problem):
                result = recursive_dls(successor, problem, limit)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
        if cutoff_occurred:
            return 'cutoff'
        return None

    return recursive_dls(Node(problem.initial), problem, limit)


def iterative_deepening_search(problem):
    for depth in range(sys.maxsize):
        result = depth_limited_search(problem, depth)
        if result is not 'cutoff':
            return result


def uniform_cost_search(problem):
    """Експандирај го прво јазолот со најниска цена во пребарувачкиот граф."""
    return graph_search(problem, PriorityQueue(lambda a, b:
                                               a.path_cost < b.path_cost))


# Vasiot kod pisuvajte go pod ovoj komentar


class Prepreka:

    # koristi goren lev agol za pretstavuvanje na pozicija


    def __init__(self, preprekaX1, preprekaY1, preprekaX2, preprekaY2, prostorX1, prostorY1, prostorX2, prostorY2, deltaX, deltaY):
        """
        :param prostorX1: redica vo koja e goren lev agol na preprekata
        :param prostorY1: kolona vo koja e goren lev agol na preprekata
        :param prostorX2: redica vo koja e dolniot desen agol na preprekata
        :param prostorY2: kolona vo koja e dolniot desen agol na preprekata
        :param prostorX1: redica vo koja e goren lev agol na prostorot vo koj mozhe da se dvizhi
        :param prostorY1: kolona vo koja e goren lev agol na prostorot vo koj mozhe da se dvizhi
        :param prostorX2: redica vo koja e dolniot desen agol na prostorot vo koj mozhe da se dvizhi
        :param prostorY2: kolona vo koja e dolniot desen agol na prostorot vo koj mozhe da se dvizhi
        :param deltaX: za eden moment kolku pozicii po x-oska se pridvizhuva
        :param deltaY: vo eden moment kolku pozicii po y-oska se pridvizhuva
        """

        self.preprekaX1 = preprekaX1
        self.preprekaY1 = preprekaY1
        self.preprekaX2 = preprekaX2
        self.preprekaY2 = preprekaY2

        self.deltaX = deltaX
        self.deltaY = deltaY

        self.prostorX1 = prostorX1
        self.prostorY1 = prostorY1
        self.prostorX2 = prostorX2
        self.prostorY2 = prostorY2

    def move(self):
        """

        :return: new object of type Prepreka
        """
        deltaX = self.deltaX
        deltaY = self.deltaY

        if self.preprekaX1 == self.prostorX1\
            or self.preprekaX2 == self.prostorX2\
            or self.preprekaX1 == self.prostorX2\
            or self.preprekaX2 == self.prostorX1:
                deltaX *= -1

        if self.preprekaY1 == self.prostorY1 \
            or self.preprekaY2 == self.prostorY2\
            or self.preprekaY1 == self.prostorY2\
            or self.preprekaY1 == self.prostorY1:
            deltaY *= -1

        return Prepreka(self.preprekaX1 + deltaX, self.preprekaY1 + deltaY,
                        self.preprekaX2 + deltaX, self.preprekaY2 + deltaY,
                        self.prostorX1, self.prostorY1, self.prostorX2, self.prostorY2,
                        deltaX, deltaY)

    def hitChoveche(self, choveche):
        return (choveche[0] >= self.preprekaX1 and choveche[0] <= self.preprekaX2 and choveche[1] >= self.preprekaY1 and choveche[1] <= self.preprekaY2)

    def __str__(self):
        l = [self.preprekaX1, self.preprekaY1, self.preprekaX2, self.preprekaY2]
        return str(l)

    def __eq__(self, other):
        return self.preprekaX1 == other.preprekaX1 and \
               self.preprekaX2 == other.preprekaX2 and \
               self.preprekaY1 == other.preprekaY2 and \
               self.preprekaY2 == other.preprekaY2


class PodvizniPrepreki(Problem):
    # za prepreki chuvame goren lev agol
    def __init__(self, choveche = (0, 0), kukja = (10, 10)):
        prepreka1 = Prepreka(2, 2, 2, 3, 2, 0, 2, 5, 0, -1)
        prepreka2 = Prepreka(7, 2, 8, 3, 5, 0, 10, 5, -1, 1)
        prepreka3 = Prepreka(7, 8, 8, 8, 5, 8, 10, 8, 1, 0)
        initial = (choveche, prepreka1, prepreka2, prepreka3, "")
        super().__init__(initial, kukja)

    def goal_test(self, state):
        g = self.goal
        choveche = state[0]

        return (g[0] == choveche[0] and g[1] == choveche[1])

    def successor(self, state):
        choveche = state[0]
        prepreka1 = state[1]
        prepreka2 = state[2]
        prepreka3 = state[3]


        sucessors = {}

        prepreka1 = prepreka1.move()
        prepreka2 = prepreka2.move()
        prepreka3 = prepreka3.move()

        # print(choveche)

        desnoChoveche = (choveche[0], choveche[1] + 1)
        levoChoveche = (choveche[0], choveche[1] - 1)
        goreChoveche = (choveche[0] - 1, choveche[1])
        doleChoveche = (choveche[0] + 1, choveche[1])

        def ispadaChoveche(choveche):
            if (choveche[0] < 0 or choveche[0] > 10):
                return True

            if (choveche[1] < 0 or choveche[1] > 10):
                return True

            if choveche[0] >= 0 and choveche[0] <= 4:
                if choveche[1] >= 0 and choveche[1] <= 5:
                    return False
                return True


        if (not ispadaChoveche(desnoChoveche) and not prepreka1.hitChoveche(desnoChoveche) and not prepreka2.hitChoveche(desnoChoveche) and not prepreka3.hitChoveche(desnoChoveche)) :
            sucessors['Desno'] = (desnoChoveche, prepreka1, prepreka2, prepreka3, "Desno")

        if (not ispadaChoveche(doleChoveche) and not prepreka1.hitChoveche(doleChoveche) and not prepreka2.hitChoveche(doleChoveche) and not prepreka3.hitChoveche(doleChoveche)) :
            sucessors['Dolu'] = (doleChoveche, prepreka1, prepreka2, prepreka3, "Dolu")

        if (not ispadaChoveche(levoChoveche) and not prepreka1.hitChoveche(levoChoveche) and not prepreka2.hitChoveche(levoChoveche) and not prepreka3.hitChoveche(levoChoveche)) :
            sucessors['Levo'] = (levoChoveche, prepreka1, prepreka2, prepreka3, "Levo")

        if (not ispadaChoveche(goreChoveche) and not prepreka1.hitChoveche(goreChoveche) and not prepreka2.hitChoveche(goreChoveche) and not prepreka3.hitChoveche(goreChoveche)):
            sucessors['Gore'] = (goreChoveche, prepreka1, prepreka2, prepreka3, "Gore")


        return sucessors


    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        possible = self.successor(state)
        return possible[action]


# Vcituvanje na vleznite argumenti za test primerite

choveche_redica = int(input())
choveche_kolona = int(input())
kukja_redica = int(input())
kukja_kolona = int(input())

reprezentacija = PodvizniPrepreki((choveche_redica, choveche_kolona), (kukja_redica, kukja_kolona))


print(breadth_first_graph_search(reprezentacija).solve())
# answer = breadth_first_graph_search(reprezentacija).solve()
#
# answerList = []
#
# for step in answer:
#     if step[4] != "":
#         answerList += [step[4]]
#
# print(answerList)

# testiranje na prepreka1
#     prepreka1 = Prepreka(2, 2, 2, 3, 2, 0, 2, 5, 0, -1)
#     for i in range(0, 20):
#         print(prepreka1)
#         prepreka1 = prepreka1.move()

# testiranje na prepreka2
#     prepreka2 = Prepreka(7, 2, 8, 3, 5, 0, 10, 5, -1, 1)
#     for i in range(0, 25):
#         print(prepreka2)
#         prepreka2 = prepreka2.move()

# testiranje na prepreka3
#     prepreka3 = Prepreka(7, 8, 8, 8, 5, 8, 10, 8, 1, 0)
#     for i in range(0, 20):
#         print(prepreka3)
#         prepreka3 = prepreka3.move()