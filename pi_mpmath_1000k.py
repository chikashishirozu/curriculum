from mpmath import mp
import time

# 計算したい桁数（ここを変更してください）
digits = 1000000  # 100万桁

print(f"π を {digits} 桁計算中...")

start = time.time()

mp.dps = digits + 10  # 少し余裕を持たせる
pi = mp.pi

end = time.time()
print(f"計算完了！ 所要時間: {end - start:.2f} 秒")

# 文字列に変換してファイル保存
pi_str = str(pi)

with open(f"pi_{digits}_digits.txt", "w") as f:
    f.write(pi_str)

print(f"全 {digits} 桁を 'pi_{digits}_digits.txt' に保存しました。")
print("先頭100桁:", pi_str[:102])
