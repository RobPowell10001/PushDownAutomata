import json

#Class which contains all the information about one specific transition in the PDA
class Transition:
    def __init__(self, destinationState, inputSymbol, topStack, push, pop):
        self.destinationState = destinationState
        self.inputSymbol = inputSymbol
        self.topStack = topStack
        self.push = push
        self.pop = pop
    
    def toString(self):
        return f"{self.inputSymbol}, {self.topStack} {" (pop)" if self.pop else ""}" + " \N{RIGHTWARDS ARROW} " + f"{self.push}"

#Class which is instantiated as states in the PDA which contain all the information about transitions which can occur from them
#as well as their initial and final status
class State:
    def __init__(self, name, isInitial, isFinal, transitions):
        self.name = name
        self.isInitial = isInitial
        self.isFinal = isFinal
        self.transitions = transitions

#Main function which does all the logical PDA work including being encoded and decoded from json
#as well as find all current possible transitions and doing transitions the user selects
class PDA:
    def __init__(self, states, currState):
        self.states = states
        self.stack = []
        self.currState = currState
        self.initialState = -1
    
    #Turns the PDA into a json data structure
    def jsonEncoding(self, fileName = "data"):
        jsonData = {}
        jsonData["states"] = []
        #Creates each state object
        for state in self.states:
            tempTransitionList = []
            #Creates all the transitions inside of each state object
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
        jsonData["stack"] = []
        jsonData["currState"] = self.initialState
        #Dumps all the json data into a file
        with open(f"{fileName}.json", "w") as file:
            json.dump(jsonData, file, indent=4)

    #Turns a jsonObject into a PDA 
    def jsonDecoding(self, jsonString):
        jsonObject = json.loads(jsonString) 
        self.states = []
        self.stack = []
        #Decodes each state
        for state in jsonObject["states"]:
            tempTransitionList = [] 
            #Decodes each transition within each state
            for transition in state["transitions"]:
                tempTransition = Transition(transition["destinationState"],transition["inputSymbol"],transition["topStack"],transition["push"],transition["pop"])
                tempTransitionList.append(tempTransition)
            tempState = State(state["name"],state["isInitial"],state["isFinal"],tempTransitionList)
            self.states.append(tempState)
            if state["isInitial"]:
                self.currState = len(self.states) - 1
    
    #Helper function that returns the top of the stack
    def topStack(self):
        if len(self.stack) != 0:
            return self.stack[len(self.stack)-1]
        else:
            #print("stack is empty, returning None")
            return None
    
    #Function that finds all transitions of the PDA from the current state with the given input symbol
    def findTransitions(self, inputSymbol):
        acceptedTransitions = []
        #print(f"on input {inputSymbol} and topStack {self.topStack()}:")
        for transition in self.states[self.currState].transitions:
            #print(f"\tchecking for input = {transition.inputSymbol} and topStack = {transition.topStack}")
            if ((transition.inputSymbol == inputSymbol) or transition.inputSymbol == None) and (transition.topStack == self.topStack() or transition.topStack == None):
                #print("accepted!")
                acceptedTransitions.append(transition)
        return acceptedTransitions
    
    #Function that does a valid transition on the PDA moving it to the correct state and doing the necessary operations on the stack
    def doTransitions(self,transition):
        if transition.pop:
            self.stack.pop()
        if transition.push:
            self.stack.append(transition.push)
        self.currState = transition.destinationState
        if transition.inputSymbol:
            return True
        return False    

