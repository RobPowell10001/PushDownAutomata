PDAInput = [q0,transitions,input]
currentState = q0
stack = []
for inputChar in input: 
    for transition in transitions:
        if transition.state == currentState and transition.character == inputChar:             #if transition exists for the state we are in
            currentState = transition.nextState            #Do transition
            stack.push(transition.stack)
    