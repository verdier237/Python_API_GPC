import pandas as pd
from Point import Point
from Cours import Cours
import json
class Teacher() :
    name = ""
    skills = [Cours]
    _id = ""
    def __init__(self,name,skills=[Cours],tabPointsAv=[{}]):
        """
         Initializes the TabPoints object. You need to call this before you create the TabPoints object. You need to call this before you create the TabPoints object
         
         @param name - The name of the TabPoints object
         @param skills - The list of skills that the TabPoints can apply
        """
        """
         Initializes the tabPoints object. This is the constructor for the TabPoints class. You need to call this before you create the TabPoints object
         
         @param name - The name of the TabPoints
         @param skills - The list of skills that the TabPoints can apply to
         @param tabPointsAv - The class that contains the availability of the
        """
        self.name = name
        self.skills = skills
        self.availability = self.convertClassToArray(tabPointsAv,False,False)
        
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
        if tabPoints[0]['z'] == '':
            return pd.DataFrame([["nothing"]*cols]*rows, columns = headers)
        
        arr = [[0] * cols for _ in range(rows)] 
        # Set the points in the tab points.
        # Set the points in the tab points.
        for w in range(size):
            x = int(tabPoints[w]['x'])  # Convertir en entier
            y = int(tabPoints[w]['y'])  # Convertir en entier
            z = tabPoints[w]['z']

            if 0 <= x < rows and 0 <= y < cols:  # Ajuster les bornes des indices (rows et cols)
                if tabPoints[w]['z'] == '':
                    arr[y][x] = 1  # Ajuster l'ordre des indices (y et x)
                else:
                    arr[y][x] = int(tabPoints[w]['z'])  # Convertir en entier

        return pd.DataFrame(arr, columns=headers)
    
    def updateAvailability(self,tabPoints,isAdd=True):
        rows, cols = (10, 5)
        add = 0
        if  isAdd :
            add = 1
        for w in range(len(tabPoints)):
            x = tabPoints[w]['x']
            y = tabPoints[w]['y']
            z = tabPoints[w]['z']

            if 0 <= x < cols and 0 <= y < rows:  # Check if x and y are within valid range.
                    if tabPoints[w]['z'] == '':
                        self.availability.values[x][y] = add
                    else:
                        self.availability.values[x][y] = tabPoints[w]['z']       
        
            
    