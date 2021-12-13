**Authors**: CARAYON Chloé - SPATZ Cécile (BD2)
**Date**: 13/12/2021
___
# Sentiment analyser
___

This project aims to apply some concepts and tools seen in the course Data Engineer at EFREI.
In order to run it, please install and configure poetry.

## Getting Start
---

- We use poetry for our environment. 
One can use the already build environment OR re-install it:
``` 
make install
```
if issues, delete poetry.lock and re run the command above.


- To clean the code for production:
``` 
make check
```

- Jira as project management tool test: 
https://cecilespatz.atlassian.net/jira/software/projects/DEP1/boards/1

###  Classical ML project
- Run project
``` 
make run_ml
```

- test project 
``` cd app ```
then 
``` poetry run  python -m unittest  ```

- Sphinx documentation [here](https://github.com/ChloeCarayon/Sentiment_analyser_app/blob/master/docs/build/html/index.html)

- generate requirements.txt
``` poetry export --without-hashes -f requirements.txt --output requirements.txt ```


<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>


### Flask interface
- Run project
``` 
make run
```

### Dockerization 

- dockerize
``` docker build -t flask_app_project .  ```

- run docker image 
``` docker run -p 5000:5000 ImageID ```