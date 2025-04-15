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

def burning_ship(width=800, height=800, xmin=-2.0, xmax=1.0, ymin=-2.0, ymax=1.0, max_iter=100):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    C = X + Y * 1j
    Z = np.zeros_like(C)
    ship = np.zeros(C.shape, dtype=int)
    
    for i in range(max_iter):
        mask = np.abs(Z) < 10  # 発散チェック
        Z[mask] = (np.abs(np.real(Z[mask])) + 1j * np.abs(np.imag(Z[mask])))**2 + C[mask]
        ship += mask
    
    return ship

ship = burning_ship()

plt.figure(figsize=(10, 10))
plt.imshow(ship, cmap='cool', extent=(-2.0, 1.0, -2.0, 1.0))
plt.colorbar(label='反復回数')
plt.title('バーニングシップフラクタル')
plt.xlabel('実部')
plt.ylabel('虚部')

# 画像をファイルに保存
plt.savefig('mandelbrot015.png', dpi=300, bbox_inches='tight')
plt.show()
