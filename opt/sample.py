import cv2
import pafy
import os
import img2pdf
from PIL import Image


def convert_pdf():
    pdf_FileName = "./opt/images/output.pdf"
    png_Folder = "./opt/images/"
    extension = ".jpg"

    with open(pdf_FileName, "wb") as f:
        f.write(
            img2pdf.convert(
                [
                    Image.open(png_Folder + j).filename
                    for j in os.listdir(png_Folder)
                    if j.endswith(extension)
                ]
            )
        )


def convert_main():
    os.system("mkdir -p /root/opt/images")
    # youtube url
    url = "https://www.youtube.com/watch?v=Qd2aU4uQ2rA"
    video = pafy.new(url)
    best = video.getbest()
    cap = cv2.VideoCapture(best.url)
    threshold = 12000

    cap.set(cv2.CAP_PROP_FPS, 5)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 420)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # print(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))
    _, previous = cap.read()

    frame_Num, j = 0, 0
    frame = None
    try:
        while cap.isOpened() and frames > frame_Num + 1000:
            _, frame = cap.read()
            frame_Num = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_Num + 1000)

            diff = getDiff(previous, frame)

            if diff > threshold:
                page_num = str(j).zfill(4)
                cv2.imwrite("opt/images/image{}.jpg".format(page_num), previous)
                j += 1
            previous = frame
        page_num = str(j).zfill(4)
        cv2.imwrite("opt/images/image{}.jpg".format(page_num), frame)
        convert_pdf()
    except:
        pass
    finally:
        cap.release()
        os.system("rm -rf opt/images/*.jpg")


# ２値化
def binarization(img, threshold=100):
    _, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    return img


# 差分を数値化
def getDiff(img1, img2):
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    mask = cv2.absdiff(img1, img2)
    mask = binarization(mask)
    return cv2.countNonZero(mask)  # 白の要素数


# convert_main()
