##
##  SimpleUserModel.py
##  Brief:  Implement our baseline user model, which is a logistic regression over [muA, sigmaA, muB, sigmaB]
##  Initial commit:  5th July 24
##
'''
Overview:

We implement a class that performs a simple analysis R^4 -> R[0,1]
'''

import logging

import numpy      as np
import pandas     as pd
import tensorflow as tf

##  Get module-level logger
logger = logging.getLogger("models.SimpleUserModel.py")


class SimpleUserModel :
    """
    """

    def __init__(
            use_bias   : bool       = True,
            build_model: bool       = True,
            load_model : str | None = None,
        ) -> None :
        """
        """
        ##  Log construction of class
        logging.debug(
            f"Constructing SimpleUserModel class with parameters use_bias={use_bias}, \
            build_model={build_model}, load_model={load_model}"
        )

        ##  Set params
        self.use_bias = use_bias
        self.model    = None

        ##  Construct model if requested
        if build_model :
            self.build()

        ##  Load model if requested
        if load_model :
            self.load(load_model)


    def build() -> tf.keras.Model :
        """
        Build a new tf keras model. If one exists, it becomes re-initialised
        """
        raise NotImplementedError()


    def generate_action_by_sampling(df: pd.DataFrame) -> np.ndarray :
        """
        Sample predicted probabilities for table of A/B decisions
        Return shape [N] for N tests
        """
        raise NotImplementedError()


    def generate_action_by_argmax(df: pd.DataFrame) -> np.ndarray :
        """
        Return argmax over predicted probabilities for table of A/B decisions
        Return shape [N] for N tests
        """
        raise NotImplementedError()


    def fit(
            fit_data: pd.DataFrame,
            **kwargs,
        ) -> None :
        """
        Fit the internal keras model to the given data
        """
        raise NotImplementedError()


    def load(kerasname:str) -> None :
        """
        Load a new tf keras model from keras file
        """
        raise NotImplementedError()


    def predict_logits(df:pd.DataFrame) -> np.ndarray :
        """
        Generate predicted logits for table of A/B decisions
        Return shape [N x 2] for N tests
        """
        raise NotImplementedError()


    def predict_probs(df:pd.DataFrame) -> np.ndarray :
        """
        Generate predictions for table of A/B decisions
        Return shape [N x 2] for N tests
        """
        raise NotImplementedError()


    def save(kerasname:str) -> None :
        """
        Save tf keras model to keras file
        """
        raise NotImplementedError()