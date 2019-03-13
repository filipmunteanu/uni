from random import random
import math
import sys
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import pylab
from train import eval_nn


def identity(x, derivate = False):
    return x if not derivate else np.ones(x.shape)

def logistic(x, derivate = False):
    if derivate == True:
        return (x * (1 - x))

    if x < -10.0:
        return 0.0
    if x > 10.0:
        return 1.0
    return (1 / ( 1 + np.exp(-x)))

def hyperbolic_tangent(x, derivate = False):
    if derivate == True:
        return (1 - x * x)
    return ((np.exp(2 * x) - 1) / (np.exp(2 * x) + 1))


class CandidNode(object):
    def __init__(self, inp_nodes):
        self.weights = np.array([(random() - 0.5) for _ in range(inp_nodes)])
        self.activations = []
        self.score = 0.0


class CascNet(object):
    def __init__(self, inp_nodes, outp_nodes, function=logistic, num_candid_nodes=3, 
                train_candids_max_epochs=1000, learn_rate=0.01):

        self.learn_rate = learn_rate
        self.train_candids_max_epochs = train_candids_max_epochs
        self.bias_u = 1
        self.w_init_f = lambda: random() - 0.5
        self.function = function
        self.outp_nodes = outp_nodes
        self.inp_nodes = inp_nodes
        self.num_candid_nodes = num_candid_nodes

        self.cscd_conn = []
        self.outp_conn = np.array([[self.w_init_f() for _ in range(inp_nodes + 1)] for _ in range(outp_nodes)])
        
        self.activations = np.zeros(self.inp_nodes+self.bias_u)
        self.outp_activations = np.zeros(self.outp_nodes)
        self.activations[0] = 1.0


    def nr_inp_and_hid(self):
        return self.inp_nodes + len(self.cscd_conn) + self.bias_u


    def forward_hidd_n(self, input):
        for i in xrange(len(input)):
            self.activations[i + self.bias_u] = input[i]

        con_idx = self.inp_nodes + self.bias_u 
        for i in xrange(len(self.cscd_conn)):
            self.activations[i+con_idx] = self.function(np.dot(self.cscd_conn[i], self.activations[:len(self.cscd_conn[i])]))


    def forward(self, input):
        self.forward_hidd_n(input)
        
        for i in xrange(len(self.outp_conn)):
            self.outp_activations[i] = self.function(np.dot(self.outp_conn[i], self.activations[:len(self.outp_conn[i])]))

        return self.outp_activations


    def backprop(self, result, target):
        label = np.zeros(len(result))
        label[target] = 1.0
        outp_errors = np.subtract(result, label)

        for outp in range(len(result)):
            for input in range(self.nr_inp_and_hid()):
                self.outp_conn[outp][input] -= self.learn_rate * outp_errors[outp] * self.activations[input] 


    def train_node(self, input, target):
        result = self.forward(input)
        self.backprop(result, target)

        return np.sum(np.subtract(result, target) ** 2)


    def train_conn(self, inputs, targets, err_threshold=0.05, iter_per_epoch=200):
        no_improv_iter = 0
        prev_tr_error = sys.float_info.max

        for i in xrange(iter_per_epoch):
            if no_improv_iter > 1 or prev_tr_error < err_threshold:
                break

            tr_error = 0.0
            for j in xrange(len(inputs)):
                tr_error += self.train_node(inputs[j], targets[j])

            if tr_error > prev_tr_error:
                no_improv_iter += 1

            prev_tr_error = tr_error

        return tr_error


    def add_hid_n(self, candid_weights):
        self.cscd_conn.append(candid_weights)
        outp_n = [[self.w_init_f()] for x in range(self.outp_nodes)]
        self.activations = np.zeros(self.inp_nodes + self.outp_nodes + len(self.cscd_conn) + self.bias_u)
        self.outp_conn = np.concatenate([self.outp_conn, outp_n], axis=1)
        self.activations[0] = 1.0


    def gen_candid(self, inputs, targets):
        errors = []
        activations = []

        for i in xrange(len(inputs)):
            result = self.forward(inputs[i])
            error = np.subtract(result, targets[i]) ** 2
            errors.append(error)

        err_len = len(errors[0])
        mean_errors = [sum([x[y] for x in errors]) / len(errors) for y in xrange(err_len)]

        candids = [CandidNode(self.nr_inp_and_hid()) for _ in range(self.num_candid_nodes)]

        for input in inputs:
            self.forward_hidd_n(input)
            activations.append(np.copy(self.activations[:self.nr_inp_and_hid()]))

        best_correlation_score = sys.float_info.min

        no_improv_iter = 0
        for epochs in xrange(self.train_candids_max_epochs):
            
            for input in inputs:
                self.forward_hidd_n(input)
                for candid in candids:
                    prod = np.dot(candid.weights, self.activations[:len(candid.weights)])
                    activ = self.function(prod)
                    candid.activations.append(activ)

            for candid in candids:
                vp = sum(candid.activations) / len(candid.activations)
                correlations = np.zeros(err_len)
                for o in xrange(err_len):
                    for p in xrange(len(candid.activations)):
                        correlations[o] += (candid.activations[p] -vp) * (errors[p][o] - mean_errors[o])
                        

                correlation_signs = [math.copysign(1, x) for x in correlations]
                candid.score = sum(correlations)

                derivatives = []
                for i in range(len(candid.weights)):
                    dcdw = sum([(errors[p][o] - mean_errors[o]) * correlation_signs[o] * self.function(candid.activations[p], True) \
                                      * activations[p][i] for p in range(len(errors)) for o in range(len(mean_errors))])
                    derivatives.append(dcdw)

                candid.weights = np.add(candid.weights, -np.multiply(derivatives, self.learn_rate))

            best_candid = max(candids, key=lambda x: x.score)
            last_best = best_correlation_score
            best_correlation_score = best_candid.score

            if best_correlation_score <= last_best:
                no_improv_iter += 1

            if no_improv_iter >= 3:
                break

            for candid in candids:
                candid.activations = []

        return best_candid


    def train_netw(self, data, inputs, targets, err_threshold=sys.float_info.min,
                             max_hid_nodes=10, iter_per_epoch=100): 
        err_sum = self.train_conn(inputs, targets, err_threshold=err_threshold, iter_per_epoch=iter_per_epoch)

        train_acc, train_cm = eval_nn(self, inputs, targets)
        test_acc, test_cm = eval_nn(self, data["test_imgs"], data["test_labels"], 2000)
        print("Train acc: %2.6f ; Test acc: %2.6f" % (train_acc, test_acc))
        print ""

        while err_sum > err_threshold and len(self.cscd_conn) < max_hid_nodes:
            winning_candid = self.gen_candid(inputs, targets)
            self.add_hid_n(winning_candid.weights)

            err_sum = self.train_conn(inputs, targets, iter_per_epoch=iter_per_epoch)

            # Evaluate the network
            train_acc, train_cm = eval_nn(self, inputs, targets)
            test_acc, test_cm =  eval_nn(self, data["test_imgs"], data["test_labels"], 2000)
            print("Train acc: %2.6f ; Test acc: %2.6f" % (train_acc, test_acc))
            print ""
            pylab.imshow(test_cm, interpolation='none', cmap='viridis')
            pylab.draw()
            matplotlib.pyplot.pause(0.001)

        return err_sum