import tensorflow as tf
from tensorflow.python.keras import layers


class agent(tf.keras.Model):
    

    def __init__(self, nActions: int, nHiddenUnits:int):

        super().__init__()

        self.common1 = layers.Dense(nHiddenUnits, activation = "relu")
        self.common2 = layers.Dense(round(nHiddenUnits/2,0), activation = "relu")
        self.actor  = layers.Dense(nActions)
        self.critic = layers.Dense(1)

    def call(self, inputs: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        x = self.common1(inputs)
        x = self.common2(x)
        return self.actor(x), self.critic(x)
    
    
