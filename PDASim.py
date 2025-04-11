
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
            if ((transition.inputSymbol == inputSymbol) or transition.inputSymbol == None) and (transition.topStack == self.topStack() or transition.topStack == None):
                acceptedTransitions.append(transition)
        return acceptedTransitions
    def doTransitions(self,transition):
        if transition.pop:
            self.stack.pop()
        if transition.push:
            self.stack.append(transition.push)
        self.currState = transition.destinationState
        if transition.inputSymbol:
            return True
        return False    

