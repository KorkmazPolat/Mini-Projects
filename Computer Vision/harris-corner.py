from scipy import *  # import SciPy/NumPy for arrays and math
from scipy import signal  # signal processing tools (convolution)
from PIL import Image  # image I/O
from pylab import *  # plotting utilities
import os  # filesystem utilities for saving outputs


def main():  # script entry for a quick demo
  run_demo_and_save()  # run batch over sudoku images and save results

def gauss_derivative_kernels(size, sizey=None):  # build Gaussian derivative kernels (x and y)
      """ returns x and y derivatives of a 2D
          gauss kernel array for convolutions """
      size = int(size)  # ensure integer kernel half-size in x
      if not sizey:  # default y to x size if not provided
          sizey = size  # square kernel if sizey omitted
      else:
          sizey = int(sizey)  # ensure integer kernel half-size in y
      y, x = mgrid[-size:size+1, -sizey:sizey+1]  # coordinate grid for the kernel

      #x and y derivatives of a 2D gaussian with standard dev half of size
      # (ignore scale factor)
      gx = - x * exp(-(x**2/float((0.5*size)**2)+y**2/float((0.5*sizey)**2)))  # derivative in x
      gy = - y * exp(-(x**2/float((0.5*size)**2)+y**2/float((0.5*sizey)**2)))  # derivative in y

      return gx,gy  # return derivative kernels
def gauss_derivatives(im, n, ny=None):  # filter image with Gaussian derivative kernels
    """ returns x and y derivatives of an image using gaussian
        derivative filters of size n. The optional argument
        ny allows for a different size in the y direction."""

    gx,gy = gauss_derivative_kernels(n, sizey=ny)  # build derivative kernels

    imx = signal.convolve(im,gx, mode='same')  # convolve for Ix
    imy = signal.convolve(im,gy, mode='same')  # convolve for Iy

    return imx,imy  # return gradient images


def compute_harris_response(image, k=0.05):  # return three response maps: R1, R2, R3
    """ compute the Harris corner detector response function
        for each pixel in the image"""

    #derivatives
    imx,imy = gauss_derivatives(image, 3)  # compute smoothed gradients Ix, Iy

    #kernel for blurring
    gauss = gauss_kernel(3)  # Gaussian window for second-moment tensor

    #compute components of the structure tensor
    Wxx = signal.convolve(imx*imx,gauss, mode='same')  # <Ix^2>
    Wxy = signal.convolve(imx*imy,gauss, mode='same')  # <Ix Iy>
    Wyy = signal.convolve(imy*imy,gauss, mode='same')  # <Iy^2>

    #determinant and trace
    Wdet = Wxx*Wyy - Wxy**2  # determinant of 2x2 matrix
    Wtr = Wxx + Wyy  # trace of 2x2 matrix

    # R1 = det M / trace M (Noble measure)
    eps = 1e-12  # numerical stability for division
    R1 = Wdet / (Wtr + eps)  # avoid divide-by-zero

    # R2 = det M – k (trace M)**2 (Harris)
    R2 = Wdet - k * (Wtr**2)  # classic Harris score

    # R3 = min(lambda1, lambda2) (Shi-Tomasi)
    disc = Wtr**2 - 4.0*Wdet  # discriminant under sqrt
    disc = where(disc < 0, 0, disc)  # clamp negatives from numerical errors
    sqrt_disc = sqrt(disc)  # sqrt of discriminant
    lam1 = 0.5 * (Wtr + sqrt_disc)  # larger eigenvalue
    lam2 = 0.5 * (Wtr - sqrt_disc)  # smaller eigenvalue
    R3 = minimum(lam1, lam2)  # min eigenvalue response

    return R1, R2, R3  # return all three response maps

def get_harris_points(harrisim, min_distance=10, threshold=0.1, max_points=10):  # return up to N strongest corners
    """ return corners from a Harris response image
        min_distance is the minimum nbr of pixels separating
        corners and image boundary"""

    #find top corner candidates above a threshold
    corner_threshold = max(harrisim.ravel()) * threshold  # relative threshold
    harrisim_t = (harrisim > corner_threshold) * 1  # binary mask of candidates

    #get coordinates of candidates
    candidates = harrisim_t.nonzero()  # candidate coordinates (rows, cols)
    coords = [ (candidates[0][c],candidates[1][c]) for c in range(len(candidates[0]))]  # list of (r,c)
    #...and their values
    candidate_values = [harrisim[c[0]][c[1]] for c in coords]  # associated scores

    #sort candidates by score descending
    index = argsort(candidate_values)[::-1]  # strongest first

    #store allowed point locations in array
    allowed_locations = zeros(harrisim.shape)  # mask of allowed picks
    allowed_locations[min_distance:-min_distance,min_distance:-min_distance] = 1  # exclude borders

    #select the best points taking min_distance into account
    filtered_coords = []  # selected points
    for i in index:  # iterate strongest to weakest
        if allowed_locations[coords[i][0]][coords[i][1]] == 1:  # only if location allowed
            filtered_coords.append(coords[i])  # keep it
            allowed_locations[(coords[i][0]-min_distance):(coords[i][0]+min_distance),
                (coords[i][1]-min_distance):(coords[i][1]+min_distance)] = 0  # suppress neighborhood
            if max_points is not None and len(filtered_coords) >= max_points:  # stop at N
                break  # reached cap

    return filtered_coords  # list of (row,col) points
def plot_harris_points(image, filtered_coords):  # plot image and overlay corners
    """ plots corners found in image"""
    figure()  # create a new figure
    gray()  # set grayscale colormap
    imshow(image)  # display the image
    plot([p[1] for p in filtered_coords],[p[0] for p in filtered_coords],'*')  # draw corner markers
    axis('off')  # hide axes for clarity
    show()  # show the plot window

def plot_harris_points_save(image, filtered_coords, save_path):  # save plot instead of showing
    """ saves a plot with overlaid corners to the given path """
    figure()  # create a new figure
    gray()  # grayscale colormap
    imshow(image)  # display image
    plot([p[1] for p in filtered_coords],[p[0] for p in filtered_coords],'*')  # overlay corners
    axis('off')  # hide axes
    tight_layout()  # minimal margins around
    savefig(save_path, dpi=150)  # save to disk
    close()  # close the figure to free memory

def gauss_kernel(size, sizey = None):  # build normalized 2D Gaussian kernel
    """ Returns a normalized 2D gauss kernel array for convolutions """
    size = int(size)  # integer half-size in x
    if not sizey:  # default to square kernel
        sizey = size  # y half-size equals x
    else:
        sizey = int(sizey)  # ensure integer half-size in y
    x, y = mgrid[-size:size+1, -sizey:sizey+1]  # grid coordinates
    g = exp(-(x**2/float(size)+y**2/float(sizey)))  # unnormalized Gaussian
    return g / g.sum()  # normalize so kernel sums to 1

def run_demo_and_save():  # batch run on sudoku images and save figures for R1, R2, R3
    base_dir = os.path.dirname(__file__)  # directory of this script
    img_dir = os.path.join(base_dir, 'project1-images')  # images folder
    out_dir = os.path.join(base_dir, 'outputs')  # output folder
    os.makedirs(out_dir, exist_ok=True)  # create outputs directory if not exists

    images = ['sudoku1-250.bmp', 'sudoku2-250.bmp']  # demo images

    # heuristic starting thresholds per score (tune per image if needed)
    thresholds = {
        'R1': 0.02,
        'R2': 0.01,
        'R3': 0.02,
    }

    min_distance = 6  # enforce spatial separation between corners
    max_points = 100  # allow many points for richer visualization; adjust as needed
    k = 0.05  # Harris k value

    for name in images:  # iterate demo images
        img_path = os.path.join(img_dir, name)  # full path to image
        im = array(Image.open(img_path).convert('L'))  # load grayscale as array

        R1, R2, R3 = compute_harris_response(im, k=k)  # compute response maps
        responses = {'R1': R1, 'R2': R2, 'R3': R3}  # map labels to responses

        stem = os.path.splitext(name)[0]  # base filename without extension
        for label, resp in responses.items():  # for each score type
            thr = thresholds[label]  # choose threshold for this score
            coords = get_harris_points(resp, min_distance=min_distance, threshold=thr, max_points=max_points)  # select corners
            save_path = os.path.join(out_dir, f'{stem}_{label}.png')  # output path
            plot_harris_points_save(im, coords, save_path)  # save visualization
            print(f'Saved: {save_path} (points={len(coords)}, threshold={thr})')  # log output
 
if __name__=='__main__':  # run demo if executed as script
    main()  # call entry point
