################## Imports section ###################
# -*- coding: cp1252 -*-
import numpy as np
import matplotlib.pyplot as plt
import random

from sklearn.datasets import fetch_mldata
mnist = fetch_mldata('MNIST original')

from sklearn.model_selection import train_test_split

################ Load Data section ##################
def load_MNIST_Data():
    train_img, test_img, train_lbl, test_lbl = train_test_split(mnist.data, mnist.target, test_size=1/7.0, random_state=0)
    return train_img, train_lbl, test_img, test_lbl

################# Neural section ####################


class Neural_Network(object):
    def __init__(self):
        self.inputSize = 784                #Im�genes de 28x28 
        self.outputSize = 10                #n�meros del 0 al 9
        self.hiddenSize1 = 512              #Primera capa de 512
        self.hiddenSize2 = 128              #Segunda capa de 128

        #inicializo el W con pesos aleatorios 
        self.W1 = np.random.randn(self.inputSize, self.hiddenSize1)     # (784, 512) entrada
        self.W2 = np.random.randn(self.hiddenSize1, self.hiddenSize2)   # (512, 128) primera capa
        self.W3 = np.random.randn(self.hiddenSize2, self.outputSize)    # (128, 10)  segunda capa
        
    def forward(self, X):
        self.z = np.dot(X, self.W1)
        self.z2 = self.relu(self.z)                     # activation function capa 1
        self.z3 = np.dot(self.z2,self.W2) 
        self.z4 = self.relu(self.z3)                    # activation function capa 2
        self.z5 = np.dot(self.z4,self.W3)
        output = self.relu(self.z5)                     # final activation function
            
        print(output.shape)
        return output 

    def relu(self,x):
        return np.maximum(x, 0, x)

    
    #https://deepnotes.io/softmax-crossentropy
    def softmax(self, X):
        exps = np.exp(X)                      #calcula cada e**Xi (de cada elemento de la matriz)
        return exps / np.sum(exps)

    def cross_entropy(self,X,y):
        """
        X is the output from fully connected layer (num_examples x num_classes)
        y is labels (num_examples x 1)
        """
        m = y.shape[0]
        p = self.softmax(X)
        log_likelihood = -np.log(p)#[range(m),y])
        loss = np.sum(log_likelihood) / m
        return loss


    #Aun no funciona
    '''def cross_entropy(predictions, targets, epsilon=1e-12):
        """
        Computes cross entropy between targets (encoded as one-hot vectors)
        and predictions. 
        Input: predictions (N, k) ndarray
               targets (N, k) ndarray        
        Returns: scalar
        """
        predictions = np.clip(predictions, epsilon, 1. - epsilon)
        N = predictions.shape[0]
        ce = -np.sum(np.sum(targets*np.log(predictions+1e-9)))/N
        return ce
    '''
    
#As� llaman a cross entropy loss en el ejemplo que encontre
"""
predictions = np.array([[0.25,0.25,0.25,0.25],
                        [0.01,0.01,0.01,0.96]])
targets = np.array([[0,0,0,1],
                   [0,0,0,1]])
ans = 0.71355817782  #Correct answer
x = cross_entropy(predictions, targets)
print(np.isclose(x,ans))
"""


def Train():
    cantTrain = 35          #N�mero de im�genes del train que se usar�n como test
    
    data = load_MNIST_Data()
    train_X = data[0]       #imagenes de entrenamiento (60000)
    train_Y = data[1]       #Labeld de entrenamiento (60000)

    test_X = data[2]        #Imagenes de prueba (10000)
    test_Y = data[3]        #Labels de prueba (10000)

    testRandom = random.sample(range(len(train_X)),cantTrain) #toma los �ndices aleatoriamente para las im�genes de testing
    X = [train_X[i] for i in testRandom]                      #Datos de testing con los �ndices anteriores
    Y = [train_Y[i] for i in testRandom]                      #labels de los datos anteriores

    #print X

    Y_vectorizado = np.zeros((len(Y), 10))       #Creacion de labels vectorizados para mandarlos a cross-entropy (10 columnas->10 clases)
    #One Hot Encoding
    for i in range(len(Y)):                     
        Y_vectorizado[i][int(Y[i])] = 1                 #Se pone 1.0 en la posicion del vector

    NN = Neural_Network()
    output = NN.forward(X)
    
    #print Y_vectorizado

    output = output/np.amax(output, axis=0)
    #print "Predicted Output: \n" + str(output) 
    #print "Actual Output: \n" + str(Y) 


    #No funciona aun

    output = output/np.amax(output, axis=0)
    ce = NN.cross_entropy(output, Y_vectorizado)
    print ce

    
Train()
