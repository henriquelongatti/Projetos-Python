import black_jack, games, cards

class BJ_Hand_Aposta(cards.Hand):

    def __init__(self, name, bet = 0, give_up = False):
        super(BJ_Hand_Aposta, self).__init__()
        self.name = name
        self.bet = bet
        self._give_up = give_up

    def aposta(self):
        self.bet = games.ask_number(self.name + ":Do your bet:\t", 5,100000)

    def __str__(self):
        rep = self.name + " | Bet: " + str(self.bet) +"\t| Hand: " + super(BJ_Hand_Aposta, self).__str__() + str(not(self._give_up))
        if self.total:
            rep += "\t(" + str(self.total) + ")"
        return rep

        return rep

    @property
    def total(self):
        # if a card in the hand has value of None, then total is None
        for card in self.cards:
            if not card.value:
                return None

        # Add up card values, treat each Ace as 1
        t = 0
        for card in self.cards:
            t += card.value

        # determine if hand contains an Ace
        contains_ace = False
        for card in self.cards:
            if card.value == black_jack.BJ_Card.ACE_VALUE:
                contains_ace = True

        # If hand contains Ace and total is low enough treat ace as 11
        if contains_ace and t <= 11:
            # add only 10 since we've already added 1 for the Ace
            t += 10

        return t
    
    def is_busted(self):
        return self.total > 21

class BJ_Player_Aposta(BJ_Hand_Aposta):
    """A Blackjack Player."""

    def is_hitting(self):
        response = games.ask_yes_no("\n" + self.name + ", do you want a hit? (Y/N): ")
        return response == "y"

    def bust(self):
        print(self.name, "busts.")
        self.lose()


    def lose(self):
        print(self.name, "loses.")

    def win(self):
        print(self.name, "wins.")

    def push(self):
        print(self.name, "pushes.")

    def give_up(self):
        response = games.ask_yes_no("\n" + self.name + ", do you want a give up? (Y/N): ")
        if response == "y":
            print("I don't have money")
            self.bust()
            self._give_up = True
        return self._give_up


class BJ_Game_Aposta(object):
    """A Blackjack Game."""

    def __init__(self, names):
        self.players = []
        for name in names:
            player = BJ_Player_Aposta(name)
            self.players.append(player)

        self.dealer = black_jack.BJ_Dealer("Dealer")

        self.deck = black_jack.BJ_Deck()
        self.deck.populate()
        self.deck.shuffle()


    def maior_aposta(self,apostas):
        m = 0;
        for a in apostas:
            if m < a:
                m = a
        return m

    @property
    def still_playing(self):
        sp = []
        for player in self.players:
            if not player.is_busted() and not player._give_up:
                sp.append(player)
        return sp
    #------------------------------------
    def still_bet(self):
        apostas = []
        for player in self.players:
            player.aposta()
        for player in self.players:
            apostas.append(int(player.bet))

        return apostas
    #---------------------------------------

    def __additional_cards(self, player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust()

    def play(self):
        # deal initial 2 cards to everyone
        self.deck.deal(self.players + [self.dealer], per_hand=2)
        self.dealer.flip_first_card()  # hide dealer's first card
        for player in self.players:
            print(player)
        print(self.dealer)

        # -----------------------------------------------------
        # deal bets
        apostas = self.still_bet()

        for player in self.still_playing:
            if player.bet < self.maior_aposta(apostas):
                print("A mesa vale: " + str(self.maior_aposta(apostas)))
                while player.bet < self.maior_aposta(apostas):
                    if player.give_up():
                        break
                    player.aposta()







        for player in self.players:
            print(player)
        print(self.dealer)
        # -----------------------------------------------------



        # deal additional cards to players
        for player in self.still_playing:
            self.__additional_cards(player)

        self.dealer.flip_first_card()  # reveal dealer's first

        if not self.still_playing:
            # since all players have busted, just show the dealer's hand
            print(self.dealer)

        else:
            # deal additional cards to dealer
            print(self.dealer)
            self.__additional_cards(self.dealer)

            if self.dealer.is_busted():
                # everyone still playing wins
                for player in self.still_playing:
                    player.win()
            else:
                # compare each player still playing to dealer
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        player.win()
                    elif player.total < self.dealer.total:
                        player.lose()
                    else:
                        player.push()

            # remove everyone's cards
            for player in self.players:
                player.clear()
            self.dealer.clear()

def main():
    print()
    names = []
    number = games.ask_number("How many players? (1 - 7): ", low=1, high=8)
    for i in range(number):
        name = input("Enter player name: ")
        names.append(name)

    print()

    game = BJ_Game_Aposta(names)

    again = None

    while again != "n":
        game.play()
        again = games.ask_yes_no("\nDo you want to play again?: ")
        game = BJ_Game_Aposta(names)

main()
input("\n\nPress the enter key to exit.")

if __name__ == "__main__":
    print("This is a module with classes for playing cards.")
    input("\n\nPress the enter key to exit.")


