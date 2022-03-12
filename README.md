# OGE-ESIREM-API

## Introdution
API to retrieve the number of grades on the OGE website (Website listing the grades of students) to know if a new grade is available. If a new grade has been entered, the program sends a notification e-mail with the subject.

## Why ?
I decided to do this program because we had to wait until the end of the semester to get our grades and we wanted to know when they would be in.

## How it's work
The program connects to my OGE account and then goes to the summary page of my grades. Then it retrieves all the subjects and their respective number of grades. Then it compares with the data.json file if the number of grades per subject is consistent otherwise it sends me an email. On my raspberry pi, I made a "crontab" command which execute my python script every 10 minutes.

## Final render
### Display of subjects in the console
![alt text](https://github.com/Orchanyne/API-OGE-ESIREM/blob/main/result.png)
### Mail sent when there was a new subject
![alt text](https://github.com/Orchanyne/API-OGE-ESIREM/blob/main/email.png)
