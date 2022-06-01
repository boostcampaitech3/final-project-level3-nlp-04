import math
import cv2
import numpy as np
from typing import Tuple, Dict

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


# 이미지를 회전시켜주는 함수
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


def img_to_binary(img: np.ndarray) -> bytes:
    cv2.imwrite("temp.jpg", img)

    return cv2.imencode(".PNG", img)[1].tobytes()
