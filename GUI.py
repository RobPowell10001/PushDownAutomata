import tkinter as tk
from tkinter import messagebox
import PDASim
import Forms

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
        state_tag = None
        for tag in tags:
            if tag.startswith("state_"):
                state_tag = tag
            break
        if state_tag is not None:
            items_to_move = canvas.find_withtag(state_tag)
            for item in items_to_move:
                canvas.move(item, dx, dy)
        update_arrows(states, matrix, selected_item)

#draws an arrow from state 1 to state 2
def draw_arrow(matrix, states, index1, index2, transition):
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
    text_id = canvas.create_text(midpoint_x, midpoint_y - 10, text=f"{transition.toString()}", fill="black")

    # Associate the text ID with the arrow
    canvas.itemconfig(newArrow, tags=(f"arrow_{index1}_{index2}", f"text_{text_id}"))

    # Store the arrow in the matrix
    if matrix[index1][index2] != 0:
        matrix[index1][index2].append((newArrow, text_id))
    else:
        matrix[index1][index2] = [(newArrow, text_id)]

def draw_circular_arrow(matrix, stateList, stateID, transition):
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
    circular_arrow = canvas.create_arc(x1, y1, x2, y2, start=0, extent=300, style=tk.ARC, tags=(f"state_{stateID}"))

    # Add an arrowhead pointing straight down
    arrow_offset_x = 19
    arrow_offset_y = -15
    arrow_x1 = start_x + arrow_offset_x
    arrow_y1 = start_y + loop_offset * 0.7 + arrow_offset_y
    arrow_x2 = start_x + arrow_offset_x
    arrow_y2 = start_y + loop_offset * 0.9 + arrow_offset_y
    canvas.create_line(arrow_x1, arrow_y1, arrow_x2, arrow_y2, arrow=tk.LAST, tags=(f"state_{stateID}"))

    # Add the transition text near the circular arrow
    text_x = start_x - loop_offset * 1.5
    text_y = start_y - loop_offset * 1.5
    text_id = canvas.create_text(text_x, text_y, text=f"{transition.toString()}", fill="black", tags=(f"state_{stateID}"))

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
                midpoint_x = (state1_edge[0] + state2_edge[0]) / 2
                midpoint_y = (state1_edge[1] + state2_edge[1]) / 2
                canvas.coords(text_id, midpoint_x, midpoint_y - 10)

def create_nested_circle(x1, y1, x2, y2, stateID):
    # Outer circle
    outer_circle = canvas.create_oval(x1, y1, x2, y2, fill="white", tags=(f"state_{stateID}", "draggable"))
    
    # Calculate coordinates for the inner circle
    inner_margin = 10  # Margin between the outer and inner circles
    inner_x1 = x1 + inner_margin
    inner_y1 = y1 + inner_margin
    inner_x2 = x2 - inner_margin
    inner_y2 = y2 - inner_margin
    
    # Inner circle
    inner_circle = canvas.create_oval(inner_x1, inner_y1, inner_x2, inner_y2, fill="white", tags=(f"state_{stateID}"))
    
    return outer_circle, inner_circle


def constructPDAStates(pda):

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
        if state.isFinal == True:
            currState = (create_nested_circle(x1, y1, x2, y2, stateID))[0]
        elif state.isInitial:
            # Add the initial arrow
            currState = canvas.create_oval(x1, y1, x2, y2, fill="white", tags=(f"state_{stateID}", "draggable"))
            arrow_x1 = x1 - 30
            arrow_y1 = (y1 + y2) / 2
            arrow_x2 = x1
            arrow_y2 = (y1 + y2) / 2
            canvas.create_line(arrow_x1, arrow_y1, arrow_x2, arrow_y2, arrow=tk.LAST, tags=(f"state_{stateID}"))
        else:
            currState = canvas.create_oval(x1, y1, x2, y2, fill="white", tags=(f"state_{stateID}", "draggable"))
        
        # Display state name above the circle
        text_x = (x1 + x2) / 2
        text_y = y1 - 10  # Position slightly above the circle
        canvas.create_text(text_x, text_y, text=state.name, tags=(f"state_{stateID}"))
        displayedStates.append(currState)
        stateID += 1

    return displayedStates

def constructPDAArrows(pda, stateList, matrix):
    
    for stateID in range(len(pda.states)):
        for transition in pda.states[stateID].transitions:
            if stateID == transition.destinationState:
                draw_circular_arrow(matrix, stateList, stateID, transition)
            else:
                draw_arrow(matrix, stateList, stateID, transition.destinationState, transition)
            



# Create the main application window
root = tk.Tk()
root.title("Canvas")

# Create a canvas widget
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

restart = False
first = True

def on_submit():
    global restart
    restart = True
    root.quit()

while True:
    restart = False
    #clear canvas
    canvas.delete("all")

    pda = PDASim.PDA([], 0)

    stateList = []
    adjacency_matrix = []
    # Construct State circles via form
    stateForm = Forms.AddStateForm(tk.Toplevel(root), pda, constructPDAStates, constructPDAArrows, stateList) #CHANGE tk.Toplevel(root) TO WHEREVER THE FORM SHOULD BE DISPLAYED UNDER

    # Draw Arrows for Transitions
    # Initialized to 0 -- if there is no arrow, will be 0. If there is an arrow, it is a list of arrow objects
    # transitionForm = 

    # Bind mouse events 
    selected_item = None
    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", lambda event: on_drag(event, stateList, stateForm.transitionForm.adjacencyMatrix))

    if first:
        # Create a submit button
        submit_button = tk.Button(root, text="Restart", command=on_submit)
        submit_button.pack(pady=10)

    # Run the application
    root.mainloop()
    if not root.winfo_exists():
        break
    first = False
    
