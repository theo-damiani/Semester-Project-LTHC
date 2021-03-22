import torch
import tensorflow as tf
import numpy as np

#Size of the matrix Y
N = 10
M = N
dim = 1

#
lambda_ = 1

#temperatures
beta_u = 1
beta_v = beta_u

#learning rates
lambda_1 = 1
lambda_2 = lambda_1


# genere un vecteur sur l'hypersphere
def generate_vector(d):
    x = torch.normal(0, 1, size=(1, d)).float()
    x = x / torch.linalg.norm(x)
    x = x * torch.sqrt(torch.tensor(d).float())
    return x

# calcul l'overlap entre deux tenseurs.
def overlap(x_etoile, x,d):
    return torch.dot(x_etoile, x)/d


def generate_Y(u_,v_): 
	n = list(u_.shape)[1]
	m = list(v_.shape)[1]
	uv = torch.mm(torch.transpose(u_,0,1),v_)
	eta = torch.normal(0, 1, size=(n, m))
	return uv + np.sqrt(n/lambda_)*eta
	
def gradient_v_1(u_,v_,Y):
	n = list(u_.shape)[1]
	m = list(v_.shape)[1]
	x = []
	for d in range(m):
		sum = 0
		for i in range(n):
			sum += u_[i]*(Y[i][d].item()-u_[i]*v_[d])
		x.append(-2/(n*m)*sum)
	return torch.tensor(x)
	
def gradient_u_1(u_,v_,Y):
	n = list(u_.shape)[1]
	m = list(v_.shape)[1]
	x = []
	for d in range(n):
		sum = 0
		for i in range(m):
			sum += v_[i]*(Y[d][i].item()-u_[d]*v_[i])
		x.append(-2/(n*m)*sum)
	return torch.tensor(x)	
	

def gradient_v_2(u_,v_,Y):
	n = list(u_.shape)[1]
	m = list(v_.shape)[1]
	x = []
	for d in range(m):
		sum = 0
		for i in range(n):
			sum += u_[i]*(Y[i][d].item()-np.sqrt(lambda_/n)*u_[i]*v_[d])
		x.append(-np.sqrt(lambda_/m)*sum)
	return torch.tensor(x)
	
def gradient_u_2(u_,v_,Y):
	n = list(u_.shape)[1]
	m = list(v_.shape)[1]
	x = []
	for d in range(n):
		sum = 0
		for i in range(m):
			sum += v_[i]*(Y[d][i].item()-np.sqrt(lambda_/n)*u_[d]*v_[i])
		x.append(-np.sqrt(lambda_/n)*sum)
	return torch.tensor(x)	
	