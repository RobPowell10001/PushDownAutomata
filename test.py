#print("hi world")

import tkinter as tk
import PDASim

#pass the wherever the form should be displayed under to as root
class AddTransitionForm:
    def __init__(self, root, pda):
        self.root = root
        self.root.title("Transition Entry Form")
        
        self.pda = pda

        self.transition_sections = []  # To track all transition entry blocks

        # Title
        title = tk.Label(root, text="Add Transitions", font=("Arial", 14))
        title.pack(pady=10)

        # Container for dynamic form sections
        self.form_frame = tk.Frame(root)
        self.form_frame.pack()

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

    def add_transition_section(self):
        """Add a new transition entry section (name, email, phone)."""
        frame = tk.Frame(self.form_frame, borderwidth=1, relief="groove", padx=10, pady=10)
        frame.pack(pady=5, fill="x", expand=True)

        # Store the input widgets
        inputs = {}

        # Source
        tk.Label(frame, text="Source state:").grid(row=0, column=0, sticky="e")
        inputs['sourceState'] = tk.Entry(frame)
        inputs['sourceState'].grid(row=0, column=1, pady=2, padx=5)

        # Destination
        tk.Label(frame, text="Destination state:").grid(row=1, column=0, sticky="e")
        inputs['destinationState'] = tk.Entry(frame)
        inputs['destinationState'].grid(row=1, column=1, pady=2, padx=5)

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
        all_people = []
        for idx, transition in enumerate(self.transition_sections):
            sourceState = transition['sourceState'].get()
            destinationState = transition['destinationState'].get()
            inputSymbol = transition['inputSymbol'].get()
            stackSymbol = transition['stackSymbol'].get()
            pop = transition['pop'].get()
            push = transition['push'].get()
            all_people.append({'sourceState': sourceState, 'destinationState': destinationState, 'inputSymbol': inputSymbol, 'stackSymbol': stackSymbol, 'pop': pop, 'push': push})

        #print("Submitted Transitions:")
        stateMap = {item.name: index for index, item in enumerate(pda.states)}
        for i, transition in enumerate(all_people):
            #print(f"Transition {i + 1}: src={transition['sourceState']}, destinationState={transition['destinationState']}")
            src = stateMap.get(transition['sourceState'], -1)
            dest = stateMap.get(transition['destinationState'], -1)
            if src == -1 or dest == -1:
                print(f"either the source state or the destination state does not exist! transition {i} skipped.")
            else:
                toAdd = PDASim.Transition(src, dest, transition['inputSymbol'], transition['stackSymbol'], transition['push'], transition['pop'])
                pda.states[src].transitions.append(toAdd)
            #for state in pda.states:
                #print(stateMap)
                #print(state.name)

        self.result_label.config(text="Form submitted! Check console for data.")
        
        
        
        
             
        
#pass the wherever the form should be displayed under to as root
class AddStateForm:
    def __init__(self, root, pda):
        self.root = root
        self.root.title("State Entry Form")
        
        self.pda = pda

        self.state_sections = []  # To track all state entry blocks

        # Title
        title = tk.Label(root, text="Add States", font=("Arial", 14))
        title.pack(pady=10)

        # Container for dynamic form sections
        self.form_frame = tk.Frame(root)
        self.form_frame.pack()

        # Add initial state section
        self.add_transition_section()

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        add_button = tk.Button(btn_frame, text="Add State", command=self.add_transition_section)
        add_button.pack(side="left", padx=5)

        submit_button = tk.Button(btn_frame, text="Submit", command=self.submit_form)
        submit_button.pack(side="left", padx=5)

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

    def add_transition_section(self):
        """Add a new state entry section (name, email, phone)."""
        frame = tk.Frame(self.form_frame, borderwidth=1, relief="groove", padx=10, pady=10)
        frame.pack(pady=5, fill="x", expand=True)

        # Store the input widgets
        inputs = {}

        # name
        tk.Label(frame, text="Name:").grid(row=0, column=0, sticky="e")
        inputs['name'] = tk.Entry(frame)
        inputs['name'].grid(row=0, column=1, pady=2, padx=5)

        # initial
        inputs['initial'] = tk.BooleanVar()
        tk.Checkbutton(frame, text="Initial state?", variable=inputs['initial']).grid(row=1, column=1, pady=2, padx=5)

        # final
        inputs['final'] = tk.BooleanVar()
        tk.Checkbutton(frame, text="Final state?", variable=inputs['final']).grid(row=2, column=1, pady=2, padx=5)
        

        self.state_sections.append(inputs)

    def submit_form(self):
        """Save data from all state sections to a PDA."""
        all_states = []
        for idx, state in enumerate(self.state_sections):
            name = state['name'].get()
            initial = state['initial'].get()
            final = state['final'].get()
            all_states.append({'name': name, 'initial': initial, 'final': final})

        #print("Submitted States:")
        for i, state in enumerate(all_states):
            #print(f"State {i + 1}: name={state['name']}, final={state['final']}")
            pda.states.append(PDASim.State(state['name'], state['initial'], state['final'], []))
            if state['initial']:
                pda.currState = len(pda.states) - 1

        #self.result_label.config(text="Form submitted! Check console for data.")

# Run the app
root = tk.Tk()
pda = PDASim.PDA([], 0)
app = AddStateForm(tk.Toplevel(root), pda) #CHANGE tk.Toplevel(root) TO WHEREVER THE FORM SHOULD BE DISPLAYED UNDER
app2 = AddTransitionForm(tk.Toplevel(root), pda)
root.mainloop()
