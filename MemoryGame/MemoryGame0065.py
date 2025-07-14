import tkinter as tk
from tkinter import messagebox, simpledialog
import random
from PIL import Image, ImageTk, ImageFont, ImageDraw
import tkinter.font as tkfont
from tkinter import font as tkFont
import os
import time

def round_corners(image, radius):
    """画像の角を丸くする"""
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, image.size[0], image.size[1]), radius, fill=255)
    result = image.copy()
    result.putalpha(mask)
    return result

class MemoryGame:
    def __init__(self, root):
        self.root = root       
        self.root.title("神経衰弱ゲーム - 完全版")
        self.root.geometry("900x675")
        self.root.minsize(900, 675)
        
        font_path = "/home/hiroppy123/.local/share/fonts/NotoSansJP-Regular.ttf"
        self.pil_font = ImageFont.truetype(font_path, size=60)
        self.custom_font = tkfont.Font(family="liberation sans", size=14)        
        
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

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.is_destroyed = False
        
        # 初期化
        self.menu_frame = tk.Frame(self.root)  # 例: menu_frameを初期化
        self.load_assets()
        self.show_menu()        
    
    def load_assets(self):
        """カード画像などのアセットを読み込む"""
        self.card_images = {}  # 辞書を初期化（既存コードにない場合）
        
        # カードの表画像を読み込む
        for i in range(1, 10):  # 仮に9種類のカードがあるとする
            try:
                image = Image.open(f"cards/card_{i}.png").resize((113, 168))  # 適切なサイズに調整
                # 画像ファイルを読み込み
                image = round_corners(image, radius=9)

                self.card_images[f"card_{i}"] = ImageTk.PhotoImage(image)
            except FileNotFoundError:
                print(f"カード画像 card_{i}.png が見つかりません")
                # 簡易画像で代用
                self.card_images[f"card_{i}"] = self.create_card_image("blue")
        
        # カードの裏画像を読み込む
        try:     
            back_image = Image.open("cards/card_back.png").resize((113, 168))  # 適切なサイズに調整
            back_image = round_corners(back_image, radius=9)

            self.card_images["back"] = ImageTk.PhotoImage(back_image)
        except FileNotFoundError:
            print("裏面画像 card_back.png が見つかりません")
            self.card_images["back"] = self.create_card_image("gray")
            
    def draw_card(self, canvas, card_id, x, y, is_face_up):
        """カードを描画する"""
        if is_face_up:
            image = self.card_images.get(f"card_{card_id}")  # 表画像
        else:
            image = self.card_images.get("back")  # 裏画像
        
        if image:  # 画像が存在する場合のみ描画
            canvas.create_image(x, y, image=image, anchor="nw")
        else:
            print(f"エラー: カード画像が見つかりません (card_id: {card_id})")          
    
    def create_card_image(self, color):
        # 簡易的なカード画像を生成
        from tkinter import font as tkfont
        from PIL import Image, ImageDraw, ImageFont    
        
        # 実際のゲームでは本物のカード画像を使用してください
        width, height = 113, 168
        image = Image.new("RGB", (width, height), color)
        draw = ImageDraw.Draw(image)
        
        
        # 大きなフォントで描画（※ファイルパスは要確認）
        try:
            font = ImageFont.truetype("./NotoSansJP-Regular.ttf", 15)  # 24ptに変更
        except:
            font = ImageFont.load_default()        
        
        # 枠線を描画
        draw.rectangle([0, 0, width-1, height-1], outline="black")
        draw.text(
            (width//2, height//2),
            "テスト",  # 実際はカードの内容を表示
            fill="black",
            font=font,
            anchor="mm"  # 中央揃え
        )        
        
        return ImageTk.PhotoImage(image)
    
    def show_menu(self):
        """メニュー画面を表示"""
        self.game_active = False  # ゲームを非アクティブに
        self.stop_timer()
        
        # 既存のゲームフレームを破棄
        if hasattr(self, 'game_frame'):
            self.safe_destroy(self.game_frame)        
        
        self.stop_timer()  # タイマーを停止          
        if self.game_frame:
            self.game_frame.destroy()

        # メニューフレームの初期化        
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(fill="both", expand=True)
        
        # PILのImageFontを初期化
        font_path = "/home/hiroppy123/.local/share/fonts/NotoSansJP-Regular.ttf"
        self.pil_font = ImageFont.truetype(font_path, size=30)
        self.custom_font = tkfont.Font(family="liberation sans", size=28)

        # フォントが見つからない場合のフォールバック
        if self.custom_font.cget("family") == "liberation sans":
            self.custom_font = tkfont.Font(family="sazanami gothic", size=15)

        """print(f"Using PIL font: {self.pil_font.getname()}, size: {self.pil_font.size}")
        print(f"Using font: {self.custom_font.cget('family')}, size: {self.custom_font.cget('size')}")
        print("Available font families:", tkfont.families())"""
        
        tk.Label(self.menu_frame, text="", font=self.custom_font.actual()).pack(pady=5)
                
        # PIL で画像に文字を描画
        if self.pil_font:
            img = Image.new("RGB", (220, 57), color="#00CED1")
            draw = ImageDraw.Draw(img)
            draw.text((9, 5), "神経衰弱GAME", font=self.pil_font, fill="#191970")

            # Tkinterで表示するためImageTkに変換
            self.tk_image = ImageTk.PhotoImage(img)
            tk.Label(self.menu_frame, image=self.tk_image).pack()                
                        
        # 背景画像の読み込み        
        try:        
            bg_image_path = os.path.join(os.path.dirname(__file__), "background.jpg")
            bg_image = Image.open(bg_image_path).resize((900, 675))  # 適切なサイズに調整
            bg_image = round_corners(bg_image, radius=0)

            self.bg_photo = ImageTk.PhotoImage(bg_image)
            
            bg_label = tk.Label(self.menu_frame, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()
        except Exception as e:
            print(f"背景画像の読み込みに失敗しました: {e}")                
        
        # 設定オプション
        settings_frame = tk.Frame(self.menu_frame)
        settings_frame.pack(expand=True, padx=5, pady=5)

        # フォント設定
        font_settings = ("liberation sans", 14)

        tk.Label(settings_frame, text="プレイヤー人数:", 
                font=("liberation sans", 14), width=15, height=1).grid(row=0, column=0, sticky="e")
        self.players_var = tk.StringVar(value=str(self.default_settings['players']))
        tk.Entry(settings_frame, textvariable=self.players_var, width=5, font=font_settings).grid(row=0, column=1)
       
        tk.Label(settings_frame, text="行数:", 
                font=("liberation sans", 14), width=15, height=1).grid(row=1, column=0, sticky="e")
        self.rows_var = tk.StringVar(value=str(self.default_settings['rows']))
        tk.Entry(settings_frame, textvariable=self.rows_var, width=5, font=font_settings).grid(row=1, column=1)
        
        tk.Label(settings_frame, text="列数:", 
                font=("liberation sans", 14), width=15, height=1).grid(row=2, column=0, sticky="e")
        self.cols_var = tk.StringVar(value=str(self.default_settings['cols']))
        tk.Entry(settings_frame, textvariable=self.cols_var, width=5, font=font_settings).grid(row=2, column=1)
        
        # スタートボタン
        tk.Button(self.menu_frame, text="ゲーム開始", 
                 command=self.start_game, bg="#000080", fg="#E0FFFF", font=("liberation sans", 17), width=14, height=2).pack(pady=(5, 30), padx=5, anchor="center")                
    
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
            name = simpledialog.askstring("プレイヤー名", f"プレイヤー{i+1}の名前を入力してください:", parent=self.root)
            if name is None:  # ユーザーがキャンセルを押した場合
                return  # ゲーム開始を中止            
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
        
    def on_close(self):
        """ウィンドウを閉じる前の確認ダイアログ"""
        if messagebox.askokcancel("終了", "ゲームを終了しますか？"):
            self.is_destroyed = True  # 破棄状態を記録
            self.stop_timer()
            self.root.destroy()        
    
    def show_game(self):
        """ゲーム画面を表示（安全にmenu_frameを破棄）"""  
        self.safe_destroy(self.menu_frame)
        if self.menu_frame:
            self.menu_frame.destroy()
            
        self.game_active = True  # ゲームをアクティブに設定
        self.start_time = time.time()  # タイマー開始時間をリセット            
        
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(expand=True, fill="both")
        
        # ステータスバー
        status_frame = tk.Frame(self.game_frame)
        status_frame.pack(fill="x", pady=10)
        
        self.status_label = tk.Label(status_frame, text="", font=("liberation sans", 14))
        self.status_label.pack(side="left", padx=5, pady=(0, 20))
        
        self.timer_label = tk.Label(status_frame, text="00:00", font=("liberation sans", 17))
        self.timer_label.pack(side="right", padx=5, pady=(0, 20))
        
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
        tk.Button(self.game_frame, text="メニューに戻る", bg="#40E0D0", font=self.custom_font, command=self.show_menu).pack(padx=10, pady=(0, 20))
        
        self.update_status()
        self.update_timer()
        
    def safe_destroy(self, widget):
        """安全にウィジェットを破棄"""
        if self.is_destroyed or not widget:  # アプリケーションが破棄済みなら何もしない
            return
        try:
            if widget.winfo_exists():
                widget.destroy()
        except tk.TclError:
            pass  # Tkinterが既に破棄された場合
        except AttributeError:
            pass  # widgetが不正なオブジェクトの場合
        except Exception as e:
            print(f"safe_destroyで予期せぬエラー: {e}")  # その他エラーはログに記録       
    
    def update_status(self):
        # ウィンドウが破棄されていたら何もしない
        if not hasattr(self, 'root') or not self.root.winfo_exists():
            return    
    
        if not hasattr(self, 'status_label') or not self.status_label.winfo_exists():
            return  # ラベルが存在しない場合は何もしない    
    
        """ステータスを更新"""
        status_text = f"現在のターン: {self.players[self.current_player]['name']}"
        score_text = " | ".join([f"{p['name']}: {p['score']}点" for p in self.players])
        self.status_label.config(text=f"{status_text} | {score_text}")
    
    def update_timer(self):
        """タイマーを更新"""
        if not self.game_active:
            return
            
        if not hasattr(self, 'timer_label') or not self.timer_label.winfo_exists():
            return  # ラベルが存在しない場合は処理をスキップ            
        
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        
        # 1秒後に再度更新
        self.timer_id = self.root.after(1000, self.update_timer)
    
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
        self.stop_timer()  # タイマーを停止   
        # 結果を計算
        elapsed = int(time.time() - self.start_time)
        winner = max(self.players, key=lambda x: x['score'])
       
        # 結果メッセージ
        result_text = "ゲーム終了!\n"
        result_text += f"経過時間: {elapsed // 60}分{elapsed % 60}秒\n"
        result_text += "スコア:\n"
        for player in self.players:
            result_text += f"{player['name']}: {player['score']}点\n"
        
        result_text += f"優勝者: {winner['name']}!"
        
        messagebox.showinfo("ゲーム結果", result_text)
    
    def run(self):
        """ゲームを実行"""
        self.game_active = True
        self.root.mainloop()
        
    def stop_timer(self):
        if hasattr(self, 'timer_id') and self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

if __name__ == "__main__":
    root = tk.Tk()
    
    # 利用可能なフォントを確認
    """print("利用可能なフォント:", tkFont.families())"""
    
    # デフォルトのフォントを取得・変更
    default_font = tkFont.Font(family="Liberation Sans", size=14)    
    
    game = MemoryGame(root)
    game.run()
