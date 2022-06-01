import numpy as np
import cv2
import numpy as np
from typing import List

# 이미지 회전 함수
def img_rotate(img: np.ndarray, angle: int) -> np.ndarray:
    # image_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image_RGB = img
    img_len, img_wid, channel = img.shape

    rotate_point = int(img_wid / 2), int(img_len / 2)
    rotate_degree = angle
    new_len, new_wid = int(img_len), int(img_wid)

    img_rotate = cv2.getRotationMatrix2D(rotate_point, rotate_degree, 0.7)
    rotate_img = cv2.warpAffine(image_RGB, img_rotate, (new_wid, new_len))

    return rotate_img


# 이미지 선명도 높이기
def img_sharpening(img: np.ndarray) -> np.ndarray:

    sharpening_mask = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

    sharpening_out = cv2.filter2D(img, -1, sharpening_mask)
    # sharpening_out = cv2.cvtColor(sharpening_out, cv2.COLOR_BGR2RGB)
    return sharpening_out


# 이미지 노이즈 제거
def img_denoising(img: np.ndarray) -> np.ndarray:
    denoising_img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    # dst = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    return denoising_img


# 이미지 전처리 총망라
def img_augmentation(img: np.ndarray) -> List[np.ndarray]:

    # 1. 기본 이미지 : img

    # 2. 기본 이미지 +15도
    img_plus_15 = img_rotate(img, 15)

    # 3. 기본 이미지 -15도
    img_minus_15 = img_rotate(img, -15)

    # 4. 선명도 높이기
    img_sharped = img_sharpening(img)

    # 5. 이미지 노이즈 제거
    img_denoised = img_denoising(img)

    augmentation_img = [img, img_plus_15, img_minus_15, img_sharped, img_denoised]

    return augmentation_img
