import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import PDASim
import Forms
import json
import os

def on_press(event):
    # Find the item under the cursor
    global selected_item
    items = canvas.find_overlapping(event.x, event.y, event.x, event.y)
    for item in items:
        if "draggable" in canvas.gettags(item):  # Check if the item has the "draggable" tag
            selected_item = item
            break
    else:
        selected_item = None

def on_drag(event, states, matrix):
    # Move the selected item with the mouse
    if selected_item:
        original_coords = canvas.coords(selected_item)
        dx = event.x - (original_coords[0] + original_coords[2]) / 2
        dy = event.y - (original_coords[1] + original_coords[3]) / 2
        tags = canvas.gettags(selected_item)
        movement_tag = None
        for tag in tags:
            if tag.startswith("mvmt_group_"):
                movement_tag = tag
                break
        if movement_tag is not None:
            items_to_move = canvas.find_withtag(movement_tag)
            for item in items_to_move:
                canvas.move(item, dx, dy)
        
        update_arrows(states, matrix, selected_item)

#draws an arrow from state 1 to state 2
def draw_arrow(matrix, states, index1, index2, transition):
    numTransitions = 0
    if matrix[index1][index2] != 0:
        numTransitions = len(matrix[index1][index2])

    state1 = states[index1]
    state2 = states[index2]
    # Get coordinates of each circle
    state1_coords = canvas.coords(state1)
    state2_coords = canvas.coords(state2)

    # Calculate the center of each circle
    state1_center = ((state1_coords[0] + state1_coords[2]) / 2, (state1_coords[1] + state1_coords[3]) / 2)
    state2_center = ((state2_coords[0] + state2_coords[2]) / 2, (state2_coords[1] + state2_coords[3]) / 2)

    # Calculate the vector from state1 to state2
    dx = state2_center[0] - state1_center[0]
    dy = state2_center[1] - state1_center[1]
    distance = (dx**2 + dy**2)**0.5

    # Calculate the points on the edge of each circle
    state1_edge = (state1_center[0] + dx / distance * 50, state1_center[1] + dy / distance * 50)
    state2_edge = (state2_center[0] - dx / distance * 50, state2_center[1] - dy / distance * 50)

    # Draw the arrow
    newArrow = canvas.create_line(state1_edge[0], state1_edge[1], state2_edge[0], state2_edge[1], arrow=tk.LAST)

    # Calculate the midpoint of the arrow
    midpoint_x = (state1_edge[0] + state2_edge[0]) / 2
    midpoint_y = (state1_edge[1] + state2_edge[1]) / 2

    # Create the text at the midpoint
    text_id = canvas.create_text(midpoint_x, midpoint_y - (13 * (1 + numTransitions)), text=f"{transition.toString()}", fill="black")

    # Associate the text ID with the arrow
    canvas.itemconfig(newArrow, tags=(f"arrow_{index1}_{index2}", f"text_{text_id}_{numTransitions}"))

    # Store the arrow in the matrix
    if matrix[index1][index2] != 0:
        matrix[index1][index2].append((newArrow, text_id))
    else:
        matrix[index1][index2] = [(newArrow, text_id)]

def draw_circular_arrow(matrix, stateList, stateID, transition):    
    numTransitions = 0
    if matrix[stateID][stateID] != 0:
        numTransitions = len(matrix[stateID][stateID])
    
    # Get the coordinates of the state
    state_coords = canvas.coords(stateList[stateID])
    state_center = ((state_coords[0] + state_coords[2]) / 2, (state_coords[1] + state_coords[3]) / 2)
    outer_radius = 50  # Radius of the larger state circle
    loop_offset = 20  # Offset for the self-loop

    # Calculate the start and end points of the circular arrow on the edge of the larger circle
    start_x = state_center[0] - outer_radius - loop_offset * 0.25
    start_y = state_center[1] - outer_radius * 0.33 - loop_offset

    # Define the bounding box for the circular arrow
    x1 = start_x - loop_offset
    y1 = start_y - loop_offset
    x2 = start_x + loop_offset
    y2 = start_y + loop_offset

    # Draw the circular arrow
    circular_arrow = canvas.create_arc(x1, y1, x2, y2, start=0, extent=300, style=tk.ARC, tags=(f"mvmt_group_{stateID}"))

    # Add an arrowhead pointing straight down
    arrow_offset_x = 19
    arrow_offset_y = -15
    arrow_x1 = start_x + arrow_offset_x
    arrow_y1 = start_y + loop_offset * 0.7 + arrow_offset_y
    arrow_x2 = start_x + arrow_offset_x
    arrow_y2 = start_y + loop_offset * 0.9 + arrow_offset_y
    canvas.create_line(arrow_x1, arrow_y1, arrow_x2, arrow_y2, arrow=tk.LAST, tags=(f"mvmt_group_{stateID}"))

    # Add the transition text near the circular arrow
    text_x = start_x - loop_offset * 1.5 
    text_y = start_y - loop_offset * 1.5 - (13 * numTransitions)
    text_id = canvas.create_text(text_x, text_y, text=f"{transition.toString()}", fill="black", tags=(f"mvmt_group_{stateID}"))

    # Store the circular arrow and text in the matrix
    if matrix[stateID][stateID] != 0:
        matrix[stateID][stateID].append((circular_arrow, text_id))
    else:
        matrix[stateID][stateID] = [(circular_arrow, text_id)]

#update all arrows associated with the selected state
def update_arrows(states, matrix, selectedState):
    tags = canvas.gettags(selectedState)
    for tag in tags:
        if tag.startswith("state_"):
            sourceID = int(tag.split("_")[1])
            break
    # update outward arrows
    destinationID = 0
    if matrix:
        for arrowsToDestination in matrix[sourceID]:
            if arrowsToDestination != 0:
                for arrow, text_id in arrowsToDestination:
                    update_arrow(arrow, states, sourceID, destinationID)
            destinationID += 1
        # now update inward arrows
        destinationID = sourceID
        sourceID = 0
        for arrowListsFromSource in matrix:
            if arrowListsFromSource[destinationID] != 0:
                for arrow, text_id in arrowListsFromSource[destinationID]:
                    update_arrow(arrow, states, sourceID, destinationID)
            sourceID += 1

def update_arrow(arrow, states, id1, id2):
    if id1 == id2:  # Handle circular arrows (self-loops)
        a = 0
    else:  # Handle normal arrows
        # Get the center of the first circle
        state1_coords = canvas.coords(states[id1])
        state1_center = ((state1_coords[0] + state1_coords[2]) / 2, (state1_coords[1] + state1_coords[3]) / 2)

        # Get the center of the second circle
        state2_coords = canvas.coords(states[id2])
        state2_center = ((state2_coords[0] + state2_coords[2]) / 2, (state2_coords[1] + state2_coords[3]) / 2)

        # Calculate the vector from state1 to state2
        dx = state2_center[0] - state1_center[0]
        dy = state2_center[1] - state1_center[1]
        distance = (dx**2 + dy**2)**0.5

        # Calculate the points on the edge of each circle
        state1_edge = (state1_center[0] + dx / distance * 50, state1_center[1] + dy / distance * 50)
        state2_edge = (state2_center[0] - dx / distance * 50, state2_center[1] - dy / distance * 50)

        # Update the arrow to connect the edges of the circles
        canvas.coords(arrow, state1_edge[0], state1_edge[1], state2_edge[0], state2_edge[1])

        # Update the position of the associated text
        tags = canvas.gettags(arrow)
        for tag in tags:
            if tag.startswith("text_"):
                text_id = int(tag.split("_")[1])
                transition_num = int(tag.split("_")[2])
                midpoint_x = (state1_edge[0] + state2_edge[0]) / 2
                midpoint_y = ((state1_edge[1] + state2_edge[1]) / 2) - (13 * (transition_num))
                canvas.coords(text_id, midpoint_x, midpoint_y - 10)

def create_nested_circle(x1, y1, x2, y2, stateID):
    # Outer circle
    outer_circle = canvas.create_oval(x1, y1, x2, y2, fill="white", tags=(f"state_{stateID}", f"mvmt_group_{stateID}", "draggable"))
    
    # Calculate coordinates for the inner circle
    inner_margin = 10  # Margin between the outer and inner circles
    inner_x1 = x1 + inner_margin
    inner_y1 = y1 + inner_margin
    inner_x2 = x2 - inner_margin
    inner_y2 = y2 - inner_margin
    
    # Inner circle
    inner_circle = canvas.create_oval(inner_x1, inner_y1, inner_x2, inner_y2, fill="white", tags=(f"state_{stateID}", f"mvmt_group_{stateID}"))
    
    return outer_circle, inner_circle

def update_state_color(stateID, isCurrent):
    # Target the correct stateTag
    stateTag = f"state_{stateID}"

    # Determine the color based on whether the state is current
    color = "red" if isCurrent else "black"

    # Get all items with the specified stateTag
    items = canvas.find_withtag(stateTag)

    for item in items:
        # Check the type of item and update its color accordingly
        if canvas.type(item) == "oval":  # For circles, change the outline color
            canvas.itemconfig(item, outline=color)
        elif canvas.type(item) == "text":  # For text, change the text color
            canvas.itemconfig(item, fill=color)

def construct_PDA_states(pda):
    """    Constructs and displays the states of a Pushdown Automaton (PDA) on a canvas.
    This function creates draggable circles representing the states of the PDA, 
    along with their labels and additional visual elements such as initial state 
    arrows and nested circles for final states. Each state is assigned a unique 
    identifier and grouped for movement on the canvas.
    Args:
        pda (PDA): An object representing the Pushdown Automaton. It is expected 
                   to have a `states` attribute, where each state has the following 
                   properties:
                   - name (str): The name of the state.
                   - isFinal (bool): Indicates if the state is a final state.
                   - isInitial (bool): Indicates if the state is the initial state.
    Returns:
        list: A list of canvas objects representing the displayed states.
    """
    # Draw n draggable circles
    circle_radius = 50
    circle_spacing = 20
    displayedStates = []

    stateID = 0
    for state in pda.states:
        x1 = (circle_radius * 2 + circle_spacing) * stateID + circle_spacing
        y1 = circle_spacing
        x2 = x1 + circle_radius * 2
        y2 = y1 + circle_radius * 2

        # Display state name above the circle
        text_x = (x1 + x2) / 2
        text_y = y1 - 10  # Position slightly above the circle
        canvas.create_text(text_x, text_y, text=state.name, tags=(f"state_{stateID}", f"mvmt_group_{stateID}"))

        # Display circle
        if state.isFinal:
            currState = (create_nested_circle(x1, y1, x2, y2, stateID))[0]
        else:
            currState = canvas.create_oval(x1, y1, x2, y2, fill="white", tags=(f"state_{stateID}", f"mvmt_group_{stateID}", "draggable"))
        
        # Add the initial arrow
        if state.isInitial:
            arrow_x1 = x1 - 30
            arrow_y1 = (y1 + y2) / 2
            arrow_x2 = x1
            arrow_y2 = (y1 + y2) / 2
            canvas.create_line(arrow_x1, arrow_y1, arrow_x2, arrow_y2, arrow=tk.LAST, tags=(f"state_{stateID}", f"mvmt_group_{stateID}"))
            # Set Color to Red
            update_state_color(stateID, True)
        
        
        displayedStates.append(currState)
        stateID += 1

    return displayedStates

def construct_PDA_arrows(pda, stateList, matrix):
    """
    Constructs and draws arrows representing the transitions of a Pushdown Automaton (PDA) 
    on a graphical interface.

    This function iterates through the states and transitions of the given PDA, and for each 
    transition, it determines whether to draw a circular arrow (for self-loops) or a standard 
    arrow (for transitions between different states). The arrows are drawn on the provided 
    matrix using the state positions from the stateList.

    Args:
        pda (PDA): The Pushdown Automaton object containing states and transitions.
        stateList (list): A list of state objects or their graphical representations, 
                          used to determine the positions of states.
        matrix: The graphical matrix or canvas where the arrows will be drawn.

    Returns:
        None
    """
    for stateID in range(len(pda.states)):
        for transition in pda.states[stateID].transitions:
            if stateID == transition.destinationState:
                draw_circular_arrow(matrix, stateList, stateID, transition)
            else:
                draw_arrow(matrix, stateList, stateID, transition.destinationState, transition)
            
def restart_canvas(fromJson):
    global restart
    restart = True

    # Clear the canvas instead of destroying the root window
    canvas.delete("all")

    # Destroy the state form window
    if not fromJson:
        stateForm.root.destroy()

    # Destroy all widgets in the root window except the canvas
    for widget in root.winfo_children():
        if widget != canvas:
            widget.destroy()
    root.quit()

def make_step(pda, input, currIndex, sourceButton):
    #print(currIndex)
    if currIndex < len(input):
        currSymbol = input[currIndex]
    elif pda.states[pda.currState].isFinal:
        messagebox.showinfo("Accepted", "This input was accepted!")
        return
    else:
        currSymbol = None
    validTransitions = pda.findTransitions(currSymbol)
    #print (f"list of valid transitions: {validTransitions}")
    if len(validTransitions) > 0:
        transitionToTake = None
        currStateIndex = pda.currState
        if len(validTransitions) == 1:
            transitionToTake = validTransitions[0]
        else:
            # Create a pop-up window for transition selection
            popup = tk.Toplevel(root)
            popup.title("Select Transition")
            popup.geometry("300x200")
            popup.grab_set()  # Block interaction with the main window

            # Add a label to the pop-up
            label = tk.Label(popup, text="Select a transition:")
            label.pack(pady=10)

            # Create a variable to store the selected transition
            selected_transition = tk.StringVar(popup)
            selected_transition.set(validTransitions[0].toString())  # Default to the first transition

            # Create a dropdown menu for transitions
            dropdown = tk.OptionMenu(popup, selected_transition, *[t.toString() for t in validTransitions])
            dropdown.pack(pady=10)
            
            # Function to confirm the selection
            def confirm_selection(): #function defined in an if else block wtf am i smoking
                nonlocal transitionToTake
                for t in validTransitions:
                    if t.toString() == selected_transition.get():
                        transitionToTake = t
                popup.destroy()
            
            # Add a confirm button
            confirm_button = tk.Button(popup, text="Confirm", command=confirm_selection)
            confirm_button.pack(pady=10)

            # Wait for the user to make a selection
            popup.wait_window()

        # Proceed with the selected transition
        resultStateIndex = transitionToTake.destinationState
        update_state_color(currStateIndex, False)
        update_state_color(resultStateIndex, True)
        pda.doTransitions(transitionToTake)
        display_stack(pda)
        if pda.states[pda.currState].isFinal and currIndex == len(input) - 1:
            messagebox.showinfo("Accepted", "This input was accepted!")
        if transitionToTake.inputSymbol is None:
            sourceButton.config(command=lambda: make_step(pda, input, currIndex, sourceButton))
            display_input(input, currIndex)
        else:
            sourceButton.config(command=lambda: make_step(pda, input, currIndex + 1, sourceButton))
            display_input(input, currIndex + 1)
    else:
        messagebox.showerror("Did Not Accept", "Failed, no valid transitions")
        sourceButton.config(command=lambda: messagebox.showerror("Did Not Accept", "Failed, no valid transitions"))
    # take the first one

def submit_input_string(pda):
    user_input = input_box.get()
    #Create a step forward button
    display_input(user_input, 0)
    step_button = tk.Button(root, text="Step", command=lambda: make_step(pda, user_input, 0, step_button))
    reset_button = tk.Button(root, text="Reset with new Input", command=lambda: restart_PDA(pda))
    reset_button.pack(pady=10)
    step_button.pack(pady=10)
    submit_input_button.pack_forget()  # Hide the button that called this
    input_box.pack_forget() # Hide the box used for input
    label.pack_forget() #Hide the label for input
        # Create a button to reset to take new input

# Function to display the stack on the canvas
def display_stack(pda):
    # Clear any existing stack display
    canvas.delete("stack_display")

    # Format the stack as a string
    stack_text = "Stack:\n" + "\n".join(pda.stack)

    # Display the stack in the top-left corner
    canvas.create_text(10, 10, anchor="nw", text=stack_text, fill="black", font=("Arial", 12), tags="stack_display")

def display_input(input, currIndex):
    # Clear any existing input display
    canvas.delete("input_display")

    # Format the input string with the current character highlighted
    formatted_input = ""
    for i, char in enumerate(input):
        if i == currIndex:
            formatted_input += f"[{char}]"  # Highlight the current character
        else:
            formatted_input += char

    # Display the input string at the bottom of the canvas
    canvas.create_text(400, 580, text=f"Input: {formatted_input}", fill="black", font=("Arial", 14), tags="input_display")

def restart_PDA(pda):
    #save PDA to temp file
    pda.jsonEncoding("cache")
    #set flag to use cached PDA
    global fromCache
    fromCache = True
    #restart entire program
    restart_canvas(True)
    pass

# Create a simple tkinter form to prompt the user
def prompt_import_method():
    def set_from_json(value):
        global fromJson
        fromJson = value
        prompt_window.destroy()

    # Create a new window for the prompt
    prompt_window = tk.Toplevel(root)
    prompt_window.title("Import Method")
    prompt_window.geometry("300x150")
    prompt_window.grab_set()  # Block interaction with the main window

    # Add a label
    label = tk.Label(prompt_window, text="Do you want to import from data.json?")
    label.pack(pady=10)

    # Add buttons for Yes and No
    yes_button = tk.Button(prompt_window, text="Yes", command=lambda: set_from_json(True))
    yes_button.pack(side=tk.LEFT, padx=20, pady=20)

    no_button = tk.Button(prompt_window, text="No", command=lambda: set_from_json(False))
    no_button.pack(side=tk.RIGHT, padx=20, pady=20)

    # Wait for the user to make a selection
    prompt_window.wait_window()


# Create the main application window
root = tk.Tk()
root.title("Canvas")

# Create a canvas widget
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

restart = False
fromCache = False

while True:
    # Call the prompt function to set fromJson
    fromJson = False  # Default value
    importValid = False 
    while not importValid:
        if not fromCache:
            prompt_import_method()         
        importValid = True

    restart = False
    #clear canvas
    canvas.delete("all")

    pda = PDASim.PDA([], 0)
    stateList = []
    
    # If user tries to input from JSON
    # Read the JSON file as a string
    if fromJson or fromCache:
        json_string = ""
        filepath = filedialog.askopenfilename(initialdir = ".", title = "Select a File",filetypes = (("Json files",
                                                        "*.json*"),
                                                       ("all files",
                                                        "*.*")))
        if not ("json" in filepath):
            messagebox.showerror("File Error", "Did not select Json File")
            continue
        with open(f'{filepath if fromJson else "cache.json"}', 'r') as file:
            json_string = file.read()
        pda.jsonDecoding(json_string)
        stateList = construct_PDA_states(pda)
        adjacency_matrix = [[0 for _ in range(len(stateList))] for _ in range(len(stateList))]
        construct_PDA_arrows(pda, stateList, adjacency_matrix)
    else: 
        # Construct State circles via form
        stateForm = Forms.AddStateForm(tk.Toplevel(root), pda, construct_PDA_states, construct_PDA_arrows, stateList) #CHANGE tk.Toplevel(root) TO WHEREVER THE FORM SHOULD BE DISPLAYED UNDER
    
    # Now that the PDA has been initialized, display the (empty) stack
    display_stack(pda)

    # Bind mouse events, allowing draff
    selected_item = None
    canvas.bind("<ButtonPress-1>", on_press)
    if fromJson or fromCache:
        canvas.bind("<B1-Motion>", lambda event: on_drag(event, stateList, adjacency_matrix))
    else:
        canvas.bind("<B1-Motion>", lambda event: on_drag(event, stateList, stateForm.transitionForm.adjacencyMatrix))

    # Create a restart button
    restart_button = tk.Button(root, text="New PDA", command=lambda: restart_canvas(fromJson))
    restart_button.pack(pady=10)
    
    # Create a label
    label = tk.Label(root, text="Input to Machine:")
    label.pack(pady=5)

    # Create a text box
    input_box = tk.Entry(root, width=40)
    input_box.pack(pady=5)

    #Create a submit input button, which itself creates a step forward button
    submit_input_button = tk.Button(root, text="Submit Input", command=lambda: submit_input_string(pda))
    submit_input_button.pack(pady=10)

    #Create a submit input button, which itself creates a step forward button
    save_as_json_button = tk.Button(root, text="Save PDA to data.json", command=lambda: pda.jsonEncoding())
    save_as_json_button.pack(pady=10)

    if fromCache:
        # Delete cache.json file
        if os.path.exists("cache.json"):
            os.remove("cache.json")

    # Run the application
    root.mainloop()
    if not root.winfo_exists():
        break
    
