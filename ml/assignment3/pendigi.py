from svm import *
from svmutil import *

import numpy as np
from sklearn.preprocessing import StandardScaler

M = 10
sigma = 0.6

#gamma = (1.0 / (2.0 * sigma * sigma))
gamma = sigma
def filter_set_wta(x, y, lbl):
	new_y = []
	for s in y:
		if s != lbl:
			new_y.append(-1)
		else:
			new_y.append(1)
	return x, new_y

def filter_set_mwv(x, y, lbl1, lbl2):
	new_x = []
	new_y = []
	for i in xrange(len(x)):
		if y[i] == lbl1:
			new_y.append(1)
			new_x.append(x[i])
		elif y[i] == lbl2:
			new_y.append(-1)
			new_x.append(x[i])
	return new_x, new_y

def get_pred_wta(classif_idx, y_train, x_train, y_test, x_test):
	x_train, y_train = filter_set_wta(x_train, y_train, classif_idx)
	m = svm_train(y_train, x_train, '-q -t 1 -g ' +  str(gamma))
	return svm_predict(y_test, x_test, m)[0]

def get_pred_mwv(lbl1, lbl2, y_train, x_train, y_test, x_test):
	x_train, y_train = filter_set_mwv(x_train, y_train, lbl1, lbl2)
	m = svm_train(y_train, x_train, '-q -t 1 -g ' +  str(gamma))
	return svm_predict(y_test, x_test, m)[0]

def predict_wta(pred_vect, i):
	mmax = float('-Inf')
	imax = None
	for classif_idx in pred_vect:
		p = pred_vect[classif_idx][i]
		if p > mmax:
			mmax = p
			imax = classif_idx
	return imax

def predict_mwv(pred_vect, k):
	votes = {}
	for lbl1, lbl2 in pred_vect:
		p = pred_vect[(lbl1, lbl2)][k]
		if lbl1 not in votes:
			votes[lbl1] = 0
		if lbl2 not in votes:
			votes[lbl2] = 0
		votes[lbl1] += 1 if p >= 0 else -1
		votes[lbl2] += -1 if p >= 0 else 1

	return max(votes.iterkeys(), key=(lambda x: votes[x]))

def get_accuracy_wta(pred_vectors, y_test):
	good = 0
	for i in xrange(len(y_test)):
		if y_test[i] == predict_wta(pred_vectors, i):
			good += 1
	return good * 1.0 / len(y_test)

def get_accuracy_mwv(pred_vectors, y_test):
	good = 0
	for i in xrange(len(y_test)):
		if y_test[i] == predict_mwv(pred_vectors, i):
			good += 1
	return good * 1.0 / len(y_test)


def scale(x):
	for s in x:
		for i in s:
			s[i] /= 100.0


def main():

	y_test, x_test = svm_read_problem('../../pendigits.t')
	y_train, x_train = svm_read_problem('../../pendigits.txt')

	scale(x_test)
	scale(x_train)
	
	# WTA_SVM
	pred_vectors_wta = {}
	for classif_idx in range(M):
		pred_vectors_wta[classif_idx] = get_pred_wta(classif_idx, y_train, x_train, y_test, x_test)

	print "\n\n"
	# MWV_SVM
	pred_vectors_mwv = {}
	for i in xrange(M-1):
		for j in xrange(1, M-i):
			lbl1 = i
			lbl2 = i + j
			pred_vectors_mwv[(lbl1, lbl2)] = get_pred_mwv(lbl1, lbl2, y_train, x_train, y_test, x_test)

	print sigma
	print "WTA_acc = " + str(get_accuracy_wta(pred_vectors_wta, y_test))
	print "MWV_acc = " + str(get_accuracy_mwv(pred_vectors_mwv, y_test))




if __name__ == "__main__":
	main()