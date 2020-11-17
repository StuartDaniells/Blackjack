import random
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}


class Cards:
    
    def __init__(self, ranks, suits):
        self.suits = suits
        self.ranks = ranks
        self.value = values[ranks]
        
    def __str__(self):
        return f"{self.ranks} of {self.suits}"
        


class Bank:
    
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        
    def bet(self, amount):
        if self.balance < amount:
            print(f"\nSorry {self.name} you don't have sufficient funds to play")
            print("\n--------------------------------------Game Over!--------------------------------------")
            return False
        
        else:
            self.balance -= amount
            print(f"\n[{self.name}'s balance is -> {self.balance}]")
            
    def withdraw(self, amount):
        temp_balance = self.balance
        self.balance -= amount
        return temp_balance
    
    def deposit(self, amount):
        self.balance += amount
        print(f"\n[{amount} credited to {self.name}]")
        print(f"[{self.name}'s balance is {self.balance}]")




class Deck:
    
    def __init__(self):
        
        self.all_cards = []
        
        for suit in suits:
            for rank in ranks:
                
                self.all_cards.append(Cards(rank,suit))
                
    def shuffle(self):
        random.shuffle(self.all_cards)
    
    def deal_one(self):
        return self.all_cards.pop(0)
    


class Player:
    
    def __init__(self, name):
        self.name = name
        
        self.player_cards = []
    
    def add_card(self, new_card):
        if type(new_card) == type([]):
            self.player_cards.extend(new_card)
        else:
            self.player_cards.append(new_card)
            
    def cards_sum(self, summing):
        cards_sum = 0
        for cards in summing:
            cards_sum += cards.value
        return cards_sum
    
    
    def printing(self, cards_inhand):
        for cards in cards_inhand:
            print(f"{cards}")
        
        
    def ace_valuation(self, player_ace_card):
        
        for ace in player_ace_card:
            if ace.ranks == 'Ace':

                value_choice = True
                while value_choice:
                    ace_value_choice = input("Enter the value for Ace (either 1 or 11 only): \t -> ")
                    
                    if ace_value_choice.isdigit() == False:
                        print("\n[Enter a number, not a character. Either 1 or 11]\n")
                        continue
                    elif int(ace_value_choice) not in [1, 11]:
                        print("\n[Enter either 1 or 11 as Ace value]\n")
                        continue
                    else:
                        ace.value = int(ace_value_choice)
                        break
    
    def ace_valuation_dealer(self, dealer_ace_card):
        
        previous_dealer_sum = test_dealer.cards_sum(test_dealer.player_cards)
        present_dealer_sum = previous_dealer_sum + dealer_ace_card[0].value
        
        if present_dealer_sum > 21:
            dealer_ace_card[0].value = 1
            test_dealer.add_card(dealer_ace_card)
            
        else:
            dealer_ace_card[0].value = 11
            test_dealer.add_card(dealer_ace_card)
            
        

# GAME LOGIC

def continuing():
    
    decision = True 
    
    while decision:
        print("\n--------------------------------------Continuing?----------------------------------------")
        choice = input("\nWould you like to continue playing? \n\n\n ---> Input either 'Y' - (for yes) or 'N' - (for no)\n\n->")
        choice = choice.upper()
        
        if choice == 'Y':
            clear_output()
            return 'yes'
            
        elif choice == 'N':
            clear_output()
            print("\n--------------------------------------Game Over!--------------------------------------")
            return False
            
        else:
            print("\n[Enter either Y or N to proceed]")




def bets_on_table():
    betting_on = True
    while betting_on:
        
        try:
            betting_amount = int(input("\nEnter the bet amount: \t -> "))
        
        except:
            print("\nEnter any number, not a character.")
            continue
            
        else:
            return betting_amount


def choice_player():
    choice = True
    while choice:
        players_choice = input("\nHit or Stay? [For Hit - H, Stay - S]\t-> ").upper()

        if players_choice == 'H' or players_choice == 'S':
            choice = False
            break
        else:
            print("\n[Enter either:'H' or 'S']\n")
            continue
    return players_choice



from IPython.display import clear_output

game_on = True


player_name = input("Enter players name\t -> ")
clear_output()

# Adding the players
test_dealer = Player("Dealer")
test_player = Player(player_name)
    
    
    
    
# Placing bets and checking balance to continue
players_bank = Bank(player_name, 500)
dealers_bank = Bank("Dealer", 10000)
betting_box = Bank("Betting box", 0)



while game_on:
        
    # adding the deck and shuffling
    test_deck = Deck()
    test_deck.shuffle()
    
    # Resetting players and dealers cards
    test_player.player_cards = []
    test_dealer.player_cards = []
    
    
    betting_amount = bets_on_table()

    check_funds = players_bank.bet(betting_amount)

    if check_funds == False:
        break

    dealers_bank.bet(betting_amount)


    betting_box.deposit(betting_amount * 2)
    
    
    
    # Dishing out the cards
    for x in range(2):
        test_player.add_card(test_deck.deal_one())
        test_dealer.add_card(test_deck.deal_one())
        
        
    # Showing one of the Dealers cards
    print("\n-------------------------------------------------------------------------------------- ")
    print("\nDealers card is:")
    print(f"{test_dealer.player_cards[0]} \n")
    
    
    # Showing the Players cards
    print(f"{test_player.name} cards are:")
    test_player.printing(test_player.player_cards)
    
    
    # Checking for ace and setting its value:
    test_player.ace_valuation(test_player.player_cards)
       
    
    if test_player.cards_sum(test_player.player_cards) == 21:
        print(f"\n\n ---> {test_player.name} Wins! -----------------------------------------------")
        players_bank.deposit(betting_box.withdraw(betting_box.balance))
        game_on = continuing()
        
    elif test_player.cards_sum(test_player.player_cards) > 21:
        print("\n\n ---> Dealer Wins! -----------------------------------------------")
        dealers_bank.deposit(betting_box.withdraw(betting_box.balance))
        game_on = continuing()
        
    
    if game_on == False:
        break
    elif game_on == 'yes':
        game_on = True
        continue
    
    
    check_player = True
         
    while check_player:  

        choice = choice_player()

        if choice == 'H':
            
            # Since Card object is not iterable, we set new_card variable to a list type
            new_card_delt = [test_deck.deal_one()]
            
            # If player Hit, the new delt card is checked if Ace and its value is assigned ---------------
            test_player.ace_valuation(new_card_delt)
            
            test_player.add_card(new_card_delt)
            
            # Showing Players cards:
            print(f"\n{test_player.name} cards are:")
            test_player.printing(test_player.player_cards)

            if test_player.cards_sum(test_player.player_cards) > 21:
                print("\n\n ---> Player busted, dealers wins!")
                dealers_bank.deposit(betting_box.withdraw(betting_box.balance))
                check_player = False
                game_on = continuing()
                break

            elif test_player.cards_sum(test_player.player_cards) == 21:
                print(f"\n\n ---> {test_player.name} Wins!")
                players_bank.deposit(betting_box.withdraw(betting_box.balance))
                check_player = False
                game_on = continuing()
                break

            else:
                continue

        elif choice == 'S':
            print("\n----------------------Dealers turn now----------------------")
            check_player = False
            break
            
    
    if game_on == False:
        break
    elif game_on == 'yes':
        game_on = True
        continue
    
        
    check_dealer = True

    while check_dealer:
        print("\nDealers cards are:")
        
        #Showing dealers cards:
        test_dealer.printing(test_dealer.player_cards)

        if test_dealer.cards_sum(test_dealer.player_cards) > 21:
            print(f"\n\n ---> Dealer busted, {test_player.name} wins! ------------------------------------------")
            players_bank.deposit(betting_box.withdraw(betting_box.balance))
            check_dealer = False
            game_on = continuing()
            break
            

        elif test_dealer.cards_sum(test_dealer.player_cards) >= test_player.cards_sum(test_player.player_cards):
            print("\n\n ---> Dealer wins!-----------------------------------------------")
            dealers_bank.deposit(betting_box.withdraw(betting_box.balance))
            check_dealer = False
            game_on = continuing()
            break

        else: 
            # Auto setting Ace card value for dealer, based on cards possesses  
            new_dealer_card = [test_deck.deal_one()]
            
            if new_dealer_card[0].ranks == 'Ace':
                test_dealer.ace_valuation_dealer(new_dealer_card)
                continue
            else:
                test_dealer.add_card(new_dealer_card)
                continue

    if game_on == 'yes':
        game_on = True
