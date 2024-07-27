

class ButtonAction:

    def __init__(self):
        pass

    def action_forward(self):
        raise NotImplementedError()

    def action_backward(self):
        raise NotImplementedError()

    def primary_select(self):
        raise NotImplementedError()

    def secondary_select(self):
        raise NotImplementedError()

    def primary_modify(self):
        raise NotImplementedError()

    def secondary_modify(self):
        raise NotImplementedError()

    def hybrid_action_move(self, direction: str):
        raise NotImplementedError()



