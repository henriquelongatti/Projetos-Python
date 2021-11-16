import black_jack, games, cards

class BJ_Game(object):
    """A Blackjack Game."""

    def __init__(self, names):
        self.players = []
        for name in names:
            player = black_jack.BJ_Player(name)
            self.players.append(player)

        self.dealer = black_jack.BJ_Dealer("Dealer")

        self.deck = black_jack.BJ_Deck()
        self.deck.populate()
        self.deck.shuffle()

    @property
    def still_playing(self):
        sp = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp

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

        # deal additional cards to players
        for player in self.players:
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

    game = BJ_Game(names)

    again = None

    while again != "n":
        game.play()
        again = games.ask_yes_no("\nDo you want to play again?: ")
        game = BJ_Game(names)


main()
input("\n\nPress the enter key to exit.")

if __name__ == "__main__":
    print("This is a module with classes for playing cards.")
    input("\n\nPress the enter key to exit.")