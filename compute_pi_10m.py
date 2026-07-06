from mpmath import mp
import time
import sys

# ================== 設定 ==================
digits = 10000000          # 1000万桁
output_file = "pi10000000.txt"
# =========================================

print(f"π を {digits:,} 桁計算開始...")
sys.stdout.flush()

start_time = time.time()

# 精度設定（最後の数桁の信頼性を高めるために余裕を持たせる）
mp.dps = digits + 100

# π の計算（mpmath内部で高精度Chudnovskyなどを使用）
pi = mp.pi

end_time = time.time()
elapsed = end_time - start_time

print(f"計算完了！ 所要時間: {elapsed:.2f} 秒")

# ファイルへ出力
print(f"ファイル '{output_file}' に保存中...（ファイルサイズは約10MBになります）")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(str(pi))

print(f"✅ 完了！ {digits:,} 桁のπを {output_file} に保存しました。")
print("先頭100桁:", str(pi)[:102])
