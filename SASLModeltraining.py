from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense , Dropout
import os

img_size = 128
# Step 1 - Building the CNN

# Initializing the CNN
model = Sequential()

# First convolution layer and pooling
model.add(Convolution2D(32, (3, 3), input_shape=(img_size, img_size, 1), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
# Second convolution layer and pooling
model.add(Convolution2D(32, (3, 3), activation='relu'))
# input_shape is going to be the pooled feature maps from the previous convolution layer
model.add(MaxPooling2D(pool_size=(2, 2)))

# Flattening the layers
model.add(Flatten())

# Adding a fully connected layer
model.add(Dense(units=128, activation='relu'))
model.add(Dropout(0.40))
model.add(Dense(units=96, activation='relu'))
model.add(Dropout(0.40))
model.add(Dense(units=64, activation='relu'))
model.add(Dense(units=27, activation='softmax')) # softmax for more than 2 classses for classification

# Compiling the CNN
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy']) # categorical_crossentropy for more than 2


# Step 2 - Preparing the train/test data and training the model
model.summary()
from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
    shear_range=0.2,
    zoom_range=0.2,
    rescale=1./255,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(
    horizontal_flip=True,
    rescale=1./255)

training_set = train_datagen.flow_from_directory('SASLData/train',
                                                 target_size=(img_size, img_size),
                                                 batch_size=16,
                                                 color_mode='grayscale',
                                                 class_mode='categorical')

test_set = test_datagen.flow_from_directory('SASLData/test',
                                            target_size=(img_size, img_size),
                                            batch_size=16,
                                            color_mode='grayscale',
                                            class_mode='categorical') 


history = model.fit(training_set,epochs=150, validation_data=test_set)

# Saving the model
model_json = model.to_json()
with open("betterSASLmodellest.json", "w") as json_file:
    json_file.write(model_json)
print('Model Saved')
model.save_weights('betterSASLmodellatest.h5')
print('Weights saved')
import  matplotlib.pyplot  as  plt
train_loss = history.history['loss']
train_acc = history.history['accuracy']
val_loss = history.history['val_loss']
val_accuracy = history.history['val_accuracy']
#ploting training and validation loss vs. epochs
epochs = list(range(1,151))
plt.plot(epochs, train_loss, label = "training loss")
plt.plot(epochs, val_loss, label = "validation  loss")
plt.legend()
plt.show()
#ploting training and validation accuracy vs. epochs

plt.plot(epochs, train_acc, label = "training accuracy")
plt.plot(epochs, val_accuracy, label = "validation  accuracy")
plt.legend()
plt.show()