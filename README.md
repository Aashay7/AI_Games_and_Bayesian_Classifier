# CSCI-B551 FA2021 Assignment 2 Games and Bayesian Classifiers

### Group Members: Aashay Gondalia (aagond), Harsh Atha (hatha), Sai Hari Chandan Morapakala (saimorap)


## Part 1: Raichu

### 1.1 Problem Statement:
Raichu is a popular childhood game played on an n ×n grid (where n ≥ 8 is an even number) with three kinds of pieces (Pichus, Pikachus, and Raichus) of two different colors (black and white). 

W: White Pikachu

w: White Pichu 

@: White Raichu 

B: Black Pikachu 

b: Black Pichu 

$: Black Raichu 


Initial State of board is given as:

![image](https://media.github.iu.edu/user/18130/files/9050f680-3ddb-11ec-8347-26b2fed78d05)


Possible Moves by pieces:

A. Pichu: (1 empty square forward diagonally) or (2 squares forward diagonally if the landing spot is empty and Pichu has jumped over an enemy.) Like a bishop in Chess, but with limitations that it only moves forward, has limit on steps and can jump.

B. Pikachu: (1 or 2 empty squares forward, left or right) or (Jump over enemy piece, where landing spot is empty and only 1 enemy piece in jump. 2 to 3 moves). Like a Rook in Chess but with no backward movement, can jump and has limits on step.

C. Raichu: Created only when pichu/pikachu reach opposite row of the board. (any number of squares forward, backward, left, right, diagonal) or (jump over an enemy piece where in landing square is empty and there is only one enemy jumped over). Like a Queen in Chess, but can jump over 1 piece.

Jumping over an enemy piece removes the enemy piece from the board. Pichus can only defeat Pichus, Pikachus can defeat Pichus and Pikachus, Raichus can defeat all types of pieces.

The objective is to defeat the opponent. When there is no enemy piece left, player wins. Output is a string of the format of the board at the extent.
### 1.2 Approaches Used:

#### Computing successors and Validity:

We have used the principles of coordinate geometry to fast compute the successors. 
At first, we pre-compute movements of each piece assuming the piece was at (0,0). We translate the coordinates of each pre-computed value to generate final possible moves of the piece. Once we get list of all possible moves, we check for validity of the moves. 

Additional check on top of this is if the given move is possible or not. To check if the move is possible or not, we abstract the game logic to a generalized pattern that is similar for all kinds of pieces. Drawback of this approach is the possibility of generating duplicate states in the successor set. Further work can be done on this to remove duplicates.

#### 1.2.1 Minimax Algorithm:

We started off with the most basic version of the Minimax Algorithm. Initially the utility function being used was the difference in number of pieces between player team and opponent team.
This approach worked pretty well till level 2 of the Minimax tree, but as we reach depth 3 and below the time consumed was too high and sometimes it failed to generate the better move in given timeout limit.

#### 1.2.2 Minimax with Alpha-Beta Pruning:

In this approach, we tried to reduce the number of nodes by using alpha-beta pruning to the already above applied Minimax algorithm. This process made the code a bit faster as compared to our previous approach.

#### 1.2.3 Modified Minimax with Iterative deepening and Alpha-Beta Pruning:

We created a tweaked version of Minimax Algorithm that gave us a better successor as compared to above methods. In this version we loop over the infinite depth, till the timer stops us to go iteratively down the tree. In some test cases, as it went down the tree we realized that the best successor at a deeper level of the tree migt not be the best move. So we stored the move that had the best alpha value at each level and return the move with max value at end of each move timeout. This ensures that we get a best possible move explored in that limited time. 

### 1.3 Utility Function:

In order to compute the utility function, we have chosen various sub-heuristics and assigned weights to them based on their importance. 
We have used the following functions:
    
    1. Difference in number of each type of piece between opponent and player team
    2. Threat to piece: Given a piece and left untouched the opponent would have a chance to kill it in the next turn.
    3. Number of kills our piece commits without losing our own piece.
    4. Distance between pichu/pikachu to become a Raichu.
    5. Number of player's pieces reduced.
    
Weights to each utility function: [4, -1, 2, -1.5, -1]

Using only weights would have been okay if each piece had the same value. As Raichu is able to move in all directions as well kill all pieces, it should have the highes weight. Pikachu will have the middle value and pichu has the least value.

Weights for Pieces: 
    
1. Raichu:3
2. Pikachu:2
3. Pichu: 1


Using a heuristic that is a weighted sum of all above sub-heuristics, we compute the next possible state.

### References Used:

[1] http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.39.742&rep=rep1&type=pdf

## Part 2: The Game of Quintris

### 2.1 Problem Statement:

The Game of Quintris is very similar to that of Tetris. Random shaped pieces of length will fall into blank board. As soon as the entire row is filled, player gets 1 point. Objective is to get maximum points before a block reaches the topmost layer. 

Possible Moves of pieces:
b: To Move Left 

m: To Move Right 

n: To Rotate piece Horizontally 

h: To Flip the piece 

" ": To cause the piece to fall 

Distribution of the pieces are random.

### 2.2 Successor Function

The Successor function explores all the states of a given current piece and evaluates them based on a cost function. 
We reduce the number of states explored by excluding rotation for rotation invariant pieces like (+) piece. (No point of rotating or flipping this piece.)
Example: For piece '|', we check two rotation 0 degree (|) and 90 degree (-). It is also flip invariant. 
This step lets us explore all the non-redundant states/configuration on the board. 
The Successor function keeps track of board commands in a list. For example - ['n', 'nn', 'b', 'hn', 'hnb', 'hnbbbb', 'hnmmm'] (* Not included all possible states here.)



### 2.3 Approaches Used:

#### 2.3.1 ExpectiMiniMax Algorithm:

We initially started using ExpectiMiniMax by considering the next piece and next state. Let current piece be p0, current state be s0, next piece is p1 and next state is s1. By using our prior knowledge of p0 and p1, we calculate a cost that gives us the best orientation and position of piece p0, while also considering where p1 might lie in s1. This process keeps repeating by looking d steps into the future. Assuming d=1 currently, there is a possibility that the state we predicted for s1 might not be the best fit given the information of p2. This can be considered a bigram calculation when d=1. If we look multiple steps into the future, we might get different values in the future calculations. This approach did not yield good results, where score was always ending up in range of 10-30 for us. Another problem being faced was the time and memory complexity. As we traverse multiple depths, the number of states explored was higher and took too much time and memory. 

#### 2.3.2 Genetic Algorithm:

The best approach to use here would be the genetic algorithms. As the name suggests, this is a natural selection process that demands survival of the fittest. Choosing a range of values for weights and cost functions, we choose a seed for the piece distribution. By running the different weight combinations on the functions for the same model, we try to find the best possible combination of weight and functions. We encountered two major issues with this method: 

1. Time taken to train the model is very high 
2. Lack of knowledge of seed of random generator. As the seed we may use for training maybe somethng way different, the weights that converge may not be the best choice.

#### 2.3.3 Greedy Approach

We decided that the best approach to suit our needs is the Greedy Approach. We chose 6 different functions with a set of weights that our computed empirically by evaluating their importance in the game as well as over various trials and errors. 

The functions chosen were as follows:

1. Agg_ht = Aggregate of heights of all columns in successor state.
2. num_holes: No. of holes left behind. Holes are blocks left empty, where in the rows above them in the same column are already filled.
3. Bumps: This indicates sum of absolute difference in heights of consecutive columns.
4. lines_cleared: This indicates the number of rows cleared in the next state. (Rewarding situation)
5. reached_top: This function indicates if we have reached the top of the board and game ends. (Punishing)
6. abs_mean_diff: This computes the mean of absolute difference of column height and total mean of heights.


The weights given are [1.6, 8.3, 0.76, -100000, 100. 0.63] in order of functions specified above. 

The importance of reward and punishment is justified as follows in increasing order of values:

1. -100000: As we want to score more points, we assign a very low negative cost to lines cleared, so this successor is favoured the most.
2. 0.63: The mean abs diff in heights needs to be low overall to avoid losing.
3. 0.76: If height of consecutive columns vary, it needs to be punished as well.
4. 1.6: If sum of all column heights is high, it impacts negatively on the game and we need to avoid that successor.
5. 8.3: If number of holes left behind is high, it will keep piling up pieces while not clearing lines. The game will end pretty quickly here.
6. 100: If game ends with next move, we need to add a high punishment weight and avoid that state.
 
Cost is given by sum(weights * functions). We try to minimize the cost as much as possible and use the greedy approach of choosing the next successor that best fits our needs. 

While this approach is not perfect and weights are empirically calculated, the approach works pretty well in lots of cases. If a distribution of pieces favouring more points (difficulty level: easy) is provided score goes in range of a few thousands as shown below (1 in 15 turns), while in some cases it scores in single digits (4-5 in 15 turns). On an average we get values around 95-160. 

<img width="636" alt="Screenshot 2021-11-05 at 9 24 49 PM" src="https://media.github.iu.edu/user/18130/files/a4eac880-3e87-11ec-8666-bccece1cf1c0">


-> Max Score achieved on a favourable random distribution of pieces.
<img width="636" alt="Screenshot 2021-11-05 at 10 58 58 PM" src="https://media.github.iu.edu/user/18070/files/555acb80-3e8c-11ec-962a-4024eb3ac0b8">


#### References Used:

1. https://theultramarine19.github.io/data/Tetris.pdf
2. https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
3. http://yutow.squarespace.com/gameplaying-ai
4. https://www.geeksforgeeks.org/generic-tree-level-order-traversal/
5. https://www.geeksforgeeks.org/expectimax-algorithm-in-game-theory/
6. https://luckytoilet.wordpress.com/2011/05/27/coding-a-tetris-ai-using-a-genetic-algorithm/
7. https://towardsdatascience.com/beating-the-world-record-in-tetris-gb-with-genetics-algorithm-6c0b2f5ace9b


## Part 3: Truth be Told

### 3.1 Problem Statement: 

We need to classify text objects into classes. Here 2 class classification needs to be done by using Naive Bayes classifier. For a given
textual object D consisting of words w1, w2, ..., wn, a Bayesian classifier evaluates decides that D belongs to A by computing the “odds” and comparing to a threshold,
P (A|w1, w2, ..., wn)/P (B|w1, w2, ..., wn) > 1,
where P (A|w1, ...wn) is the posterior probability that D is in class A.

This dataset contains user generated reviews of 20 hotels in Chicago. Some reviews are true while some are deceptive. Goal is to create a model that predicts the correct class as accurately as possible.


### 3.2 Approaches Used:

#### 3.2.1 Simple Naive Bayes using MLE

Initially, we tried to compute the probabilities of each review using a simple MLE (Max Likelihood Estimate). This estimate value can be expressed as p(w|c)= #(w∧c)/#(c)

w= Word
c= class
#(w∧c) = Number of word tokens in class c that are word w i.e frequency of word w in class c
#(c) = Number of word tokens in class c.

This approach has multiple issues. If the word that is present in Class A but not in Class B, the probability of the entire sentence will be 0 as final estimate is multiplication of word probabilities in that sentence. It will automatically assume the class to be Class A, without giving any importance to other words in the sentence. The accuracy here was 50.75%. This level of accuracy is almost similar to randomly choosing a class using a flip of a coin. 


#### 3.2.2 Naive Bayes using MAP (Laplace Smoothing)

In order to avoid issue where count of word in class is 0, we need to use another approach. Rather than calculating MLE, we can introduce prior values and add a smoothing factor to compute the MAP estimate (Max a posteriori). We include the prior probability of individual class to find if there is a class with higher probability and consider that as a weight. Additionally we introduce the smoothing factor "m". The initial formula now becomes: p(w|c)= (#(w∧c)+m)/(#(c)+mV)

where #(w∧c), #(c) are same as above and m= smoothing factor, V = length of total bag of words. 

When plugging in any value of m!=0, we realize that the probability of word will never be 0. It will smoothen out the MLE values and avoid extreme class A/class B situations.

This process is similar to using Laplace Smoothing which considers no. of classes in it's equation instead of V. We include a non-zero pseudo count m to artificially adjust 0 probabilities. We cannot simply make the count of word = 1, as it will have same impact as words actually having count = 1. Hence we add m in numerator and mV in denominator to add a small value.

In order to avoid underflow error which occurs when computing over very small values, we considered addition of log probabilities instead of multiplying the probabilities. This can be done as following holds true:

if A>B, log(A)>log(B).

This brought the accuracy to around 84%.

### 3.3 Data Preprocessing:

#### 3.3.1 Removing punctuation using Regex
Words separated by punctuations like !,'":)(? do not mean anything different than words in general. Often times a word with punctuation or capitalized words will be considered as a different word if not handled correctly. Using Regex we removed all characters other than space and alphabets. We also converted the words to lower case, so as to avoid hindrance from case changes.

The accuracy after this step was 85.75%

#### 3.3.2 Removing Stop Words

The data contains words that are occurring quite frequently but are sources of low information. Certain pronouns, articles, prepositions are commonly used in the language but do not contribute a lot to the overall information. We remove these words so as to get a better gauge of the accuracy provided by other words. 
We used the NLTK library to compute list of stop words in english language, stored those words in a txt file and removed them from our dataset while running train and test model.

The accuracy after this step was 87.25%, which is what is being displayed in the output.


#### 3.3.3 Stemming of words

Another thing that can be done here is to treat words with different forms or tense as the same. Words with forms like walk, walks, walking, walked will all be reduced to the base stem walk and dimensionality of data is reduced. This helps us cut down unwanted noise in our data. Using in-built libraries can achieve this pocess, but it was not added to our program.


### Final Output for given train, test data: Classification accuracy = 87.25%


#### References Used:
1. https://stackoverflow.com/questions/18429143/strip-punctuation-with-regex-python
2. https://docs.python.org/3/library/re.html
3. https://www.datacamp.com/community/tutorials/python-list-comprehension
4. List of stop words is derived from NLTK: stopwords.words('english')
5. Algorithm discussed in CSCI B555 Programming Assignment 1.
