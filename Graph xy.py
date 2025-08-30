import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

xx=np.array([15,30,45,60,75],dtype=float)
yy=np.array([25,50,75,100,125],dtype=float)

sl=tf.Variable(0.0)
intc=tf.Variable(0.0)

opt=tf.optimizers.SGD(0.01)

for i in range(500):
    with tf.GradientTape() as t:
        yp=sl*xx+intc
        l=tf.reduce_mean((yy-yp)**2)
    dsl,dint=t.gradient(l,[sl,intc])
    opt.apply_gradients([(dsl,sl),(dint,intc)])

print("m:",sl.numpy())
print("c:",intc.numpy())

p=sl.numpy()*6+intc.numpy()
print("x=6 y:",p)

plt.scatter(xx,yy,color="blue")
plt.plot(xx,sl.numpy()*xx+intc.numpy(),color="red")
plt.show()
