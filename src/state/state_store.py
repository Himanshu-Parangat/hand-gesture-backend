import shelve
import os.path


class StateManager:
    def __init__(self, path):
        self.possible_state = ["ideal", "start", "stop", "terminate"] 
        self.default_state = "ideal"
        self.db_path = path
        self._initialize_db()

    def _initialize_db(self):
        if not os.path.exists(self.db_path):
            with shelve.open(self.db_path, 'c') as state_db:
                state_db['state'] = self.default_state


    def set_state(self, state):
        if state not in self.possible_state:
               raise ValueError(f"Invalid state: {state}. possible states are: {', '.join(self.possible_state)}")

        with shelve.open(self.db_path, 'w') as state_db:
            state_db['state'] = state


    def get_state(self):
        with shelve.open(self.db_path, 'r') as state_db:
            return state_db.get('state', 'ideal')


    def reset_state(self):
        with shelve.open(self.db_path, 'w') as state_db:
            state_db['state'] = "ideal"


def main():
    statemanager = StateManager("state.db")
    cur_state = statemanager.set_state("start")
    cur_state = statemanager.get_state()
    print(cur_state)

if __name__ == "__main__":
    main()

from src.configuration import model_handlers

import pprint

pprint.pprint(model_handlers)

# class StateController:
#
#     def state_fetch(self,state):
#
#         if state["backend"] == "start": 
#             module_state: dict = {
#                 "endpoints" : True,
#                 "tracking" : True,
#                 "websocket" : True,
#             } 
#             return module_state 
#
#         elif state["backend"] == "stop": 
#             module_state: dict = {
#                 "endpoints" : True,
#                 "tracking" : False,
#                 "websocket" : False,
#             } 
#             return module_state 
#
#         elif state["backend"] == "ideal":
#             module_state: dict = {
#                 "endpoints" : True,
#                 "tracking" : False,
#                 "websocket" : False,
#             } 
#             return module_state 
#
#         else:
#             module_state: dict = {
#                 "endpoints" : False,
#                 "tracking" : False,
#                 "websocket" : False,
#             } 
#             return module_state 
