import math

tinyFloat = 0.0000001

class Vector:
    def __init__(self, x=0, y=0):
      self.x = float(x)
      self.y = float(y)

    def __add__(self, other):
      return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
      return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scale):
      return Vector(scale*self.x, scale*self.y)

    def __rmul__(self, scale):
      return self*scale

    def int_x(self):
      return int(round(self.x))

    def int_y(self):
      return int(round(self.y))

    def get_x(self):
      return self.x

    def get_y(self):
      return self.y

    def magnitude(self):
      return math.sqrt(self.x**2 + self.y**2)

    def unit_vector(self):
      if abs(self.x) < tinyFloat and abs(self.y) < tinyFloat:
        return Vector(0,0)
      else:
        return Vector(self.x/self.magnitude(), self.y/self.magnitude())

    def theta(self):
      return math.atan2(self.y, self.x)

    def getComponent(self, theta):
      alpha = self.theta() - theta
      magnitude = math.cos(alpha)*self.magnitude()
      return Vector(math.cos(theta)*magnitude, math.sin(theta)*magnitude)

    def getNormalComponent(self, theta):
      alpha = self.theta() - theta
      magnitude = math.sin(alpha)*self.magnitude()
      return Vector(math.cos(theta + (math.pi/2))*magnitude, math.sin(theta + (math.pi/2))*magnitude)

    def component(self, v):
        alpha = self.alpha(v)
        alphaMagnitude = math.cos(alpha)*self.magnitude()
        return v.unit_vector()*alphaMagnitude

    def alpha(self, v):
        return v.theta() - self.theta()

    def __str__(self):
      return "Vector (%.3f, %.3f)" % (self.x, self.y)

    def distance(self, v):
      return math.sqrt((self.x - v.x)**2 + (self.y - v.y)**2)

    def rotated(self, theta):
        return Vector(self.x*math.cos(theta)  - self.y*math.sin(theta), self.x*math.sin(theta)  + self.y*math.cos(theta))
      
    def __repr__(self):
      return self.__str__()
