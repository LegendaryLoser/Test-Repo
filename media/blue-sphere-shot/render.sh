#!/usr/bin/env bash
# Full pipeline: capture frames -> synthesize audio -> encode + mux MP4.
# Usage: ./render.sh <workdir>   (workdir holds frames/ and intermediates)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="${1:?usage: render.sh <workdir>}"
FF=/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2

mkdir -p "$WORK"
if [ ! -f "$WORK/frames/f_0000.png" ]; then
  node "$HERE/capture.cjs" "$WORK/frames" | tee "$WORK/capture.log"
fi

# markers -> audio (duration = frame count / 60)
MARKERS=$(grep -o '{.*}' "$WORK/capture.log" | tail -1)
NFRAMES=$(ls "$WORK/frames" | wc -l)
DUR=$(python3 -c "print($NFRAMES/60)")
read TL TD TC TS <<<"$(python3 -c "
import json; m = json.loads('$MARKERS')
print(m['tLaunch'], m['tDil'], m['tContact'], m['tSnap'])")"
python3 "$HERE/sound.py" "$DUR" "$TL" "$TD" "$TC" "$TS" "$WORK/audio.wav"

"$FF" -y -framerate 60 -i "$WORK/frames/f_%04d.png" -i "$WORK/audio.wav" \
  -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -movflags +faststart \
  -c:a aac -b:a 192k -shortest "$WORK/blue-sphere-shot.mp4"
echo "wrote $WORK/blue-sphere-shot.mp4"
