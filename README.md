Getting Started

Dependencies:
    Python: 3.6.7rc2

PIP Dependencies

 pip install -r requirements.txt

 Key Dependencies:
Flask is a lightweight backend microservices framework. Flask is required to handle requests and responses.

SQLAlchemy is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

Flask-CORS is the extension we'll use to handle cross origin requests from our frontend server.

Database Setup:
  Manually create database using PgAdmin4 named as trivia;

  Create two tables named as Questions and Categories;

  Question Table Querry:
  

  CREATE TABLE IF NOT EXISTS public.questions
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    question text COLLATE pg_catalog."default",
    answer text COLLATE pg_catalog."default",
    difficulty integer,
    category integer,
    CONSTRAINT questions_pkey PRIMARY KEY (id),
    CONSTRAINT questions_category_fkey FOREIGN KEY (category)
        REFERENCES public.categories (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.questions
    OWNER to postgres;

Command to create categories table
CREATE TABLE IF NOT EXISTS public.categories
(
    id integer NOT NULL,
    type text COLLATE pg_catalog."default",
    CONSTRAINT categories_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.categories
    OWNER to postgres;


enter the following data inside questions table:

5	Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?	Maya Angelou	2	4
9	What boxer's original name is Cassius Clay?	Muhammad Ali	1	4
2	What movie earned Tom Hanks his third straight Oscar nomination, in 1996?	Apollo 13	4	5
4	What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?	Tom Cruise	4	5
6	What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?	Edward Scissorhands	3	5
10	Which is the only team to play in every soccer World Cup tournament?	Brazil	3	6
11	Which country won the first ever soccer World Cup in 1930?	Uruguay	4	6
12	Who invented Peanut Butter?	George Washington Carver	2	4
13	What is the largest lake in Africa?	Lake Victoria	2	3
14	In which royal palace would you find the Hall of Mirrors?	The Palace of Versailles	3	3
15	The Taj Mahal is located in which Indian city?	Agra	2	3
16	Which Dutch graphic artist–initials M C was a creator of optical illusions?	Escher	1	2
17	La Giaconda is better known as what?	Mona Lisa	3	2
18	How many paintings did Van Gogh sell in his lifetime?	One	4	2
19	Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?	Jackson Pollock	2	2
20	What is the heaviest organ in the human body?	The Liver	4	1
21	Who discovered penicillin?	Alexander Fleming	3	1
22	Hematology is a branch of medicine involving the study of what?	Blood	4	1
23	Which dung beetle was worshipped by the ancient Egyptians?	Scarab	4	4


enter the following data in the categories table:

1	Science
2	Art
3	Geography
4	History
5	Entertainme



From backend folder run the following commands:
export FLASK_APP=flaskr
export FLASK_ENV=development
python -m flask run



API

GET/categories Fetches a dictionary of all available categories

Request parameters: none
Example response:
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}

GET \questions?page=<page_number> Fetches a paginated dictionary of questions of all available categories

Request parameters (optional): page:int
Example response:
 "categories": {
   "1": "Science", 
   "2": "Art", 
   "3": "Geography", 
   "4": "History", 
   "5": "Entertainment", 
   "6": "Sports"
 }, 
 "current_category": null, 
 "questions": [
   {
     "answer": "Maya Angelou", 
     "category": 4, 
     "difficulty": 2, 
     "id": 5, 
     "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
   },  
   {
     "answer": "Escher", 
     "category": 2, 
     "difficulty": 1, 
     "id": 16, 
     "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
   }
 ], 
 "success": true, 
 "total_questions": 2
}
DELETE /questions/<question_id> Delete an existing questions from the repository of available questions

Request arguments: question_id:int
Example response:
{
  "deleted": "28", 
  "success": true
}
POST /questions Add a new question to the repository of available questions

Request body: {question:string, answer:string, difficulty:int, category:string}
Example response:
{
  "created": 29, 
  "success": true
}
POST /questions/search Fetches all questions where a substring matches the search term (not case-sensitive)

Request body: {searchTerm:string}
Example response:
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Lisbon", 
      "category": 2, 
      "difficulty": 1, 
      "id": 29, 
      "question": "What is the capital of Portugal?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
GET /categories/<int:category_id>/questions Fetches a dictionary of questions for the specified category

Request argument: category_id:int
Example response:
{
  "current_category": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
  ], 
  "success": true, 
  "total_questions": 2
}
POST /quizzes Fetches one random question within a specified category. Previously asked questions are not asked again.

Request body: {previous_questions: arr, quiz_category: {id:int, type:string}}
Example response:
{
  "question": {
    "answer": "The Liver", 
    "category": 1, 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }, 
  "success": true
}