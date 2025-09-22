import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

true_slope = 3.0
true_intercept = -2.0

num_examples = 100
x_data = np.linspace(-5, 5, num=num_examples)
y_data = true_slope * x_data + true_intercept + np.random.normal(size=num_examples)

slope = tf.Variable(0.0)
intercept = tf.Variable(0.0)

def linear_model(x):
    return slope * x + intercept

def mean_squared_error(y_true, y_pred):
    return tf.reduce_mean(tf.square(y_true - y_pred))

optimizer = tf.optimizers.Adam(learning_rate=0.01)

x_tensor = tf.constant(x_data, dtype=tf.float32)
y_tensor = tf.constant(y_data, dtype=tf.float32)

for epoch in range(1000):
    with tf.GradientTape() as tape:
        y_predicted = linear_model(x_tensor)
        loss = mean_squared_error(y_tensor, y_predicted)
    gradients = tape.gradient(loss, [slope, intercept])
    optimizer.apply_gradients(zip(gradients, [slope, intercept]))

print(f'Original equation: y = {true_slope}x + {true_intercept}')
print(f'Learned equation: y = {slope.numpy():.2f}x + {intercept.numpy():.2f}')
print(f'Slope: {slope.numpy():.2f}')
print(f'Intercept: {intercept.numpy():.2f}')

plt.figure(figsize=(8, 6))
plt.scatter(x_data, y_data, c='red', label='Generated Data')
x_line = np.linspace(min(x_data), max(x_data), 100)
plt.plot(x_line, linear_model(x_line), c='blue', linewidth=2, label='Learned Line (TensorFlow)')
plt.title('Linear Regression using TensorFlow')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()
plt.savefig('linear_regression_graph.png')
