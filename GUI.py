import tkinter as tk

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

def on_drag(event):
    # Move the selected item with the mouse
    if selected_item:
        canvas.coords(selected_item, event.x - 50, event.y - 50, event.x + 50, event.y + 50)

# Create the main application window
root = tk.Tk()
root.title("Canvas")

# Create a canvas widget
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

# Draw a draggable circle
circle = canvas.create_oval(50, 50, 150, 150, fill="blue", tags="draggable")

# Draw a non-draggable rectangle
rectangle = canvas.create_rectangle(200, 200, 300, 300, fill="red")

# Bind mouse events
selected_item = None
canvas.bind("<ButtonPress-1>", on_press)
canvas.bind("<B1-Motion>", on_drag)

# Run the application
root.mainloop()