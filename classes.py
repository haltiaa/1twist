

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
    pass

























