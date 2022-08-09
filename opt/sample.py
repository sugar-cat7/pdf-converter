import cv2
import pafy
import os
import img2pdf
from PIL import Image  # img2pdfと一緒にインストールされたPillowを使います


def convert_pdf():
    pdf_FileName = "./opt/output.pdf"  # 出力するPDFの名前
    png_Folder = "./opt/sample/"  # 画像フォルダ
    extension = ".jpg"  # 拡張子がPNGのものを対象

    with open(pdf_FileName, "wb") as f:
        # 画像フォルダの中にあるPNGファイルを取得し配列に追加、バイナリ形式でファイルに書き込む
        f.write(
            img2pdf.convert(
                [
                    Image.open(png_Folder + j).filename
                    for j in os.listdir(png_Folder)
                    if j.endswith(extension)
                ]
            )
        )


def main():

    # youtube url
    url = "https://www.youtube.com/watch?v=Qd2aU4uQ2rA"
    # print("cv2:", cv2.__version__)
    video = pafy.new(url)
    best = video.getbest()
    cap = cv2.VideoCapture(best.url)
    threshold = 12000  # 変化の敷居値

    cap.set(cv2.CAP_PROP_FPS, 5)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 420)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # print("そうフレーム数:", frames)
    # 最初のフレームを背景画像に設定
    _, previous = cap.read()

    j = 0
    try:
        while cap.isOpened():
            # フレームの取得
            _, frame = cap.read()
            # frame_Num = int(cap.get(cv2.CAP_PROP_POS_FRAMES))  # 現在の再生位置（フレーム位置）の取得
            # cap.set(cv2.CAP_PROP_POS_FRAMES, frame_Num + 100)
            # 差分計算
            diff = getDiff(previous, frame)

            if diff > threshold:
                cv2.imwrite("./opt/sample/sample{}.jpg".format(j), previous)
                j += 1
            previous = frame

    except:
        cv2.imwrite("opt/sample/sample{}.jpg".format(j), frame)
    finally:
        cap.release()
        convert_pdf()
    # cv2.destroyAllWindows()


# ２値化
def binarization(img, threshold=100):
    ret, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    return img


# 差分を数値化
def getDiff(img1, img2):
    # グレースケール変換
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # 差分取得
    mask = cv2.absdiff(img1, img2)
    # ２値化
    mask = binarization(mask)
    return cv2.countNonZero(mask)  # 白の要素数


if __name__ == "__main__":
    main()
