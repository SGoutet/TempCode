# AI usage Report

## Prompt
You are tasked with developing a REST service that a bank would use. You can use a python FastAPI service for users management. Each user should be able to sign up to the API. A user should be able to sign in after having signed up. Signing in creates and returns a session token. The API will rely on a single DB for now. Users should be recorded in a database table. Sessions should be recorded in a separate table, and contain the user name, each session start time and max time. Sessions will be limited to a maximum of 1 hour. If an existing valid session exists, do not create a new one.
User should log in with a user id and password that they give at sign up. Passwords should be stored and compared hashed with Argon2 algorithm. User ids and passwords should match before a session is created. 
Follow context7 and agents.md guidelines

# Tools
I used cursor

# Challenges
Lack of time to complete the assignement 
Lot of time spent testing and debugging. I could not get to the interesting parts :(

