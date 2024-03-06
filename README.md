# Satellogic - Satellite Task Selector

System to find the 'higher profit' subset in a list of tasks.

## How to use it?

### Using docker-compose

1. Clone this repo.
2. Execute `docker-compose up -d --build`
   This will set up the database, run migrations and run the server.
3. The server will be up in port 8000 and the database in port 54321

### Without Docker

1. Clone this repo
2. Go back one folder and create a virtual env `python -m venv venv`
3. Placed in the root folder of the repo, install requirements with `pip install -r requirements.txt`
4. Create a new PostgreSQL database called 'satellogic_tasks_db'
5. Setup your database configuration in the satellogic/settings.py file. Lookup for the 'DATABASES.default' dictionary
6. Placed in the root folder run `python manage.py migrate` and `python manage.py runserver`
7. The server will be up in port 8000

## Available endpoint

POST `localhost:8000/api/tasks`

Expected body:
```
[
  { "name": "the name of the task,
    "resources": [ "resources", "required", "for", "task" ],
    "profit": 0.8 // A positive number
  }
] 
```

Succesful response template:
```
{
  "tasks": [ // List of tasks of the 'higher profit' subset ],
  "resources": [ // List of the resources involved in all tasks ],
  "total_profit": 9.5 // Sum of the profit of the tasks subset
}
```

## How does it work?

I am proposing to different solutions:

### Solution 1: Exploring *all* possible subsets of compatible tasks

This solution creates all the possible combinations of tasks from the input, excluding those with conflicting tasks.
While creating the combinations, it tracks the higher profit to find the maximum.

### Solution 2: Exploring *some* possible subsets of compatible tasks

This solution explores only some possible subsets of compatible tasks.
At first, it sorts the tasks by profit and then searches for compatible tasks starting from one different task at a time.

### Some discussions about the solutions

While solution 1 ensures that it will find the subset with the actual highest profit, in the worst cases it has an O(2^n) time complexity. So it doesn't work for larger inputs.
Even though solution 2 doesn't explore all the possible combinations, it has a considerable lower time complexity (On^2). Also, even if it doesn't ensure finding the 'highest' subset, it seems like solution number 2 also works fine getting an approximation to it, as shown in the graphs below.

In these graphs we can see the results of a little simulation of how both solutions behave with increasing length of the input. We can see that solution 2 tends to find the 'highest' subset in much less time. Also, the times it found a subset with a profit lower than the actual maximum, the differences are small.

![image](https://github.com/melisaguevara/satellogic_code_challenge/assets/56703907/005cf57e-30d1-409c-b76c-5a044d39c694)

![image](https://github.com/melisaguevara/satellogic_code_challenge/assets/56703907/e91a4ec4-677a-4782-8e5d-e1227ad1e5a5)

Other options might include storing the task list as a graph. They would be worth exploring if their time complexity is lower than O(n^2).
