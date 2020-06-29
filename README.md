# Calendario
Calendar app that calculates the total of hours worked from the amount of hours worked each day

To create a calendar and start working, a year, the day of the week that that year starts on and an amount of hours to work need to be established.
Once we set these three values, a calendar will show up and we can set any amount of hours on each day and it'll sum up to tell you the difference between the amount of hours that you work and the amount of hours that you have to work.
To set an amount of hours into a cell, insert the amount and press ENTER.

Once the calendar has been created, when the app starts it's possible to open a previous calendar by inserting the year of the calendar that you want to open.

The day of the week is specified in spanish:
  - Lunes
  - Martes
  - Miercoles
  - Jueves
  - Viernes
  - Sabado
  - Domingo
  
Calendars are saved in json format in the <data> directory as .sv(it stands for save) files. If it doesn´t exist, it will be created automatically.
There´s some examples of data files in this repository.
  
Tkinter is needed to run this app. Tkinter is included in the python standard library.
The json library is also needed.

To run the app, just execute the app_calendario.pyw file. It can be done by double-clicking it or by using the following command:
python/python3 app_calendario.pyw

python is used when python3 is installed as the only python version in the system. If there´s other versions of python installed, it's necesary to use python3.
