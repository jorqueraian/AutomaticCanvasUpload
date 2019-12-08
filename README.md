# AutomaticCanvasUpload
Given a submission file, this tool utilizes the python library [CanvasAPI](https://github.com/ucfopen/canvasapi) to find all courses a student is currently enrolled in. It then compares all upcoming or undated assignments with the provided submission file name using a dynamic programming sequence alignment algorithm. With the best match, the file provdided will be uploaded.

## Usage
This script requires a json file with student Canvas API token. Follow [these](https://community.canvaslms.com/docs/DOC-10806-4214724194) instructions to optain a token.
The formatting of the `credentials.json` file should be as follows
```json
{
  "type": "Canvas",
  "auth_token": "<Canvas API Token>",
  "student_email": "<student email address>",
  "api_url": "<Canvas URL ex. https://canvas.colorado.edu/>"
}
```
Currently `student_email` is not used.
