Date: 4/6/23
Author: Rachel Grace Treene

Changes:
- started with RGT_flaskplotly_app.py
- from search_flask app.py, brought over new packages - PyMongo, plotly.figure_factory
- from search_flask app.py, copied setup - see lines 10-18
    - defined app differently, including template_folder
    - set up app.config["MONGO_DBNAME] and app.config["MONGO_URI"] with Ami's credentials
    - set mongo and columns
- on line 20, began "homepage" section
    - kept everything as original RGT_flaskplotly_app.py
    - note that this page renders chartsajax.html which is in the templates folder
    - on line 35, called dataframe from MongoDB rather than from csv file
    - kept all plotly code the same, returned the same JSON object
- on line 85, began "simple search" section
    - did not copy over line 33 from search_flask app.py, which was '@app.route("/")' since that's the home URL and it's already defined as containing the RGT_flaskplotly_app
    - copied over the "/records_list" route
    - the view records_list() renders the template records_list.html in the original search_flask app; I copied that html file over and called it "records_list_search.html" and it is now in the templates folder, that is also what records_list() renders in the new app
    - copied over the "/search" route and made no changes to its contents except, like above, it renders records_list_search.html instead of records_list.html
    - copied over the route "@app.errorhandler(404)" and copied the 404.html file into the templates folder
    - did NOT copy the last section of this app, which initializes with if __name__ == "__main__":
- on line 237, began "interactive visualization" section
    - here once again, did not copy over the "/" route
    - this app wouldn't load for me on its own; it's possible I messed something up and then accidentally pushed it to GitHub! If so, feel free to recommit your version of that app
    - did copy over the records_list() view and the records_list.html - renamed these to be called records_list_graph so there wouldn't be any conflicts
    - didn't change anything else - copied everything, and changed anywhere that said "records_list" to "records_list_graph"
- on line 327, began the "run" section
    - copied over the section from the graph app, lines 129-130
- finally, copied over base.html to the templates folder
- copied js over to the static folder, created a js directory and copied script.js to that directory
- did not copy over style.css! already have main.css
- at the moment, search and home load perfectly but graph loads forever and never renders - either I messed something up or there was an issue with the HTML to begin with

-----------------------------------------------------------------------------------------------------------------------

Date:
Author:

Changes: