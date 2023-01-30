import shutil
import time
import cv2
import pytesseract
import subprocess
import os
import img2pdf
from PIL import Image
import concurrent.futures

BASE_DIRECTORY = "/Users/sugar/Downloads/images"


def extract_video_url(url):
    if not os.path.exists(BASE_DIRECTORY):
        os.makedirs(BASE_DIRECTORY)
    else:
        for filename in os.listdir(BASE_DIRECTORY):
            file_path = os.path.join(BASE_DIRECTORY, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Failed to delete %s. Reason: %s" % (file_path, e))
    subprocess.run(
        ["yaydl", "-o", BASE_DIRECTORY + "/output.mp4", url],
        capture_output=True,
        text=True,
    )


def extract_text_from_frame(frame):
    # 画像認識
    return pytesseract.image_to_string(frame)


def extract_frames():
    cap = cv2.VideoCapture(BASE_DIRECTORY + "/output.mp4")
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    return frames


def process_frame(frame, prev_frame, threshold, idx):
    diff = cv2.absdiff(frame, prev_frame)
    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    diff = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]
    text = extract_text_from_frame(diff)
    text_len = len(text)
    if text_len > 0:
        cv2.imwrite(BASE_DIRECTORY + "/{}.jpg".format(idx), frame)
    return frame


def extract_text_from_frames(frames, threshold):
    prev_frame = frames[0]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [
            executor.submit(process_frame, frame, prev_frame, threshold, i)
            for i, frame in enumerate(frames[1::100])
        ]
        for future in concurrent.futures.as_completed(results):
            prev_frame = future.result()


def save_pdf():
    pdf_FileName = "/Users/sugar/Downloads/output.pdf"
    png_Folder = BASE_DIRECTORY + "/"
    extension = ".jpg"

    with open(pdf_FileName, "wb") as f:
        f.write(
            img2pdf.convert(
                [
                    Image.open(png_Folder + j).filename
                    for j in sorted(os.listdir(png_Folder))
                    if j.endswith(extension)
                ]
            )
        )


def main():
    url = input("youtubeのリンク: ")
    print("-------Video DownLoading...-------")
    t1 = time.time()
    extract_video_url(url)
    print("-------PDF Creating...-------")
    frames = extract_frames()
    extract_text_from_frames(frames, 10)
    save_pdf()
    print("-------DONE-------")
    t2 = time.time()
    print(f"経過時間：{t2-t1}")


if __name__ == "__main__":
    main()
