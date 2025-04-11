import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors, font_manager
import matplotlib
# バックエンド設定（Qt5Aggを使用）
matplotlib.use('Qt5Agg')

# フォント設定
try:
    font_path = "/home/hiroppy123/.local/share/fonts/NotoSansJP-VariableFont_wght.ttf"
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
except:
    plt.rcParams['font.family'] = 'sazanami-gothic-fonts'

def newton_fractal(width=800, height=800, xmin=-2.0, xmax=2.0, ymin=-2.0, ymax=2.0, max_iter=50):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    Z = X + Y * 1j
    roots = [1, -0.5+0.866j, -0.5-0.866j]  # z^3-1=0の解
    colors = np.zeros(Z.shape, dtype=int)
    
    for i in range(max_iter):
        Z = Z - (Z**3 - 1)/(3*Z**2)
    
    # 各点がどの解に収束したかを判定
    for i, root in enumerate(roots):
        colors[np.isclose(Z, root, atol=1e-3)] = i + 1
    
    return colors

newton = newton_fractal()

plt.figure(figsize=(10, 10))
plt.imshow(newton, cmap='viridis', extent=(-2.0, 2.0, -2.0, 2.0))
plt.title('ニュートンフラクタル (z^3-1=0)')
plt.xlabel('実部')
plt.ylabel('虚部')

# 画像をファイルに保存
plt.savefig('mandelbrot08.png', dpi=300, bbox_inches='tight')
plt.show()
