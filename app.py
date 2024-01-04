import tkinter as tk
from functools import reduce

''' Title displayed in app window. '''
WINDOW_TITLE = "Flashcards"

''' User guesses with a correctness score above or equal this threshold will be
counted as correct. See the `correctness_score` function in this file for a
precise definition.
'''
LEVENSHTEIN_THRESHOLD = 0.90

class App:
    def __init__(self, sets_configuration):
        self.model = Model()
        self.view = View()
        self.controller = Controller(sets_configuration)

        self.view.set_controller(self.controller)
        self.view.set_model(self.model)

        self.model.set_view(self.view)
        self.model.set_controller(self.controller)

        self.controller.set_model(self.model)
        
        print("App initialized.")

    def run(self):
        self.view.start()

# Receives user events from view. Manipulates model.
class Controller:
    def __init__(self, sets_configuration):
        self.sets_config = sets_configuration
        self.reset_state()
        print("Controller initialized.")
    
    def reset_state(self):
        self.selected_set = None
        self.card_index = None
        self.session_correct_streak = 0
        self.session_num_correct = 0

    def set_model(self, model):
        self.model_delegate = model
        self.model_delegate.set_sets_list(self.__get_sets_list())
        self.model_delegate.commit_changes()
    
    def __get_sets_list(self):
        set_names = []
        for s in self.sets_config:
            set_names.append(s["name"])
        return set_names
    
    def on_set_select(self, set_name):
        self.reset_state()
        for i in range(len(self.sets_config)):
            if s["name"] == set_name:
                self.selected_set = s
        
        if self.selected_set is None:
            raise Exception(f'Set {set_name} does not exist.')
        
        if len(self.__get_cards()) == 0:
            raise Exception(f'Set {set_name} has no cards.')
        
        self.card_index = self.__get_first_card_index()

        self.model_delegate.set_set_selection(self.selected_set["name"])
        self.model_delegate.set_card_count(len(self.__get_cards()))
        self.model_delegate.set_current_card(self.__get_current_card())
        self.model_delegate.set_session_correct_streak(self.session_correct_streak)
        self.model_delegate.set_session_num_correct(self.session_num_correct)
        self.model_delegate.commit_changes()
    
    def on_guess(self, guess):
        score = correctness_score(preprocess_key(guess), preprocess_key(self.__get_current_card()["key"]))
        if is_guess_correct(score):
            self.model_delegate.set_previous_guess_correct(True)
            self.session_correct_streak += 1
            self.session_num_correct+= 1
        else:
            self.model_delegate.set_previous_guess_correct(False)
            self.session_correct_streak = 0

        self.__go_to_next_card()
        self.model_delegate.set_current_card(self.__get_current_card())

    # TODO(jsnl): Implement shuffle in these two functions.
    def __go_to_next_card(self):
        self.card_index += 1
        if self.card_index >= len(self.__get_cards()):
            self.__reset_session()
    
    def __get_first_card_index(self):
        return 0

    def __reset_session(self): 
        self.card_index = self.__get_first_card_index()
        self.session_correct_streak = 0
        self.session_num_correct = 0
        self.model_delegate.set_session_correct_streak(self.session_correct_streak)
        self.model_delegate.session_num_correct(self.session_num_correct)

    def __get_current_card(self):
        return self.__get_current_card()
    
    def __get_cards(self):
        return self.selected_set["cards"]

def is_set_in_config(set_name, config):
    return reduce(lambda accum, curr: accum or curr["name"] == set_name, config, False)

# TODO(jsnl): Design the application starting from the model. Consider:
#
#     1. "on_correct_guess" / "on_incorrect_guess"
#     2. Displaying correctness score.
#     3. Tracking correctness streak.
#     4. Tracking number correct in set.
#     5. Need some concept of a "session" (i.e. one play thru of cards)
#     6. Need card shuffling mechanic.
#     7. Need set selection functionality.

# On change, notifies view.
class Model:
    def __init__(self):
        self.set_selection = None
        self.sets_list = []
    
        self.cards_count = 0
        self.current_card = None

        self.session_num_correct = 0
        self.session_correct_streak = 0
        self.previous_guess_correct = None

        print("Model initialized.")
    
    ''' Delegate interfaces ''' 
    def set_controller(self, controller):
        self.controller_delegate = controller
    
    def set_view(self, view):
        self.view_delegate = view
    
    ''' Model manipulation '''
    def commit_changes(self):
        self.view_delegate.rerender()

    def set_current_card(self, card):
        self.current_card = card
    
    def set_card_count(self, num_cards):
        self.cards_count = num_cards
    
    def set_sets_list(self, set_names):
        self.sets_list = set_names
    
    def set_set_selection(self, selected_set):
        self.set_selection = selected_set
    
    def set_session_num_correct(self, num_correct):
        self.session_num_correct = num_correct

    def set_session_correct_streak(self, correct_streak):
        self.session_correct_streak = correct_streak
    
    def set_previous_guess_correct(self, is_correct):
        self.previous_guess_correct = is_correct
    
    ''' Model retrieval '''
    def get_current_card(self):
        return self.current_card
    
    def get_card_count(self):
        return self.cards_count
    
    def get_sets_list(self):
        return self.sets_list
    
    def get_set_selection(self):
        return self.set_selection
    
    def get_session_num_correct(self):
        return self.session_num_correct

    def get_session_correct_streak(self):
        return self.session_correct_streak
    
    def get_previous_guess_correct(self):
        return self.previous_guess_correct

# Pulls data from model. Receives user events and pushes to Controller.
class View:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title(WINDOW_TITLE)
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
        
        print("View starting.")
        self.window.mainloop()

    def rerender(self):
        print("Re-rendering view.")
        self.__build_view(self.__pull_model_configuration())
        self.window.update()
    
    def __build_view(self, configuration = None):
        # Set image layout

        # Create textbox

        # Create submit button

        # TODO(jsnl): this
        pass

    def __pull_model_configuration(self):
        return {
            "current_card" : self.model_delegate.get_current_card(),
            "card_count" : self.model_delegate.get_card_count(),
            "sets_list" : self.model_delegate.get_sets_list(),
            "set_selection" : self.model_delegate.get_set_selection(),
            "session_num_correct" : self.model_delegate.get_session_num_correct(),
            "session_correct_streak" : self.model_delegate.get_session_correct_streak()
        }

def preprocess_key(k):
    return k.lower()

def is_guess_correct(score):
    return score >= LEVENSHTEIN_THRESHOLD

def correctness_score(guess, answer):
    distance = levenshtein(guess, answer)
    return (len(answer) - distance) / len(answer)

class Memoize:
    def __init__(self, func):
        self.func = func
        self.memo = {}
    
    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.func(*args)
        return self.memo[args]

@Memoize
def levenshtein(a, b):
    if len(a) == 0:
        return len(b)
    
    if len(b) == 0:
        return len(a)

    if head(a) == head(b):
        return levenshtein(tail(a), tail(b))

    results = []

    results.append(levenshtein(a, tail(b)))
    results.append(levenshtein(tail(a), b))
    results.append(levenshtein(tail(a), tail(b)))

    return 1 + min(results)

def tail(string):
    return string[1:]

def head(string):
    return string[0]
