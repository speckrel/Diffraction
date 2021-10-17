import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def fftshift(x, axes=None):
    """
    Shift the zero-frequency component to the center of the spectrum.
    This function swaps half-spaces for all axes listed (defaults to all).
    ----------
    x : array_like
        Input array.
    axes : int or shape tuple, optional
        Axes over which to shift.  Default is None, which shifts all axes.
    Returns
    -------
    y : ndarray
        The shifted array.
    Examples
    --------
    >>> freqs = np.fft.fftfreq(10, 0.1)
    >>> freqs
    array([ 0.,  1.,  2., ..., -3., -2., -1.])
    >>> fftshift(freqs)
    array([-5., -4., -3., -2., -1.,  0.,  1.,  2.,  3.,  4.])
    """
    x = np.asarray(x)
    if axes is None:
        axes = tuple(range(x.ndim))
        shift = [dim // 2 for dim in x.shape]
    elif isinstance(axes, integer_types):
        shift = x.shape[axes] // 2
    else:
        shift = [x.shape[ax] // 2 for ax in axes]

    return np.roll(x, shift, axes)

def supress_bg(arr):
    threshold = 0.001
    for i in range(len(arr[0])):
        for j in range(len(arr[0])):
            if np.absolute(arr[i,j])<threshold:
                arr[i,j] = 0


#Plot Attributes
N   = 500
x1  = -1000
x2  = 1000
lam = 0.532 #Wavelength in microns
z0  = 150 #Distance from screen in cm
bw  = 100 #Beam width in microns

xarr = np.linspace(x1,x2,N+1)[:N]
yarr = np.copy(xarr)
xin, yin = np.meshgrid(xarr, yarr)
xin = xin/bw
yin = yin/bw
zarr = np.exp(-(xin**2+yin**2))

xoutmax =  N*lam*z0*0.5/(x2-x1)
xoutarr = np.linspace(-xoutmax,xoutmax,N+1)[:N]
youtarr = np.copy(xoutarr)

def mask(type,p1,p2):
    ap_mask = np.zeros((N,N))
    smin = 10
    smax = 100
    sstep = 4
    if type == 'ss':
        n = int(p1*N/(x2-x1))
        ap_mask[(N-n)//2:(N+n)//2,:] = np.ones((n,N))
        smin = 8
        smax = 104
        sstep = 8
    elif type == 'ds':
        n1 = int(p1*N/(x2-x1))
        n2 = int(p2*N/(x2-x1))
        ap_mask[(N+n2)//2:(N+n2)//2+n1,:] = np.ones((n1,N))
        ap_mask[(N-n2)//2-n1:((N-n2)//2),:] = np.ones((n1,N))
        smin = 8
        smax = 64
        sstep = 8
    elif type == 'w':
        n = int(p1 * N / (x2 - x1))
        ap_mask[(N - n) // 2:(N + n) // 2, :] = np.ones((n, N))
        ap_mask = 1-ap_mask
        smin = 8
        smax = 256
        sstep = 8
    elif type == '1dg':
        smin = 4
        smax = 48
        sstep = 4
        xcurr = 15
        n = int(p1 * N / (x2 - x1))
        sep = 6
        while xcurr < 490:
            ap_mask[xcurr:xcurr + n, :] = np.ones((n, N))
            xcurr = xcurr + sep + n
    elif type == 'tg':
        smin = 32
        smax = 200
        sstep = 4
        n = int(p1*N/(x2-x1))
        h = int(round((0.5*np.sqrt(3)*n),0)) #Height of triangle
        ystart = N//2 + int(round(2*h/3,0))
        for j in range(ystart,ystart-h,-1):
            half_w = int(round(((ystart-j)/np.sqrt(3)),0))
            ap_mask[N//2-half_w:N//2+half_w,j] = np.ones(2*half_w)
    elif type == 'c':
        smin = 8
        smax = 100
        sstep = 4
        n = int(p1 * N / (x2 - x1))
        for j in range(N//2,N//2+n):
            yprime = j - N//2
            #print(yprime,n,sep=' ')
            xmax = int(round((np.sqrt(n**2-yprime**2)),0))
            ap_mask[N//2-xmax:N//2+xmax,j] = np.ones(2*xmax)
            ap_mask[N // 2 - xmax:N // 2 + xmax, N-j] = np.ones(2 * xmax)
    elif type == 'sq':
        n = int(0.5 * p1 * N / (x2 - x1))
        ap_mask[N//2-n:N//2+n,N//2-n:N//2+n] = np.ones((2*n, 2*n))
        smin = 8
        smax = 200
        sstep = 4
    elif type == '2dg':
        smin = 4
        smax = 48
        sstep = 4
        xcurr = 15
        n = int(p1 * N / (x2 - x1))
        sep = 6
        while xcurr < 490:
            ap_mask[xcurr:xcurr + n, :] = np.ones((n, N))
            xcurr = xcurr + sep+n
        xcurr = 15
        while xcurr < 490:
            ap_mask[:,xcurr:xcurr + n] = np.ones((N,n))
            xcurr = xcurr + sep+n
    elif type == 'hex':
        fh = open('hex.txt')
        i=0
        for line in fh.readlines():
            ap_mask[i,:] = np.array(list(map(int,list(line.strip()))))
            i = i+1

    return ap_mask,smin,smax,sstep

def plot(type,p1,p2):
    amask,smin,smax,sstep = mask(type,p1,p2)
    zin = zarr*amask
    zout = fftshift(np.fft.fftn(zin))/(N*N)
    zout = zout/np.absolute(zout[N//2,N//2])
    supress_bg(zout)
    fig = make_subplots(rows=1, cols=2,subplot_titles=('Input', 'Output'))
    fig.add_trace(go.Contour(z=zin.T[int(0.25*N):int(0.75*N),int(0.25*N):int(0.75*N)], x=xarr[int(0.25*N):int(0.75*N)], y=yarr[int(0.25*N):int(0.75*N)], colorscale='Hot',contours_showlines=False), 1, 1)
    fig.add_trace(go.Contour(z=np.absolute(zout.T)[int(0.15*N):int(0.85*N),int(0.15*N):int(0.85*N)], x=xoutarr[int(0.15*N):int(0.85*N)], y=youtarr[int(0.15*N):int(0.85*N)], colorscale='Hot', contours_showlines=False), 1, 2)
    fig.update_xaxes(title_text="x' (micron)", row=1, col=1)
    fig.update_xaxes(title_text="x (cm)", row=1, col=2)
    fig.update_layout(height=550, width=1100)
    return fig,smin,smax,sstep

