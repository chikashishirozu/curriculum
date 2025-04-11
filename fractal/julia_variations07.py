import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# フォント設定
try:
    font_path = "./NotoSansCJK-Regular.ttc"
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
except:
    plt.rcParams['font.family'] = 'Noto Sans CJK JP'

def julia_set(c, width=800, height=800, xmin=-1.5, xmax=1.5, 
              ymin=-1.5, ymax=1.5, max_iter=100, func=lambda z, c: z**2 + c):
    # 初期化処理（これが欠落していた）
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    Z = X + Y * 1j  # ここでZを定義
    julia = np.zeros(Z.shape, dtype=int)
    
    for i in range(max_iter):
        mask = np.abs(Z) < 1000  # ここで正しくZを使用できる
        Z[mask] = func(Z[mask], c)  # 関数適用
        julia += mask
    
    return julia

def plot_julia_variations():
    patterns = [
        (lambda z, c: z**2 + c, "標準 z² + c", 'viridis'),
        (lambda z, c: z**3 + c, "3次 z³ + c", 'plasma'),
        (lambda z, c: np.sin(z) + c, "sin(z) + c", 'magma'),
    ]
    
    plt.figure(figsize=(15, 5))
    for i, (func, title, cmap) in enumerate(patterns, 1):
        julia = julia_set(c=0.355+0.355j, func=func)
        plt.subplot(1, 3, i)
        plt.imshow(julia, cmap=cmap, extent=(-1.5, 1.5, -1.5, 1.5))
        plt.title(title)
    plt.tight_layout()
    plt.savefig('julia_variations.png', dpi=300)
    plt.show()

plot_julia_variations()
