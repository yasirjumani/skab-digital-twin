from collections import deque
from config import DEBOUNCE_SIZE

class EnsembleFusion:
    def __init__(self):
        self.buffer = deque(maxlen=DEBOUNCE_SIZE)

    def evaluate(self, if_pred, spc_pred):
        vote = if_pred + spc_pred
        self.buffer.append(vote)
        if len(self.buffer) == DEBOUNCE_SIZE and all(v == 2 for v in self.buffer):
            return "RED", 2
        elif vote >= 1:
            return "YELLOW", 1
        else:
            return "GREEN", 0

    @staticmethod
    def state_label(state):
        icons = {
            "RED": "🔴 HIGH-CONFIDENCE ALERT",
            "YELLOW": "🟡 LOW-CONFIDENCE WARNING",
            "GREEN": "🟢 NOMINAL"
        }
        return icons.get(state, "UNKNOWN")
