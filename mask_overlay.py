import sys
import os
import cv2
import shutil
import tkinter as tk
from tkinter import messagebox


os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

KEY_CODE_WINDOWS_LEFT = 0x00250000
KEY_CODE_WINDOWS_RIGHT = 0x00270000
KEY_CODE_WINDOWS_DEL = 0x002E0000

MASK_SUB_DIR = "mask_inpaint_face"
WINDOW_TITLE = "Image with Mask"
SKIP_MARK = "Skip"

args = len(sys.argv)
if args <= 1:
    print("Mask Overlay For Inpainting v0.04", file=sys.stderr)
    print("Usage:", file=sys.stderr)
    print(f"python {os.path.basename(__file__)} (image files folder)", file=sys.stderr)
    messagebox.showerror("Error", "Please pass the image folder.")
    exit(1)

img_folder = sys.argv[1]
mask_folder = os.path.join(img_folder, MASK_SUB_DIR)

if not os.path.isdir(img_folder):
    messagebox.showerror("Error", "Invalid image folder path.")
    exit(1)

if not os.path.isdir(mask_folder):
    messagebox.showerror("Error", "Invalid mask folder path.")
    exit(1)

skip_folder = os.path.join(img_folder, SKIP_MARK)
skip_mask_folder = os.path.join(skip_folder, MASK_SUB_DIR)

# 画像フォルダ内の画像を取得
images = []
for filename in os.listdir(img_folder):
    if filename.endswith(".png"):
        img_path = os.path.join(img_folder, filename)
        images.append(img_path)

# マスクフォルダ内の画像を取得
masks = []
for filename in os.listdir(mask_folder):
    if filename.endswith(".png"):
        mask_path = os.path.join(mask_folder, filename)
        masks.append(mask_path)

# 要素数が一致しない場合、エラーメッセージを表示して終了
if len(images) != len(masks):
    messagebox.showerror("Error", "The number of images and masks does not match.")
    exit(1)

index = 0  # 表示中の画像のインデックス
skip_indices = []  # スキップする画像のインデックスリスト

root = tk.Tk()
root.withdraw()  # ウィンドウを非表示にする

while True:
    # 画像とマスクを読み込み
    img = cv2.imread(images[index])
    mask = cv2.imread(masks[index], cv2.IMREAD_GRAYSCALE)

    # マスクを画像に重ねる
    overlay = cv2.bitwise_and(img, img, mask=mask)

    # マスクの透過処理
    overlay = cv2.addWeighted(img, 0.2, overlay, 0.8, 1)

    # マークを付ける
    if index in skip_indices:
        cv2.putText(overlay, SKIP_MARK, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # 画像と重ねた結果を表示
    cv2.imshow(WINDOW_TITLE, overlay)

    # キー入力を待機（時間待ちを挿入）
    key = cv2.waitKeyEx(1)  # 1ミリ秒待機

    # ウィンドウが閉じられた場合、終了
    if cv2.getWindowProperty(WINDOW_TITLE, cv2.WND_PROP_VISIBLE) < 1:
        break

    # キーに応じた処理を実行
    if key == 27:
        # ESCキーが押された場合、終了
        break
    elif key == KEY_CODE_WINDOWS_LEFT:
        # 左矢印キーが押された場合、前の画像へ
        index = max(0, index - 1)
    elif key == KEY_CODE_WINDOWS_RIGHT:
        # 右矢印キーが押された場合、次の画像へ
        index = min(len(images) - 1, index + 1)
    elif key == KEY_CODE_WINDOWS_DEL:
        # Delキーが押された場合、画像のスキップリストに追加または削除
        if index in skip_indices:
            skip_indices.remove(index)
        else:
            skip_indices.append(index)
            index = min(len(images) - 1, index + 1)  # 次の画像へ

# ファイルの移動を実行するか確認
if skip_indices:
    result = messagebox.askquestion("Confirmation", "Do you want to move the skipped files?")
    if result == "yes":
        # 画像とマスクをskipフォルダに移動
        os.makedirs(skip_folder, exist_ok=True)
        os.makedirs(skip_mask_folder, exist_ok=True)
        for index in skip_indices:
            removed_image_path = images[index]
            removed_mask_path = masks[index]
            shutil.move(removed_image_path, skip_folder)
            shutil.move(removed_mask_path, skip_mask_folder)

# ウィンドウを閉じる
cv2.destroyAllWindows()
