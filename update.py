import tensorflow as tf
model = tf.keras.models.load_model("model/MobileNet_lung_disease_diagnosis-5_Class.keras")
model.save("model/MobileNet_lung_disease_diagnosis-5_Class.h5")