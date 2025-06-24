# SteamAppDataVisulisation

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Data Collection](#data-collection)  
   - [Steam API](#steam-api)  
   - [Steam Spy API](#steam-spy-api)  
   - [Links to dataset](#links-to-dataset)  
3. [Data Cleaning & Preprocessing](#data-cleaning--preprocessing)  
4. [Exploratory Data Analysis (EDA) & Visualisations](#exploratory-data-analysis-eda--visualisations)  
5. [Machine Learning](#machine-learning)  
6. [Usage](#usage)  
7. [Future Work](#future-work)   

## Project Overview

This project will explore trends and patterns within PC video games released on Steam. A comprehensive EDA will be performed to pick out trends over the Years.

Additionally, a multi-class machine learning tool will be created to assess the viability of using the features within the dataset to predict how well users receive a game by targeting the user-review score (Self made feature, aggregating the reviews of the game into groups, i.e 'Positive,', 'Very Positive'. 'Negative' etc)

## Data Collection

### Steam API

The Steam API was used to collect data from 348,312 app's on steam

This process was completed using a Python script to automatically call the Steam API to collect this information, which was placed on an Amazon Web Service (AWS) machine to complete, a process which took 2 and a half weeks due to steams strict API limits, which frequently resulted in HTTP error 429 (too many requests) imposing 5-minute timeouts.

### Steam Spy API

Once the Steam data was collected, it was determined that this dataset was lacking in features to perform a comprehensive EDA and partake in a machine learning tool.  

To resolve this Steam Spy's API was used to collect additional information using a similar Python script to append this data onto the steam data. 

Steam Spy gathers daily data from Steam regarding player numbers, providing additional information to explore in order to learn if any clear correlations exist that indicate if a game is likely to be successful.  

Although Steam Spy's API requests we're more generous than Steams (comfortably allowing 1 request per second), non-games (software, DLC, movies) from the original SteamExport.csv dataset were excluded to cut down on the time required for the Python script to complete.

This is the final version of the dataset which will be explored, which contains 94,955 records (prior to data cleaning). The original dataset from Steam without the Steam Spy data is also linked below, but unused further in this project.

### Links to dataset:

The datasets collected, are publicly available here: (Updated as of December 2024)

- **SteamSpyExport.csv** (513 MB) (Primary dataset used)  
  [⬇️ Download SteamSpyExport.csv](https://www.dropbox.com/scl/fi/zbgdcx9en8mifvaox0a02/SteamSpyExport.csv?rlkey=uuw89urezjobf5asg82e70shz&st=jgcefz9v&dl=0)

- **SteamExport.csv** (134 MB)  
  [⬇️ Download SteamExport.csv](https://www.dropbox.com/scl/fi/31mj1eny5wdo15vleocvc/SteamSpyExport.csv?rlkey=npkf91iqte0ebezcyrkosmsxz&e=1&st=5xid3gwy&dl=0)

## Data Cleaning & Preprocessing

## Exploratory Data Analysis (EDA) & Visulisations

## Machine Learning

## Usage

The dataset used is the SteamSpyExport.csv containing all neccecary data to run the Python script. The links to download them via Dropbox is located [here](#links-to-dataset).

## Future Work