import tkinter as tk

class App:
    def __init__(self, sets_configuration):
        self.model = Model()
        self.controller = Controller(sets_configuration)
        self.view = View()

        self.model.set_controller(self.controller)
        self.model.set_view(self.view)

        self.controller.set_model(self.model)
        
        self.view.set_controller(self.controller)
        self.view.set_model(self.model)

        print("App initialized.")

    def run(self):
        self.view.start()

# Receives user events from view. Manipulates model.
class Controller:
    def __init__(self, sets_configuration):
        self.sets_config = sets_configuration
        print("Controller initialized.")
    
    def set_model(self, model):
        self.model_delegate = model

# On change, notifies view.
class Model:
    def __init__(self):
        print("Model initialized.")
    
    def set_controller(self, controller):
        self.controller_delegate = controller
    
    def set_view(self, view):
        self.view_delegate = view

# Pulls data from model. Receives user events and pushes to Controller.
class View:
    def __init__(self):
        self.window = tk.Tk()
        print("View initialized.")

    def set_controller(self, controller):
        self.controller_delegate = controller
    
    def set_model(self, model):
        self.model_delegate = model

    def start(self):
        if not hasattr(self, 'controller_delegate'):
            raise Exception("View needs a controller delegate to start.")
        
        if not hasattr(self, 'model_delegate'):
            raise Exception("View needs a model delegate to start.")
        
        self.window.mainloop()
        print("View started.")

    def rerender(self):
        print("Re-rendering view.")
        self.window.update()

    def __build_initial_view():
        # Set image layout

        # Create textbox

        # Create submit button
        pass


# TODO(jsnl): Design the application starting from the model. Consider:
#
#     1. "on_correct_guess" / "on_incorrect_guess"
#     2. Displaying correctness score.
#     3. Tracking correctness streak.
#     4. Tracking number correct in set.
#     5. Need some concept of a "session" (i.e. one play thru of cards)
#     6. Need card shuffling mechanic.
#     7. Need set selection functionality.