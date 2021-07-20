import numpy as np
import tensorflow as tf 
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

#* load data
with np.load('data.npz') as data:
    vecs = data['vecs']
    labels = data['labels']

    vocab_size = data['vocab_size']
    input_len = data['input_len']


#* split data (also shuffled) 
train_data, test_data, train_labels, test_labels = train_test_split(vecs, labels, train_size=0.9, random_state=8)
train_data, val_data, train_labels, val_labels = train_test_split(train_data, train_labels, train_size=0.9) 

#* create datasets 
train_dataset = tf.data.Dataset.from_tensor_slices((train_data, train_labels))
val_dataset = tf.data.Dataset.from_tensor_slices((val_data, val_labels))
test_dataset = tf.data.Dataset.from_tensor_slices((test_data, test_labels))

#* batch the datasets 
BATCH_SIZE = 32
train_dataset = train_dataset.batch(BATCH_SIZE)
val_dataset = val_dataset.batch(BATCH_SIZE)
test_dataset = test_dataset.batch(BATCH_SIZE)

#* build model 
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=30, input_length=input_len),
    tf.keras.layers.Conv1D(filters=10, kernel_size=5, activation=tf.nn.relu, kernel_regularizer='l2'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(units=100, activation=tf.nn.relu, kernel_regularizer='l2'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(units=1, activation=tf.nn.sigmoid)
])

print(model.summary())

#* test run 
# input_test = vecs[:2]
# print(input_test)
# print(np.shape(input_test))
# output_test = model.predict(input_test)
# print(output_test)
# print(np.shape(output_test))

#* compile model
metrics = [
    tf.keras.metrics.BinaryAccuracy(name='accuracy'),
    tf.keras.metrics.TruePositives(name='tp'),
    tf.keras.metrics.FalsePositives(name='fp'),
    tf.keras.metrics.TrueNegatives(name='tn'),
    tf.keras.metrics.FalseNegatives(name='fn'), 
    tf.keras.metrics.Precision(name='precision'),
    tf.keras.metrics.Recall(name='recall'),
]
model.compile(
    loss=tf.keras.losses.BinaryCrossentropy(),
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    metrics=metrics
)

#* fit model
#! TODO: when to stop 
history = model.fit(train_dataset, epochs=15, validation_data=val_dataset)

#* plot
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.savefig('accuracy.png')



#* evaluate model
results = model.evaluate(test_dataset)
print(f"RESULTS\n{results}")

