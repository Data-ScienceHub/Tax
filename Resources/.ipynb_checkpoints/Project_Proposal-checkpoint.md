# Project Proposal: One Shared Story MSDS Capstone

Group Members: Ami Kano, Chunru Zheng, Rachel Grace

Sponsor: Robin Patton - One Shared Story

Advisors: Dr. Judy Fox, Ian Liu

February 16, 2023

## Introduction

This document seeks to define the goals, objectives, work structure, constraints, and limitations of the University of Virginia MSDS Capstone project for One Shared Story (OSS). Over the course of the semester, this document will be a guide for tracking project progress and help to keep the project focused on its main goals. The end of this document outlines key deliverables and deadlines. After review by the capstone group, Robin Patton, and Dr. Judy Fox, this document will serve as an authoritative plan for the semester.

## Project Goals & Objectives

### Motivation

From a societal perspective, this project is motivated by the current challenges in tracing ancestry in Virginia, especially for people of color and women. OSS seeks to address this difficulty by making historic county property tax records accessible and searchable for the public. Because people of African descent in Virginia were most often considered to be property prior to the Civil War, these individuals were not recorded in census data, but were recorded in personal property tax records, usually only by first name. After the Civil War, these individuals with surnames were first identified in county tax records, and the documents note the employer or residence of the formerly enslaved. This data can provide clues that will link ancestors of color to specific places where they may have been enslaved. This project seeks to provide a database structure to hold county property tax records transcribed by volunteers.

### Goal

The concrete goal of this project is to create a functional, scalable, and searchable database for OSS. The database must have a functional backend and be hosted reliably. Further, it must have a public dashboard application stored on the OSS website for searching the database to locate records, and a method to bulk upload spreadsheets of data.

## Project Requirements

### Expected Quality

The most important quality benchmark in this project is functionality of the database. Robin’s priority is a functional database. A beautiful dashboard application would be ideal, but is not the key deliverable of this project. The group will do our best to meet all requirements, but will especially focus on the dashboard functionality for public access to the data. As this is a student project and a learning experience for the members of the group, it is understood that the product will be professional-quality to the fullest extent possible, given group members’ experience and skills.

### Cost

Ideally, tools for the database hosting and dashboard applications will not incur extra cost to OSS. The capstone group agrees to prioritize free or low-cost tools whenever possible. Robin will provide feedback as needed when tools are chosen.

## Project Scope Description

### Work Breakdown Structure

Below is a graphic representation of this project’s tasks. Tasks are organized in a parent-child orientation, with parent nodes representing a particular part of the project and child nodes representing components of the parent task. Thus, the top layer represents the final product, the next layer down represents the four main components of the project, and so on.

![](Images/wbs.png)

### Task Specification and Description

Below is a more detailed description of each component of the above graphic, along with deliverables listed. The most important deliverables for the project are under the database and hosting components of the Work Breakdown Structure. See the end of this document for a deliverable timeline and importance rating of each deliverable.

#### Database: Data Structure

##### Restructure Data.

The data in the database must be structured such that it may be potentially merged with datasets from other organizations. In particular, it should be compatible with Ancestry.com and the organization On These Grounds’ (OTG) data structure. This will entail a change in structure from the current tabular data provided by OSS to a JSON structure. Deliverable: restructured data compatible with, or at least similar to, Ancestry.com datasets.

##### Adjust Column Names.

The current data features, or columns, have names that make queries difficult to write and do not reflect the desired data structure. These will be renamed to honor the controlled vocabulary data structure of OTG and make queries easier to write. Deliverable: renamed feature names in the database for ease of querying and OTG controlled vocabulary adherence.

#### Database: Querying

##### Write Name-Event Query.

The query function for accessing and searching the database must return names in association with events. This can be expressed as a name-event relationship. The query should search by name, location, date (as a range), and record type. In addition, the query must be flexible and capable of searching new datasets that are similar or identical in their features. This means the query should be general enough to search for names and events with data from a slightly different historical record. For example, the queries will be designed around the current available data, which is property tax records. However, queries should also function for other property tax records with similar feature names. Deliverable: Queries that return names in association with events, and are general enough to accommodate new datasets.

##### Document Query Writing.

The queries should be well-documented such that Robin can understand and replicate them, even modifying them when appropriate. Deliverable: a well-documented query function with instructions for replicating and editing queries in the future.

#### Searching: Public Dashboard

##### Choose Tool.

A no-cost tool will be chosen for the dashboards. Currently, the team’s pick is a Python package called Starlette, recommended by Professor Fox. This package is free of charge and offers easy interfacing with MongoDB, as well as extensive documentation. Deliverable: a dashboard made with a free tool, most likely Starlette.

##### Configure Search Fields.

For the search dashboard, which must be a publicly available application, search fields should reflect similar ancestry record search interfaces, such as the dashboard provided by Ancestry.com. These fields may be tweaked and adjusted in conversation with Robin. Important fields include Name, Location, and Event. Deliverable: appropriate search terms on search dashboard for returning genealogy records by name, event, and/or location.

##### Choose Output Display.

The search dashboard should display results in an appropriately neat and clear manner. The query returns should include a link to the hosted document image (when available as a URL) to open in a new window. This could be a dataframe format or more structured, like the format of Ancestry.com. Other visualizations like charts or graphs are also possible. Deliverable: a neat and readable search result display.

##### Update Query as Needed.

As the search dashboard and search fields are chosen and adjusted, the query function may need updates. This should be done concurrently with search term decisions and well-documented, as specified under the Database: Querying deliverable. Deliverable: edited and documented query function as needed to accommodate search dashboard.

#### Data Entry: Spreadsheet Entry

##### Choose Tool.

Spreadsheet entry should be accomplished either through the same dashboard tool used for searching, or directly in MongoDB Compass. Deliverable: a dashboard or direct upload pipeline.

##### Write Code or Documentation.

The data entry dashboard must be appropriately connected to the database and enter data correctly. This will require writing functional code that correctly adds an entire spreadsheet of data to the database in such a way that it will be accessible by the query function. Additionally, the format of the spreadsheet that is to be added has been or will be defined by Robin and OSS. Alternatively, instead of code, this functionality could be achieved with documentation for uploading a spreadsheet directly in MongoDB Compass. Deliverable: working data entry code for adding an entire collection to the MongoDB database, or documentation for uploading a spreadsheet to MongoDB.

#### Hosting: MongoDB

##### Run Tests

The database, once created, must be appropriately tested. This includes testing its scalability by adding new data and checking for the functionality of the query function, testing its performance, and testing its usability among other important tests. Deliverable: appropriately tested and, when needed, fixed database.

##### Choose Hosting Location.

The database needs to be hosted on the OSS website through its hosting service, Reclaim Cloud, or on AWS through MongoDB. Deliverable: working database hosted appropriately.

##### Document Maintenance.

Robin would like to maintain the database herself whenever possible. The maintenance of the database should be well-documented to facilitate this. This documentation will be developed with Dr. Fox and Ian Liu, who have expertise and knowledge about maintaining a database. Deliverable: detailed documentation for maintaining the database.

## Project Exclusions

This project intentionally excludes any work with location data that involves mapping, in particular with regards to the search dashboard. It also excludes access issues, like granting certain users access to different levels of control, except for Robin. This project also does not deal with attributing record ownership to particular sources.

This project only involves datasets generated from tax property records from various counties within the state of Virginia. Data unrelated to tax records will not be included in our project; however, the scalability of the database to other data in the future is a goal of the project.

## Project Constraints

The project is limited by time, as the team will complete their work on or before May 3, 2023. This constrains the project, as its scope must be manageable within this time frame. Another key constraint is Robin’s wish for limited expense in tools. While the capstone group can request a budget from UVA, the project must be done with a view toward the sustainability of the product for OSS in the future.

The project is also constrained by the limited experience of the group with database hosting, creation, and deployment. As specified in the Expected Quality section, the group will accomplish the project to the best of their ability, using all resources available. Key resources include the help of Dr. Fox and Ian Liu, the TA for the capstone course.

## Project Assumptions

The capstone group commits to being available and responsive in a timely manner throughout the week, Monday through Friday, during business hours. Weekends and weeknights will not be assumed available, but the group may be available during these times on a case-by-case basis. Responses may be delayed at these times. The group expects that Robin and Dr. Fox will also be available and responsive during business hours.

Throughout the project, the capstone group will communicate with both sponsor (Robin) and advisor (Dr. Fox) in a timely manner and seek to follow the requirements and advice of both whenever possible. In the event of a conflict in advice, Robin has final authority over project priorities, requirements, and goals. Dr. Fox has final authority over what is realistic and appropriate given our time and expertise constraints. 

## Project Workflow and Roles

### Workflow

Monday, 9\:00am-11\:00am\: capstone course meeting, project update with Ian and Dr. Fox

Monday, midday: sponsor meeting, project update with Robin

Tuesday, 2\:00pm-3\:00pm\: team meeting, debrief Monday meetings and delegate weekly tasks

### Roles and Responsibilities

Ami Kano: coding, query and database lead

Chunru Zheng: dashboard and data visualization lead

Rachel Grace: communication lead

## Project Deliverables

2/15/23 - **Database: Data Structure** Restructured data compatible with, or at least similar to, Ancestry.com datasets.

2/15/23 - **Database: Data Structure** Renamed feature names in the database for ease of querying

2/22/23 - **Database: Querying** Queries that return names in association with events, and are general enough to accommodate new datasets

4/1/23 - **Data Entry** A dashboard or direct upload pipeline

4/1/23 - **Searching** A dashboard made with a free tool, most likely Starlette

4/1/23 - **Searching** Appropriate search terms on search dashboard for returning genealogy records by name, event, and/or location

4/1/23 - **Searching** A neat and readable search result display

4/1/23 - **Data Entry** Working data entry code for adding an entire collection to the MongoDB database, or documentation for uploading a spreadsheet to MongoDB

5/3/23 - **Hosting** Appropriately tested and, when needed, fixed database

5/3/23 - **Hosting** Working database hosted appropriately

5/3/23 - **Searching** Edited and documented query function as needed to accommodate search dashboard

5/3/23 - **Database: Querying** A well-documented query function with instructions for replicating and editing queries in the future

5/3/23 - **Hosting** Detailed documentation for maintaining the database

5/3/23 - Complete project
