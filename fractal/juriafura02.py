import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors, font_manager
import matplotlib
# バックエンド設定（Qt5Aggを使用）
matplotlib.use('QtAgg')

# フォント設定
try:
    font_path = "/home/hiroppy123/.local/share/fonts/NotoSansJP-VariableFont_wght.ttf"
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
except:
    plt.rcParams['font.family'] = 'sazanami-gothic-fonts'

def julia_set(c=-0.7+0.27j, width=800, height=800, xmin=-1.5, xmax=1.5, ymin=-1.5, ymax=1.5, max_iter=100):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    Z = X + Y * 1j
    julia = np.zeros(Z.shape, dtype=int)
    
    for i in range(max_iter):
        mask = np.abs(Z) < 1000  # 発散チェック
        Z[mask] = Z[mask]**2 + c
        julia += mask
    
    return julia

julia = julia_set(c=-0.835-0.2321j)  # 美しいパターンのパラメータ

plt.figure(figsize=(10, 10))
plt.imshow(julia, cmap='twilight', extent=(-1.5, 1.5, -1.5, 1.5))
plt.colorbar(label='反復回数')
plt.title('ジュリア集合 (c = -0.835 -0.2321i)')
plt.xlabel('実部')
plt.ylabel('虚部')

# 画像をファイルに保存
plt.savefig('mandelbrot03.png', dpi=300, bbox_inches='tight')
plt.show()
