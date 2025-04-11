from numba import jit, prange
import numpy as np
from mayavi import mlab
import time

@jit(nopython=True)
def mandelbrot_kernel(Z, C, output, iterations):
    height, width = Z.shape
    for _ in range(iterations):
        for i in prange(height):
            for j in prange(width):
                if abs(Z[i, j]) < 4:
                    Z[i, j] = Z[i, j] ** 2 + C[i, j]
                    output[i, j] += 1
    return Z

def mandelbrot_3d(width, height, max_iter, xmin, xmax, ymin, ymax):
    # 複素平面の設定
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    
    Z = np.zeros_like(C, dtype=np.complex128)
    output = np.zeros((height, width), dtype=np.float64)
    
    start_time = time.time()
    for i in range(max_iter):
        Z = mandelbrot_kernel(Z, C, output, 1)
        
        # 進捗表示
        if i % (max_iter//10) == 0 or i == max_iter-1:
            elapsed = time.time() - start_time
            remaining = (max_iter-i-1) * (elapsed/(i+1)) if i > 0 else 0
            print(f'\rIteration {i+1}/{max_iter} ({((i+1)/max_iter*100):.1f}%) | '
                  f'経過: {elapsed:.1f}s | 残り: {remaining:.1f}s', end='', flush=True)
    
    print(f"\n総計算時間: {time.time()-start_time:.2f}秒")
    return output

# パラメータ設定
params = {
    'width': 300,
    'height': 300,
    'max_iter': 50,
    'xmin': -2.0,
    'xmax': 1.0,
    'ymin': -1.5,
    'ymax': 1.5
}

# マンデルブロ集合を生成
mandelbrot_set = mandelbrot_3d(**params)

# データ正規化
mandelbrot_normalized = (mandelbrot_set - mandelbrot_set.min()) / (mandelbrot_set.max() - mandelbrot_set.min())

# 3D可視化
fig = mlab.figure(size=(800, 800), bgcolor=(1, 1, 1))
mlab.surf(mandelbrot_normalized, colormap='jet', warp_scale='auto')
mlab.title('3Dマンデルブロ集合')
mlab.xlabel('実部')
mlab.ylabel('虚部')

# 視点調整と保存
mlab.view(azimuth=45, elevation=45)
mlab.savefig('mandelbrot_3d010.png', size=(2000, 2000))
mlab.show()
