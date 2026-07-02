import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
from mpmath import mp, mpf, sin, cos, tan, radians, degrees

class HighPrecisionTrigApp:
    def __init__(self, root):
        self.root = root
        self.root.title("高精度三角関数計算機 (mpmath)")
        self.root.geometry("900x700")
        
        mp.dps = 100  # 初期精度
        
        self.create_widgets()
        self.calc_thread = None
    
    def create_widgets(self):
        # ==================== 上部コントロール ====================
        top_frame = ttk.Frame(self.root)
        top_frame.pack(pady=8, padx=10, fill="x")
        
        ttk.Label(top_frame, text="精度 (桁数):").pack(side="left")
        self.precision_var = tk.IntVar(value=100)
        ttk.Entry(top_frame, textvariable=self.precision_var, width=12).pack(side="left", padx=5)
        
        ttk.Button(top_frame, text="精度適用", command=self.set_precision).pack(side="left", padx=5)
        
        # ファイル保存ボタン
        ttk.Button(top_frame, text="結果をファイル保存", command=self.save_to_file).pack(side="right", padx=5)
        
        # ==================== 入力エリア ====================
        input_frame = ttk.LabelFrame(self.root, text="入力", padding=10)
        input_frame.pack(pady=8, padx=10, fill="x")
        
        ttk.Label(input_frame, text="角度:").grid(row=0, column=0, sticky="w", pady=5)
        self.angle_var = tk.StringVar(value="45")
        ttk.Entry(input_frame, textvariable=self.angle_var, width=50).grid(row=0, column=1, sticky="ew", padx=5)
        
        # 単位選択
        self.unit_var = tk.StringVar(value="degrees")
        ttk.Radiobutton(input_frame, text="度数 (degrees)", variable=self.unit_var, value="degrees").grid(row=1, column=1, sticky="w")
        ttk.Radiobutton(input_frame, text="ラジアン (radians)", variable=self.unit_var, value="radians").grid(row=2, column=1, sticky="w")
        
        # 関数選択
        func_frame = ttk.LabelFrame(self.root, text="関数", padding=10)
        func_frame.pack(pady=8, padx=10, fill="x")
        
        self.func_var = tk.StringVar(value="sin")
        for i, func in enumerate(["sin", "cos", "tan"]):
            ttk.Radiobutton(func_frame, text=func.upper(), variable=self.func_var, value=func).grid(row=0, column=i, padx=20)
        
        # 計算ボタン
        ttk.Button(self.root, text="計算開始", command=self.start_calculation).pack(pady=12)
        
        # ==================== 結果表示 ====================
        result_frame = ttk.LabelFrame(self.root, text="結果", padding=10)
        result_frame.pack(pady=8, padx=10, fill="both", expand=True)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=25, wrap=tk.WORD, font=("Consolas", 10))
        self.result_text.pack(fill="both", expand=True)
    
    def set_precision(self):
        try:
            dps = self.precision_var.get()
            if dps < 10 or dps > 2000000:
                messagebox.showwarning("警告", "精度は10〜2000000の範囲で設定してください。")
                return
            mp.dps = dps
            messagebox.showinfo("設定完了", f"精度を {dps} 桁に変更しました。")
        except:
            messagebox.showerror("エラー", "有効な数値を入力してください。")
    
    def start_calculation(self):
        if self.calc_thread and self.calc_thread.is_alive():
            messagebox.showinfo("情報", "現在計算中です...")
            return
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "計算を開始しています...（画面が固まらないようバックグラウンドで処理中）\n\n")
        
        self.calc_thread = threading.Thread(target=self.calculate, daemon=True)
        self.calc_thread.start()
    
    def calculate(self):
        try:
            angle_input = self.angle_var.get().strip()
            if not angle_input:
                self.update_result("エラー: 角度を入力してください。")
                return
            
            x = mpf(angle_input)
            unit = self.unit_var.get()
            
            # 度数をラジアンに変換
            if unit == "degrees":
                x = radians(x)
            
            func = self.func_var.get()
            if func == "sin":
                result = sin(x)
            elif func == "cos":
                result = cos(x)
            else:
                result = tan(x)
            
            result_str = str(result)
            
            output = f"計算結果\n"
            output += f"関数: {func.upper()}\n"
            output += f"入力角度: {self.angle_var.get()} [{unit}]\n"
            output += f"使用精度: {mp.dps} 桁\n"
            output += f"結果:\n{result_str}\n\n"
            output += f"({unit}モードで計算済み)"
            
            self.update_result(output)
            
        except Exception as e:
            self.update_result(f"計算エラー: {str(e)}")
    
    def update_result(self, text):
        self.root.after(0, lambda: self._update_text(text))
    
    def _update_text(self, text):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
    
    def save_to_file(self):
        content = self.result_text.get(1.0, tk.END).strip()
        if not content or content.startswith("計算を開始しています"):
            messagebox.showwarning("警告", "保存する結果がありません。先に計算を実行してください。")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="結果を保存"
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("保存完了", f"結果を保存しました:\n{file_path}")
            except Exception as e:
                messagebox.showerror("保存エラー", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = HighPrecisionTrigApp(root)
    root.mainloop()
