import pandas as pd
import numpy as np
import random as rndm

policy = 20

epochs = 100000

cards =[]

episode = []

visited = np.zeros([10,10,2,2], dtype= int)

v_func = np.zeros([10,10,2], dtype= float)

returns = np.zeros([10,10,2], dtype= float)

visit=np.zeros([10,10,2], dtype= float)
 

for i in range(epochs):
    
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
                
    
    sum_for_player = cards[0]+ cards[1]
    
    
    while sum_for_player < 12:
    #automatically hit if less than 12 to get within the states of 12-21
        
        hit = rndm.randint(1,13)
        if hit >= 10:
            hit = 10
        
        
        
        cards.append(hit)
        
        sum_before = sum(cards)
    
        for indx,card in enumerate(cards):
            if card == 1:
                if sum_before + 10 <= 21:
                    cards[indx]= 11
                    
                else: 
                    cards[indx] = 1
                    
                    
        sum_for_player = sum(cards)
    
    state_hand = sum(cards)
    target_integer = 11
    if target_integer in cards:
        usable = True
    else: 
        usable= False
        
    
    while sum_for_player < 20: #This is your policy
        action = True
        state = (state_hand, dealer_shown, int(usable))
        episode.append((state, int(action),reward))
        
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

        state_hand = sum(cards)
        sum_for_player = state_hand

    
   
    
    
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
                
    
    
    action = False
    state = (state_hand, dealer_shown, int(usable))
    episode.append((state, int(action),reward))
    
    
    
    for st, act, rwrd in episode:
        if st[0]>21:
            continue
        else:
            if visited[st[0]-12,st[1]-1, st[2],act] == 0:
                
                visited[st[0]-12,st[1]-1, st[2],act] = 1
            
            
                returns[st[0]-12, st[1]-1, st[2]] += reward
                visit[st[0]-12, st[1]-1, st[2]] +=1
                v_func[st[0]-12, st[1]-1, st[2]] = returns[st[0]-12, st[1]-1, st[2]] / visit[st[0]-12, st[1]-1, st[2]]
        
        
    
    
print(v_func)

    
    
    
