# The Snow And Ice Removal Prioritizer

## About
The Snow and Ice Removal Prioritizer is a tool designed to assist city officials in determining what areas of a city are most likely to
experience accidents with a high severity. The tool can be used to determine the order in which snow and ice removal efforts, such as snow
plowing and preventative salt placement, that would be most beneficial for reducing overall accident occurrence and accident severity throughout
the day. The final output of the Prioritizer is a ranked list of coordinates to the third decimal point for the specified city with a Severity rating of average accident likelihood throughout the day. The interface displays additional interactive
visuals to give insights on historical conditions that pertain to car-accidents and factors that may affect the likelihood.

## File Descriptions

### EDA_Vehicle_Accident_Severity.ipynb

The purpose of this file is to show users the Exploratory Analysis we performed before training the final model.

### Chunking_Dataset.ipynb

The purpose of this file is to extract data from Boston, MA. The code is displayed for reference. It is not needed to utilize the interface. 
If a user is interested in using the code to chunk a different area or subset of the data, they can modify the portion of the code below,
where the value in the single quotes within the brackets indicates the desired column and the value in the single quotes after '==' indicates
the desired column value:

```
filtered_chunk = chunk[(chunk['City'] == 'Boston') & (chunk['State'] == 'MA')]
```

### Train_Vehicle_Accident_Severity_Model.ipynb

The purpose of this file is to showcase the efforts taken to clean the data, join and create the relevant datasets, experiment with three different
types of models, and finalize the selected model, Random Forest Regression. This code is dispalyed for reference. It is not needed to utilize the 
interface.

### random_forest_accident_likelihood_model.pkl

The purpose of this file is to save the final model created in Train_Vehicle_Accident_Severity_Model.ipynb and utilize this model within the
interface. The details of the file cannot be viewed directly on this repository. However, if necessary, the file can be downloaded to extract the
file contents. This file is needed to utilize the interface.

### Predict_From_User_Input.ipynb

The purpose of this file is to integrate the final model stored in random_forest_accident_likelihood_model.pkl to the user interface. This file is needed
to utilize the interface.

### predict_for_city.py

This file contains a great deal of overlap with Predict_From_User_Input.ipynb. The purpose is to integrate the final model with the user interface.

### 5500trafficFlowData.ipynb
This file provide an example use of the Tom Tom api to provide a real time traffic flow speed information of a certain location based on logtitude and latitude. It can be used as an extra information for users to understand the traffic and traffic accidents or that it can be corporate with the traffic accident rates model in the future to help with better estimate.

### utils.py

The purpose of this file is to make useful functions within our project available to users.

### County.json

The purpose of this file is to organize on a county level.

### app.py

The purpose of this file is to run the final interface.

### CSV files

All files ending with .csv are data used within the project.

## Running The Interface

After downloading County.json and all csv files, the application can be run with app.py. Due to complexities in running the interface due to downloads and dependencies, we have provided a link to a Demo of the interface for those unable to run locally on their machine. Our next steps in this project are to run the interface on a cloud-based site for a simpler way to access the tool. See the link below to view the Demo:

[Demo](https://drive.google.com/file/d/1oIyiKZkNNMDKG4tYOKJScjLyxO4EsDGm/view?usp=drive_link)

## Project Contributors

Matthew Quaglia          
Dachuan Zhang         
Sri Lakshmi Tirupathamma Manduri         
Serena (Jiahui) Zeng        
