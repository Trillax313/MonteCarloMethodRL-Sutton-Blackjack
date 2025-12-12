Going through Richard Sutton's Introduction to Reinforcement Learning, I created built an Environment to simulate the card game black jack. I then used the algorithms in the book to optimize policy pi using MCM. 

The blackjack_RL code simply introduces policy evaluation with a static policy, no policy iteration/improvement. The policy is fixed at if the current hand sum is less than 20 hit.

The Blackjack_MCM_e-soft.py code introduces an e-soft policy where we have policy improvement and using policy improvement and policy evaluation you get your MCM method. This algorithm is in the Sutton book and introduces the reader to their first applicable RL algorithm
