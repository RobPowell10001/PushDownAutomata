import json
class Transition:
    def __init__(self, destinationState, inputSymbol, topStack, push, pop):
        self.destinationState = destinationState
        self.inputSymbol = inputSymbol
        self.topStack = topStack
        self.push = push
        self.pop = pop
    
    def toString(self):
        
        return f"{self.inputSymbol}, {self.topStack} {" (pop)" if self.pop else ""}" + " \N{RIGHTWARDS ARROW} " + f"{self.push}"

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
    def jsonExporting(self):
        jsonData = {}
        jsonData["states"] = []
        for state in self.states:
            tempTransitionList = []
            for transition in state.transitions:
                tempTransition = {
                    "destinationState": transition.destinationState,
                    "inputSymbol": transition.inputSymbol,
                    "topStack": transition.topStack,
                    "push": transition.push,
                    "pop": transition.pop
                }
                tempTransitionList.append(tempTransition)
            tempStateData = {
                "name": state.name,
                "isInitial": state.isInitial,
                "isFinal": state.isFinal,
                "transitions": tempTransitionList
            }
            jsonData["states"].append(tempStateData)
        jsonData["currState"] = self.currState
        jsonData["stack"] = self.stack
        with open("data.json", "w") as file:
            json.dump(jsonData, file, indent=4)
    def jsonDecoding(self, jsonString):
        jsonObject = json.loads(jsonString) 
        self.states = []
        self.stack = []
        for state in jsonObject["states"]:
            tempTransitionList = [] 
            for transition in state["transitions"]:
                tempTransition = Transition(transition["destinationState"],transition["inputSymbol"],transition["topStack"],transition["push"],transition["pop"])
                tempTransitionList.append(tempTransition)
            tempState = State(state["name"],state["isInitial"],state["isFinal"],tempTransitionList)
            self.states.append(tempState)
            if state["isInitial"]:
                self.currState = len(self.states) - 1
    def topStack(self):
        if len(self.stack) != 0:
            return self.stack[len(self.stack)-1]
        else:
            print("stack is empty, returning None")
            return None
    def findTransitions(self, inputSymbol):
        acceptedTransitions = []
        for transition in self.states[self.currState].transitions:
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

