import numpy as np
import cv2
import math
from typing import Dict, Tuple, List

"""
Image 자체를 처리하는 함수를 모아 놓은 Module
"""
# when preprocessing
def rotate_image(
    img_byte: bytes, image_degree: float, middle_point_x: int, middle_point_y: int
) -> np.ndarray:
    encoded = np.fromstring(img_byte, dtype=np.uint8)
    image_BGR = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    image_RGB = cv2.cvtColor(image_BGR, cv2.COLOR_BGR2RGB)
    img_len, img_wid, channel = image_BGR.shape

    rotate_point = int(middle_point_x), int(middle_point_y)
    rotate_degree = image_degree
    new_len, new_wid = int(img_len * 1.3), int(img_wid)

    img_rotate = cv2.getRotationMatrix2D(rotate_point, rotate_degree, 1)
    rotate_result = cv2.warpAffine(image_RGB, img_rotate, (new_wid, new_len))

    return rotate_result


# when augmentation
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


# pre-OCR output을 기반으로 이미지의 기울기 및 명함의 중점을 파악하는 함수
def find_degree_and_point(ocr_output: Dict) -> Tuple[float, int, int]:
    test_list = ocr_output["ocr"]["word"]

    cnt = 0
    degree_sum = 0
    x_point_sum = 0
    y_point_sum = 0

    # 회전 중심축 알아야함
    for i in range(len(test_list)):
        start_point_1 = test_list[i]["points"][0]  # 1번 좌표(좌상)
        end_point_1 = test_list[i]["points"][1]  # 2번 좌표(우상)
        start_point_2 = test_list[i]["points"][3]  # 4번 좌표(좌하)
        end_point_2 = test_list[i]["points"][2]  # 3번 좌표(우하)

        # 각도 1 계산
        tangent_theta_1 = (end_point_1[1] - start_point_1[1]) / (
            end_point_1[0] - start_point_1[0]
        )
        arctangent_1 = math.atan(tangent_theta_1)
        degree_1 = math.degrees(arctangent_1)

        # 각도 2 계산
        tangent_theta_2 = (end_point_2[1] - start_point_2[1]) / (
            end_point_2[0] - start_point_2[0]
        )
        arctangent_2 = math.atan(tangent_theta_2)
        degree_2 = math.degrees(arctangent_2)

        # 각종 계산
        if (degree_1 != 0) & (degree_2 != 0):

            cnt += 1

            # if sum more than 10 times, check outliers
            if cnt >= 10:

                # temp_average_degree
                temp_average_degree = degree_sum / cnt / 2

                # if number is minus or not

                if degree_1 > temp_average_degree + 20:
                    continue
                elif degree_1 < temp_average_degree - 20:
                    continue
                elif degree_2 > temp_average_degree + 20:
                    continue
                elif degree_2 < temp_average_degree - 20:
                    continue
                else:
                    # 평균 기울기
                    degree_sum += math.degrees(arctangent_1)
                    degree_sum += math.degrees(arctangent_2)

                    # 박스 중심점
                    x_point_sum += start_point_1[0]
                    x_point_sum += end_point_1[0]
                    x_point_sum += start_point_2[0]
                    x_point_sum += end_point_2[0]

                    y_point_sum += start_point_1[1]
                    y_point_sum += end_point_1[1]
                    y_point_sum += start_point_2[1]
                    y_point_sum += end_point_2[1]

            else:
                # 평균 기울기
                degree_sum += math.degrees(arctangent_1)
                degree_sum += math.degrees(arctangent_2)

                # 박스 중심점
                x_point_sum += start_point_1[0]
                x_point_sum += end_point_1[0]
                x_point_sum += start_point_2[0]
                x_point_sum += end_point_2[0]

                y_point_sum += start_point_1[1]
                y_point_sum += end_point_1[1]
                y_point_sum += start_point_2[1]
                y_point_sum += end_point_2[1]

    image_degree = degree_sum / cnt / 2  # 이미지의 평균 기울기
    middle_point_x = x_point_sum / 4 / cnt  # 명함 x 중점
    middle_point_y = y_point_sum / 4 / cnt  # 명함 y 중점

    return image_degree, middle_point_x, middle_point_y


# 이미지를 잘라주는 함수
def crop_image(img: np.ndarray) -> np.ndarray:

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thr = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cont in contours:
        approx = cv2.approxPolyDP(cont, cv2.arcLength(cont, True) * 0.02, True)
        vtc = len(approx)
        # 만약 사각형이면 출력
        if vtc == 4:
            (x, y, w, h) = cv2.boundingRect(cont)
            pt1 = (x, y)
            pt2 = (x + w, y + h)
            # 작은 사각형 다지움
            if (w > 500) & (h > 500):
                # 이미지 자르기
                img_trim = img[pt1[1] : pt2[1], pt1[0] : pt2[0]]
                return img_trim
    
    return img


# 이미지를 바이트로 바꾸는 작업
def img_to_binary(img: np.ndarray) -> bytes:
    cv2.imwrite("temp.jpg", img)
    return cv2.imencode(".PNG", img)[1].tobytes()


# 이미지 이진화(임계처리)
def img_binary_process(img):
    image_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Adaptive Thresholding 적용
    max_output_value = 255  # 출력 픽셀 강도의 최대값
    neighborhood_size = 99
    subtract_from_mean = 10
    image_binarized = cv2.adaptiveThreshold(image_grey,
                                            max_output_value,
                                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY,
                                            neighborhood_size,
                                            subtract_from_mean)
    return image_binarized


# 이미지 대비 높이기
def img_contrast(img):
    image_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image_enhanced = cv2.equalizeHist(image_grey)

    return image_enhanced

# 이미지를 다양한 방법으로 처리한다, 처리한 이미지는 multi thread로 실행
def img_augmentation(img: np.ndarray) -> List[np.ndarray]:
    # 1. 기본 이미지(1차 전처리)
    convert_img = img_sharpening(ori_img)
    convert_img = img_denoising(convert_img)
    # 2. 이진화 이미지
    binary_image = img_binary_process(convert_img)
    # 3. 대비 향상 이미지
    contrast_image = img_contrast(convert_img)
    # 4. 색반전 이미지
    negative_image = 255 - convert_img

    # OCR input 이미지를 담은 리스트
    augmentation_img = [convert_img, binary_image, contrast_image, negative_image]

    return augmentation_img
