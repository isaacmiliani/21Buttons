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
5. Test API con Postman
  Importar 21Buttons.postman.collection.json y Test.postman_environment.json al cliente de postman
6. Desde Postman ejecutar las siguientes llamadas:
  * Login
  * New Game
  * POst Play
  * All games
7. TODO: Documentar la API con Swagger 

