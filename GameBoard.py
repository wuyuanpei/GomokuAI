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

    def getEmpty(self, param=1):
        """ 以列表形式返回空的格子坐标 列表的每一项为(row,col)
            param 1: 按照到最近的棋子的距离由近到远的顺序排序
            param 2: 过滤掉到最近的棋子的距离大于3的棋子
        """
        res = []
        filled = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i * self.size + j] == 0:
                    res.append((i, j))
                elif param != 0:
                    filled.append((i, j))

        def shortest(element):
            return min(map(lambda e: (element[0] - e[0]) ** 2 + (element[1] - e[1]) ** 2, filled))

        if param == 1:
            if len(filled) != 0:
                res.sort(key=shortest)
            else:
                res.sort(key=lambda element: (element[0] - self.size//2) ** 2 + (element[1] - self.size//2) ** 2)
        
        if param == 2:
            if len(filled) != 0:
                return list(filter(lambda x: shortest(x) <= 9, res))
            else:
                return list(filter(lambda x: x[0] == x[1] == self.size//2, res))

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
        
    def evaluateBoard(self, player):
        """ 根据player返回棋盘状态
            player 是 1 此时是黑棋下 2 此时是白棋下
            返回-1 ~ 1, 接近1代表黑棋即将胜利 接近-1代表白棋即将胜利
        """

        def testStones(stones, side):
            """检查格子 并返回所有测试的列表"""
            res = []
            res.append(testStonesParam(stones[0:5], side, 1) or testStonesParam(stones[1:6], side, 1))
            res.append(testStonesParam(stones, 3 - side, 2))
            res.append(testStonesParam(stones[0:5], 3 - side, 1) or testStonesParam(stones[1:6], 3 - side, 1))
            res.append(testStonesParam(stones, side, 3))
            res.append(testStonesParam(stones, 3 - side, 3))
            res.append(testStonesParam(stones, side, 4))
            res.append(testStonesParam(stones, 3 - side, 4))
            return res

        def testStonesParam(stones, side, param):
            """ 检查一些格子的情况
                param:  1: 在5个格子里有4个side,另外一个为空 ○●●●●   ●○●●●   ●●○●● 以及镜像 (对于一个state来说，这种情况已经胜利了)
                        2: 在6个格子里中间连续4个是side,边上两个是空 ○●●●●○ (对手出现这样的情况，如果没有1已经输了)
                        3: 在6个格子里中间三个连着是side,另外三个为空 ○●●●○○   ○○●●●○   ○●○●●○   ○●●○●○ (对于一个state来说，只要对面没有情况1，那么这种情况也已经胜利了)
                        4: 在6个格子里中间有两个side,另外四个为空 ○●●○○○   ○○●○●○   ○●○○●○ 以及镜像 （逼迫对手反应的state不然就变成2了)
            """
            if param == 1:
                count = 0
                for stone in stones:
                    if stone == side:
                        count += 1
                    elif stone == 0:
                        pass
                    else:
                        return False
                if count == 4:
                    return True
                else:
                    return False

            elif param == 2:
                return stones[0] == stones[5] == 0 and stones[1] == stones[2] == stones[3] == stones[4] == side

            elif param == 3:
                if stones[0] != 0 or stones[5] != 0:
                    return False #两端必须为空
                count = 0
                for stone in stones[1:5]:
                    if stone == side:
                        count += 1
                    elif stone == 0:
                        pass
                    else:
                        return False
                if count == 3:
                    return True
                else:
                    return False

            elif param == 4:
                if stones[0] != 0 or stones[5] != 0:
                    return False #两端必须为空
                count = 0
                for stone in stones[1:5]:
                    if stone == side:
                        count += 1
                    elif stone == 0:
                        pass
                    else:
                        return False
                if count == 2:
                    return True
                else:
                    return False

            
            
        def connectedNum(side):
            """ 根据x的长度切片棋盘(所有可能性),并根据param对切片进行测试,返回测试[c54, c64o, c54o, c63, c63o, c62, c62o]通过的情况T/F"""
            res = [False, False, False, False, False, False, False]
            x = 6 # 截取片段长度
            # 横
            for i in range(self.size):
                for j in range(self.size - x + 1):
                    stones = self.board[i * self.size + j : i * self.size + j + x]
                    test = testStones(stones, side)
                    for t in range(len(test)):
                        res[t] = res[t] or test[t]

            # 竖
            for j in range(self.size):
                for i in range(self.size - x + 1):
                    stones = self.board[i * self.size + j : (i + x) * self.size + j : self.size]
                    test = testStones(stones, side)
                    for t in range(len(test)):
                        res[t] = res[t] or test[t]

            # 左下到右上 (上半部分)
            for i in range(x - 1, self.size):
                for j in range(i - x + 2):
                    end = (i - j - x) * self.size + (j + x) # end可能会小于0 切片时会有错误
                    if end < 0:
                        end = 0
                    stones = self.board[(i - j) * self.size + j : end : -self.size + 1]
                    test = testStones(stones, side)
                    for t in range(len(test)):
                        res[t] = res[t] or test[t]

            # 左下到右上 (下半部分)
            for i in range(self.size - x, 0, -1): #self.size - 5 到 1
                for j in range(self.size - i - x + 1):
                    stones = self.board[(self.size - 1 - j) * self.size + i + j : (self.size - x - 1 - j) * self.size + i + j + x: -self.size + 1]
                    test = testStones(stones, side)
                    for t in range(len(test)):
                        res[t] = res[t] or test[t]

            # 左上到右下 (上半部分)
            for i in range(self.size - x + 1):
                for j in range(self.size - i - x + 1):
                    stones = self.board[j * self.size + i + j : (j + x) * self.size + i + j + x : self.size + 1]
                    test = testStones(stones, side)
                    for t in range(len(test)):
                        res[t] = res[t] or test[t]

            # 左上到右下 (下半部分)
            for i in range(1, self.size - x + 1):
                for j in range(self.size - i - x + 1):
                    stones = self.board[(i + j) * self.size + j : (i + j + x) * self.size + j + x : self.size + 1]
                    test = testStones(stones, side)
                    for t in range(len(test)):
                        res[t] = res[t] or test[t]

            return res

        #函数返回的值
        if player == 1:
            factor = 1
        elif player == 2:
            factor = -1

        c54, c64o, c54o, c63, c63o, c62, c62o = connectedNum(player)
        if c54: #出现c54已经胜利
            return 0.99 * factor

        #c64o = connectedNum(3 - player, x=6, param=2)
        if c64o: #对手出现c64,且自己没有c54,已经输了
            return -0.99 * factor

        #c54o = connectedNum(3 - player, x=5, param=1)
        if c54o: #对手出现c54,必须堵住,很不利
            return -0.9 * factor

        #c63 = connectedNum(player, x=6, param=3)
        if c63: #出现c63,不出意外,即将胜利
            return 0.7 * factor

        #c63o = connectedNum(3 - player, x=6, param=3)
        if c63o: #对手出现c63,很被动,必须堵住
            return -0.5 * factor

        #c62 = connectedNum(player, x=6, param=4)
        if c62: #出现c62再下一步可以变成c63,给对手造成威胁
            return 0.3 * factor

        #c62o = connectedNum(3 - player, x=6, param=4)
        if c62o: #对手出现c62再下一步可以变成c63
            return -0.1 * factor

        return 0
        

        




# gb = GameBoard(size=8)
# gb.random(34)
# print(gb)
# print(gb.evaluateBoard(2))

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