HANDS = [
    "Ones",
    "Twos",
    "Threes",
    "Fours",
    "Fives",
    "Sixes",
    "Choice",
    "Full House",
    "Four Numbers",
    "Small Straight",
    "Large Straight",
    "Yacht"
]

def getScore(dice: list):
    return [
        sum(i for i in dice if i == 1),
        sum(i for i in dice if i == 2),
        sum(i for i in dice if i == 3),
        sum(i for i in dice if i == 4),
        sum(i for i in dice if i == 5),
        sum(i for i in dice if i == 6),
        sum(dice),
        sum(dice) if len(set(dice)) == 2 and 2 in [dice.count(i) for i in set(dice)] else 0,
        sum(dice) if len(set(dice)) == 2 and 4 in [dice.count(i) for i in set(dice)] else 0,
        15 if len(set(dice)) == 5 and 3 not in [dice.count(i) for i in set(dice)] else 0,
        30 if len(set(dice)) == 5 and 3 in [dice.count(i) for i in set(dice)] else 0,
        50 if len(set(dice)) == 1 else 0
    ]