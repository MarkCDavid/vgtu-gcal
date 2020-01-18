# vgtu-gcal
Converts VGTU timetable HTML files into CSV files that you would be able to import to Google Calendar.

## Getting Started

### Python Virtual Environment

Once you clone/download the project, I suggest launching the script from a Python virtual environment.

To set it up, navigate to the project directory and run:

```
python -m venv <enviroment-name>
```

This command creates a virtual environment for you, so that your native Python environment does not get cluttered.

To activate:

#### Windows

```
<enviroment-name>/Scripts/activate.bat
```

#### Linux

```
source <enviroment-name>/Scripts/activate
```

### Dependencies

This project uses several dependencies, named in [requirements.txt](requirements.txt) file. 

To install these dependencies run:
```
pip install -r requirements.txt
```

Once installed, you will be able to start using the script.

## Usage

### HTML Files

Unfortunetaly, as VGTU is using SAML SSO for authentication it is not trivial to authenticate a user to automatically fetch the required data. As such, there is no authentication supported as of yet.

#### Getting the correct files

Because of missing authentication, you will have to fetch the HTML files yourself.
1. Login to mano.vgtu.lt
2. Navigate to Studies -> Lecture schedule (Studijos -> Paskaitų tvarkaraščiai)
3. Select GROUPS (GRUPĖS) tab and make a query for a schedule
4. Once it appears, save the entire page as a complete webpage

Now you will be able to use this downloaded file (along with *_files folder) to generate Google Calendar CSV file.

##### NOTE

I have not tested the other types of schedules (FACULTY, COURSE, TEACHER) using this script, but as the format for the tables seem similar, it is possible that it will work just fine. If any issue arises, go ahead and create an issue request.

### Script

#### Usage
```
app.py [-h] [--simple] [--nogroups] input output

positional arguments:
  input       input HTML file
  output      output HTML file

optional arguments:
  -h, --help  show this help message and exit
  --simple    course code and additional information in parentheses are discarded from the subject
  --nogroups  subgroups are discarded from the subject
```

#### Flag examples

##### --simple

Removes any information that is not neccessary to know, what kind of a subject it is.
###### Command
``` 
app.py input.html output.csv 
```
###### Subject format
```
Human's Safety at Events (STGSB17060) gr. 0 (Lectures)
Entertaining Events Practicum in Human Safety (course project) (STGSB17061) gr. 0 (Practical exercises)
```

###### Command
``` 
app.py input.html output.csv --simple
```
###### Subject format
```
Human's Safety at Events gr. 0 (Lectures)
Entertaining Events Practicum in Human Safety gr. 0 (Practical exercises)
```

##### --nogroup

Removes subgroup information from output
###### Command
``` 
app.py input.html output.csv 
```
###### Subject format
```
Human's Safety at Events (STGSB17060) gr. 0 (Lectures)
Entertaining Events Practicum in Human Safety (course project) (STGSB17061) gr. 0 (Practical exercises)
```

###### Command
``` 
app.py input.html output.csv --nogroup
```
###### Subject format
```
Human's Safety at Events (STGSB17060) (Lectures)
Entertaining Events Practicum in Human Safety (course project) (STGSB17061) (Practical exercises)
```

### Google Calendar

Prior to importing the CSV, I suggest creating a separate calendar and importing the CSV there.

Unfortunately, Google Calendar does not provide a possibility to import recurring events using CSV, so if you import the data to your main calendar and then decide that you do not need it, you would have to remove the events one by one.

## Future plans

- If any issues arise, fix them.
- Add a possibiliy to specify certain lectures to be ignored
    - Say if you have optional lectures and you have not signed on to them, they could be ignored
- Add additional flag to only remove 0-th groups from the subject as it is redundant information.