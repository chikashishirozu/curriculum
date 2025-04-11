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

def sierpinski_triangle(size=512, iterations=50000):
    vertices = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]])
    points = np.zeros((iterations, 2))
    points[0] = [0.5, 0.5]  # 開始点
    
    for i in range(1, iterations):
        vertex = vertices[np.random.randint(0, 3)]
        points[i] = (points[i-1] + vertex) / 2
    
    return points

points = sierpinski_triangle()

plt.figure(figsize=(10, 10))
plt.scatter(points[:, 0], points[:, 1], s=0.1, c='black')
plt.axis('equal')
plt.axis('off')
plt.title('シェルピンスキーの三角形')
plt.xlabel('実部')
plt.ylabel('虚部')

# 画像をファイルに保存
plt.savefig('mandelbrot018.png', dpi=300, bbox_inches='tight')
plt.show()
