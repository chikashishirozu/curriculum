import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from mpmath import mp, mpf, sin, cos, tan, pi

class HighPrecisionTrigApp:
    def __init__(self, root):
        self.root = root
        self.root.title("高精度三角関数計算機 (mpmath)")
        self.root.geometry("800x600")
        
        # mpmath設定（初期精度）
        mp.dps = 100  # デフォルト精度（ユーザーが変更可能）
        
        self.create_widgets()
    
    def create_widgets(self):
        # 精度設定
        precision_frame = ttk.Frame(self.root)
        precision_frame.pack(pady=10, padx=10, fill="x")
        
        ttk.Label(precision_frame, text="精度 (桁数):").pack(side="left")
        self.precision_var = tk.IntVar(value=100)
        precision_entry = ttk.Entry(precision_frame, textvariable=self.precision_var, width=10)
        precision_entry.pack(side="left", padx=5)
        
        ttk.Button(precision_frame, text="精度適用", command=self.set_precision).pack(side="left")
        
        # 入力角度
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10, padx=10, fill="x")
        
        ttk.Label(input_frame, text="角度 (ラジアン):").pack(side="left")
        self.angle_var = tk.StringVar(value="0")
        angle_entry = ttk.Entry(input_frame, textvariable=self.angle_var, width=50)
        angle_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # 関数選択
        func_frame = ttk.Frame(self.root)
        func_frame.pack(pady=10)
        
        ttk.Label(func_frame, text="関数:").pack(side="left")
        self.func_var = tk.StringVar(value="sin")
        for func in ["sin", "cos", "tan"]:
            ttk.Radiobutton(func_frame, text=func.upper(), variable=self.func_var, value=func).pack(side="left", padx=10)
        
        # 計算ボタン
        calc_button = ttk.Button(self.root, text="計算", command=self.calculate)
        calc_button.pack(pady=10)
        
        # 結果表示
        result_frame = ttk.Frame(self.root)
        result_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        ttk.Label(result_frame, text="結果:").pack(anchor="w")
        self.result_text = scrolledtext.ScrolledText(result_frame, height=20, wrap=tk.WORD)
        self.result_text.pack(fill="both", expand=True)
    
    def set_precision(self):
        try:
            dps = self.precision_var.get()
            if dps < 10 or dps > 2000000:
                messagebox.showwarning("警告", "精度は10〜2000000桁の範囲で設定してください。")
                return
            mp.dps = dps
            messagebox.showinfo("成功", f"精度を {dps} 桁に設定しました。")
        except ValueError:
            messagebox.showerror("エラー", "有効な整数を入力してください。")
    
    def calculate(self):
        try:
            angle_str = self.angle_var.get().strip()
            if not angle_str:
                messagebox.showerror("エラー", "角度を入力してください。")
                return
            
            # mpfに変換（高精度）
            x = mpf(angle_str)
            
            func = self.func_var.get()
            if func == "sin":
                result = sin(x)
            elif func == "cos":
                result = cos(x)
            else:  # tan
                result = tan(x)
            
            # 結果を文字列化
            result_str = str(result)
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"{func.upper()}({angle_str}) = \n{result_str}\n\n")
            self.result_text.insert(tk.END, f"使用精度: {mp.dps} 桁\n")
            self.result_text.insert(tk.END, f"角度 (ラジアン): {x}\n")
            
            # コピー用ヒント
            self.result_text.insert(tk.END, "\n(結果はクリップボードにコピー可能です)")
            
        except Exception as e:
            messagebox.showerror("計算エラー", f"計算中にエラーが発生しました:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HighPrecisionTrigApp(root)
    root.mainloop()
