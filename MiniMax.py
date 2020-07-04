class MiniMax():
    
    def getAction(self, gameState):
        """
            返回在当前状态下的MiniMax分数和决策
        """

        def max_value(state, alpha, beta):
            v = 0
            res_action = None
            actions = state.getActions()
            succ_states = state.getSuccessorStates()
            for i in range(len(succ_states)):
                val,_ = value(succ_states[i], alpha, beta)
                if val >= beta:
                    return val, actions[1][i]
                alpha = max(alpha, val)
                if res_action is None or val > v:
                    v = val
                    res_action = actions[1][i]
                
            return v,res_action

        def min_value(state, alpha, beta):
            v = 0
            res_action = None
            actions = state.getActions()
            succ_states = state.getSuccessorStates()
            for i in range(len(succ_states)):
                val,_ = value(succ_states[i], alpha, beta)
                if val <= alpha:
                    return val, actions[1][i]
                beta = min(beta, val)
                if res_action is None or val < v:
                    v = val
                    res_action = actions[1][i]
            return v,res_action

        def value(state, alpha, beta):
            eval_res = state.evaluate()
            if eval_res is not None: # leaf node
                return eval_res, None
            if state.player == 1: # 黑棋取大
                return max_value(state, alpha, beta)
            else:
                return min_value(state, alpha, beta)

        return value(gameState, -999999, 999999)


from state import State
from GameBoard import GameBoard
gb = GameBoard(size = 7)
gb.random(38)
print(gb)
s = State(board=gb, player=1)
print(s)
print("======================================================")
mm = MiniMax()
print(mm.getAction(s))

