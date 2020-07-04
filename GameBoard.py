import random

class GameBoard():
    """管理五子棋的棋盘"""
    def __init__(self, size=15, anotherBoard = None):
        """ 棋盘构造器
            size棋盘大小,根据这个大小创建一个空棋盘
            anotherBoard另外一个棋盘,如果不为None,深度克隆这个棋盘"""
        if anotherBoard is None:
            self.board = [0 for _ in range(size * size)]
            self.size = size
        else:
            self.board = anotherBoard.board[:]
            self.size = anotherBoard.size
        

    def __str__(self):
        """棋盘转换成字符串"""
        res = ""
        for i in range(0, self.size):
            res += str(i + 1)
            if i < 9:
                res += " "
            for j in range(0, self.size):
                if self.board[i * self.size + j] == 1:
                    res += "○"
                elif self.board[i * self.size + j] == 2:
                    res += "●"
                elif i == j == 0:
                    res += "┌ "
                elif i == 0 and j == self.size - 1:
                    res += "┐ "
                elif i == self.size - 1 and j == 0:
                    res += "└ "
                elif i == j == self.size - 1:
                    res += "┘ "
                elif i == 0:
                    res += "┬ "
                elif i == self.size - 1:
                    res += "┴ "
                elif j == 0:
                    res += "├ "
                elif j == self.size - 1:
                    res += "┤ "
                else:
                    res += "┼ "
            res += "\n"
        res += "  "
        for j in range(0, self.size):
            res += chr(j + 65) + " "
        res += "\n"
        return res
    
    def addStone(self, side, row, col):
        """在棋盘上添加一个棋子,该方法并不检查覆盖 side = 1 (B) or 2 (W)"""
        self.board[row * self.size + col] = side

    def clear(self):
        """清空棋盘"""
        for i in range(self.size * self.size):
            self.board[i] = 0

    def getEmpty(self):
        """以列表形式返回空的格子坐标 列表的每一项为(row,col)"""
        res = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i * self.size + j] == 0:
                    res.append((i, j))
        return res

    def random(self, hand):
        """随机填充棋盘 先黑后白共hand个棋, hand不得超过self.size平方"""
        if hand > self.size * self.size:
            hand = self.size * self.size
        player = 1
        for i in range(hand):
            moveList = self.getEmpty()
            idx = random.randint(0, len(moveList) - 1)
            self.addStone(player, moveList[idx][0], moveList[idx][1])
            player = 3 - player

    def identifyWin(self):
        """判断输赢(连续5个) 返回 1 B赢 2 W赢 0 棋盘已经占满(平) -1 没有结束"""
        # 横
        for i in range(self.size):
            successor = 0 #多少个连续的相同的
            side = 0 #连续相同的势力 1B 2W
            for j in range(self.size):
                stone = self.board[i * self.size + j]
                if stone != 0:
                    if stone != side:
                        successor = 1
                        side = stone
                    else:
                        successor += 1
                        if successor == 5:
                            return side
                else:
                    successor = 0
                    side = 0

        # 竖
        for j in range(self.size):
            successor = 0 #多少个连续的相同的
            side = 0 #连续相同的势力 1B 2W
            for i in range(self.size):
                stone = self.board[i * self.size + j]
                if stone != 0:
                    if stone != side:
                        successor = 1
                        side = stone
                    else:
                        successor += 1
                        if successor == 5:
                            return side
                else:
                    successor = 0
                    side = 0
        
        # 左下到右上 (上半部分)
        for i in range(4, self.size):
            successor = 0 #多少个连续的相同的
            side = 0 #连续相同的势力 1B 2W
            for j in range(i + 1):
                stone = self.board[(i - j) * self.size + j]
                if stone != 0:
                    if stone != side:
                        successor = 1
                        side = stone
                    else:
                        successor += 1
                        if successor == 5:
                            return side
                else:
                    successor = 0
                    side = 0
        # 左下到右上 (下半部分)
        for i in range(self.size - 5, 0, -1): #self.size - 5 到 1
            successor = 0 #多少个连续的相同的
            side = 0 #连续相同的势力 1B 2W
            for j in range(self.size - i):
                stone = self.board[(self.size - 1 - j) * self.size + i + j]
                if stone != 0:
                    if stone != side:
                        successor = 1
                        side = stone
                    else:
                        successor += 1
                        if successor == 5:
                            return side
                else:
                    successor = 0
                    side = 0

        # 左上到右下 (上半部分)
        for i in range(0, self.size - 4):
            successor = 0 #多少个连续的相同的
            side = 0 #连续相同的势力 1B 2W
            for j in range(self.size - i):
                stone = self.board[j * self.size + i + j]
                if stone != 0:
                    if stone != side:
                        successor = 1
                        side = stone
                    else:
                        successor += 1
                        if successor == 5:
                            return side
                else:
                    successor = 0
                    side = 0
        # 左上到右下 (下半部分)
        for i in range(1, self.size - 4):
            successor = 0 #多少个连续的相同的
            side = 0 #连续相同的势力 1B 2W
            for j in range(self.size - i):
                stone = self.board[(i + j) * self.size + j]
                if stone != 0:
                    if stone != side:
                        successor = 1
                        side = stone
                    else:
                        successor += 1
                        if successor == 5:
                            return side
                else:
                    successor = 0
                    side = 0

        if len(self.getEmpty()) == 0:
            return 0 # 平局

        return -1 # 没有结束
        

        




# gb = GameBoard()
# gb.random(24)
# print(gb)
# print(gb.identifyWin())
# gb.addStone(1, 3, 5)
# gb.addStone(1, 4, 5)
# gb.addStone(2, 6, 5)
# gb.addStone(2, 7, 6)
# gb.addStone(2, 8, 7)
# gb.addStone(2, 9, 8)
# gb.addStone(1, 10, 9)
# gb.addStone(1, 6, 11)
# gb.addStone(2, 10, 14)
# gb.addStone(2, 11, 13)
# gb.addStone(2, 12, 12)
# gb.addStone(2, 13, 11)
# gb.addStone(2, 14, 10)
# gb.addStone(2, 0, 4)
# gb.addStone(2, 1, 3)
# gb.addStone(2, 2, 2)
# gb.addStone(2, 3, 1)
# gb.addStone(2, 4, 0)
# # print(gb)
# # print(gb.getEmpty())
# # print(len(gb.getEmpty()))
# # gb2 = GameBoard(anotherBoard=gb)
# # gb.clear()
# # print(gb)
# # print("gb2:")
# # print(gb2)
# # print(gb.getEmpty())
# # print(len(gb.getEmpty()))
# print(gb)
# print(gb.identifyWin())