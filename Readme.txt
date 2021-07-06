				Phases of the project
# Brainstorming 
The end result of this project is an Algorithmic trading bot that can make optimal/sub-optimal trading decisions in the inhouse simulated environment. The simulated stock market is created using data scraped from yahoo finance web portal. The API for the same is deprecated and scraping it is one of the way around for me. 

The bot will be trainned using Reinforcement learning paradigm which allows for optimization of actions based on the reward received from the simulator. 

The architecture of the project can be thought as two isolated environments communicating through the gateway. The components are Simulator and Trading bot, which will use the rest API to communicate with one another.

The simulator is planned to be developed in such a way that it can be beneficial and usable outside the scope of this project and same design thinking is put into the Trading bot as well. This is important for me that even though someone who wants to test either their own market condition or machine learning model, cannot feel left out and can build upon either of the components of this project.

For the sake of experimentation I will be incorporating some subset of RL as well as some other timeseries forecasting models into the test so as to benchmark the RL baed solution with respect to traditional models.

# Data-collection
The first and foremost module that I am starting to work upon is responsible for scarping the yahoo finance web site and retrive the stock market data which meets the specified condition and shall be returned in the Pandas dataframe format suitable for furthur analysis.
