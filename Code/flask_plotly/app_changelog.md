# Capstone Flask App Changelog

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

Date: 4/7/2023

Author: Ami Kano

Changes:
- Added links to base.html
- Changed chartsajax.html to extension of base.html and renamed as main_page.html
- Consolidated records_list and records_list_search into one: simple_search.html
- Created new html graph_interactive.html
- ISSUE: Plots in simple_search.html and graph_interactive.html do not show up. This is most likely due to changes in HTML.

-----------------------------------------------------------------------------------------------------------------------

Date: 4/10/2023

Author: Rachel Grace Treene

Changes:
- from a few days ago:
    - added new CSS to customize colors, fonts, and font sizes
    - added a menu in header (in base.html) for navigation
    - added a column option to CSS which is used (and will be used more) on the home page to help with layout
- from today:
    - rewrote interactive graph code to be more explicit; added new if-statement logic; all done in app.py (no changes in HTML)
    - tested code extensively in JupyterLab for all possible cases; all combinations of inputs now either return an error message directing the user to fix the problem or return a meaningful graph - see uploaded RGT_graph_code_testing.ipynb to see testing and code
    - fixed search display problem by reverting simple_search.html to a much earlier iteration (April 5 I think)
- functionality to dos:
    - graph: make the agg_func and fig_type options buttons instead of drop-down menus... I had trouble because when I clicked the buttons it submitted the form and I want it to store the information but not submit until we click 'make graph'
    - search: make it more intuitive to select columns to display... currently it's not clear how to select multiple and I think this needs to be improved for UX
    
-----------------------------------------------------------------------------------------------------------------------

Date: 4/11/2023

Author: Ami Kano

Changes:
- Changed Aggregation Function and Figure Type from dropdown menu to radio buttons
- Added string output to show previous input selections
- deleted files records_list.html and Tax_1867_Cleaned.csv

-----------------------------------------------------------------------------------------------------------------------

Date: 4/15/2023

Author: Rachel Grace Treene

Changes:
- changed search dropdown menu to make it possible to select multiple non-consecutive columns - did this by making menu into a dropdown menu of checkboxes rather than a multiple select dropdown
- fixed bug with graph page: problem was that the agg_options and fig_options didn't have a default value of None, so if nothing was selected the page submitted a bad request; added try/except statements to catch this issue

-----------------------------------------------------------------------------------------------------------------------

Date: 4/16/2023

Author: Rachel Grace Treene

Changes:
- explored Plotly graphs not resizing; decided not to use columns because of an apparent unsolved bug
- fixed HTML issue with search page
- changed colors of plotly graphs manually
- made output string prettier

-----------------------------------------------------------------------------------------------------------------------

Date: 4/17/2023

Author: Rachel Grace Treene

Changes:
- updated CSS to match new Plotly color scheme
- successfully centered graphs on home page
- enlarged and formatted inputs and dropdown menus
- enlarged and formatted navigation menu
- still need to enlarge and format radio buttons