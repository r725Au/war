from random import shuffle

class Deck:
    def __init__(self):
        '''
        s -> スペード
        h -> ハート
        d -> ダイアモンド
        c -> クローバー
        '''
        suits = ["s", "h", "d", "c"]
        numbers = ["A"] + [str(i) for i in range(2, 11)] + ["J", "Q", "K"]
        self.cards = []
        for s in suits:
            for n in numbers:
                self.cards.append("{}{}".format(s, n))
        #カードの山札
        shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

class Player():
    def __init__(self, name):
        self.hand = []
        self.name = name
    
    def receive(self, card):
        self.hand.append(card)

    def play_card(self):
        if not self.hand:
            return None
        return self.hand.pop(0)


        
    
class Game:
    def __init__(self, player_num):
        self.players_hand = []
        self.deck = Deck()
        self.players = [Player("Player{}".format(i+1)) for i in range(player_num)]


    
    def deal(self):
        per_card = 52 // len(self.players)
        for _ in range(per_card):
            for player in self.players:
                card = self.deck.draw()
                player.receive(card)
        print("カードが配られました")

            
    def strength(self, card):
        number = card[1:]
        rank_table = {
            "A": 14,
            "K": 13,
            "Q": 12,
            "J": 11
        }

        if number in rank_table:
            return rank_table[number]
        
        else :
            return int(number)
    def rule(self):
        # 今回の勝負で出たカード（場札）
        table_cards = []

        # 今回勝負に参加するプレイヤー
        active_players = self.players[:]
        active_players = [p for p in active_players if len(p.hand) > 0]

        if len(active_players) <= 1:
            return

        while True:
            player_card = []   # (player, value) の対応関係
            numbers = []       # value だけ

            # 各プレイヤーがカードを出す
            for player in active_players:
                card = player.play_card()
                table_cards.append(card)
                value = self.strength(card)
                player_card.append((player, value))
                numbers.append(value)
                print(f"{player.name} のカードは {card} です")

            # 最大値を求める
            max_value = max(numbers)

            # 最大値を出したプレイヤーを集める
            winners = []
            for p, v in player_card:
                if v == max_value:
                    winners.append(p)

            # 勝者が1人なら終了
            if len(winners) == 1:
                winner = winners[0]
                print(f"勝者は {winner.name} です")

                # 場札をすべて勝者の手札に加える
                for card in table_cards:
                    winner.receive(card)
                break

            # 引き分けの場合、そのプレイヤーだけで続行
            else:
                print("引き分け！もう一度勝負します")
                active_players = winners


    def is_game_over(self):
        for player in self.players:
            if len(player.hand) == 0:
                return True
        return False
    
    def show_ranking(self):
    # 手札が多い順にソート
        ranking = sorted(
            self.players,
            key=lambda p: len(p.hand),
            reverse=True
        )

        print()
        # 手札が0枚になったプレイヤーを表示
        for player in ranking:
            if len(player.hand) == 0:
                print(f"{player.name}の手札がなくなりました。")

        # 各プレイヤーの手札枚数を表示
        for player in ranking:
            print(f"{player.name}の手札の枚数は{len(player.hand)}枚です。")

        print()

        # 順位表示
        for i, player in enumerate(ranking, start=1):
            print(f"{player.name}が{i}位です。")
    
    def start(self):
        print("ゲーム開始")
        self.deal()

        turn = 1
        while True:
            if self.is_game_over():
                self.show_ranking()
                break
            self.rule()
            turn += 1




game = Game(4)
game.start()
