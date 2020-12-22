import re
from collections import deque
from functools import cache

FILE = "test.txt"
FILE = "puzzle.txt"


with open(FILE, "r") as f:
    text = [group.split("\n") for group in f.read().split("\n\n")]


def read():
    players = {}

    with open(FILE, "r") as f:
        for index in (1, 2):
            while re.match(f"Player {index}\:", f.readline()) is None:
                pass

            cards = deque()
            for line in f:
                line = line.strip()
                if not line:
                    break
                cards.appendleft(int(line))

            players[index] = cards

    return players


def do_copy(players):
    return {key: val.copy() for key, val in players.items()}


def do_recurse(players, card1, card2):
    players = do_copy(players)
    cards = (-1, card1, card2)

    for player in (1, 2):
        while len(players[player]) > cards[player]:
            players[player].popleft()

    return recursive_combat(players)


def play_round(players, part2=False):
    card1, card2 = players[1].pop(), players[2].pop()

    if part2 and (card1 <= len(players[1])) and (card2 <= len(players[2])):
        winner, _ = do_recurse(players, card1, card2)
    else:
        if card1 > card2:
            winner = 1
        elif card1 < card2:
            winner = 2

    if winner == 1:
        cards = [card1, card2]
    else:
        cards = [card2, card1]

    players[winner].extendleft(cards)

    return players


def is_finished(players):
    return 0 in [len(x) for x in players.values()]


def get_winner(players):
    if len(players[1]):
        return 1
    else:
        return 2


def calc_score(players):
    player = players[get_winner(players)]

    total = 0
    for index, card in enumerate(player, 1):
        total += index * card
    return total


def part1():
    players = read()

    while not is_finished(players):
        players = play_round(players)

    return calc_score(players)


def recursive_combat(players):
    history = [do_copy(players)]

    while not is_finished(players):
        players = play_round(players, True)

        for hist in history:
            if players == hist:
                return 1, players

        history.append(do_copy(players))

    winner = get_winner(players)

    return winner, players


def part2():
    players = read()

    winner, players = recursive_combat(players)

    return calc_score(players)


print(part1())
print(part2())
