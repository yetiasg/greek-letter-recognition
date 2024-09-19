import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator # type: ignore
from tensorflow.keras import layers, models, regularizers, Input # type: ignore

train_data_dir = 'alphabet_lib/'

# generator danych z normalizacją obrazów
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    horizontal_flip=False,
    fill_mode='nearest',
    validation_split=0.2
)

# generator danych treningowych
train_generator = datagen.flow_from_directory(
    train_data_dir,
    target_size=(45, 45),
    color_mode='grayscale',
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

# Generator danych walidacyjnych
validation_generator = datagen.flow_from_directory(
    train_data_dir,
    target_size=(45, 45),
    color_mode='grayscale',
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

# Definicja CNN
model = models.Sequential([
    Input(shape=(45, 45, 1)),
    layers.Conv2D(64, (3, 3), activation='relu', kernel_regularizer=regularizers.l2(0.001)), # Dodanie kar za duże wagi w sieci, co pomaga zmniejszyć przeuczenie.
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu', kernel_regularizer=regularizers.l2(0.001)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu', kernel_regularizer=regularizers.l2(0.001)),
    layers.Flatten(),
    layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
    layers.Dropout(0.5),  # Dodanie dropoutu 50% Wyłączanie losowych neuronów podczas treningu, co zmusza model do uczenia się bardziej ogólnych wzorców.
    layers.Dense(5, activation='softmax')  # Zakładamy 5 klas: Alpha, Beta, Delta, Fi, Sigma
])

model.compile(optimizer='adam', 
              loss='categorical_crossentropy', 
              metrics=['accuracy'])

model.fit(
    train_generator,
    epochs=20,
    validation_data=validation_generator
)

model.save('greek_letter_recognition_model.h5')

print("generated")
