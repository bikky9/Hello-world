import numpy as np
import matplotlib.pyplot as plt
import math


def fit_gmm(data,K=3,max_iter = 30):

    def init(X,K):
        # can change the init
        _,n = X.shape
        
        a = np.full((K),1/K)
        mu = [X[i] for i in range(K)]
        mu = np.array(mu)
        sigma = np.zeros((n,n))
        for i in range(n):
            sigma[i,i] = 1
        
        Sigma = [sigma for i in range(K)]
        return a,mu,Sigma

    def gaussian(x,mean,cov):

        ''' return gaussian at x '''
        # print(cov)
        n = x.shape[0]
        return np.exp(-((x - mean) . T @ np.linalg.inv(cov) @ (x - mean))/2)/np.sqrt((2*np.pi)**n * np.linalg.det(cov))

    def GMM(data,K,iter_num = 1):
        # fit the data by completing 
        # Refer to tutorial 6
        # can change the code to terminate under log-likelihood convergence
        
        m,_ = data.shape
        a,mu,sigma = init(data,K)
        # a is the weights of gaussians in MM
        # mu is the array of mean
        # sigma is the array of variance
        posterior = np.zeros((m,K))
        # vfunc = np.vectorize(gaussian,signature='(n),(n),(n,n)->()')
        for _ in range(iter_num):

            # E_step
            ''' write code for E-step here , '''
            for j in range(K):
                for i in range(m):
                    gaussians = gaussian(data[i,:],mu[j],sigma[j])
                    posterior[i,j] = a[j] * gaussians
            for i in range(m):
                posterior[i,:] /= np.sum(posterior,axis=1)[i]
            # posterior /= np.sum(posterior,axis = 0)
            # M_step
            ''' write code for M-step here '''
            a = np.mean(posterior,axis=0)
            mu = posterior . T @ data
            for i in range(K):
                mu[i] /= np.sum(posterior,axis=0)[i]
            # for i in range(K):
            #     sigma[i] = np.multiply(np.subtract(data,mu[i]),np.reshape(posterior[:,i],(-1,1))) . T @ np.subtract(data,mu[i])
            #     sigma[i] /= np.sum(posterior, axis=0)[i]

            for i in range(K):
                sigma[i] = 0
                for j in range(m):
                    sigma[i] += posterior[j, i] * np.reshape((data[j] - mu[i]), (-1, 1)) @ np.reshape((data[j] - mu[i]), (-1, 1)) . T
                    # sigma[i] = (np.multiply(np.subtract(data,mu[i]),np.reshape(posterior[:,i],(-1,1))) @ np.subtract(data,mu[i]) . T)/np.sum(posterior,axis=0)[i]
                sigma[i] /= np.sum(posterior, axis=0)[i]


            for i in range(K):
                plt.plot(mu[i][0],mu[i][1],'o',c = 'r')
        
        return a,mu,sigma


    a,mu,sigma = GMM(data,K,max_iter)
    print(a)
    print(mu)
    print(sigma)

    num = 200
    l = np.linspace(0,15,num)
    X, Y = np.meshgrid(l, l)

    plt_data = np.dstack((X,Y))
    for i in range(K):
        Z = [[gaussian(plt_data[k][j],mu[i],sigma[i]) for j in range(num)] for k in range(num)]
        cs = plt.contour(X,Y,Z)
        plt.clabel(cs)
    plt.show()
