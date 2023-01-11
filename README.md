# county-records


### Project Overview

OneSharedStory is a non-profit organization that helps African American families connect with their ancestry. The organization transcribes historical documents, allowing families to then search for information about their family history. To this point, these transcriptions have been housed in excel sheets. The goal of our project is to:

1. Create a database to house previously transcribed data
2. Create a software tool for future volunteers to transcribe data and have records entered into the database
3. Create a software tool for families to search the database and learn about the historical records.

### Code Format

Within the OneSharedStory folder you will find several files which ultimately will be used to surface a web application using flask. The following are important notes about the files:

- app.py is our python file that powers the application. Here you'll find that we create a MongoDB database, add our data from csv files into collections within the database, and initialize get/post methods for each of our landing pages. 
- .csv files contain the data from 
- templates folder houses all of our .html files that contribute to the web application. 
- static folder houses our CSS and JS files
