import math
import time

def sqrt(n, one):
    """Newton法による固定小数点平方根（多倍長対応）"""
    floating_point_precision = 10**16
    n_float = float((n * floating_point_precision) // one) / floating_point_precision
    x = int(floating_point_precision * math.sqrt(n_float)) * one // floating_point_precision
    n_one = n * one
    while True:
        x_old = x
        x = (x + n_one // x) // 2
        if x == x_old:
            break
    return x

def pi_chudnovsky_bs(digits):
    """
    Chudnovsky法 + Binary Splitting で π を digits 桁計算
    戻り値: 整数 (pi * 10**digits)
    """
    C = 640320
    C3_OVER_24 = C**3 // 24

    def bs(a, b):
        """Binary Splitting 再帰関数"""
        if b - a == 1:
            if a == 0:
                Pab = Qab = 1
            else:
                Pab = (6*a - 5) * (2*a - 1) * (6*a - 1)
                Qab = a * a * a * C3_OVER_24
            Tab = Pab * (13591409 + 545140134 * a)
            if a % 2 == 1:
                Tab = -Tab
            return Pab, Qab, Tab
        else:
            m = (a + b) // 2
            Pam, Qam, Tam = bs(a, m)
            Pmb, Qmb, Tmb = bs(m, b)
            Pab = Pam * Pmb
            Qab = Qam * Qmb
            Tab = Qmb * Tam + Pam * Tmb
            return Pab, Qab, Tab

    # 必要な項数の見積もり
    DIGITS_PER_TERM = math.log10(C3_OVER_24 / 6 / 2 / 6)  # 約14.18桁/項
    N = int(digits / DIGITS_PER_TERM + 2)

    P, Q, T = bs(0, N)

    one = 10**digits
    sqrtC = sqrt(10005 * one, one)
    pi = (Q * 426880 * sqrtC) // T
    return pi

if __name__ == "__main__":
    digits = 100000  # 10万桁
    print(f"π を {digits} 桁計算中...")
    start = time.time()
    
    pi_int = pi_chudnovsky_bs(digits)
    
    # 文字列に変換して保存
    pi_str = str(pi_int)
    pi_str = pi_str[0] + "." + pi_str[1:]
    
    end = time.time()
    print(f"計算完了！ 所要時間: {end - start:.2f} 秒")
    
    # 先頭100桁を表示
    print("π ≈", pi_str[:102])
    
    # ファイル保存（オプション）
    with open("pi_100000_digits.txt", "w") as f:
        f.write(pi_str)
    print("全桁を 'pi_100000_digits.txt' に保存しました。")
