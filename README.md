Demonstration of a Deployed Recommender System
==============================
The recommender and visualization can be found here:
http://52.14.98.50:5000/recommender

This project is best summarized by its parts:
1. deployment of a factorization machine recommender in a production environment. This includes:
    * Building a deployable factorization machine recommender
    * Building a RESTFUL API for hosting a factorization machine recommender

2. Building front-end UI for visualizing recommendations and similar items. The visualizations built include:
    * [Tool to compare personalized and popularity recommendations](http://52.14.98.50:5000/recommender)
    * [Tool for finding similar movies](http://52.14.98.50:5000/similar_movies)

## Building a deployable factorization machine recommender
To demonstrate the deployment of a factorization machine model, I utilize a well studied dataset of [10M interactions between users and movies](http://files.grouplens.org/datasets/movielens/ml-10m-README.html)). I began by first exploring the dataset, followed by implementing methods to clean and prepare the data, and finally modeling. To build the recommendation models, I utilize factorization machine algorithms via [lightfm](http://lyst.github.io/lightfm/docs/home.html), a wonderful library written by Maciej Kula. Further reading can be found [here](https://arxiv.org/pdf/1507.08439.pdf). Upon building a suitable model, I consolidated the preprocessing and modeling code into a single python class labelled [FM](https://github.com/jscottcronin/recommender_deployed/blob/master/app/models/fm.py). This class was designed for a simplified deployment process.

Jupyter was utilized in the development stage. Some [notebooks](https://github.com/jscottcronin/recommender_deployed/tree/master/notebooks) of interest are:
* [Exploratory analysis](https://github.com/jscottcronin/recommender_deployed/blob/master/notebooks/Downloading%20data%20and%20exploratory%20analysis.ipynb) for defining cleaning and preprocessing requirements.
* [Performance analysis](https://github.com/jscottcronin/recommender_deployed/blob/master/notebooks/Performance%20Analysis%20of%20Factorization%20Machine%20Model.ipynb) of factorization machine models compared to a popularity baseline
* [Similar Item Analysis](https://github.com/jscottcronin/recommender_deployed/blob/master/notebooks/Analyzing%20Item%20Similarities.ipynb) calculated via cosine similarity of factorization machine embedding vectors

Next, a deployable [`train.py`](https://github.com/jscottcronin/recommender_deployed/blob/master/app/train.py) script was built. This script executes the following components:
1. ingests data
2. preprocesses data
3. trains factorization machine
4. serializes factorization machine to disk

Once a model is serialized and stored to disk, it's time to build a RESTFUL API for hosting it.

## Building a RESTFUL API for hosting a factorization machine recommender
For real time recommendations, a trained model must be loaded into a server's memory and called behind a RESTFUL endpoint. To setup the server and endpoints, I utilized [Flask](http://flask.pocoo.org/). The app server code can be found in [`app_svc.py`](https://github.com/jscottcronin/recommender_deployed/blob/master/app/app_svc.py).  We create the following endpoints on our server for real time requests:
* [`rec_predict`](https://github.com/jscottcronin/recommender_deployed/blob/master/app/app_svc.py#L20-L44) - for both personalized and popularity recommendations
* [`get_historical_likes`](https://github.com/jscottcronin/recommender_deployed/blob/master/app/app_svc.py#L46-L60) - to see what a user has liked in the past
* [`get_similar_movies`](https://github.com/jscottcronin/recommender_deployed/blob/master/app/app_svc.py#L70-L83) - to find similar movies to one you input

## Building front-end UI for visualizing recommendations and similar items
Also built into the app server are routes for visualizing the results of the deployed recommender. Specifically, two routes are defined in the server:
1. http://52.14.98.50:5000/recommender where the route is defined by [this server code](https://github.com/jscottcronin/recommender_deployed/blob/master/app/app_svc.py#L14-L18)
2. http://52.14.98.50:5000/similar_movies where the route is defined by [this server code](https://github.com/jscottcronin/recommender_deployed/blob/master/app/app_svc.py#L14-L18)

The GET requests at these routes return a static html. Javascript is utilized to interact with html and make async POST requests to the real-time recommendation endpoints described above. It also enables a nice user experience for engaging and interacting with the deployed recommender model.
* [HTML code can be found here](https://github.com/jscottcronin/recommender_deployed/tree/master/app/templates)
* [Javascript can be found here](https://github.com/jscottcronin/recommender_deployed/tree/master/app/static/js)
* [CSS can be found here](https://github.com/jscottcronin/recommender_deployed/tree/master/app/static/css)
