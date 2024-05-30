import cv2
import numpy as np
import transliterate
import math
import os


def create_video(message: str, media_root: str):
    fps = 60
    frames = fps * 3
    width, height = 100, 100

    if len(message) > 50:
        title = message[:50]
    elif len(message) == 0:
        title = 'empty-video'
    else:
        title = message
    title = transliterate.slugify('ъ' + title)

    video_path = os.path.join(media_root, f"videos/{title}.mp4")
    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    frame_clear = np.full((height, width, 3), (51, 102, 0), dtype=np.uint8)

    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 1
    font_thickness = 1
    font_color = (108, 105, 255)

    message_size = cv2.getTextSize(message, font, font_scale, font_thickness)
    x, y = width, (height + message_size[0][1]) // 2
    speed = math.ceil((message_size[0][0] + width) / frames) if math.ceil((message_size[0][0] + width) / frames) != 0 else 1

    for _ in range(frames):
        frame = frame_clear.copy()
        x -= speed
        if x >= -message_size[0][0]:
            cv2.putText(frame, message, (x, y), font, font_scale, font_color, font_thickness)
        out.write(frame)

    out.release()

    return {'title': title, 'path': video_path}
