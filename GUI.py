import tkinter as tk

# Create the main application window
root = tk.Tk()
root.title("Canvas")

# Create a canvas widget
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

#Draw Circle
canvas.create_oval(50, 50, 150, 150, fill="blue")

# Run the application
root.mainloop()