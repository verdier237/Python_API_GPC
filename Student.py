import pandas as pd
from Point import Point
class Student:
    name = ""
    availability = pd.DataFrame()
    schedule = pd.DataFrame()
    def __init__(self,name,pointSc=[Point()]):
        self.name = name
        self.availability = self.convertClassToArray([],True,False)
        self.schedule = self.convertClassToArray([{'x':'','y':'','z':'sting'}],False,True)
        
    def convertClassToArray (self ,tabPoints,isFull = False,isEmpty = True):
        """
        Converts a list of class objects into a 2D array of z values. If isFull is True the array will be full
        
        @param tabPoints - A list of class objects
        @param isFull - A boolean indicating whether or not we are dealing with full or non - full data
        
        @return A 2D array of z values for each class in the list ( 0 = empty 1 = full
        """
        rows, cols = (10, 5)
        size = len(tabPoints)
        print(tabPoints)
        headers = ["Lundi", "Mardi", "Mercredi", "jeudi","vendredi"]
        # Returns a pandas. DataFrame with the full data.
        if isFull :
            return pd.DataFrame([[1]*cols]*rows, columns = headers)
        if isEmpty :
            return pd.DataFrame([[0]*cols]*rows, columns = headers)
        if size == 0 :
            return pd.DataFrame()
        if tabPoints[0]['z'] != '':
            return pd.DataFrame([[" "]*cols]*rows, columns = headers)
        
        arr = [[0] * cols for _ in range(rows)] 
        # Set the points in the tab points.
        # Set the points in the tab points.
        for w in range(size):
            x = tabPoints[w]['x']
            y = tabPoints[w]['y']
            z = tabPoints[w]['z']

            if 0 <= x < cols and 0 <= y < rows:  # Check if x and y are within valid range.
                    if tabPoints[w]['z'] == '':
                        arr[x][y] = 1
                    else:
                        arr[x][y] = tabPoints[w]['z']

        print(arr)
        return pd.DataFrame(arr, columns=headers)