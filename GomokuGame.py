from state import State
from GameBoard import GameBoard
from MiniMax import MiniMax

class GomokuGame():
    """五子棋游戏 方便测试"""
    def __init__(self, player = 2, size = 15):
        """ 构造器
            player: 玩家执方 默认2为白棋
            size:   棋盘大小
        """
        self.player = player
        self.size = size

    def start(self):
        """ 开始游戏 """
        gb = GameBoard(size = self.size)
        print(gb)
        print("Game Starts!")

        if self.player == 1:
            r, c = self.prompt()
            gb.addStone(1, r, c)
            print(gb)
        
        i = 0
        # 游戏循环
        while gb.identifyWin() == -1:
            print("Waiting for computer...")
            s = State(board=gb, player=3-self.player)
            mm = MiniMax()
            action = mm.getAction(gameState=s, maxDepth=3, maxBranch=50)
            print("Best Predicted Score:"+str(action[0]) + "; Location:(" + str(action[1][0] + 1) +"," + chr(action[1][1] + 65) +")")
            gb.addStone(3-self.player, action[1][0], action[1][1])
            print(gb)
            if gb.identifyWin() != -1:
                break
            r, c = self.prompt()
            gb.addStone(self.player, r, c)
            print(gb)
            i += 1

        winSide = gb.identifyWin()
        if winSide == 1:
            if self.player == 2:
                print("BLACK(c) wins!")
            else:
                print("BLACK wins!")
        if winSide == 2:
            if self.player == 1:
                print("WHITE(c) wins!")
            else:
                print("WHITE wins!")
        if winSide == 0:
            print("DRAW!")

    def prompt(self):
        """引导用户输入 返回row,col 如果输入不合法 递归调用自己"""
        text = input("Your turn!\n[row] [col]:")
        info = text.split()
        if len(info) != 2:
            print("Invalid input!")
            return self.prompt()
        r = int(info[0]) - 1
        c = ord(info[1][0]) - 65
        if r < 0 or r >= self.size or c < 0 or c >= self.size:
            print("Invalid input!")
            return self.prompt()
        return r, c

gg = GomokuGame()
gg.start()
