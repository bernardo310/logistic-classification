""" 
    This script containg utility functions used for logistic classification
    Author : Bernardo Cardenas Domene
    Institution : Universidad de Monterrey
    First Created : 6/April/2020
    Email : bernardo.cardenas@udem.edu
"""

import numpy as np
import math
import sys

def load_data(file, includes_y, split:100, flag):
    """
        Reads data from csv file and returns numpy type array for x data and y data
        inputs: 
            file: string of csv file
            includes_y: if set to 1, csv file must include y column at the end. If set to 0, csv file only contains x data columns
            split: indicates percentage to be used as training data, residual percentage is used for testing data, for example split=80 means 80% of the data will be used for training and 20% for testing
            flag: if flag = 1, the training data is printed. if flag = 0, data is not printed
        output: numpy type arrays x_data and y_data representing the data found in file

    """
    #read data from file
    try:
        headers = np.genfromtxt(file, delimiter=',', max_rows=1)
        data = np.genfromtxt(file, delimiter=',', skip_header=1)
    except:
        print('File not found:', file)
        sys.exit()
    
    #shuffle data order
    np.random.shuffle(data)

    if(includes_y):
        #separate data into x and y. (y is assumed to be last column in csv file)
        number_x_columns = len(headers) - 1
        #get splitting point to divide data 
        splitting_point = math.floor(len(data) * (split / 100))
        #get training data from data
        x_training_data = data[:splitting_point, :number_x_columns]
        y_training_data = data[:splitting_point, number_x_columns:]
        #get testing data from data
        x_testing_data = data[splitting_point:, :number_x_columns]
        y_testing_data = data[splitting_point:, number_x_columns:]
        #print data if flag is set
        if(flag):
            print('-'*100)
            print('Training Data and Y outputs')
            print('-'*100)
            for i in range(len(data)):
                print(x_training_data[i], y_training_data[i])
            print('\n')
        #return x and y training and testing data
        return x_training_data, y_training_data, x_testing_data, y_testing_data
    else: #doesnt inclyde y column (used for reading testing data)
        return data



def scale_data(data, flag, mean=0, std=0):
    """
        Returns feature scaling applied to data so range in values are -1 >= x <= 1
        input:
            data: numpy type array containing data to be scaled
            flag: if flag = 1, the scaled training data is printed. if flag = 0, data is not printed
            mean: (optional) mean array from training data
            std: (optional) std array from training data
        output: 
            scaled_data: numpy type array containing scaled data
            mean: mean from data
            std: standard deviation from data
    """
    scaled_data = []
    n_columns = len(data[0])
    if(not isinstance(mean, np.ndarray) and not isinstance(std, np.ndarray)):
        mean = []
        std = []
        #calculate mean and standerd deviation
        mean = np.mean(data, axis=0)
        std = np.std(data, axis=0)

        #scale data 
        for i in range(len(data)):
            temp = []
            for j in range(0, n_columns):
                temp.append((data[i][j] - mean[j]) / std[j])
            scaled_data.append(temp)

        #convert to numpy array
        scaled_data = np.array(scaled_data)

        #print data if flag is set
        if(flag):
            print('-'*100)
            print('Scaled Training Data and Y outputs')
            print('-'*100)
            for i in range(len(scaled_data)): print(scaled_data[i])
            print('\n')
        return scaled_data, mean, std
    else:
        #scale testing data 
        for i in range(len(data)):
            temp = []
            for j in range(0, n_columns):
                temp.append((data[i][j] - mean[j]) / std[j])#2
            scaled_data.append(temp)

        #convert to numpy array
        scaled_data = np.array(scaled_data)
        return scaled_data


def eval_hypothesis_function_multivariate(w, x):
    """
    obtains hypothesis function for multivariate linear regression
    input parameter: 
        w: numpy array containing w parameters
        x: numpy type array containing x data
    output: 
        hypothesis: numpy type array containing hypothesis linear function  
    """
    #apply hypothesis function x.*w to logistic function
    hypothesis = 1 / (1 + np.exp(np.matmul(x.T, w) * -1) )
    return hypothesis


def compute_gradient_of_cost_function_multivariate(hypothesis, x, y, n):
    """
    calculates gradient for multivariate linear regression
    input parameter: 
        hypothesis: numpy type array containing hypothesis function 
        x: numpy type array containing x data
        y: numpy type array containing y data
        n: integer representing number of rows in x data
    output: 
        gradient: gredient array
    """ 
    #calculate error
    error = np.subtract(hypothesis, y)  
    #calculate gradient
    gradient = np.matmul(x, error) / n    
    return gradient


def compute_L2_norm_multivariate(gradient):
    """
    calculates L2 norm 
    input parameter: 
        hypothesis: numpy type array containing gradient of cost function
    output: 
        L2: float value for L2 norm
    """     
    #calculate l2 norm (Euclidean norm)
    l2 = np.sqrt(np.sum(gradient**2))
    return l2


def gradient_descent(x, y, w, learning_rate, stopping_criteria):
    """
    obtains optimal w parameters using gradient descent algorithm
    input parameter: 
        x: numpy type array containing x data
        y: numpy type array containing y data 
        w: numpy array where optimal w parameters will be stored
        learning_rate: float learning rate
        stopping_criteria: float stopping criteria
    output: 
        w: numpy type array containing optimal parameters
    """
    #add column of ones to x data. w0 + w1x1 + w2x2 + ... wnxn
    ones = np.ones((len(x), 1))
    x = np.hstack((ones, x))
    x = x.T
    #calculate number of rows
    n = len(y)
    while(1):
        #calculate hypothesis
        hypothesis = eval_hypothesis_function_multivariate(w, x) 
        #calculate gradient
        gradient = compute_gradient_of_cost_function_multivariate(hypothesis, x, y, n) 
        #calculate l2 norm
        l2 = compute_L2_norm_multivariate(gradient) 
        #apply gradient descent alorithm
        w = w - learning_rate * gradient  
        if(l2 < stopping_criteria): #stop if l2 is lower than stopping criteria
            return w  
    return


def predict(x, w):
    """
    predicts y values using w parameters and x testing data
    input parameter: 
        x: numpy type array containing x testing data
        w: numpy type array containing w parameters
    output: 
        predictions: numpy type array containing y predictions (values are 1 or 0)
    """
    #add 1's column to x
    ones = np.ones((len(x), 1))
    x = np.hstack((ones, x))
    #evalutate x testing data with logistic function
    predictions = 1 / (1 + np.exp(np.matmul(x, w) * -1) )
    #asign to positive or negative class
    for i in range(len(predictions)):
        if(predictions[i] >= 0.5):
            predictions[i] = 1
        else:
            predictions[i] = 0

    return predictions


def get_confusion_matrix(predictions, y):
    """
    obtains confusion matrix values using predictions and y testing data
    input parameter: 
        predictions: numpy type array containing predictions
        y: numpy type array containing y testing data
    output: 
        matrix: list containing confusion matrix values
    """
    matrix = [0,0,0,0]
    #iterate predictions and compare with y data
    for i in range(len(predictions)):
        if(predictions[i] == 1 and y[i] == 1): #true positive
            matrix[0] += 1
        elif(predictions[i] == 0 and y[i] == 0): #true negative
            matrix[1] += 1
        elif(predictions[i] == 1 and y[i] == 0): #false positive
            matrix[2] += 1
        elif(predictions[i] == 0 and y[i] == 1): #false negative
            matrix[3] += 1
    return matrix


def print_performance_metrics(m):
    """
    prints confusion matrix and performance metrics using confusion matrix
    input parameter: 
        m: list containing confusion matrix values
    """
    #calculate metrics
    accuracy = (m[0] + m[1]) / (m[0] + m[1] + m[2] + m[3])
    precision = m[0] / (m[0] + m[2])
    recall = m[0] / (m[0] + m[3]) 
    specificity = m[1] / (m[1] + m[2])
    f1 = 2 * ((precision * recall) / (precision + recall))
    #print matrix
    print('-'*120)
    print('Confusion matrix')
    print('-'*120)

    print('|','{0: >36}'.format(""), "|", '{0: >36}'.format("Actual has diabetes (1)"), "|", '{0: >36}'.format("Actual doesn't have diabetes (0)", "|"))
    print('-'*120)
    print('|','{0: >36}'.format("Predicted has diabetes (1)"), "|", '{0: >36}'.format(m[0]), "|", '{0: >36}'.format(m[2]), "|")
    print('-'*120)
    print('|','{0: >36}'.format("Predicted does not have diabetes (0)"), "|", '{0: >36}'.format(m[3]), "|", '{0: >36}'.format(m[1]), "|")
    print('-'*120, '\n')
    #print metrics
    print('\n', '-'*120)
    print('Performance metrics')
    print('-'*120)
    print('Accuracy:', accuracy)
    print('Precision:', precision)
    print('Recall:', recall)
    print('Specificity:', specificity)
    print('F1 Score:', f1)
    return 