"""Projette une vidéo plate (1920x1080) sur un grand écran dans une photo 360° (fond assombri).
make_flat(parts, out): parts = liste de (fichier, début, durée, piste_audio_ou_None) -> vidéo plate enchaînée.
project(flat, pano, out, yaw=0, pitch=-2, hfov=80)."""
import subprocess, json
def run(a): subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + a, check=True)
def seg(src, ss, du, audio, out, aud_ss=0):
    vf = f"fps=25,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p,fade=t=in:d=0.6,fade=t=out:st={du - 0.6}:d=0.6"
    if audio == "own":
        run(["-ss", str(ss), "-t", str(du), "-i", src, "-vf", vf, "-af", f"aformat=sample_rates=44100:channel_layouts=stereo,loudnorm=I=-17:TP=-1.5,afade=t=in:d=0.6,afade=t=out:st={du - 0.8}:d=0.8",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", out])
    else:
        run(["-ss", str(ss), "-t", str(du), "-i", src, "-f", "lavfi", "-t", str(du), "-i", "anullsrc=r=44100:cl=stereo", "-vf", vf, "-map", "0:v", "-map", "1:a",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-shortest", out])
def concat(files, out):
    open("/tmp/cc.txt", "w").write("".join(f"file '{f}'\n" for f in files))
    run(["-f", "concat", "-safe", "0", "-i", "/tmp/cc.txt", "-c", "copy", out])
def music_over(video, music, out, mss=0, gain=1.0):
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video]))
    run(["-i", video, "-ss", str(mss), "-t", str(d), "-i", music, "-map", "0:v", "-map", "1:a", "-af", f"aformat=sample_rates=44100:channel_layouts=stereo,loudnorm=I=-17,volume={gain},afade=t=in:d=1,afade=t=out:st={d - 3}:d=3",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out])
def project(flat, pano, out, yaw=0, pitch=-2, hfov=80):
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", flat]))
    vf = hfov * 9 / 16
    fc = (f"[0:v]format=yuva420p,v360=input=flat:output=e:ih_fov={hfov}:iv_fov={vf}:pitch={pitch}:yaw={yaw}:w=3840:h=1920:alpha_mask=1[scr];"
          "[1:v]scale=3840:1920,eq=brightness=-0.18:saturation=0.85,format=yuv420p[bg];[bg][scr]overlay=format=auto[v]")
    run(["-i", flat, "-loop", "1", "-framerate", "25", "-t", str(d), "-i", pano, "-filter_complex", fc, "-map", "[v]", "-map", "0:a", "-t", str(d),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "5.1", "-c:a", "copy", "-movflags", "+faststart", out])
    return d
