# mySAM
Backend Development Test - Check with 'hello-sam' directory contains implementation of below requirements and Bonus.

[![link package][ddb-image]][package-url]


## Requirements

> Started with this sample project https://serverlessland.com/patterns/apigw-lambda-dynamodb that has a simple lambda function that puts data into a DynamoDB table

-	Amend the lambda function so that “id” and “Weather” are passed into the function in some JSON in the request body, rather than being hardcoded — <b>Done</b>

-	Add a validation that “id” and “Weather” are in the request body before updating DynamoDB. An error message should be returned if either attribute is missing  — <b>Done</b>

-	Add a validation that “id” and “Weather” are the only attributes in the request body. An error message should be returned if any other attributes are present  — <b>Done</b>

-	Add a unit test for the lambda function that tests a successful update and the two validations that have been added  — <b>Done</b>

-	The unit test needs to be repeatable and can be executed automatically using pytest  — <b>Done</b>

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

> Note: All changes are deployed and tested in AWS

[ddb-image]: https://docs.aws.amazon.com/images/apigateway/latest/developerguide/images/ddb-crud.png
[package-url]: https://github.com/RajaSakthiyan/mySAM/tree/main/hello-sam


---

## Run the Unit Test
[unit_test.py](hello-sam/tests/unit_test.py) 

> install pipenv, for more information visit https://pipenv.pypa.io/en/latest/#install-pipenv-today

```shell
# environment variables are need not to be valid.
cd tests
export AWS_ACCESS_KEY_ID=xxxxxxx
export AWS_SECRET_ACCESS_KEY=xxxxxxx
export AWS_DEFAULT_REGION=xx-xxx-2
pipenv install
pipenv shell
pytest unit_test.py
```