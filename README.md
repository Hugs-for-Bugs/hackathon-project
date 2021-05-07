# hackathon-project
This bot was created to search for vacancies by a team of young developers «Hugs for bugs». The bot was developed to solve a social problem - unemployment as part of the Hackathon 2021 project.
Bot functionality:
1) For the employer
-  the ability to add the vacancies;
-  the ability to add the contact information (phone, email, site link)
-  the ability to change location.
2) For employee
-  the ability to search for a job online;
-  the ability to search for a job from vacancies which were added to the bot database;
-  the ability to change location.

How to start?
You need to install using pip bs4, lxml, pytelegrambotapi, dotenv packages, create .env in project folder and write token (BOT_TOKEN) and database path (DATABASE), and then run with python run.py

```shell script
cd project
touch .env
echo "BOT_TOKEN=<YOUR_BOT_TOKEN>" > .env
echo "DATABASE=<DATABASE_NAME>" >> .env
cd ..
python3 run.py
```
