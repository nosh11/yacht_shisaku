class Player:
    def __init__(self, name: str):
        self.name = name
        self.__score: list = [None] * 12

    @property
    def score(self):
        return self.__score

    def getName(self):
        return self.name

    def setScore(self, index: int, score: int):
        self.__score[index] = score

    def getScore(self, index: int):
        return self.__score[index]