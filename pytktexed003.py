import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, font
import os

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter 高機能テキストエディター")
        self.root.geometry("700x500")
        
        self.file_path = None  # 現在開いているファイルのパス
        self.current_font_size = 12  # 初期フォントサイズ
        self.current_font = font.Font(family="Helvetica", size=self.current_font_size)        

        # メニューバー
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # ファイルメニュー
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="新規作成", command=self.new_file)
        file_menu.add_command(label="開く", command=self.open_file)
        file_menu.add_command(label="保存", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.root.quit)
        self.menu_bar.add_cascade(label="ファイル", menu=file_menu)
        
         # フォントメニュー
        font_menu = tk.Menu(self.menu_bar, tearoff=0)
        for size in [10, 12, 14, 16, 18, 20, 22, 24]:
            font_menu.add_command(label=f"{size} pt", command=lambda s=size: self.change_font_size(s))
        self.menu_bar.add_cascade(label="フォントサイズ", menu=font_menu)       

        # 編集メニュー
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="コピー", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="カット", command=lambda: self.text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="ペースト", command=lambda: self.text_area.event_generate("<<Paste>>"))
        self.menu_bar.add_cascade(label="編集", menu=edit_menu)

        # 表示メニュー（背景色・フォント変更）
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        view_menu.add_command(label="背景色を変更", command=self.change_bg_color)
        view_menu.add_command(label="フォントを変更", command=self.change_font)
        self.menu_bar.add_cascade(label="表示", menu=view_menu)

        # 検索バー
        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(fill=tk.X, padx=5, pady=5)

        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.search_button = tk.Button(self.search_frame, text="検索", command=self.search_text)
        self.search_button.pack(side=tk.RIGHT)

        # テキストウィジェット
        self.text_area = tk.Text(self.root, wrap=tk.WORD, undo=True)
        self.text_area.pack(expand=True, fill=tk.BOTH)

        # スクロールバー
        self.scrollbar = tk.Scrollbar(self.text_area)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)

        # 右クリックメニュー
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="コピー", command=lambda: self.text_area.event_generate("<<Copy>>"))
        self.context_menu.add_command(label="カット", command=lambda: self.text_area.event_generate("<<Cut>>"))
        self.context_menu.add_command(label="ペースト", command=lambda: self.text_area.event_generate("<<Paste>>"))
        self.text_area.bind("<Button-3>", self.show_context_menu)
        
    def update_title(self, filename="(新規ファイル)"):
        """ウィンドウタイトルを更新する"""
        self.root.title(f"Tkinter 高機能テキストエディター - {filename}")

    def new_file(self):
        """新規作成 - テキストエリアをリセット"""
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.update_title("(新規ファイル)")

    def open_file(self):
        """ファイルを開く"""    
        file_path = filedialog.askopenfilename(filetypes=[("テキストファイル", "*.txt"), ("すべてのファイル", "*.*")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())
                
            self.file_path = file_path
            self.update_title(os.path.basename(file_path))  # ファイル名のみ表示               

    def save_file(self):
        """ファイルを保存"""
        if not self.file_path:
            self.file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("テキストファイル", "*.txt")])
        
        if self.file_path:
            with open(self.file_path, "w", encoding="utf-8") as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.update_title(os.path.basename(self.file_path))  # タイトル更新
            messagebox.showinfo("保存完了", "ファイルを保存しました。")

    def search_text(self):
        self.text_area.tag_remove("search", "1.0", tk.END)
        keyword = self.search_entry.get()
        if keyword:
            start = "1.0"
            while True:
                start = self.text_area.search(keyword, start, stopindex=tk.END)
                if not start:
                    break
                end = f"{start}+{len(keyword)}c"
                self.text_area.tag_add("search", start, end)
                self.text_area.tag_config("search", background="yellow")
                start = end

    def change_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.config(bg=color)

    def change_font(self):
        font_choice = tk.Toplevel(self.root)
        font_choice.title("フォント選択")

        font_list = list(font.families())
        font_listbox = tk.Listbox(font_choice, height=10)
        font_listbox.pack(fill=tk.BOTH, expand=True)

        for f in font_list:
            font_listbox.insert(tk.END, f)

        def apply_font():
            selected_font = font_listbox.get(tk.ACTIVE)
            self.current_font.configure(family=selected_font)
            self.text_area.config(font=self.current_font)
            font_choice.destroy()

        apply_button = tk.Button(font_choice, text="適用", command=apply_font)
        apply_button.pack()
        
    def change_font_size(self, size):
        """フォントサイズを変更"""
        self.current_font_size = size
        self.current_font.configure(size=self.current_font_size)
        self.text_area.configure(font=self.current_font)        

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()

