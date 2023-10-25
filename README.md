# Rule 30

*Animate [Rule 30](https://en.wikipedia.org/wiki/Rule_30) forward and reversed.*

<img src="screen.png" width="50%" height="50%" alt="Rule 30 in reverse">

[YouTube](https://www.youtube.com/watch?v=FfcuzJxyBkk)

## Usage

Install Pygame:

    pip install -r requirements.txt

Animate forward:

    python -m forward

Use space to pause, esc to exit.

Animate backward (requires running forward first):

    python -m reverse

Record video:

    python -m forward record | ffmpeg -y -f rawvideo -pix_fmt bgra -s 1920x1080 -framerate 60 -i - -vcodec libx264 forward.mp4

## License

MIT
