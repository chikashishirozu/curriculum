import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
from mpmath import mp, mpf, sin, cos, tan, radians

class HighPrecisionTrigApp:
    def __init__(self, root):
        self.root = root
        self.root.title("高精度三角関数計算機 (mpmath) - 改善版")
        self.root.geometry("950x720")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # ウィンドウ閉じる処理
        
        mp.dps = 100
        
        self.calc_thread = None
        self.stop_event = threading.Event()  # 中断用
        
        self.create_widgets()
    
    def create_widgets(self):
        # 上部コントロール
        top_frame = ttk.Frame(self.root)
        top_frame.pack(pady=8, padx=10, fill="x")
        
        ttk.Label(top_frame, text="精度 (桁数):").pack(side="left")
        self.precision_var = tk.IntVar(value=100)
        ttk.Entry(top_frame, textvariable=self.precision_var, width=12).pack(side="left", padx=5)
        ttk.Button(top_frame, text="精度適用", command=self.set_precision).pack(side="left", padx=5)
        
        ttk.Button(top_frame, text="結果をファイル保存", command=self.save_to_file).pack(side="right", padx=5)
        self.stop_button = ttk.Button(top_frame, text="計算中断", command=self.stop_calculation, state="disabled")
        self.stop_button.pack(side="right", padx=5)
        
        # 入力エリア
        input_frame = ttk.LabelFrame(self.root, text="入力", padding=10)
        input_frame.pack(pady=8, padx=10, fill="x")
        
        ttk.Label(input_frame, text="角度:").grid(row=0, column=0, sticky="w", pady=5)
        self.angle_var = tk.StringVar(value="45")
        ttk.Entry(input_frame, textvariable=self.angle_var, width=50).grid(row=0, column=1, sticky="ew", padx=5)
        
        self.unit_var = tk.StringVar(value="degrees")
        ttk.Radiobutton(input_frame, text="度数 (degrees)", variable=self.unit_var, value="degrees").grid(row=1, column=1, sticky="w")
        ttk.Radiobutton(input_frame, text="ラジアン (radians)", variable=self.unit_var, value="radians").grid(row=2, column=1, sticky="w")
        
        # 関数選択
        func_frame = ttk.LabelFrame(self.root, text="関数", padding=10)
        func_frame.pack(pady=8, padx=10, fill="x")
        self.func_var = tk.StringVar(value="sin")
        for i, func in enumerate(["sin", "cos", "tan"]):
            ttk.Radiobutton(func_frame, text=func.upper(), variable=self.func_var, value=func).grid(row=0, column=i, padx=20)
        
        ttk.Button(self.root, text="計算開始", command=self.start_calculation).pack(pady=12)
        
        # 結果表示
        result_frame = ttk.LabelFrame(self.root, text="結果", padding=10)
        result_frame.pack(pady=8, padx=10, fill="both", expand=True)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=28, wrap=tk.WORD, font=("Consolas", 10))
        self.result_text.pack(fill="both", expand=True)
    
    def set_precision(self):
        try:
            dps = int(self.precision_var.get())
            if 10 <= dps <= 2000000:
                mp.dps = dps
                messagebox.showinfo("成功", f"精度を {dps} 桁に設定しました。")
            else:
                messagebox.showwarning("警告", "10〜2000000の範囲で入力してください。")
        except:
            messagebox.showerror("エラー", "数値を正しく入力してください。")
    
    def start_calculation(self):
        if self.calc_thread and self.calc_thread.is_alive():
            messagebox.showinfo("情報", "計算中です...")
            return
        
        self.stop_event.clear()
        self.stop_button.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "計算を開始しています...\n")
        
        self.calc_thread = threading.Thread(target=self.calculate, daemon=True)
        self.calc_thread.start()
    
    def calculate(self):
        try:
            angle_input = self.angle_var.get().strip()
            if not angle_input:
                self.update_result("エラー: 角度を入力してください。")
                return
            
            self.update_result("角度を変換中...\n")
            x = mpf(angle_input)
            if self.unit_var.get() == "degrees":
                x = radians(x)
            
            func = self.func_var.get()
            self.update_result(f"{func.upper()} を計算中... (高精度のため時間がかかる場合があります)\n")
            
            if self.stop_event.is_set():
                return
            
            if func == "sin":
                result = sin(x)
            elif func == "cos":
                result = cos(x)
            else:
                result = tan(x)
            
            if self.stop_event.is_set():
                return
            
            result_str = str(result)
            output = f"【計算完了】\n"
            output += f"関数: {func.upper()}\n"
            output += f"入力: {self.angle_var.get()} [{self.unit_var.get()}]\n"
            output += f"精度: {mp.dps} 桁\n"
            output += f"結果:\n{result_str}\n"
            
            self.update_result(output)
            
        except Exception as e:
            self.update_result(f"計算エラー: {str(e)}")
        finally:
            self.root.after(0, lambda: self.stop_button.config(state="disabled"))
    
    def stop_calculation(self):
        self.stop_event.set()
        self.result_text.insert(tk.END, "\n\n計算中断をリクエストしました...\n")
    
    def update_result(self, text):
        self.root.after(0, lambda: self._update_text(text))
    
    def _update_text(self, text):
        self.result_text.insert(tk.END, text)
        self.result_text.see(tk.END)
    
    def save_to_file(self):
        content = self.result_text.get(1.0, tk.END).strip()
        if not content or "計算を開始しています" in content:
            messagebox.showwarning("警告", "保存する結果がありません。")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("保存完了", f"保存しました:\n{file_path}")
            except Exception as e:
                messagebox.showerror("保存エラー", str(e))
    
    def on_closing(self):
        if self.calc_thread and self.calc_thread.is_alive():
            if messagebox.askyesno("確認", "計算中です。強制終了しますか？"):
                self.stop_event.set()
                time.sleep(0.5)
                self.root.destroy()
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HighPrecisionTrigApp(root)
    root.mainloop()
