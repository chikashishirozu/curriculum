import tkinter as tk
from sympy import sympify, SympifyError


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.geometry("300x250")
        self.master.title('Calculation')

        self.entry = tk.Entry(self.master)

        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        self.create_widgets()

    def input(self, action):
        self.entry.insert(tk.END, action)

    def clear_all(self):
        self.entry.delete(0, tk.END)

    def clear_one(self):
        txt = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, txt[:-1])

    def equals(self):
        try:
            # 入力された式を取得し、演算子を置換
            expr = self.entry.get().replace('÷', '/').replace('x', '*').replace('%', '/100')
            # Sympyで式を評価
            result = sympify(expr)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(result.evalf()))
        except SympifyError:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error")
        except Exception as e:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, f"Error: {str(e)}")

    def create_widgets(self):
        file_menu = tk.Menu(self.menu_bar)
        file_menu.add_command(label='Exit', command=self.master.quit)
        self.menu_bar.add_cascade(label='File', menu=file_menu)

        self.entry.grid(row=0, column=0, columnspan=6, pady=3, sticky="ew")
        self.entry.focus_set()

        # 数字ボタン
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
            ('0', 4, 0), ('.', 4, 1), ('÷', 4, 2),
            ('x', 1, 3), ('-', 2, 3), ('+', 3, 3), ('%', 4, 3),
            ('AC', 1, 4), ('C', 1, 5),
        ]

        for (text, row, col) in buttons:
            if text in ['AC', 'C']:
                if text == 'AC':
                    cmd = self.clear_all
                else:
                    cmd = self.clear_one
            else:
                cmd = lambda t=text: self.input(t)
            
            tk.Button(self.master, text=text, width=3, 
                     command=cmd).grid(row=row, column=col)

        tk.Button(self.master, text='=', width=6,
                 command=self.equals).grid(row=4, column=4, columnspan=2)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
