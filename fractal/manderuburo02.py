import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors, font_manager
import matplotlib
print(matplotlib.rcsetup.interactive_bk)
print(matplotlib.rcsetup.non_interactive_bk)
# バックエンド設定（Qt5Aggを使用）
matplotlib.use('QtAgg')

# フォント設定
try:
    font_path = "/home/hiroppy123/.local/share/fonts/NotoSansJP-VariableFont_wght.ttf"
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
except:
    plt.rcParams['font.family'] = 'sazanami-gothic-fonts'

def mandelbrot_numpy(width, height, xmin, xmax, ymin, ymax, max_iter):
    # 複素数のグリッドを作成
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    c = x + y[:, None] * 1j  # 複素数平面のグリッドを作成
    
    # 計算用の配列を初期化
    z = np.zeros_like(c, dtype=np.complex128)
    mandelbrot_set = np.zeros(c.shape, dtype=int)
    
    # マンデルブロ計算
    for n in range(max_iter):
        mask = np.abs(z) <= 2  # まだ発散していない点
        z[mask] = z[mask]**2 + c[mask]
        mandelbrot_set[mask] = n
    
    return mandelbrot_set

# パラメータ設定
width, height = 800, 800  # 画像サイズ
xmin, xmax = -2.0, 1.0    # x範囲（実部）
ymin, ymax = -1.5, 1.5    # y範囲（虚部）
max_iter = 100            # 最大反復回数

# マンデルブロ集合を生成
mandelbrot_set = mandelbrot_numpy(width, height, xmin, xmax, ymin, ymax, max_iter)

# 可視化
plt.figure(figsize=(10, 10))
plt.imshow(mandelbrot_set, extent=(xmin, xmax, ymin, ymax), 
           cmap='cool', norm=colors.PowerNorm(0.3))           
plt.colorbar(label='反復回数')
plt.title('マンデルブロ集合')
plt.xlabel('実部')
plt.ylabel('虚部')

# 画像をファイルに保存
plt.savefig('mandelbrot05.png', dpi=300, bbox_inches='tight')
plt.show()
