from itertools import product, combinations
from random import shuffle
import emoji #pip installable
from pyfiglet import Figlet #pip installable
from time import sleep


coppe = emoji.emojize(':trophy:')
denari = emoji.emojize(':coin:')
spada = emoji.emojize(':crossed_swords:')
bastoni = emoji.emojize(':flute:')


values = list(range(1,11))
suits = [coppe, denari, spada, bastoni]

value_point_dict = {
    7 : 21,
    6 : 18,
    1 : 16,
    5 : 15,
    4 : 14,
    3 : 13,
    2 : 12,
    8 : 10,
    9 : 10,
    10: 10
    }

class Card():
    def __init__(self, value, suit, in_deck = True):
        self.value = value
        self.suit = suit
        self.in_deck = in_deck
        
    def __str__(self):
        return str(self.value) + self.suit + " "
      
        
class Scopa_Deck():
    def __init__(self):
        self.cards = [Card(value, suit, in_deck = True) for value, suit in product(values, suits)]
        self.removed = []
        
    def draw(self, range = 1):
        """Draw card(s) by removing them from deck"""
        drawn_cards = self.cards[:range]
        for card in drawn_cards:
            card.in_deck = False
        del self.cards[:range]
        self.removed.append(drawn_cards)
        return drawn_cards
    
    def shuffle_deck(self):
        """Shuffles deck object in place"""
        shuffle(self.cards)
        
    def is_not_empty(self):
        return bool(self.cards)
    
class Player():
    def __init__(self, name, hand = None, is_turn = False):
        self.name = name
        self.hand = hand
        self.is_turn = is_turn
        self.score = 0
        self.selected_card = None
        self.pile = []
        self.num_scopa = 0
        self.last_move = "... ---> ... + ..."
        self.captured_last = False

    def __str__(self):
        return str(self.name)

    def remove_from_hand(self, card):
        """Removes a card object from the players hand"""
        if card in self.hand:
            position = self.hand.index(card)
            del self.hand[position]
            
    def sort_hand(self):
        sorted_hand = sorted(self.hand, key = lambda x: x.value)
        self.hand = sorted_hand
        
    def sort_pile(self):
        sorted_pile = sorted(self.pile, key = lambda x: x.value)
        self.pile = sorted_pile
        
    def hand_is_empty(self):
        return not bool(self.hand)
        
        
        
class Playing_Table():
    def __init__(self, cards = None):
        self.cards = cards
        
    def is_empty(self):
        return not bool(self.cards)
    
    def value_combos(self):
        values = []
        for card in self.cards:
            values.append(card.value)
        combos = set()
        for r in range(1, len(values)+1):
            this_combos = combinations(values, r)
            for combo in this_combos:
                if sum(combo) <= 10:
                    combos.add(sum(combo))
                
        return combos, values

        
def wait_countdown():
    print("3", end="")
    sleep(0.25)
    print(".", end="")
    sleep(0.25)
    print(".", end="")
    sleep(0.25)
    print(".")
    sleep(0.25)
    print("2", end="")
    sleep(0.25)
    print(".", end="")
    sleep(0.25)
    print(".", end="")
    sleep(0.25)
    print(".")
    sleep(0.25)
    print("1", end="")
    sleep(0.25)
    print(".", end="")
    sleep(0.25)
    print(".", end="")
    sleep(0.25)
    print(".")
    sleep(0.25)
                
  
def display_state(P1, P2, Table, Deck):
    Deck_size = len(Deck.cards)
    if P1.is_turn:
        print("\n")
        print("----------------------------------------------------------------", end="")
        print("\n" + f"Score: {P1.score} - {P2.score}                    Cards left in deck: {Deck_size}\n")
        
        P2_hand_size = len(P2.hand)
        print(f"{P2.name}:    ", end="")
        card_backs = (emoji.emojize(":joker:") + " ") * P2_hand_size
        print(card_backs, end="")
        print(f"        No. Scopa: {P2.num_scopa}")
        print("\n")
        
        print("Table:  ", end="")
        for card in Table.cards:    
            print(card, end="")
            
        print(f"    Last Played: {P2.last_move}")
        
        print("\n")
        print(f"{P1.name}:   ", end="")
        for card in P1.hand:
            print(card, end="")
        print(f"      No. Scopa: {P1.num_scopa}")
        print("----------------------------------------------------------------")
            
    else:
        print("\n")
        print("----------------------------------------------------------------", end="")
        print("\n" + f"Score: {P2.score} - {P1.score}                    Cards left in deck: {Deck_size}\n")
        
        P1_hand_size = len(P1.hand)
        print(f"{P1.name}:    ", end="")
        card_backs = (emoji.emojize(":joker:") + " ") * P1_hand_size
        print(card_backs, end="")
        print(f"        No. Scopa: {P1.num_scopa}")
        print("\n")
        
        print("Table:  ", end="")
        for card in Table.cards:    
            print(card, end="")
            
        print(f"    Last Played: {P1.last_move}")
        
        print("\n")
        print(f"{P2.name}:   ", end="")
        for card in P2.hand:
            print(card, end="")
        print(f"      No. Scopa: {P2.num_scopa}")
        print("----------------------------------------------------------------")
        
        
def make_move(P, Q, Table, Deck): #Implement try except for move input
    try:
        move = input("Play: ").strip()  #otf hand_index:table_indexes
        if ":" not in move:
            if P.hand[int(move)-1].value in Table.value_combos()[0]:
                print("Card(s) can be captured with the selected card so can't be placed on table!")
                make_move(P, Q, Table, Deck)
                return
            else:
                move = int(move) - 1
                Table.cards.append(P.hand[move])
                P.last_move = str(P.hand[move]) + "Tabled"
                del P.hand[move]
                P.is_turn = False
                Q.is_turn = True
    
                if P.hand_is_empty():
                    P.hand = Deck.draw(3)
                    P.sort_hand()
            
        else:
            hand_index, table_indexes = move.split(":")
            table_indexes = table_indexes.split(" ")
            table_indexes = [int(t) for t in table_indexes]
            hand_index = int(hand_index) - 1
            table_indexes = [t - 1 for t in table_indexes]
            selected_value = P.hand[hand_index].value
            if selected_value not in Table.value_combos()[0]:
                print("This is not a valid capture!")
                make_move(P, Q, Table, Deck)
                return
            captured_sum = 0
            for i in table_indexes:
                captured_sum += Table.cards[i].value
            if selected_value != captured_sum:
                print("This is not a valid capture!")
                make_move(P, Q, Table, Deck)
                return
            
            table_str = ""
            for i in table_indexes:
                P.pile.append(Table.cards[i])
                table_str += "+ " + str(Table.cards[i])
            P.pile.append(P.hand[hand_index])
            
            table_str = table_str[1:]
            P.last_move = str(P.hand[hand_index]) + "--->" + table_str
            
            for i in sorted(table_indexes, reverse=True):
                del Table.cards[i]
            del P.hand[hand_index]
            
            
            if len(Table.cards) == 0:
                if not (len(Deck.cards) == 0 and P.hand_is_empty() and Q.hand_is_empty()):
                    P.num_scopa += 1
                    print("\nSCOPA!")
                    sleep(2)
            
            P.captured_last = True
            Q.captured_last = False
            P.is_turn = False
            Q.is_turn = True
    
            if P.hand_is_empty():
                P.hand = Deck.draw(3)
                P.sort_hand()
    
    except (IndexError, ValueError):
        print("This is not a valid move!")
        make_move(P, Q, Table, Deck)
        return
        
    if len(Table.cards) > 0 and len(Deck.cards) == 0 and P.hand_is_empty() and Q.hand_is_empty():
        if P.captured_last:
            for card in Table.cards:     
                P.pile.append(card)
        else:
            for card in Table.cards:     
                Q.pile.append(card)
                
        Table.cards.clear()
        

def calculate_score(P1, P2): #Needs fixing
    global P1_prime_score
    global P2_prime_score
    P1.score += P1.num_scopa
    P2.score += P2.num_scopa
    
    if len(P1.pile) > len(P2.pile):
        P1.score += 1
    elif len(P1.pile) < len(P2.pile):
        P2.score += 1
    
    P1_num_denari = 0
    P1_denari_prime_score = 0
    P1_coppe_prime_score = 0
    P1_spada_prime_score = 0
    P1_bastoni_prime_score = 0
    for card in P1.pile:
        card_str = str(card)
        if "🪙" in card_str:
            if "7🪙" in card_str:
                P1.score += 1
            P1_num_denari += 1
            P1_denari_prime_score = max(P1_denari_prime_score, value_point_dict[card.value])
        elif "⚔️" in card_str:
            P1_spada_prime_score = max(P1_spada_prime_score, value_point_dict[card.value])
        elif "🪈" in card_str:
            P1_bastoni_prime_score = max(P1_bastoni_prime_score, value_point_dict[card.value])
        elif "🏆" in card_str:
            P1_coppe_prime_score = max(P1_coppe_prime_score, value_point_dict[card.value])
            
    P1_prime_score = P1_denari_prime_score + P1_coppe_prime_score + P1_spada_prime_score + P1_bastoni_prime_score
        
    
    P2_num_denari = 0
    P2_denari_prime_score = 0
    P2_coppe_prime_score = 0
    P2_spada_prime_score = 0
    P2_bastoni_prime_score = 0
    for card in P2.pile:
        card_str = str(card)
        if "🪙" in card_str:
            if "7🪙" in card_str:
                P2.score += 1
            P2_num_denari += 1
            P2_denari_prime_score = max(P2_denari_prime_score, value_point_dict[card.value])
        elif "⚔️" in card_str:
            P2_spada_prime_score = max(P2_spada_prime_score, value_point_dict[card.value])
        elif "🪈" in card_str:
            P2_bastoni_prime_score = max(P2_bastoni_prime_score, value_point_dict[card.value])
        elif "🏆" in card_str:
            P2_coppe_prime_score = max(P2_coppe_prime_score, value_point_dict[card.value])
            
    P2_prime_score = P2_denari_prime_score + P2_coppe_prime_score + P2_spada_prime_score + P2_bastoni_prime_score
    
    
    if P1_prime_score > P2_prime_score:
        P1.score += 1
    elif P1_prime_score < P2_prime_score:
        P2.score += 1
        
    if P1_num_denari > P2_num_denari:
        P1.score += 1
    elif P1_num_denari < P2_num_denari:
        P2.score += 1
        
        
def end_of_round_display(P1, P2, round_num):
    P1.sort_pile()
    P2.sort_pile()
    print("\n")
    print(f"END OF ROUND {round_num}:")
    print("\n")
    print(f"{P1.name}'s captures: ", end="")
    for card in P1.pile:
        print(str(card), end=" ")
    print(f"  No. Scopa: {P1.num_scopa}   Prime score: {P1_prime_score}")
    print("\n")
    print(f"{P2.name}'s captures: ", end="")
    for card in P2.pile:
        print(str(card), end=" ")
    print(f"  No. Scopa: {P2.num_scopa}   Prime score: {P2_prime_score}")
    print("\n")
    print(f"SCORE: {P1.name} {P1.score} - {P2.score} {P2.name}")
    print("\n")
      

def intro():
    f = Figlet(font='epic')
    print("\n")
    print(f.renderText('SCOPA'))
    my_input = input("Press enter to start! (i for instructions)  ")
    print("\n")
    if my_input == "i":
        print("1. To place a card from your hand onto the table use the\nnumber 1, 2 or 3 of the position of that card in your hand.")
        print("2. Use the format (hand position):(table position(s)) with\ntable positions separated by spaces to capture cards from table.")
        print("3. See \"Scopa\" Wiki Page for full rules of the game.")
        print("\n")
        input("Press enter to start! ")
        print("\n")
    
    

#-----------------------------------------------------------------------------


def main():

    winning_score = 11
    intro()
    
    
    P1 = Player(input("Player 1 name: ").strip(), is_turn = True)
    P2 = Player(input("Player 2 name: ").strip())
    
    
    round_num = 0
    while P1.score < winning_score and P2.score < winning_score:
        round_num += 1
        
        Deck = Scopa_Deck()
        Deck.shuffle_deck()
        Table = Playing_Table(Deck.draw(4))
        P1.hand = Deck.draw(3)   
        P1.sort_hand()
        P2.hand = Deck.draw(3)   
        P2.sort_hand()
        print()
        print(f"ROUND {round_num}:")
        while len(Table.cards) > 0 or len(Deck.cards) > 0 or len(P2.hand) > 0 or len(P1.hand) > 0:
            wait_countdown()
            display_state(P1, P2, Table, Deck)
            if P1.is_turn:
                make_move(P1, P2, Table, Deck)
            else:
                make_move(P2, P1, Table, Deck)
        
        calculate_score(P1, P2)
        wait_countdown()
        end_of_round_display(P1, P2, round_num)
        if P1.score >= winning_score or P2.score >= winning_score:
            print("\n")
            if P1.score > P2.score:
                print(f"{P1.name} wins!")
            elif P1.score < P2.score:
                print(f"{P2.name} wins!")
            print("\n")
     
        input("Press enter to continue: ")


if __name__ == "__main__":
    main()
