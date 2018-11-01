import numpy as np

def return_range(cutoff):
    '''
    Generates range out of an array.
    ex)
    input : array(0, 0.2, 0.4, 0.6, 0.8, 1.0)
    return : (0, 0.2), (0.2, 0.4) <generator object>    
    '''
    for i in range(len(cutoff)-1):
        if cutoff[i+1] <= 1.0:
            yield (cutoff[i], cutoff[i+1])
            
            
def divide_by_percent(pct_number, n_div):
    
    '''
    params
    ======
    pct_number : percentages from 0.0 to 1.0
    n_div : the number of division you want to get out of array
        
    returns
    ======
    rank
    
    ex)
    divide_by_percent(0.5, 5)
    >>> 3    
    
    '''
    
    cutoff = np.linspace(0, 1, n_div+1)
    
    rg = return_range(cutoff)
    
    for i in range(1, len(cutoff)) :
        a, b = rg.__next__()
        
        if (pct_number>=a) & (pct_number<=b):
            return (i)
        
        
__all__ = ['return_range', 'divide_by_percent']