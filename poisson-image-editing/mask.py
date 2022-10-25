import cv2

def make_mask(original_img, shadowed_img):
    original_h, original_w, _ = original_img.shape
    shadowed_h, shadowed_w, _ = shadowed_img.shape

    # gray scale
    original_gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    shadowed_gray = cv2.cvtColor(shadowed_img, cv2.COLOR_BGR2GRAY)

    # Resize the original image to the size of the shadowed image
    resized_original_gray = cv2.resize(original_gray, (shadowed_w, shadowed_h))

    diff = cv2.absdiff(resized_original_gray, shadowed_gray)
    th = (diff.max() - diff.min()) / 2

    # cv2.imshow('original', resized_original_gray)
    # cv2.imshow('shadowed', shadowed_gray)
    # cv2.imshow('diff', diff)
    # th= 0

    mask = cv2.threshold(diff, th, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow('mask', mask)
    # cv2.waitKey(0)
    mask = cv2.blur(mask, (5, 5))

    # Resize the mask to the size of the original image
    resized_mask = cv2.resize(mask, (original_w, original_h))
    resized_mask = cv2.threshold(resized_mask, 0, 255, cv2.THRESH_BINARY)[1]


    return resized_mask
