cd tesseract-5.3.4/tesstrain
make training MODEL_NAME=ita_1 EPOCHS=10 LEARNING_RATE=0.005 START_MODEL=ita PSM=13
make plot MODEL_NAME=ita_1