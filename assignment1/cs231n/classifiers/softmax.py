from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange


def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    num_classes = W.shape[1]
    num_examples = X.shape[0]
    scores = np.dot(X, W) #score.shape : (N, C)
    
    # Softmax loss
    
    for i in range (num_examples):
      f = scores[i] 
      f = f - np.max(f) # to avoid blowup, add numerical stability
      probs = np.exp(f)/np.sum(np.exp(f))
      loss += -np.log(probs[y[i]])

      # Weight의 gradient
      for j in range(num_classes):
        if j == y[i]:
          dW[:, y[i]] += X[i]*(probs[j]-1)
        else:
          dW[:, j] += X[i]*probs[j]

    loss /= num_examples
    dW /= num_examples
    # Regularization
    loss += reg*np.sum(W*W)
    dW += 2*reg*W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    num_examples = X.shape[0] # X_dev(500, 3073) --> 500
    num_classes = W.shape[1] # W(3073, 10) --> 10

    score_matrix = np.dot(X, W) # 500, 10 
    score_matrix -= np.max(score_matrix, axis = 1, keepdims = True)

    # loss 계산

    nominator = np.exp(score_matrix) # 500, 10
    denominator = np.sum(np.exp(score_matrix), axis=1, keepdims = True) # 500, 1
    softmax_matrix = nominator / denominator # 500, 10
    softmax_matrix_correct = softmax_matrix[np.arange(num_examples), y]
    loss = np.sum(-np.log(softmax_matrix_correct))

    # dW 계산
    softmax_matrix[np.arange(num_examples), y] -= 1
    dW += np.dot(X.T, softmax_matrix)
    
    loss /= num_examples
    dW /= num_examples

    loss += 2*reg*np.sum(W*W)
    dW += reg*W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
