from GameBoard import GameBoard


class State():
    """一个游戏状态 包括棋盘和将要下的玩家"""
    def __init__(self, board, player):
        """ board 是 GameBoard 对象 
            player是 1 (B) or 2 (W)"""
        self.board = board
        self.player = player


    def __str__(self):
        """状态转换为字符串"""
        return "<player:" + str(self.player) + "\n" + str(self.board) + ">"

    def getActions(self):
        """返回在这个状态下可以进行的行为 (玩家,棋盘上的空格)"""
        return self.player, self.board.getEmpty()

    def getSuccessorStates(self):
        """返回接下来的子状态列表, 和getActions[1]顺序是对应的"""
        successorStates = []
        for row, col in self.board.getEmpty():
            gb = GameBoard(anotherBoard=self.board)
            nextPlayer = 3 - self.player # 把player编号互换1和2
            gb.addStone(self.player, row, col)
            nextState = State(gb, nextPlayer)
            successorStates.append(nextState)
        return successorStates
    
    def isFinish(self):
        """ 判断游戏是否结束
            返回 1表示黑棋胜利 -1表示白棋胜利 0平局 None没有结果
        """
        gameResult = self.board.identifyWin()
        if gameResult == -1:
            return None
        elif gameResult == 1:
            return 1
        elif gameResult == 2:
            return -1
        else:
            return 0

    def evaluate(self):
        """评估当前局势"""
        return self.board.evaluateBoard(self.player)
        


# from GameBoard import GameBoard
# gb = GameBoard(size = 1)
# s = State(gb, 1)
# print(s)
# print(s.evaluate())
# print("==================================================")
# print(s.getActions())
# print("==================================================")
# for state in s.getSuccessorStates():
#     print(state)
#     print(state.evaluate())
# print("==================================================")
# for state in s.getSuccessorStates()[0].getSuccessorStates():
#     print(state)