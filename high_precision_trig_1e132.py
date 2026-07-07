import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import gzip
import os
import psutil
from mpmath import mp, mpf, sin, cos, tan, radians
import queue

class HighPrecisionTrigApp:
    def __init__(self, root):
        self.root = root
        self.root.title("高精度三角関数計算機 - 実用版 (sin/cos/tan)")
        self.root.geometry("1120x880")

        mp.dps = 1000000                    # 安全な初期値
        self.last_result = None
        self.last_output_info = ""
        self.is_calculating = False
        self.calc_start_time = None
        self.result_queue = queue.Queue()
        self.process = psutil.Process()

        self.create_widgets()

    def create_widgets(self):
        # 上部
        top = ttk.Frame(self.root)
        top.pack(pady=10, padx=12, fill="x")

        ttk.Label(top, text="精度 (桁数):").pack(side="left")
        self.precision_var = tk.IntVar(value=1000000)
        ttk.Entry(top, textvariable=self.precision_var, width=15).pack(side="left", padx=5)
        ttk.Button(top, text="適用", command=self.set_precision).pack(side="left", padx=5)

        self.status_label = ttk.Label(top, text="待機中", foreground="green", font=("Consolas", 11, "bold"))
        self.status_label.pack(side="right", padx=10)

        self.time_label = ttk.Label(top, text="経過: 0.0 秒", foreground="blue", font=("Consolas", 10))
        self.time_label.pack(side="right", padx=20)

        ttk.Button(top, text="計算停止", command=self.stop_calc).pack(side="right", padx=5)
        ttk.Button(top, text="結果保存", command=self.start_save).pack(side="right", padx=5)

        # 入力
        input_f = ttk.LabelFrame(self.root, text="入力", padding=10)
        input_f.pack(pady=8, padx=12, fill="x")
        ttk.Label(input_f, text="角度:").grid(row=0, column=0, sticky="w", pady=4)
        self.angle_var = tk.StringVar(value="28.7684")
        ttk.Entry(input_f, textvariable=self.angle_var, width=65).grid(row=0, column=1, padx=8, sticky="ew")

        self.unit_var = tk.StringVar(value="degrees")
        ttk.Radiobutton(input_f, text="度数 (degrees)", variable=self.unit_var, value="degrees").grid(row=1, column=1, sticky="w")
        ttk.Radiobutton(input_f, text="ラジアン", variable=self.unit_var, value="radians").grid(row=2, column=1, sticky="w")

        # 関数選択（3つすべて）
        func_f = ttk.LabelFrame(self.root, text="関数", padding=10)
        func_f.pack(pady=8, padx=12, fill="x")
        self.func_var = tk.StringVar(value="sin")
        ttk.Radiobutton(func_f, text="SIN", variable=self.func_var, value="sin").grid(row=0, column=0, padx=40)
        ttk.Radiobutton(func_f, text="COS", variable=self.func_var, value="cos").grid(row=0, column=1, padx=40)
        ttk.Radiobutton(func_f, text="TAN", variable=self.func_var, value="tan").grid(row=0, column=2, padx=40)

        ttk.Button(self.root, text="計算開始", command=self.start_calculation).pack(pady=15)

        self.result_text = scrolledtext.ScrolledText(self.root, height=28, font=("Consolas", 10))
        self.result_text.pack(pady=8, padx=12, fill="both", expand=True)

    def set_precision(self):
        dps = self.precision_var.get()
        if dps > 5000000:
            if not messagebox.askyesno("警告", f"{dps:,} 桁は時間がかかります（10分以上）。続けますか？"):
                return
        mp.dps = dps
        messagebox.showinfo("設定完了", f"精度を {dps:,} 桁に設定しました")

    def start_calculation(self):
        if self.is_calculating:
            messagebox.showinfo("情報", "計算中です...")
            return

        self.is_calculating = True
        self.calc_start_time = time.time()
        self.status_label.config(text="計算中...", foreground="red")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "計算を開始しています...\n")

        threading.Thread(target=self.calculate, daemon=True).start()
        self.update_status()

    def calculate(self):
        try:
            x = mpf(self.angle_var.get().strip())
            if self.unit_var.get() == "degrees":
                x = radians(x)

            func = self.func_var.get()
            if func == "sin":
                result = sin(x)
            elif func == "cos":
                result = cos(x)
            else:
                result = tan(x)

            self.result_queue.put(("success", result))
        except Exception as e:
            self.result_queue.put(("error", str(e)))

    def update_status(self):
        if not self.is_calculating:
            return

        elapsed = time.time() - self.calc_start_time
        mem = self.process.memory_info().rss // (1024 * 1024)
        self.time_label.config(text=f"経過: {elapsed:.1f} 秒 | メモリ: {mem:,} MB")

        try:
            while not self.result_queue.empty():
                typ, data = self.result_queue.get()
                if typ == "success":
                    self.finish_calc(data)
                else:
                    self.show_error(data)
                return
        except:
            pass

        self.root.after(1000, self.update_status)

    def finish_calc(self, result):
        self.is_calculating = False
        self.last_result = result
        self.status_label.config(text="計算完了", foreground="green")

        preview = str(result)[:150]
        func_name = self.func_var.get().upper()

        self.last_output_info = (f"関数: {func_name}\n"
                                f"角度: {self.angle_var.get()} [{self.unit_var.get()}]\n"
                                f"精度: {mp.dps:,} 桁\n"
                                f"計算時間: {time.time()-self.calc_start_time:.1f} 秒\n\n")

        info = self.last_output_info + f"結果 (先頭150桁):\n{preview}\n\n... (保存で全文取得可能)"
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, info)

    def show_error(self, msg):
        self.is_calculating = False
        self.status_label.config(text="エラー", foreground="red")
        self.result_text.insert(tk.END, f"\nエラー: {msg}")

    def stop_calc(self):
        self.is_calculating = False
        self.status_label.config(text="停止要求済み", foreground="orange")

    def start_save(self):
        if not self.last_result:
            messagebox.showwarning("警告", "先に計算を実行してください。")
            return

        threading.Thread(target=self.save_file, daemon=True).start()

    def save_file(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("Gzip files", "*.gz"), ("All files", "*.*")]
            )
            if not file_path:
                return

            full_text = self.last_output_info + "結果:\n" + str(self.last_result)
            use_gzip = file_path.endswith('.gz')

            if use_gzip:
                with gzip.open(file_path, "wt", encoding="utf-8", compresslevel=6) as f:
                    f.write(full_text)
            else:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(full_text)

            size_mb = os.path.getsize(file_path) / (1024*1024)
            self.root.after(0, lambda: messagebox.showinfo("保存完了", 
                f"保存完了！\n{file_path}\nサイズ: {size_mb:.2f} MB"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("保存エラー", str(e)))

if __name__ == "__main__":
    root = tk.Tk()
    app = HighPrecisionTrigApp(root)
    root.mainloop()
