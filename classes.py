import pandas as pd


class AI:
    pass



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
