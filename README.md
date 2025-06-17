# SteamAppDataVisulisation

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Data Collection](#data-collection)  
   - [Steam API](#steam-api)  
   - [Steam Spy API](#steam-spy-api)  
3. [Data Cleaning & Preprocessing](#data-cleaning--preprocessing)  
4. [Exploratory Data Analysis (EDA) & Visualisations](#exploratory-data-analysis-eda--visualisations)  
5. [Machine Learning](#machine-learning)  
6. [Usage](#usage)  
7. [Future Work](#future-work)  
 

## Project Overview

This project will explore trends and patterns within PC video games released on Steam. A comprehensive EDA will be performed  
Additionally, a multi-class machine learning tool will be created to assess the viability of using the features within the dataset to predict how well users receive a game by targeting the user-review score (Self made feature, aggregating the reviews of the game into groups, i.e 'Positive,', 'Very Positive'. 'Negative' etc)

## Data Collection

### Steam API:
[Include details about how the python script calling the steam API worked]  
The Steam API was used to collect data from 348,312 app's on steam (Dataset as of December 2024)  
This process was completed using a Python script to automatically call the Steam API to collect this information, which was placed on an Amazon Web Service (AWS) machine to complete, a process which took 2 and a half weeks due to steams strict API limits, which frequently resulted in HTTP error 429 (too many requests) imposing 5-minute timeouts.

### Steam Spy API
Steam Spy gathers daily data from steam regarding player numbers, providing additional information to explore in order to learn if any clear correlations exist that indicate if a game is likely to be successful.  
Once the Steam data was collected, it was determined that this dataset was lacking in features to perform a comprehensive EDA and partake in a machine learning tool.  
To resolve this Steam Spy's API was used to collect additional information using a similar Python script to append this additional data onto our steam data.  
Although Steam Spy's API requests we're more generous than Steams (comfortably allowing 1 request per second), non-games (software, DLC, movies) from the original SteamExport.csv dataset were excluded to cut down on the time required for the Python script to complete.

This is the final version of the dataset which will be explored.

## Data Cleaning & Preprocessing

## Exploratory Data Analysis (EDA) & Visulisations

## Machine Learning

## Usage
The dataset used is the [SteamSpy.csv](Data/SteamSpyExport Dropbox.csv), containing all neccecary data to run the Python script.

## Future Work