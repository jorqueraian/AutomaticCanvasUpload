# AutomaticCanvasUpload
Given a submission file, this tool utilizes the python library 
[CanvasAPI](https://github.com/ucfopen/canvasapi) to find all courses a student is 
currently enrolled in. It then compares all upcoming or undated assignments with the 
provided submission file name using a dynamic programming sequence alignment algorithm. 
With the best match, the file provdided will be uploaded.

## Usage
This script requires a json file with student Canvas API token. Follow 
[these](https://community.canvaslms.com/docs/DOC-10806-4214724194) instructions to 
obtain a token. The formatting of the `credentials.json` file should be as follows
```json
{
  "type": "Canvas",
  "auth_token": "<Canvas API Token>",
  "student_email": "<student email address>",
  "api_url": "<Canvas URL ex. https://canvas.colorado.edu/>"
}
```
Currently `student_email` is not used.

### Building and using script
These scripts can be converted to .exe files using [PyInstaller](https://pypi.org/project/PyInstaller/).
Once Converted, and credentials file is put in dist folder, Desired files for upload 
can be dragged onto the exe file. 

### Naming files for submission
Naming the files is the most important part. Files for upload should contain the 
course code and the name of the assignment. For example if I wanted to submit my 
work for the assignment, **Homework 2** for the course with code **APPM 2350** I 
would want to name the desired file **APPM_2350_Homework2.pdf**. For assignments with 
long names like **Lab 1 - Initial System Setup** a shortened version of the assignment, 
**Lab 1** is acceptable, But may result in incorrect results. 
