This program is designed for calculating the average ping to a given server during given time
It creates a table every *5* minutes and sends it to your Skype so that you could always see
the visualized picture of your ping. 

In the end it forms a simple .csv file for you to be able to analyze the data yourself using 
modern tools like R or Python plot libraries. 

The program might take three arguments, namely: 
-url that allows you defining the targeted server. Default "https://google.ru
-c in which you define the amount of tries to get the average ping. Default - 5
-time specifies the working time of the program. Default is 60 minutes. 

To get help type -h or -help. 
