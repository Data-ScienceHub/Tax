# Uploading Additional Data on the MongoDB Database via the MongoDB Compass Application

1. If MongoDB Compass is not installed on your system, install it from MongoDB's website: https://www.mongodb.com/products/compass
2. Open the MongoDB Compass application.
3. Under the section 'New Connection,' there is a text box labeled 'URI.' Input the appropriate URI string in the text box; The URI should be created and given to you by the owner of the MongoDB deployment. 
4. After submitting the correct URI and connecting to the MongoDB deployment, you should see a list of databases on the left side of the screen. Click on the database 'TaxRecords.'
5. The screen should now show a list of collections within the 'TaxRecords' database. On the top left corner, there is a button containing the text 'Create collection.' Click on the button.
6. Clicking on the button should prompt a window pop-up with a text box labeled 'Collection Name.' Input the name of the new collection as you see fit. Then click on the 'Create Collection' button on the bottom right of the pop-up window. This will create an empty collection.
7. The screen would display the message 'This collection has no data' with an 'Import Data' button under it. Click on the 'Import Data' button. You will be prompted to select a file to upload from your device. Select the file that you intend to upload. Note that the file must be in either a CSV or a JSON format. 
8. This will prompt a pop-up window with the header 'Import.' Click on the 'Import' button at the bottom right corner of the pop-up window. 
9. If the message 'Import completed' appears on the pop-up window and the button on the bottom right now contains the text 'Done,' you are done uploading the data. Exit the pop-up window by clicking on the 'Done' button. 
