class MiniMax():
    
    def getAction(self, gameState, maxDepth, maxBranch):
        """
            返回在当前状态下的MiniMax分数和决策
            gameState 游戏状态
            maxDepth 最大迭代深度
            maxBranch 最大迭代广度 只迭代前maxBranch个action (action是按照质心由近到远排序的) 如果为None则迭代全部
        """
        if maxBranch is None:
            maxBranch = 999999

        def max_value(state, alpha, beta, depth):
            v = 0
            res_action = None
            actions = state.getActions()
            succ_states = state.getSuccessorStates()
            for i in range(len(succ_states)):
                if i == maxBranch:
                    break
                val,_ = value(succ_states[i], alpha, beta, depth)
                if val >= beta:
                    return val, actions[1][i]
                alpha = max(alpha, val)
                if res_action is None or val > v:
                    v = val
                    res_action = actions[1][i]
                
            return v,res_action

        def min_value(state, alpha, beta, depth):
            v = 0
            res_action = None
            actions = state.getActions()
            succ_states = state.getSuccessorStates()
            for i in range(len(succ_states)):
                if i == maxBranch:
                    break
                val,_ = value(succ_states[i], alpha, beta, depth)
                if val <= alpha:
                    return val, actions[1][i]
                beta = min(beta, val)
                if res_action is None or val < v:
                    v = val
                    res_action = actions[1][i]
            return v,res_action

        def value(state, alpha, beta, depth):
            finish_res = state.isFinish()
            if finish_res is not None: # leaf node
                return finish_res, None # -1 0 或 1
            if depth == maxDepth:
                return state.evaluate(), None 
            if state.player == 1: # 黑棋取大
                return max_value(state, alpha, beta, depth + 1)
            else:
                return min_value(state, alpha, beta, depth + 1)

        return value(gameState, -999999, 999999, 0)


# from state import State
# from GameBoard import GameBoard
# gb = GameBoard(size = 15)
# gb.addStone(1,7,7)
# gb.addStone(2,6,6)
# gb.addStone(1,6,7)
# gb.addStone(2,5,7)
# gb.addStone(1,7,6)
# gb.addStone(2,7,5)
# gb.addStone(1,4,8)
# gb.addStone(2,8,4)
# gb.addStone(1,9,3)
# gb.addStone(2,8,5)
# gb.addStone(1,3,8)
# gb.addStone(2,5,8)
# gb.addStone(1,2,8)
# gb.addStone(2,5,9)
# gb.addStone(1,1,8)
# gb.addStone(2,0,8)
# gb.addStone(1,5,6)
# gb.addStone(2,5,10)
# print(gb)
# #quit()
# s = State(board=gb, player=1)
# print(s)
# print("======================================================")
# mm = MiniMax()
# print(mm.getAction(gameState=s, maxDepth=1, maxBranch=64))


