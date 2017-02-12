"""
A simple wrapper for RT
"""

import numpy as np
import random as rd

class RTLearner(object):

    def __init__(self, leaf_size=1, verbose = False):
        self.verbose=verbose
        self.leaf_size=leaf_size
        pass # move along, these aren't the drones you're looking for


    def addEvidence(self, X, Y):
        def built_tree(dataX, dataY):
            leaf=-1000
            if dataX.shape[0]<=self.leaf_size: #checks if the data points in a branch has equal or less than the leaf size
                self.tree=np.array([[leaf, np.mean(dataY), np.nan, np.nan]]) #average the Y's  of data points in a leaf
                return self.tree
            elif len(set(dataY))==1:
                self.tree=np.array([[leaf,np.mean(dataY), np.nan, np.nan]]) #checks if all the Y values are the same, then just return Y
                return self.tree
            else:
                randomList=rd.sample(xrange(0,dataX.shape[1]), dataX.shape[1]) #randomly order the features in a list           
                i=randomList[0] # select the first feature in the list to split on
                z=1
                while len(set(dataX[:,i]))==1 and z<=dataX.shape[1]: # check if the feature has any information, if all data points in that feature is the same pick another feature
                    i=randomList[z]
                    z=z+1
                if len(set(dataX[:,i]))==1: # if selected feature has all the same values then make it a leaf and return the mean of the data points
                    return [[leaf,np.mean(dataY), np.nan, np.nan]]
                else:                    
                    SplitVal=np.mean(np.random.choice(dataX[:,i], size=2, replace=False)) # if selected feature has information, find two data points to split on
                    while SplitVal==np.amax(dataX[:,i]): # if split value is greater than all data points you need to select another split value to prevent the right branch from eing blank
                        SplitVal=np.mean(np.random.choice(dataX[:,i], size=2, replace=False))
                    a=dataX[:,i]<=SplitVal  # data on the left
                    leftTree=built_tree(dataX[a], dataY[a])  #recursively build the left tree     
                    rightTree=built_tree(dataX[~a], dataY[~a]) #recursively build the right tree
                    root=[[i, SplitVal,1,len(leftTree)+1]]
                    self.tree=np.concatenate((root, leftTree, rightTree), axis=0)
                    return  self.tree
        return built_tree(X,Y)
    
      
    def query(self,points):
        i=0
        results=np.zeros(points.shape[0])
        which_child=np.zeros(points.shape[0])
        while i<self.tree.shape[0]:
            if self.tree[i,0]!=-1000:
                ind=np.array(np.where(which_child==i))
                branch_direction=np.array(points[ind,int(self.tree[i,0])]<=self.tree[i,1])
                ind_left=ind[np.where(branch_direction==True)]
                ind_right=ind[np.where(branch_direction==False)]
                which_child[ind_left]=1+i
                which_child[ind_right]=self.tree[i,3]+i
            else:
                results[np.where(which_child==i)]=self.tree[i,1]
            i=i+1
        return results
            
#if __name__=="__main__":
#    print "the secret clue is 'zzyzx'"
