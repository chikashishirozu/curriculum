import numpy as np
from mayavi import mlab
import matplotlib.pyplot as plt

def mandelbulb(x, y, z, max_iter=20, power=8, bailout=4):
    pos = np.stack([x, y, z], axis=-1)
    r = np.zeros_like(x)
    
    for i in range(max_iter):
        r_current = np.sqrt(pos[...,0]**2 + pos[...,1]**2 + pos[...,2]**2)
        mask = r_current < bailout
        if not np.any(mask):
            break
        
        xy = np.sqrt(pos[...,0]**2 + pos[...,1]**2 + 1e-10)
        theta = np.arctan2(xy, pos[...,2])
        phi = np.arctan2(pos[...,1], pos[...,0] + 1e-10)
        
        zr = r_current ** power
        theta_new = theta * power
        phi_new = phi * power
        
        pos[...,0][mask] = zr[mask] * np.sin(theta_new[mask]) * np.cos(phi_new[mask]) + x[mask]
        pos[...,1][mask] = zr[mask] * np.sin(theta_new[mask]) * np.sin(phi_new[mask]) + y[mask]
        pos[...,2][mask] = zr[mask] * np.cos(theta_new[mask]) + z[mask]
        
        r[mask] += 1
    
    return r

def generate_mandelbulb(resolution=100, max_iter=20, power=8):
    x = np.linspace(-1.5, 1.5, resolution)
    y = np.linspace(-1.5, 1.5, resolution)
    z = np.linspace(-1.5, 1.5, resolution)
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    
    mb = mandelbulb(X, Y, Z, max_iter=max_iter, power=power)
    print("値の範囲:", np.min(mb), np.max(mb))
    
    # 値の分布を可視化（デバッグ用）
    plt.hist(mb.flatten(), bins=50)
    plt.show()
    
    mlab.figure(size=(800, 800), bgcolor=(1, 1, 1))
    src = mlab.pipeline.scalar_field(mb)
    
    threshold = np.percentile(mb, 95)
    mlab.pipeline.iso_surface(src, contours=[threshold], opacity=0.6, colormap='Spectral')
    
    mlab.title(f'Mandelbulb (power={power})', height=0.9, size=0.3)
    mlab.savefig('mandelbulb_3d033.png', size=(2000, 2000))
    mlab.show()

if __name__ == "__main__":
    generate_mandelbulb(resolution=100, max_iter=20, power=8)
