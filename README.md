# mySAM
Backend Development Test


## Requirements

-	Amend the lambda function so that “id” and “Weather” are passed into the function in some JSON in the request body, rather than being hardcoded — <b>Done</b>

-	Add a validation that “id” and “Weather” are in the request body before updating DynamoDB. An error message should be returned if either attribute is missing  — <b>Done</b>

-	Add a validation that “id” and “Weather” are the only attributes in the request body. An error message should be returned if any other attributes are present  — <b>Done</b>

-	Add a unit test for the lambda function that tests a successful update and the two validations that have been added  — <b>In-Progress</b>

-	The unit test needs to be repeatable and can be executed automatically using pytest  — <b>In-Progress</b>

-	Add a second lambda function that can be used to delete a record from the DynamoDB table -  — <b>Done</b>

-	This lambda function should be added to template.yaml. It should use HTTP method DELETE -  — <b>Done</b>

-	Add an authorizer to the API. This should be a simple token-based authorizer that will allow access if the bearer token “allowme” is passed with the HTTP request  — <b>Done</b>

-	Access should be denied if this token is not passed with the HTTP request  — <b>Done</b>

 
## Bonus

-	Amend the DynamoDB table definition to set a partition key of ‘id’ (string) and enable deletion protection  — <b>Done</b>

-	Enable CORS on the API to
    - Allow methods OPTIONS, GET, POST and DELETE  — <b>Done</b>
    - Allow headers of Content-Type, X-Amz-Date, Authorization and X-Api-Key — <b>Done</b>
    - Allow any origin — <b>Done</b>

-	Amend the Lambda functions to reference an environment variable for the DynamoDB table name (passed from template.yaml) instead of using a hard-coded name — <b>Done</b>
