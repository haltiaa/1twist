import pandas as pd


class AI:
    def __init__(self, user: User):
        self.user = user
    
    def evaluate_problem(self, problem: List):
        return self.user.evaluate(problem)

    def update_from_query(self, problem, choice):
        '''
        This function updates the user model based on a problem and choice. 
        
        To be used in the intial learning process 
        '''
        self.user.update(problem, choice)

    def update_from_prompt(self, problem, choice, switch):
        '''
        This is used to update the user model during the evaluation process.
        It takes a problem, which has been presented to the user, a choice, and whether the user switched to another chocie if prompted to do so
        '''
    

class User:
    pass


class Dataset:
    def __init__(self, dataset_path="./choices13k"):
        self.dataset_path = dataset_path
        self._load()

    def _load(self):
        self.problems = pd.read_json(f"{self.dataset_path}/c13k_problems.json", orient='index')
        self.choices = pd.read_csv(f"{self.dataset_path}/c13k_selections.csv")
        self.choices.set_index("Problem")

        self.data = self.problems.join(self.choices)

    def __getitem__(self, item):
        return self.data.loc[item]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        for p in self.problems.index:
            yield self[p]
