# MacdFollower
Hello, in here I have shared some scripts that helped me getting to know good buy and sell opportunities. Of course there can also be a lot of improvements and I would like to what are those that you suggest.
# How to use
I am assuming you already have Anaconda and git installed since you will need to use a set of instructions in order to get this to work.
The instructions are in the instructions.txt file but I am so gentle that i am pasting its content here:

After having git and anaconda installed, write or paste the following lines in the terminal: (don´t forget that you will say yes after some of those lines are processed)

- git clone https://github.com/numerocat/MacdFollower.git
- conda create --name macd python=3.7
- conda activate macd
- pip install yahoo_fin
- pip install matplotlib

Now, you are all set to write:

- python realtimeMACD.py

and you will get the stocks with a good buy or sell opportunity

# How to change the companies being checked:

In the script realtimeMACD.py there is the list of the tickers that are being analized, you can manually change those.







*Remember that this is intended to be used for your investigation, do not base all your investing in some random scripts.*

