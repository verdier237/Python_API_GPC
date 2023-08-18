import pandas as pd
from Point import Point
import json

def convertClassToArray(tabPoints,isFull = False,isEmpty = True):
    """
     Converts a list of class objects into a 2D array of z values. If isFull is True the array will be full
     
     @param tabPoints - A list of class objects
     @param isFull - A boolean indicating whether or not we are dealing with full or non - full data
     
     @return A 2D array of z values for each class in the list ( 0 = empty 1 = full
    """
    rows, cols = (10, 5)
    size = len(tabPoints)
    headers = ["Lundi", "Mardi", "Mercredi", "jeudi","vendredi"]
    # Returns a pandas. DataFrame with the full data.
    if isFull :
        return pd.DataFrame([[1]*cols]*rows, columns = headers)
    if isEmpty :
        return pd.DataFrame([[0]*cols]*rows, columns = headers)
    if size == 0:
        return pd.DataFrame()
    arr = [[0]*cols]*rows
    # Set the points in the tab points.
    for w in range(0,size):
        # Set the z value of the points in the array.
        for i in range(0,rows):
            # Set the value of the column to the first column in the array.
            for j in range(0,cols):
                # Set the points in the tab points
                if tabPoints[w]['x'] == i and tabPoints[w]['y'] == j:
                    # Set the z value of the tab points
                    if tabPoints[w]['z'] == '':
                        arr[i][j] = 1
                    else:
                        arr[i][j] = tabPoints[w]['z']
    return pd.DataFrame(arr , columns = headers)