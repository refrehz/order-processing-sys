# order-processing-sys
Order Processing System built with FastAPI, SQLite, and Docker. I built database on SQLite because of I wanted to improve myself on SQL queries.

## src/
"src/" folder includes source codes for microservice application. API backend for all endpoints, database config file, and __main__.py script which contains essential codebase to run application.

## test/
I created a "test/" directory exclusively for running tests. I meticulously crafted tests for each endpoint I developed. The only minor inconvenience is that some of these tests can only be executed once, requiring manual modification of the test.sh file if you wish to rerun them.

## .sh files
The project includes two shell script files. One is for running application on docker, and other one is for running tests.

## improvements
It could be more complex and could be include more functionalities than current ones. I also had in mind to use logging too, but I didn't(at least for this project).

## running app
Your local device should have Docker and Python installed. You can simply run project by running run.sh script. It will install everything inside docker container and application will run inside of it
