import numpy as np
from mayavi import mlab

def mandelbrot_3d_true(width=50, height=50, depth=50, max_iter=20):
    """3Dマンデルブロト風の集合（数学的には正確な3Dマンデルブロ集合ではありません）"""
    x = np.linspace(-2.0, 1.0, width)
    y = np.linspace(-1.5, 1.5, height)
    z = np.linspace(-1.0, 1.0, depth)
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    
    # 3D空間での発散判定（これは真の3Dマンデルブロ集合ではありません）
    # ここでは各方向の座標を組み合わせた簡易的な計算を行います
    C = X + Y*1j  # Z軸の情報は別途扱う
    V = np.zeros_like(C, dtype=np.complex128)
    result = np.zeros(C.shape)
    
    for i in range(max_iter):
        mask = np.abs(V) < 4
        V[mask] = V[mask]**2 + C[mask]  # 通常のマンデルブロト計算
        # Z軸の影響を追加（これは数学的に正確な方法ではありません）
        result += mask * (1 - Z**2 / (X**2 + Y**2 + 1))
    
    return result

# 可視化設定
fig = mlab.figure(size=(800, 800), bgcolor=(1, 1, 1))

# 3Dマンデルブロト風の集合を計算
mb = mandelbrot_3d_true(100, 100, 100)  # 解像度を下げて計算負荷を軽減

# ボリュームレンダリングで表示
src = mlab.pipeline.scalar_field(mb)
mlab.pipeline.volume(src, vmin=0, vmax=mb.max())

mlab.title('3Dマンデルブロ風集合', height=0.9, size=0.3)
mlab.xlabel('X軸')
mlab.ylabel('Y軸')
mlab.zlabel('Z軸')
mlab.colorbar(orientation='vertical')

# 保存と表示
mlab.savefig('mandelbrot_3d020.png', size=(2000, 2000))
mlab.show()
