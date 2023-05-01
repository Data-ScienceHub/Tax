# county-records


### Project Overview

OneSharedStory is a non-profit organization that helps African American families connect with their ancestry. The organization transcribes historical documents, allowing families to then search for information about their family history. To this point, these transcriptions have been housed in excel sheets. The goal of our project is to:

1. Create a database to house previously transcribed data
2. Create a public-facing search tool for users to search the database and learn about the historical records
3. Deploy the search tool as a web application that can later be deployed on the One Shared Story website

In addition, this project entails data exploration for learning purposes. To that end, the project also has the following goals:

4. Explore the data and present its significance
5. Provide an interactive way for users to explore the data

### Code Format

The contents of this repository are organized with the following structure:

    .
    ├── AWS_Deployment
    │   ├── tax_app_final_version
    │   └── Deploy the Project on AWS EC2.md
    ├── Applications
    │   ├── final_client_app
    │   └── final_student_app
    ├── Archive
    │   └── ...
    ├── Documentation
    │   ├── database_upload_data.md
    │   ├── local_app_running.md
    │   ├── DataDict.csv
    |   └── search_query_maintenance.md
    ├── README.md
    └── index.html

The majority of this repository is located in the Archive directory and records the semester-long work on the capstone project. See the README file within the directory for more information. Directions for deploying the application on AWS, a requirement for finishing our project, are within the AWS_Deployment directory. See the README file and .md file in the directory for more information. The final product is within Applications and comprises the directory final_client_app. Another important application is in Applications and comprises the directory final_student_app. The client app is a reduced version of the application which strictly adheres to the client's requirements. The student final app includes a page for the presentation of data, as well as an interactive graphing page for user exploration.

The Documentation directory includes instructions for adding data to the MongoDB, instructions for running the final applications on your local machine, and instructions for defining new feature names so that the search function will be able to access the data correctly.

In each application directory, the following directory structure is present, with the following functionality:

    .
    ├── static
    │   ├── css # defines our custom CSS stylesheet
    |   │   └── main.css
    │   └── js # contains javascript for the application
    |   │   └──script.js
    ├── templates # contains HTML for each page of the application
    │   ├── 404.html
    │   ├── base.html
    │   ├── graph_interactive.html (for student app only)
    │   ├── main_page.html (for student app only)
    │   └── simple_search.html
    └── app.py # queries the database and runs the application
