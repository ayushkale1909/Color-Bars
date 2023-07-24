import numpy as np
import av

duration = 4
fps = 60
total_frames = duration * fps
width, height = 2048, 1080  # 2K

colors = [
    [191, 191, 191],  # Grey
    [191, 191, 0],  # Yellow
    [0, 191, 191],  # Cyan
    [0, 191, 0],  # Green
    [191, 0, 191],  # Magenta
    [191, 0, 0],  # Red
    [0, 0, 191],  # Blue
]

container = av.open('color_bars_2k_60fps.mp4', mode='w')

stream = container.add_stream('mpeg4', rate=fps)
stream.width = width
stream.height = height
stream.pix_fmt = 'yuv420p'

for frame_i in range(total_frames):
    img = np.zeros((height, width, 3), dtype=np.uint8)
    for i, color in enumerate(colors):
        bar_width = width // len(colors)
        img[:, i * bar_width:(i + 1) * bar_width] = color
    frame = av.VideoFrame.from_ndarray(img, format='rgb24')
    for packet in stream.encode(frame):
        container.mux(packet)

for packet in stream.encode():
    container.mux(packet)

container.close()
