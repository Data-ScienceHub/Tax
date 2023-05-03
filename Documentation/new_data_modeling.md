# Naming Features in New Types of Data

This notebook explains how to name new features from different types of data before adding it to the database. This is important because without appropriate naming conventions, the newly added data will not be searchable with the current search function.

Currently, the search function can return records based on first name, last name, county name, and date range. Any features in new data that contains information pertaining to these search terms must contain appropriate tags.

Key tags:
- name: any feature that pertains to an individual's name, whether surname or given name, should have this tag in its name. This includes the primary individual and any other individual that relates to them, like a parent or employer.
- loc: any feature that pertains to a record's location, whether the location of recording or the source of the current record storage, should have this tag in its name.
- date: any feature that pertains to a record's date, whether the date of recording the information or some other date, should have this tag in its name.

See the examples below as a guide:
- a feature showing the name of an individual's child might be named 'PersonChildName'
- a feature with the street name of the tax recorder's address might be named 'SourceRecorderLocStreet'

Of course, features should also contain tags for other relevant information in the feature, like 'Count' if a count is reported or 'Person' if the feature pertains to the primary individual in the record. As long as these tags are kept uniform and documented well, there is flexibility in their use. This will not affect the search function.
