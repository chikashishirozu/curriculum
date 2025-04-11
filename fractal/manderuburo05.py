import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors, font_manager
import matplotlib

# バックエンド設定（TkAggを使用）
matplotlib.use('TkAgg')

# フォント設定
try:
    font_path = "/home/hiroppy123/.local/share/fonts/NotoSansJP-VariableFont_wght.ttf"
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
except:
    plt.rcParams['font.family'] = 'sazanami-gothic-fonts'

def mandelbrot_numpy(width, height, xmin, xmax, ymin, ymax, max_iter):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    c = x + y[:, None] * 1j
    z = np.zeros_like(c, dtype=np.complex128)
    mandelbrot_set = np.zeros(c.shape, dtype=int)
    
    for n in range(max_iter):
        mask = np.abs(z) <= 2
        z[mask] = z[mask]**2 + c[mask]
        mandelbrot_set[mask] = n
    
    return mandelbrot_set

# パラメータ設定
width, height = 800, 800
xmin, xmax = -2.0, 1.0
ymin, ymax = -1.5, 1.5
max_iter = 100

# 計算と描画
mandelbrot_set = mandelbrot_numpy(width, height, xmin, xmax, ymin, ymax, max_iter)

plt.figure(figsize=(10, 10))
plt.imshow(mandelbrot_set, extent=(xmin, xmax, ymin, ymax), 
           cmap='winter', norm=colors.PowerNorm(0.3))
plt.colorbar(label='反復回数')
plt.title('マンデルブロ集合')
plt.xlabel('実部')
plt.ylabel('虚部')

# 画像をファイルに保存
plt.savefig('mandelbrot02.png', dpi=300, bbox_inches='tight')
plt.show()
