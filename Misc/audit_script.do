* Timing of interview questions
egen timeinterview = rowtotal (Q1-R26)
egen timeclosing = rowtotal (end-colori)

****Age
* copy age from the file with substantive info and paste it here (into the time file)
rename Q2Y_01 yearborn
gen Age = 2015 - yearborn

**** Sex
* copy, paste sex
gen Gender = "Male" if Q1_01 == 1
replace Gender = "Female" if Q1_01 == 2

**** Difference time
gen ti = minutes(FECHA_FIN-FECHA_INI)

**** seconds to minutes
gen timeinterviewmin=timeinterview/60
gen timeclosingmin=timeclosing/60

***** Report
sum timeinterviewmin tiempo

*** device for gps
tab dispositivo if latitud==0 | longitud==0
tab dispositivo

*** interview gps
tab encuestador if latitud==0 | longitud==0
tab encuestador

* rename stuff
rename FECHA_INI Start_Date
rename FECHA_FIN End_Date
rename encuestador Interviewer
rename ED_9 Pin_Number
rename timeinterviewmin Interview_Time

**** use partial names for ED, Parish so that it will work for both antigua and St Kitts without modifying the script
* interview length
br ID_TOMA Interviewer Start_Date End_Date Pin_Number Parish_9 tiempo Interview_Time timeclosingmin ti Gender Age if Interview_Time < 20
* GPS Missing
br ID_TOMA Interviewer Start_Date End_Date Pin_Number Parish_9 Interview_Time Gender Age if latitud==0 | longitud==0
* age missing
br ID_TOMA Interviewer Start_Date End_Date Pin_Number Parish_9 Gender Age if yearborn < 100
* sex missing
br ID_TOMA Interviewer Start_Date End_Date Pin_Number Parish_9 Gender Age if Gender != "Male" & Gender != "Female"

** interviews per day
gen interview_date = dofc(Start_Date)
by interview_date, sort: tab Interviewer

