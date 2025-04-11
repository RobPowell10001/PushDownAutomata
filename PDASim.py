
class Transition:
    def __init__(self, sourceState, destinationState, inputSymbol, topStack, push, pop):
        self.sourceState = sourceState
        self.destinationState = destinationState
        self.inputSymbol = inputSymbol
        self.topStack = topStack
        self.push = push
        self.pop = pop

class State:
    def __init__(self, name, isInitial, isFinal, transitions):
        self.name = name
        self.isInitial = isInitial
        self.isFinal = isFinal
        self.transitions = transitions

class PDA:
    def __init__(self, states, currState):
        self.states = states
        self.stack = []
        self.currState = currState
    def topStack(self):
        return self.stack[len(self.stack)-1]
    def findTransitions(self, inputSymbol):
        acceptedTransitions = []
        for transition in self.currState.transitions:
            if (transition.inputSymbol == inputSymbol) and (transition.topStack == self.topStack()):
                acceptedTransitions.append(transition)