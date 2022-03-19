from tensorflow import keras
from keras import layers
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
import numpy as np
import itertools as it

classifiers: list[str] = ["meeseeks", "morty", "rick", "summer"]


def hyperparameter_tuning(train_generator):
    params_nn = {
        'neurons': [32, 64, 128],
        'activation': ['relu', 'sigmoid'],
        'batch_size': [32, 64],
        'epochs': [5, 10]
    }

    all_names = sorted(params_nn)
    combinations = list(it.product(*(params_nn[Name] for Name in all_names)))
    print(combinations)
    print("Length = ", len(combinations))

    for index, x in enumerate(combinations):
        print(f"\nIndex: {index}\n Combo: {x}")
        activation = x[0]
        batch_size = x[1]
        epochs = x[2]
        neurons = x[3]

        model = keras.Sequential(
            [
                keras.Input(shape=(250, 250, 3)),
                layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Flatten(),
                layers.Dropout(0.5),
                layers.Dense(neurons, activation=activation),  # 64 neurons
                layers.Dense(4, activation="sigmoid")  # 4 neurons
            ]
        )

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        model.fit(train_generator, epochs=epochs, batch_size=batch_size)


def main():
    # All images will be rescaled by 1./255
    train_datagen = ImageDataGenerator()
    img_folder = 'RickMorty/train'

    # Flow training images in batches of 120 using train_datagen generator
    train_generator = train_datagen.flow_from_directory(
            img_folder,  # This is the source directory for training images
            classes=classifiers,
            target_size=(250, 250),  # All images will be resized to 200x200
            # batch_size=32  # <- Not to be confused with 1 image
    )

    # Hyperparameter tuning (commented out to make training run quicker now I already know the results)
    # hyperparameter_tuning(train_generator)

    model = keras.Sequential(
        [
            keras.Input(shape=(250, 250, 3)),
            layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(64, activation="relu"),  # 64 neurons
            layers.Dense(4, activation="sigmoid")  # 4 neurons
        ]
    )

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(train_generator, epochs=10, batch_size=32)
    model.save("model.h5")

    evaluate_image(model, r"test/train/morty/00000000.png")
    evaluate_image(model, r"test/train/meeseeks/00000000.jpg")
    evaluate_image(model, r"test/train/rick/00000000.jpg")
    evaluate_image(model, r"test/train/summer/00000000.jpg")


# Evaluate the trained model
def evaluate_image(model, img_path: str):
    img = image.load_img(img_path, target_size=(250, 250))
    img.show()

    img_array = image.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_batch)
    prediction_list: list[float] = list(prediction[0])
    print(prediction_list)
    index = prediction_list.index(max(prediction_list))

    global classifiers
    print(classifiers[index])
    return classifiers[index]


if __name__ == "__main__":
    main()



