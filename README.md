This is some practice with uncertainty estimating for [CS50's Heredity](https://cs50.harvard.edu/ai/2024/projects/2/heredity/). I wrote the joint_probability, update and normalize functions. 
- The joint_probability function calculates the likelyhood of a given situation with each person's gene count and trait expression being set. 
- The update function adds a new joint_probability to the probabilities dictionary in main(). 
- The normalize function normalizes the probabilities of each persons probabilities (makes all their probabilities sum to 1)

The main() function iterates over all possible senarios given the family.csv data, and uses the three functions above to add them to the probabilties dictionary and display the likelyhood that each person has the trait or number of genes. This is called Inference by enumeration and can be summarized by the equation below:

$$ P(X|e) = \alpha P(X,e) = \alpha \sum_{y} P(X,e,y) $$

Where:
- $X$ is a query variable (a variable we want to know)
- $e$ is evdidence
- $y$ is the range of values for hidden variables
- $\alpha$ normalizes the result

This equation states that the probability of $X$ given $e$ is proportional (by $\alpha$) to the probability of $X$ and $e$. They are both proportional (by $\alpha$) to the sum of probabilities of $X$, $e$ and ALL $y$
