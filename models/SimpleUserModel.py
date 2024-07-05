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
    CLASS DOCSTRING HERE

    Inputs:
        >  TO-DO

    Returns:
        >  TO-DO
    """

    ##  List of lists
    ##  "A" -> [[pH, Ha], [pL, La]]
    ##  "B" -> [[pH, Hb], [pL, Lb]]
    df_column_name_A = "A"
    df_column_name_B = "B"

    def __init__(
            self,
            use_bias   : bool       = True,
            build_model: bool       = True,
            load_model : str | None = None,
        ) -> None :
        """
        Constuct instance of SimpleUserModel class

        Inputs:
            >  TO-DO

        Returns:
            >  TO-DO
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


    def build(
            self,
            name:str            = "SimpleUserModel keras model",
            learning_rate:float = 0.001,
        ) -> tf.keras.Model :
        """
        Build a new tf keras model; if one exists, it becomes re-initialised
        """
        ##  Input layer
        x_in = tf.keras.layers.Input((4,))

        ##  Linear transformation
        x = tf.keras.layers.Dense(1, activation="sigmoid")(x_in)

        ##  Create model
        model = tf.keras.models.Model(x_in, x, name=name)

        ##  Create optimiser
        optimizer = tf.keras.optimizers.AdamW(learning_rate=learning_rate)

        ##  Compile model
        model.compile(
            optimizer = optimizer,
            loss      = "binary_crossentropy",
            metrics   = "accuracy",
        )

        ##  Store model
        self.model = model

        ##  Return model
        return model
    

    def _pipeline_df_to_aray(self, df: pd.DataFrame) -> np.ndarray :
        """
        """
        ##  Extract A and B from table
        A = df[self.df_column_name_A]
        B = df[self.df_column_name_B]

        ##  Extract rewards and probabilities for option A
        p_Ha = np.array([item[0][0] for item in A])
        Ha   = np.array([item[0][1] for item in A])
        p_La = np.array([item[1][0] for item in A])
        La   = np.array([item[1][1] for item in A])

        ##  Calculate mean and std for option A
        mean_a = p_Ha*Ha + p_La*La
        std_a  = np.sqrt(p_Ha*np.power(Ha - mean_a, 2) + p_La*np.power(La - mean_a, 2))

        ##  Extract rewards and probabilities for option B
        p_Hb = np.array([item[0][0] for item in B])
        Hb   = np.array([item[0][1] for item in B])
        p_Lb = np.array([item[1][0] for item in B])
        Lb   = np.array([item[1][1] for item in B])

        ##  Calculate mean and std for option B
        mean_b = p_Hb*Hb + p_Lb*Lb
        std_b  = np.sqrt(p_Hb*np.power(Hb - mean_b, 2) + p_Lb*np.power(Lb - mean_b, 2))

        ##  Create array
        X = np.array([mean_a, std_a, mean_b, std_b]).transpose()

        ##  return array
        return X


    def generate_action_by_sampling(self, X: pd.DataFrame) -> np.ndarray :
        """
        Sample predicted probabilities for table of A/B decisions
        Return shape [N] for N tests
        """
        raise NotImplementedError()


    def generate_action_by_argmax(self, X: pd.DataFrame) -> np.ndarray :
        """
        Return argmax over predicted probabilities for table of A/B decisions
        Return shape [N] for N tests
        """
        ##  Get probs
        Y = self._pipeline_df_to_tensor(X)

        ##  Generate action using argmax
        A = np.where(Y > 0.5, 0, 1)

        ##  Return action
        return A


    def fit(
            self,
            X: pd.DataFrame,
            Y: list,    ## List of decisions, 0 for A, 1 for B
            **kwargs,
        ) -> tf.keras.models.Model :
        """
        Fit the internal keras model to the given data
        """

        ##  Cast df to trainable tensor
        X = self._pipeline_df_to_aray(X)

        ##  Create training callbacks
        callbacks = []
        if kwargs.get("early_stopping", True) :
            callbacks.append(
                tf.keras.callbacks.EarlyStopping(
                    restore_best_weights = True, 
                    patience             = 3,
                    monitor              = "val_loss",
                )
            )

        ##  Fit model
        self.model.fit(
            X,
            Y,
            validation_split = kwargs.get("validation_split", 0.3),
            epochs           = kwargs.get("epochs"          , 100),
            callbacks        = callbacks,
        )

        ##  Return model
        return self.model


    def load(self, kerasname:str) -> None :
        """
        Load a new tf keras model from keras file
        """
        raise NotImplementedError()


    def predict_logits(self, df:pd.DataFrame) -> np.ndarray :
        """
        Generate predicted logits for table of A/B decisions
        Return shape [N x 2] for N tests
        """
        raise NotImplementedError()


    def predict_probs(self, df:pd.DataFrame) -> np.ndarray :
        """
        Generate predictions for table of A/B decisions
        Return shape [N x 2] for N tests
        """
        raise NotImplementedError()


    def save(self, kerasname:str) -> None :
        """
        Save tf keras model to keras file
        """
        raise NotImplementedError()