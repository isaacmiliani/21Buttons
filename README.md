# 21Buttons
Mastermind Board Game

# Setup
1. Create Docker image:
   docker build . -t 21buttons/mastermind:v1.0 
2. Make Migrations:
  python manage.py makemigrations
3. Migrate
  python manage.py migrate
4. Create users:
  python manage.py createsuperuser --email admin@example.com --username admin
5. USe Postman to test the API
  * Import 21Buttons.postman.collection.json y Test.postman_environment.json into Postman
6. API calls from Postman:
  * Login
  * New Game
  * POst Play
  * All games
7. TODO: API documentation with Swagger 

