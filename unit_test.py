from Vector import Vector
import math

for i in range(30):
    theta = i*2*math.pi/30
    v1 = Vector(math.cos(theta),math.sin(theta))
    v2 = Vector(1,1)
    
    print v1, v1.component(v2), v1.component(v2).magnitude()

