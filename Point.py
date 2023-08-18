class Point:
    x=0
    y=0
    z=""
    def __init__(self,x=0,y=0,z=""):
        """
         Initialize the object with x y and z. This is used to set the values of the object when creating a 3D point
         
         @param x - x value of the point
         @param y - y value of the point ( can be None )
         @param z - z value of the point ( can be " "
        """
        self.x = x
        self.y = y
        self.z = z
    