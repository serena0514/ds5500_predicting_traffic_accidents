# The Snow And Ice Removal Prioritizer

## About
The Snow and Ice Removal Prioritizer is a tool designed to assist city officials in determining what areas of a city are most likely to
experience accidents with a high severity. The tool can be used to determine the order in which snow and ice removal efforts, such as snow
plowing and preventative salt placement, that would be most beneficial for reducing overall accident occurrence and accident severity throughout
the day. The final output of the Prioritizer is a list based on coordinates for the specified city. The interface displays additional interactive
visuals to give insights on historical conditions that pertain to car-accidents and factors that may affect the likelihood.

## File Descriptions

### EDA (change to name of file)

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
file contents.

### Interface file (change to name of file)

## Project Contributors

Matthew Quaglia          
Dachuan Zhang         
Sri Lakshmi Tirupathamma Manduri         
Serena (Jiahui) Zeng        
