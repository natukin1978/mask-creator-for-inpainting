import sys
import glob
import os
import cv2
import numpy as np

args = len(sys.argv)
if args <= 1:
    print("Usage:", file=sys.stderr)
    print(f"python {os.path.basename(__file__)} (image files folder)", file=sys.stderr)
    exit(1)

# 画像ファイルのフォルダ
img_dir_path = sys.argv[1]
list_images = glob.glob(os.path.join(img_dir_path, "*.png"))

# Haar Cascade分類器の初期化
face_cascade = cv2.CascadeClassifier("lbpcascade_animeface.xml")

for image in list_images:
    # 画像ファイルの読み込み
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 認識条件を緩くしながら探す
    min_neighbors = 100
    while True:
        faces = face_cascade.detectMultiScale(
            gray, 1.01, min_neighbors, minSize=(64, 64)
        )
        if len(faces) != 0 or min_neighbors == 0:
            break
        min_neighbors //= 2

    # 一番大きい矩形を抽出
    max_area = 0
    max_rect = None
    for x, y, w, h in faces:
        area = w * h
        if area > max_area:
            max_area = area
            max_rect = (x, y, w, h)

    # マスク画像を生成
    mask = np.zeros_like(gray)
    if max_rect:
        (x, y, w, h) = max_rect
        center_x, center_y = int(x + w / 2), int(y + h / 2)
        radius = int(max(w, h) / 2)
        cv2.circle(mask, (center_x, center_y), radius, 255, -1)

    # マスク画像を保存
    mask_dir = os.path.join(img_dir_path, "mask_inpaint_face")
    os.makedirs(mask_dir, exist_ok=True)
    mask_file = os.path.join(mask_dir, os.path.basename(image))
    cv2.imwrite(mask_file, mask)
