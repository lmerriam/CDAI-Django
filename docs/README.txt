########################################################################################################################
############################################## CDAI Django Project #####################################################
########################################################################################################################

Author: ztorstri
Owned By: loganme

This project is a simple Django project to compute and graph CDAI scores. It consists of 4 urls, as follows:

1) /login - Used to log into the site.
2) /user-profile - Used to create a new user and user profile on the site. User profile creation is open to the public
   and not moderated by an administrator.  Users must have an account to utilize the site.
3) /questionnaire - Used to fill out the Chron's Disease Activity Index questions, including a date for the questions.
   The questions are then linked to the user and saved in the database, and later retrieved and graphed.
4) /questionnaire/graph - Used to graph the CDAI score over time for the currently logged in user. Makes use of the
   javascript library Highcharts.

   This project uses Highcharts, jquery 1.10.2, Django 1.5, and python 2.7.