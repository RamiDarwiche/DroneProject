# About

This repository stores the code for a project completed in Spring 2023 at the University of Florida exploring the use of hand gesture-based flight and voice commands as a new drone control modality for improving construction site safety. This project used tensorflow and cvzone to train a hand gesture recognition model that mapped specific gestures to flight controls based on thousands of novel images processed through Google's Teachable Machine website. This hand gesture recognition algorithm then used SQLite to interface with an Unreal Engine project that simulated drone flights based on real-time data read from the SQLite database and parsed into C#. This project was presented to a board of PhD candidate researchers and University of Florida professors upon its completion. It has since been referenced as teaching material in a graduate-level course.

Instructions:

# Drone-Project

Things to download:
Pycharm 2022.3.1
  https://www.jetbrains.com/pycharm/download/other.html
  download sqlite3, cvzone, and tensorflow packages
  check sqlite file paths in python scrip
  .keras file in Model folder
  
Sqlite3
  https://www.sqlite.org/download.html
  https://sqlitebrowser.org/
  PRAGMA journal_mode wal;
  
 Visual studio
    2022, set as main IDE in unity
 
 Unity editor V. 2021.3.22f1
   drag user settings and assets
   check VS code and pycharm code for DB path 
   make sure mono.sqlite is in assets
   
   Unity assets: https://drive.google.com/drive/folders/1fGXCOg1wCecwOAFC6Yj0mYJm6CrbxBPr?usp=sharing
