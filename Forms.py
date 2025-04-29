import tkinter as tk
import PDASim

#pass the wherever the form should be displayed under to as root
class AddTransitionForm:
    def __init__(self, root, pda, constructFunction, stateList):
        self.root = root
        self.root.title("Transition Entry Form")
        self.constructFunction = constructFunction #function that creates arrows between states
        self.stateList = stateList #list of 'state' circle objects, created by the state form
        self.adjacencyMatrix = [[0 for _ in range(len(stateList))] for _ in range(len(stateList))] #matrix to store arrows
        
        self.pda = pda
        
        # Add list of state names
        self.stateNameList = []
        for state in pda.states:
            self.stateNameList.append(state.name)
        
        self.transition_sections = []  # To track all transition entry blocks

        # Title
        title = tk.Label(root, text="Add Transitions", font=("Arial", 14))
        title.pack(pady=10)

        # Scrollable Canvas Setup
        canvas_frame = tk.Frame(root)
        canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_frame, borderwidth=0)
        self.canvas.config(width=650)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Frame inside the canvas
        self.form_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.form_frame, anchor="nw")

        # Configure scrolling behavior
        def on_frame_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.form_frame.bind("<Configure>", on_frame_configure)

        # Allow mousewheel scrolling on Windows/macOS
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Add initial transition section
        self.add_transition_section()

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        add_button = tk.Button(btn_frame, text="Add Transition", command=self.add_transition_section)
        add_button.pack(side="left", padx=5)

        submit_button = tk.Button(btn_frame, text="Submit", command=self.submit_form)
        submit_button.pack(side="left", padx=5)

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()
        
    def getValue(self, entry):
        """Returns value of form element or None if element is empty"""
        if isinstance(entry, tk.BooleanVar):
            return entry.get()
        value = entry.get().strip()
        return value if value else None

    def add_transition_section(self):
        """Add a new transition entry section."""
        frame = tk.Frame(self.form_frame, borderwidth=1, relief="groove", padx=10, pady=10)
        frame.pack(pady=5, fill="x", expand=True)

        # Store the input widgets
        inputs = {}
     
        # Source
        tk.Label(frame, text="Source state:").grid(row=0, column=0, sticky="e")
        inputs['sourceState'] = tk.StringVar()
        tk.OptionMenu(frame, inputs['sourceState'], *self.stateNameList).grid(row=0, column=1, pady=2, padx=5)

        # Destination
        tk.Label(frame, text="Destination state:").grid(row=1, column=0, sticky="e")
        inputs['destinationState'] = tk.StringVar()
        tk.OptionMenu(frame, inputs['destinationState'], *self.stateNameList).grid(row=1, column=1, pady=2, padx=5)

        # Input
        tk.Label(frame, text="Input symbol:").grid(row=2, column=0, sticky="e")
        inputs['inputSymbol'] = tk.Entry(frame)
        inputs['inputSymbol'].grid(row=2, column=1, pady=2, padx=5)
        
        # Stack
        tk.Label(frame, text="Stack symbol:").grid(row=3, column=0, sticky="e")
        inputs['stackSymbol'] = tk.Entry(frame)
        inputs['stackSymbol'].grid(row=3, column=1, pady=2, padx=5)
        
        # Pop
        inputs['pop'] = tk.BooleanVar()
        tk.Checkbutton(frame, text="Should this transition pop the top of the stack? (it does not need to pop to read the symbol)", variable=inputs['pop']).grid(row=4, column=1, pady=2, padx=5)
        
        # Push
        tk.Label(frame, text="Pushed symbol:").grid(row=5, column=0, sticky="e")
        inputs['push'] = tk.Entry(frame)
        inputs['push'].grid(row=5, column=1, pady=2, padx=5)
        

        self.transition_sections.append(inputs)

    def submit_form(self):
        """Collect and display data from all transition sections."""
        allTransitions = []
        for idx, transition in enumerate(self.transition_sections):
            sourceState = self.getValue(transition['sourceState'])
            destinationState = self.getValue(transition['destinationState'])
            inputSymbol = self.getValue(transition['inputSymbol'])
            stackSymbol = self.getValue(transition['stackSymbol'])
            pop = transition['pop'].get() #can get actual value because it is a boolean and cannot be None
            push = self.getValue(transition['push'])
            allTransitions.append({'sourceState': sourceState, 'destinationState': destinationState, 'inputSymbol': inputSymbol, 'stackSymbol': stackSymbol, 'pop': pop, 'push': push})

        #print("Submitted Transitions:")
        stateMap = {item.name: index for index, item in enumerate(self.pda.states)}
        for i, transition in enumerate(allTransitions):
            #print(f"Transition {i + 1}: src={transition['sourceState']}, destinationState={transition['destinationState']}")
            src = stateMap.get(transition['sourceState'], -1)
            dest = stateMap.get(transition['destinationState'], -1)
            if src == -1 or dest == -1:
                print(f"either the source state or the destination state does not exist! transition {i} skipped.")
            else:
                toAdd = PDASim.Transition(dest, transition['inputSymbol'], transition['stackSymbol'], transition['push'], transition['pop'])
                self.pda.states[src].transitions.append(toAdd)
            #for state in pda.states:
                #print(stateMap)
                #print(state.name)

        if self.constructFunction:
            # print(self.stateList)
            # print(self.pda.states)
            # print(self.adjacencyMatrix)
            self.constructFunction(self.pda, self.stateList, self.adjacencyMatrix)
            self.root.destroy()
        
        
        
             
        
#pass the wherever the form should be displayed under to as root
class AddStateForm:
    def __init__(self, root, pda, constructFunction, constructArrowsFunction, stateList):
        self.root = root
        self.root.title("State Entry Form")
        self.constructFunction = constructFunction
        self.constructArrowsFunction = constructArrowsFunction
        self.stateList = stateList #list of circle objects
        self.transitionForm = None
        
        self.pda = pda

        self.state_sections = []  # To track all state entry blocks

        # Title
        title = tk.Label(root, text="Add States", font=("Arial", 14))
        title.pack(pady=10)

        # Scrollable Canvas Setup
        canvas_frame = tk.Frame(root)
        canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_frame, borderwidth=0)
        self.canvas.config(width=200)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Frame inside the canvas
        self.form_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.form_frame, anchor="nw")

        # Configure scrolling behavior
        def on_frame_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.form_frame.bind("<Configure>", on_frame_configure)

        # Allow mousewheel scrolling on Windows/macOS
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Add initial state section
        self.add_state_section()

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        add_button = tk.Button(btn_frame, text="Add State", command=self.add_state_section)
        add_button.pack(side="left", padx=5)

        submit_button = tk.Button(btn_frame, text="Submit", command=self.submit_form)
        submit_button.pack(side="left", padx=5)

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

    def getValue(self, entry):
        """Returns value of form element or None if element is empty"""
        if isinstance(entry, tk.BooleanVar):
            return entry.get()
        value = entry.get().strip()
        return value if value else None

    def add_state_section(self):
        """Add a new state entry section"""
        frame = tk.Frame(self.form_frame, borderwidth=1, relief="groove", padx=10, pady=10)
        frame.pack(pady=5, fill="x", expand=True)

        # Store the input widgets
        inputs = {}
        
        # get index of this state entry section
        index = len(self.state_sections)

        # name
        tk.Label(frame, text="Name:").grid(row=0, column=0, sticky="e")
        inputs['name'] = tk.Entry(frame)
        inputs['name'].grid(row=0, column=1, pady=2, padx=5)

        # initial
        inputs['initial'] = tk.BooleanVar()
        tk.Checkbutton(frame, text="Initial state?", variable=inputs['initial'], 
                       command=lambda idx=index: self.handle_initial_selection(idx)).grid(row=1, column=1, pady=2, padx=5)

        # final
        inputs['final'] = tk.BooleanVar()
        tk.Checkbutton(frame, text="Final state?", variable=inputs['final']).grid(row=2, column=1, pady=2, padx=5)
        

        self.state_sections.append(inputs)

    def handle_initial_selection(self, selected_index):
        # If the user checked this box, uncheck all others
        for idx, state in enumerate(self.state_sections):
            if idx != selected_index:
                state['initial'].set(False)
                
    def validate_states(self):
        initial_count = 0
        final_count = 0
        unnamed_state = False

        for state in self.state_sections:
            if state['initial'].get():
                initial_count += 1
            if state['final'].get():
                final_count += 1
            if not self.getValue(state['name']):
                unnamed_state = True

        errors = []
        if initial_count != 1:
            errors.append("There must be exactly one initial state.")
        if final_count == 0:
            errors.append("There must be at least one final state.")
        if unnamed_state:
            errors.append("There is at least one unnamed state")

        if errors:
            error_message = "\n".join(errors)
            self.root.lift()
            self.root.attributes('-topmost', True)
            tk.messagebox.showerror("Validation Error", error_message)
            self.root.attributes('-topmost', False)
            return False
        return True
    
    def submit_form(self):
        """Save data from all state sections to a PDA"""
        if not self.validate_states():
            return
        allStates = []
        for idx, state in enumerate(self.state_sections):
            name = self.getValue(state['name'])
            initial = state['initial'].get()
            final = state['final'].get()
            allStates.append({'name': name, 'initial': initial, 'final': final})

        #print("Submitted States:")
        for i, state in enumerate(allStates):
            #print(f"State {i + 1}: name={state['name']}, final={state['final']}") #debug message
            self.pda.states.append(PDASim.State(state['name'], state['initial'], state['final'], []))
            if state['initial']:
                self.pda.currState = len(self.pda.states) - 1
                self.pda.initialState = len(self.pda.states) - 1
        
        if self.constructFunction:
            new_states = self.constructFunction(self.pda)
            self.stateList.clear()  # Clear the existing list
            self.stateList.extend(new_states)  # Add the new states to the same list
            self.root.withdraw()  # Hide the current tkinter window
            self.transitionForm = AddTransitionForm(tk.Toplevel(self.root), self.pda, self.constructArrowsFunction, self.stateList)

