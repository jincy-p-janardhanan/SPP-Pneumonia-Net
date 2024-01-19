# SPP-Pneumonia-Net

**Disclaimer: This project was developed to meet academic curriculum requirements (semesters 7, 8 - main project, B.Tech Information Technology (2017-2021), University of Calicut).**

This project aims at classifying frontal chest X-Ray images into three classes - Bacterial Pneumonia, Viral Pneumonia, and Normal. 

Academic main projects were required to be based off of recent research publications, and this project is based on [A lightweight deep learning model for COVID-19 detection](https://ieeexplore.ieee.org/document/9188133).

## Dataset
To build our dataset, we combined data from the following public datasets from Kaggle.
1. [COVID-19 Radiography Database](https://www.kaggle.com/tawsifurrahman/covid19-radiography-database)
2. [Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia)

The combined dataset has an equal distribution of examples for each class. There are a total of 8340 images, with 2780 images for each class.
For fast performance, the entire dataset was written into an h5 file. (Although we experimented with different batch sizes, we got the best results when the entire training set was used.)

(Refer notebook: [Dataset.ipynb](https://github.com/jincy-p-janardhanan/SPP-Pneumonia-Net/blob/main/Dataset.ipynb))

### Data Labelling
Chest X-Ray images were labelled and categorized as follows:
- `O` : Normal
- `1` : Bacterial Pneumonia
- `2` : Viral Pneumonia

### Train, Validation, and Test Split
`75%` of the dataset was used for training, and the remaining `25%` was equally split between validation and test sets.

## Model Architecture
The model has 14 CNN layers with the following organization:
- 2 normal CNN layers with `6`, and `8` filters respectively.
- 4 squeeze (bottleneck) modules with filter sizes, `N = {61, 123, 199, 288}`

Hyperband optimization using Keras tuner was used to select filter sizes.

All the CNN layers used 'same' padding. Between each CNN layer, batchnormalization and leaky ReLU activation (with α = 0.1) was used.

The CNN layers are followed by a spatial pyramid pooling (SPP) module that uses 3 different kernel sizes: `4 x 4`, `3 x 3`, and `2 x 2`. Thus this layer captures information obtained from the CNN layers in three different dimensions, and hence can facilitate better predictions. The flattened output of the SPP layer is used for prediction, using a 3-unit dense layer with softmax activation.

The following table summarizes the model architecture.

| **Layer No.** 	| **Operation** 	| **No. of Filters** 	|   **Kernel**  	| **Stride** 	|
|:-------------:	|:-------------:	|:------------------:	|:-------------:	|:----------:	|
|       1       	|     Conv2D    	|          6         	|      3x3      	|     1x1    	|
|       2       	|     Conv2D    	|          8         	|      3x3      	|     1x1    	|
|       3       	|  MaxPooling2D 	|          -         	|      2x2      	|     2x2    	|
|       4       	|     Conv2D    	|         61         	|      3x3      	|     1x1    	|
|       5       	|     Conv2D    	|         30         	|      1x1      	|     1x1    	|
|       6       	|     Conv2D    	|         61         	|      3x3      	|     1x1    	|
|       7       	|  MaxPooling2D 	|          -         	|      2x2      	|     2x2    	|
|       8       	|     Conv2D    	|         123        	|      3x3      	|     1x1    	|
|       9       	|     Conv2D    	|         61         	|      1x1      	|     1x1    	|
|       10      	|     Conv2D    	|         123        	|      3x3      	|     1x1    	|
|       11      	|  MaxPooling2D 	|          -         	|      2x2      	|     2x2    	|
|       12      	|     Conv2D    	|         199        	|      3x3      	|     1x1    	|
|       13      	|     Conv2D    	|         99         	|      1x1      	|     1x1    	|
|       14      	|     Conv2D    	|         199        	|      3x3      	|     1x1    	|
|       15      	|  MaxPooling2D 	|          -         	|      2x2      	|     2x2    	|
|       16      	|     Conv2D    	|         288        	|      3x3      	|     1x1    	|
|       17      	|     Conv2D    	|         144        	|      1x1      	|     1x1    	|
|       18      	|     Conv2D    	|         288        	|      3x3      	|     1x1    	|
|       19      	|   SPP Module  	|          -         	| 4x4, 3x3, 2x2 	|     1x1    	|
|       20      	|     Dense     	|          3         	|       -       	|      -     	|

(Refer notebook: [SPP_Pneumonia_Net.ipynb](https://github.com/jincy-p-janardhanan/SPP-Pneumonia-Net/blob/main/SPP_Pneumonia_Net.ipynb))

# Optimization
Adagrad optimizer was used to train the model using categorical cross entropy loss function. Again, hyperband optimization was used to choose the following parameters for the optimizer:
 - Learning rate
 - Initial accumulator value
 - Epsilon

*(Before using hyperband optimizer, we had tried different optimizers and extensive tuning of various hyperparameters manually. The results of manual tuning can be accessed from [here](https://docs.google.com/spreadsheets/d/e/2PACX-1vRyuTVBEW_D-BaCbOQVZTYOKJ4ZI6E7KvUmpEE2HzY4vSboz4ks3PYrd3o4jMfS04KAJ1X6QpHz02JK/pubhtml?gid=0&single=true). Models were numbered and saved for each hyperparameter configuration.)*

# Performance
The trained model has a classification accuracy of 92.69%, uses only 3.18 MB of physical storage (TFLite format) and can be deployed in low compute environments. According to deployment logs from heroku, the model requires maximum upto 350MB of RAM (approximate).

# Deployment
- The trained model was converted into TFLite format and deployed using a minimal flask API.
- The deployment is available at https://spp-pneumonia-net.onrender.com/ .

# Development Environments
- Google Colaboratory
- Visual Studio

# Languages and Frameworks
- Python 3.9
- Keras (for deep learning)
- Flask (for deployment API)
- HTML and CSS (for web front-end)
