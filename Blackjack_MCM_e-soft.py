import pandas as pd
import numpy as np
import random as rndm

actions = [0, 1]

q_a = np.zeros(len(actions))

epochs = 10000000  

epsilon =0.1

q_func = np.zeros([10,10,2,2], dtype= float)

G = np.zeros([10,10,2,2], dtype= float)

visit=np.zeros([10,10,2,2], dtype= float)

policy = np.zeros([10,10,2,2], dtype= float)

policy[:,:,:,1] += epsilon/len(actions)

policy[:,:,:,0] += (1-epsilon + epsilon/len(actions))

state =  np.zeros([10,10,2], dtype= float)



for i in range(epochs):
    
    cards=[]
    episode = []
    visited = np.zeros([10,10,2,2], dtype= int)
    
    #generating hand for both dealer and player
    reward = 0
    usable = False
    action = False
    player_card1 = rndm.randint(1,13)
    player_card2 = rndm.randint(1,13) 
    dealer_shown = rndm.randint(1,13)
    dealer_hidden = rndm.randint(1,13)
    
    if player_card1 >= 10:
        player_card1 = 10
    
    if player_card2 >= 10:
        player_card2 = 10
        
    if dealer_shown >= 10:
        dealer_shown = 10
        
    if dealer_hidden >= 10:
        dealer_hidden = 10  

    cards = [player_card1, player_card2]
    dealer_cards = [dealer_hidden, dealer_shown]
    
    sum_for_player = player_card1 + player_card2
    sum_for_dealer = dealer_hidden+dealer_shown
    
    
    for indx,card in enumerate(cards):
        if card == 1:
            if sum(cards) +10 <= 21:
                cards[indx]= 11
                
            else: 
                cards[indx] = 1
                
    
    sum_for_player = sum(cards)
    
    
    while sum_for_player < 12:
    #automatically hit if less than 12 to get within the states of 12-21
        
        hit = rndm.randint(1,13)
        if hit >= 10:
            hit = 10
        
        
        
        cards.append(hit)
        
        
    
        for indx,card in enumerate(cards):
            if card == 1:
                if sum(cards) + 10 <= 21:
                    cards[indx]= 11
                    
                else: 
                    cards[indx] = 1
                    
                    
        sum_for_player = sum(cards)
    
    
    target_integer = 11
    if target_integer in cards:
        usable = True
    else: 
        usable= False
        
    action = True
        
    
    while action == True: #While your action = True keep iterating
        
        state = (sum_for_player, dealer_shown, int(usable))
        
        ep_random = rndm.random()
        
        probs = policy[state[0]-12, state[1]-1, state[2]]
        action = np.random.choice(actions, p= probs)
        
        
          
        
        
        
        episode.append((state, int(action),reward))
        
        if action == True: 
            
            
            hit = rndm.randint(1,13)
            if hit >= 10:
                hit = 10
            
            
            cards.append(hit)
            
            sum_before = sum(cards)
        

            for indx,card in enumerate(cards):
                if card == 1: 
                    if sum_before +10 <= 21:
                        cards[indx]= 11
                        
                    
                elif card == 11:
                    if sum_before > 21:
                        cards[indx]= 1
                        
            if target_integer in cards:
                usable = True
            else:
                usable= False        

            sum_for_player = sum(cards)
             
            
            if sum_for_player > 21:
                action = False
            
        else:
            break

    
   
    
    
    if sum_for_player > 21:
        reward = -1
    
    elif sum_for_player <= 21:
        
        while sum_for_dealer < 17:
        
            hit = rndm.randint(1,13)
            if hit >= 10:
                hit = 10
        
        
            dealer_cards.append(hit)
        
            sum_before = sum(dealer_cards)
    

            for indx,card in enumerate(dealer_cards):
                if card == 1: 
                    if sum_before +10 <= 21:
                        dealer_cards[indx]= 11
                        
                
                elif card == 11:
                    if sum_before > 21:
                        dealer_cards[indx]= 1
                        
            
            sum_for_dealer = sum(dealer_cards)
            
        if sum_for_dealer > 21:
            reward = 1
        else:
            if sum_for_player > sum_for_dealer:
                reward = 1
            elif sum_for_player < sum_for_dealer:
                reward = -1
            elif sum_for_player == sum_for_dealer:
                reward = 0
                
    
    
    
    state = (sum_for_player, dealer_shown, int(usable))
    episode.append((state, int(action),reward))
    
    
    
    for st, act, rwrd in episode:
        if st[0]>21:
            continue
        else:
            if visited[st[0]-12,st[1]-1, st[2],act] == 0:
                
                visited[st[0]-12,st[1]-1, st[2],act] = 1
            
            
                G[st[0]-12, st[1]-1, st[2], act] += reward
                visit[st[0]-12, st[1]-1, st[2], act] +=1
                q_func[st[0]-12, st[1]-1, st[2], act] = G[st[0]-12, st[1]-1, st[2], act] / visit[st[0]-12, st[1]-1, st[2], act]
                
                for a in range(len(actions)):
                    q_a[a] = q_func[st[0]-12, st[1]-1, st[2], a] 
                
                
                max_index = int(np.argmax(q_a))
                
                for a in range(len(actions)):
                    if a == max_index:
                        policy[st[0]-12, st[1]-1, st[2], a] = 1-epsilon + (epsilon/len(actions))
                    else:
                        policy[st[0]-12, st[1]-1, st[2], a] = (epsilon/len(actions))
                
                
        
        
    
    
print(q_func)

print(policy)

    
import matplotlib.pyplot as plt
import numpy as np

# Create policy visualization (0 = stick, 1 = hit)
policy_best = np.argmax(policy, axis=3)

fig, axes = plt.subplots(1, 2, figsize=(10, 5))

titles = ["No Usable Ace", " Usable Ace"]
for i, ax in enumerate(axes):
    im = ax.imshow(policy_best[:, :, i], origin='lower', cmap='coolwarm', extent=[1, 10, 12, 21])
    ax.set_title(titles[i])
    ax.set_xlabel("Dealer Showing")
    ax.set_ylabel("Player Sum")
    ax.set_xticks(range(1, 11))
    ax.set_yticks(range(12, 22))
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("0 = Stick, 1 = Hit")

plt.suptitle("Policy (Greedy Action per State)")
plt.tight_layout()
plt.show()

from mpl_toolkits.mplot3d import Axes3D

# Take the best action value per state
v_func = np.max(q_func, axis=3)

fig = plt.figure(figsize=(12, 6))
for i in range(2):
    ax = fig.add_subplot(1, 2, i + 1, projection='3d')
    X, Y = np.meshgrid(np.arange(1, 11), np.arange(12, 22))
    Z = v_func[:, :, i]
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_title(f"Usable Ace = {bool(i)}")
    ax.set_xlabel("Dealer Showing")
    ax.set_ylabel("Player Sum")
    ax.set_zlabel("Value (max Q)")
plt.suptitle("Value Function (Max Q per State)")
plt.tight_layout()
plt.show()



q_diff = q_func[:, :, :, 1] - q_func[:, :, :, 0]

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
for i, ax in enumerate(axes):
    im = ax.imshow(q_diff[:, :, i], origin='lower', cmap='bwr', extent=[1, 10, 12, 21])
    ax.set_title(["No Usable Ace", "Usable Ace"][i])
    ax.set_xlabel("Dealer Showing")
    ax.set_ylabel("Player Sum")
    plt.colorbar(im, ax=ax, label="Q(hit) - Q(stick)")
plt.suptitle("Q(hit) - Q(stick) Difference")
plt.tight_layout()
plt.show()

    