import cv2

def binarize(img_path, threshold):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    binarized = img < threshold
    binarized = (binarized * 255).astype('uint8')
    cv2.imwrite('binarized.png', binarized)
    return

binarize('mapa.png', 150)