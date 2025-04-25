import tkinter as tk
from tkinter import messagebox, simpledialog
import random
from PIL import Image, ImageTk
import tkinter.font as tkfont
import os
import time

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("神経衰弱ゲーム - 完全版")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)                
        
        # ゲーム設定
        self.default_settings = {
            'players': 1,
            'rows': 3,
            'cols': 6,
            'card_back': "blue_back",
            'theme': "classic"
        }
        
        # ゲーム状態
        self.game_active = False
        self.players = []
        self.current_player = 0
        self.flipped_cards = []
        self.matched_pairs = 0
        self.start_time = 0
        
        # UI要素
        self.game_frame = None
        self.status_label = None
        self.timer_label = None
        self.card_buttons = []
        self.card_images = {}
        
        # 初期化
        self.load_assets()
        self.show_menu()
    
    def load_assets(self):
        """カード画像などのアセットを読み込む"""
        # 簡易版のため、実際には画像ファイルを用意する必要があります
        colors = ["red", "blue", "green", "yellow", 
                 "purple", "orange", "pink", "cyan", "brown"]
        
        # カードの表と裏の画像を生成（簡易版）
        for i, color in enumerate(colors, 1):
            self.card_images[f"card_{i}"] = self.create_card_image(color)
        
        # カードの裏面
        self.card_images["back"] = self.create_card_image("gray")
    
    def create_card_image(self, color):
        """簡易的なカード画像を生成"""
        from tkinter import font as tkfont
        from PIL import Image, ImageDraw
        
        # 実際のゲームでは本物のカード画像を使用してください
        width, height = 100, 150
        image = Image.new("RGB", (width, height), color)
        draw = ImageDraw.Draw(image)
        
        # 枠線を描画
        draw.rectangle([0, 0, width-1, height-1], outline="black")
        
        return ImageTk.PhotoImage(image)
    
    def show_menu(self):
        """メニュー画面を表示"""
        if self.game_frame:
            self.game_frame.destroy()

        # メニューフレームの初期化        
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(fill="both", expand=True)
        
        tk.Label(self.menu_frame, text="神経衰弱ゲーム", 
                font=("Noto Sans CJK JP", 30, "bold")).pack(pady=10)
                        
        # 背景画像の読み込み        
        try:
            bg_image_path = os.path.join(os.path.dirname(__file__), "background.jpg")
            bg_image = Image.open(bg_image_path)
            bg_image = bg_image.resize((800, 600))  # 適切なサイズに調整
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            
            bg_label = tk.Label(self.menu_frame, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()
        except Exception as e:
            print(f"背景画像の読み込みに失敗しました: {e}")                
        
        # 設定オプション
        settings_frame = tk.Frame(self.menu_frame)
        settings_frame.pack(expand=True, padx=10, pady=10)

        # フォント設定
        font_settings = ("Noto Sans CJK JP", 40, "bold")

        tk.Label(settings_frame, text="プレイヤー人数:", 
                font=("Noto Sans CJK JP", 30, "bold"), width=20, height=2).grid(row=0, column=0, sticky="e")
        self.players_var = tk.StringVar(value=str(self.default_settings['players']))
        tk.Entry(settings_frame, textvariable=self.players_var, width=10, font=font_settings).grid(row=0, column=1)
       
        tk.Label(settings_frame, text="行数:", 
                font=("Noto Sans CJK JP", 30, "bold"), width=20, height=2).grid(row=1, column=0, sticky="e")
        self.rows_var = tk.StringVar(value=str(self.default_settings['rows']))
        tk.Entry(settings_frame, textvariable=self.rows_var, width=10, font=font_settings).grid(row=1, column=1)
        
        tk.Label(settings_frame, text="列数:", 
                font=("Noto Sans CJK JP", 30, "bold"), width=20, height=2).grid(row=2, column=0, sticky="e")
        self.cols_var = tk.StringVar(value=str(self.default_settings['cols']))
        tk.Entry(settings_frame, textvariable=self.cols_var, width=10, font=font_settings).grid(row=2, column=1)
        
        # スタートボタン
        tk.Button(self.menu_frame, text="ゲーム開始", 
                 command=self.start_game, bg="blue", fg="white", font=("Noto Sans CJK JP", 48, "bold"), width=20, height=2).pack(pady=10, anchor="center")                
    
    def start_game(self):
        """ゲームを開始"""
        try:
            num_players = int(self.players_var.get())
            rows = int(self.rows_var.get())
            cols = int(self.cols_var.get())
            
            if num_players < 1 or rows < 2 or cols < 2 or (rows * cols) % 2 != 0:
                messagebox.showerror("エラー", "無効な設定です。行数×列数は偶数にしてください。")
                return
        except ValueError:
            messagebox.showerror("エラー", "数値を入力してください")
            return
        
        # プレイヤー名の入力
        self.players = []
        for i in range(num_players):
            name = simpledialog.askstring("プレイヤー名", 
                                        f"プレイヤー{i+1}の名前を入力してください:", 
                                        parent=self.root)
            if not name:
                name = f"プレイヤー{i+1}"
            self.players.append({"name": name, "score": 0})
        
        # ゲーム盤面の初期化
        self.initialize_game(rows, cols)
        
        # ゲーム画面を表示
        self.show_game()
    
    def initialize_game(self, rows, cols):
        """ゲーム盤面を初期化"""
        self.rows = rows
        self.cols = cols
        self.current_player = 0
        self.flipped_cards = []
        self.matched_pairs = 0
        self.start_time = time.time()
        
        # カードペアの生成
        num_pairs = (rows * cols) // 2
        card_values = list(range(1, num_pairs + 1)) * 2
        random.shuffle(card_values)
        
        self.grid = []
        index = 0
        for _ in range(rows):
            row = []
            for _ in range(cols):
                row.append(card_values[index])
                index += 1
            self.grid.append(row)
        
        # カードの状態 (False=裏面, True=表面)
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
    
    def show_game(self):
        """ゲーム画面を表示"""
        if self.menu_frame:
            self.menu_frame.destroy()
        
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(expand=True, fill="both")
        
        # ステータスバー
        status_frame = tk.Frame(self.game_frame)
        status_frame.pack(fill="x", pady=10)
        
        self.status_label = tk.Label(status_frame, text="", font=("Noto Sans CJK JP", 14))
        self.status_label.pack(side="left", padx=20)
        
        self.timer_label = tk.Label(status_frame, text="00:00", font=("Noto Sans CJK JP", 14))
        self.timer_label.pack(side="right", padx=20)
        
        # カードグリッド
        grid_frame = tk.Frame(self.game_frame)
        grid_frame.pack(expand=True)
        
        self.card_buttons = []
        for i in range(self.rows):
            row_buttons = []
            for j in range(self.cols):
                btn = tk.Button(grid_frame, image=self.card_images["back"],
                              command=lambda i=i, j=j: self.flip_card(i, j))
                btn.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(btn)
            self.card_buttons.append(row_buttons)
        
        # メニューボタン
        tk.Button(self.game_frame, text="メニューに戻る", 
                 command=self.show_menu).pack(pady=10)
        
        self.update_status()
        self.update_timer()
    
    def update_status(self):
        """ステータスを更新"""
        status_text = f"現在のターン: {self.players[self.current_player]['name']}"
        score_text = " | ".join([f"{p['name']}: {p['score']}点" for p in self.players])
        self.status_label.config(text=f"{status_text} | {score_text}")
    
    def update_timer(self):
        """タイマーを更新"""
        if not self.game_active:
            return
        
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        
        # 1秒後に再度更新
        self.root.after(1000, self.update_timer)
    
    def flip_card(self, row, col):
        """カードをめくる"""
        if self.revealed[row][col] or len(self.flipped_cards) >= 2:
            return
        
        # カードを表面に
        self.revealed[row][col] = True
        card_value = self.grid[row][col]
        self.card_buttons[row][col].config(
            image=self.card_images[f"card_{card_value}"])
        
        self.flipped_cards.append((row, col))
        
        # 2枚めくったらチェック
        if len(self.flipped_cards) == 2:
            self.root.after(1000, self.check_match)
    
    def check_match(self):
        """めくったカードが一致するかチェック"""
        (row1, col1), (row2, col2) = self.flipped_cards
        card1 = self.grid[row1][col1]
        card2 = self.grid[row2][col2]
        
        if card1 == card2:
            # 一致した場合
            self.players[self.current_player]['score'] += 2
            self.matched_pairs += 1
            
            # カードを無効化
            for row, col in self.flipped_cards:
                self.card_buttons[row][col].config(state="disabled", relief="sunken")
            
            # ゲーム終了チェック
            if self.matched_pairs == (self.rows * self.cols) // 2:
                self.end_game()
        else:
            # 一致しなかった場合
            for row, col in self.flipped_cards:
                self.revealed[row][col] = False
                self.card_buttons[row][col].config(image=self.card_images["back"])
            
            # 次のプレイヤー
            self.current_player = (self.current_player + 1) % len(self.players)
        
        self.flipped_cards = []
        self.update_status()
    
    def end_game(self):
        """ゲームを終了"""
        self.game_active = False
        
        # 結果を計算
        elapsed = int(time.time() - self.start_time)
        winner = max(self.players, key=lambda x: x['score'])
        
        # 結果メッセージ
        result_text = "ゲーム終了!\n\n"
        result_text += f"経過時間: {elapsed // 60}分{elapsed % 60}秒\n\n"
        result_text += "スコア:\n"
        for player in self.players:
            result_text += f"{player['name']}: {player['score']}点\n"
        
        result_text += f"\n優勝者: {winner['name']}!"
        
        messagebox.showinfo("ゲーム結果", result_text)
    
    def run(self):
        """ゲームを実行"""
        self.game_active = True
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    game.run()
