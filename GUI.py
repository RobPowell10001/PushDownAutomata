import tkinter as tk
from tkinter import messagebox

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
        canvas.coords(selected_item, event.x - 50, event.y - 50, event.x + 50, event.y + 50)
        update_arrows(states, matrix, selected_item)

#draws an arrow from state 1 to state 2
def draw_arrow(matrix, states, index1, index2):
    state1 = states[index1]
    state2 = states[index2]
    # Get central coords of each
    state1_coords = canvas.coords(state1)
    state1_center = ((state1_coords[0] + state1_coords[2]) / 2, (state1_coords[1] + state1_coords[3]) / 2)
    state2_coords = canvas.coords(state2)
    state2_center = ((state2_coords[0] + state2_coords[2]) / 2, (state2_coords[1] + state2_coords[3]) / 2)
    newArrow = canvas.create_line(state1_center[0], state1_center[1], state2_center[0], state2_center[1], arrow=tk.LAST)
    matrix[index1][index2] = newArrow
    # return newArrow

#update all arrows associated with the selected state
def update_arrows(states, matrix, selectedState):
    tags = canvas.gettags(selectedState)
    for tag in tags:
        if tag.startswith("state_"):
            sourceID = int(tag.split("_")[1])
            break
    # update outward arrows
    destinationID = 0
    for arrowToDestination in matrix[sourceID]:
        if arrowToDestination != 0:
            update_arrow(arrowToDestination, states, sourceID, destinationID)
        destinationID += 1
    # now update inward arrows
    destinationID = sourceID
    sourceID = 0
    for arrowsFromSource in matrix:
        if arrowsFromSource[destinationID] != 0:
            update_arrow(arrowsFromSource[destinationID], states, sourceID, destinationID)
        sourceID += 1
    

def update_arrow(arrow, states, id1, id2):
    # Get the center of the circle
    state1_coords = canvas.coords(states[id1])
    state1_center = ((state1_coords[0] + state1_coords[2]) / 2, (state1_coords[1] + state1_coords[3]) / 2)

    # Get the center of the rectangle
    state2_coords = canvas.coords(states[id2])
    state2_center = ((state2_coords[0] + state2_coords[2]) / 2, (state2_coords[1] + state2_coords[3]) / 2)

    # Update the arrow to connect the two centers
    canvas.coords(arrow, state1_center[0], state1_center[1], state2_center[0], state2_center[1])


# Create the main application window
root = tk.Tk()
root.title("Canvas")

# Create a canvas widget
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

# Draw n draggable circles
n = 3  # Number of circles
circle_radius = 50
circle_spacing = 20
states = []

for i in range(n):
    x1 = (circle_radius * 2 + circle_spacing) * i + circle_spacing
    y1 = circle_spacing
    x2 = x1 + circle_radius * 2
    y2 = y1 + circle_radius * 2
    circle = canvas.create_oval(x1, y1, x2, y2, fill="blue", tags=["draggable", f"state_{i}"])
    states.append(circle)

# Initialized to 0 -- if there is no arrow, will be 0. If there is an arrow, it is an arrow object
adjacency_matrix = [[0 for _ in range(n)] for _ in range(n)]

draw_arrow(adjacency_matrix, states, 0, 1)
draw_arrow(adjacency_matrix, states, 1, 2)

# Bind mouse events
selected_item = None
canvas.bind("<ButtonPress-1>", on_press)
canvas.bind("<B1-Motion>", lambda event: on_drag(event, states, adjacency_matrix))

# Create a label
label = tk.Label(root, text="Formal Defn of PDA:")
label.pack(pady=5)

# Create a text box
input_box = tk.Entry(root, width=40)
input_box.pack(pady=5)
def on_submit():
    user_input = input_box.get()
    if user_input:
        print(user_input)
        #do sm with it
    else:
        messagebox.showwarning("Warning", "Input cannot be empty!")

# Create a submit button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=10)

# Run the application
root.mainloop()