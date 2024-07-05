from typing import List

import numpy as np
import pandas as pd

from models.SimpleUserModel import SimpleUserModel as User

class AI:
    def __init__(self, user: User):
        self.user = user
    
    def evaluate_problem(self, problem: list):
        '''
        returns 0 for choice A or 1 for choice B
        '''
        data = pd.DataFrame({'A' : problem[0], 'B' : problem[1]})
        return self.user.generate_action_by_argmax(data)
    
    def update_from_query(self, problem: pd.DataFrame, choice: list):
        '''
        This function updates the user model based on a problem and choice. 
        
        To be used in the intial learning process 
        '''
        data = pd.DataFrame({'A' : problem[0], 'B' : problem[1]})
        self.user.fit(data, choice)

    def update_from_prompt(self, problem, choice, switch):
        '''
        This is used to update the user model during the evaluation process.
        It takes a problem, which has been presented to the user, a choice, and whether the user switched to another chocie if prompted to do so.
        NOT IMPLEMENTED YET.
        '''
        raise NotImplementedError

    







class Dataset:
    def __init__(self, dataset_path="./choices13k"):
        self.dataset_path = dataset_path
        self._load()

    def _load(self):
        self.problems = pd.read_json(f"{self.dataset_path}/c13k_problems.json", orient='index')
        self.choices = pd.read_csv(f"{self.dataset_path}/c13k_selections.csv")
        self.choices.set_index("Problem")

        self.data = self.problems.join(self.choices)
        self.data = self.data[self.data["Amb"] == False]

    def __getitem__(self, item):
        return self.data.loc[item]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        for p in self.data.index:
            yield self[p]

    def get_split(self, train_prop):
        assert train_prop <= 1, "provided train proportion is not in a valid range"

        split_pos = min(round(len(self.data) * train_prop), len(self.data))

        return self.data.iloc[0:split_pos], self.data.iloc[split_pos:]