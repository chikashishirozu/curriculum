import numpy as np
from mayavi import mlab

def mandelbrot_3d(width=100, height=100, max_iter=30):
    """真の2Dマンデルブロト計算（3D表示用に調整）"""
    x = np.linspace(-2.0, 1.0, width)
    y = np.linspace(-1.5, 1.5, height)
    X, Y = np.meshgrid(x, y)
    C = X + Y*1j
    Z = np.zeros_like(C, dtype=np.complex128)
    mandelbrot = np.zeros(C.shape)
    
    for i in range(max_iter):
        mask = np.abs(Z) < 4
        Z[mask] = Z[mask]**2 + C[mask]
        mandelbrot += mask
    
    return mandelbrot

# 可視化設定
fig = mlab.figure(size=(800, 800), bgcolor=(1, 1, 1))

# 2Dマンデルブロトを計算
mb = mandelbrot_3d(200, 200)  # 解像度を適切に設定

# 3Dサーフェスとして表示
surf = mlab.surf(mb, colormap='jet', warp_scale='auto')
mlab.title('3Dマンデルブロ集合', height=0.9, size=0.3)
mlab.xlabel('実部')
mlab.ylabel('虚部')
mlab.outline(surf)

# 保存と表示
mlab.savefig('mandelbrot_3d.png', size=(2000, 2000))
mlab.show()
