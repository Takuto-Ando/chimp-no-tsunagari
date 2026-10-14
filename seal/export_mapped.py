import argparse
import json
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright


def export(url, output):
    output.mkdir(parents=True, exist_ok=False)
    target = output / "seal_harbor_19s-arrows.mp4"
    with sync_playwright() as driver:
        executable = (
            Path.home()
            / ".cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell"
        )
        browser = driver.chromium.launch(executable_path=str(executable))
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(url, wait_until="networkidle")
        page.wait_for_function("document.querySelector('video')?.duration === 19")
        page.wait_for_selector(".react-flow__node")
        page.add_style_tag(
            content="""
            .stage { position: fixed !important; left: 0 !important; top: 0 !important;
                width: 1280px !important; height: 720px !important; max-width: none !important;
                border-radius: 0 !important; z-index: 9999; }
            .react-flow { display: none !important; }
            .react-flow__node, .stage * { transition: none !important; }
            .react-flow__controls, .react-flow__attribution { display: none !important; }
            .overlay .bbox rect { stroke-opacity: 0 !important; }
            .relationship-telop { transform: translateY(-22px); }
            .react-flow__viewport { transform: translate(25px, 95px) scale(0.65) !important; }
        """
        )
        page.evaluate(r"""() => {
            for (const [top, height, text] of [
                [0, 48, 'アザラシ：仮名・設定つながり（ID固定）'],
                [656, 64, '名前と関係は展示用の架空設定です。実際の社会関係ではありません。\nThe Lamb Family · Harbor seals · CC BY-SA 2.0 · 無音・再圧縮・仮設定追加']
            ]) {
                const banner = document.createElement('div');
                banner.textContent = text;
                banner.style.cssText = `position:fixed;left:0;top:${top}px;width:1280px;height:${height}px;z-index:10000;background:#102b34;color:white;padding:8px;box-sizing:border-box;font:20px sans-serif;white-space:pre-line`;
                document.body.append(banner);
            }
        }""")
        page.locator("video").evaluate(
            "video => { video.pause(); video.loop = false; video.controls = false; }"
        )
        page.wait_for_timeout(500)
        process = subprocess.Popen(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-n",
                "-f",
                "image2pipe",
                "-vcodec",
                "mjpeg",
                "-framerate",
                "10",
                "-i",
                "pipe:0",
                "-an",
                "-c:v",
                "libx264",
                "-preset",
                "fast",
                "-crf",
                "22",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(target),
            ],
            stdin=subprocess.PIPE,
        )
        try:
            for frame_index in range(190):
                page.locator("video").evaluate(
                    """async (video, timestamp) => {
                    if (Math.abs(video.currentTime - timestamp) > 0.001) {
                        await new Promise(resolve => {
                            video.addEventListener('seeked', resolve, { once: true });
                            video.currentTime = timestamp;
                        });
                    }
                    await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
                }""",
                    frame_index / 10,
                )
                if frame_index == 40:
                    assert (
                        page.locator('svg.overlay [aria-label$="のBBox"]').count() >= 2
                    )
                    assert page.locator("svg.overlay .relationship-arrow").count() > 0
                    page.screenshot(
                        path=str(output / "preview.png"),
                        clip={"x": 0, "y": 0, "width": 1280, "height": 720},
                    )
                process.stdin.write(
                    page.screenshot(
                        type="jpeg",
                        quality=92,
                        clip={"x": 0, "y": 0, "width": 1280, "height": 720},
                    )
                )
            process.stdin.close()
            assert process.wait() == 0
        finally:
            if process.poll() is None:
                process.terminate()
                process.wait()
        browser.close()
        assert not errors, errors
    probe = json.loads(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_streams",
                "-show_format",
                "-of",
                "json",
                str(target),
            ]
        )
    )
    stream = probe["streams"][0]
    assert (stream["width"], stream["height"], int(stream["nb_frames"])) == (
        1280,
        720,
        190,
    )
    assert float(probe["format"]["duration"]) == 19
    (output / "LICENSE.txt").write_text(
        "The Lamb Family, Harbor seals (Phoca vitulina). CC BY-SA 2.0.\n"
        "Source: https://commons.wikimedia.org/wiki/File:Harbor_seals_(Phoca_vitulina).webm\n"
        "License: https://creativecommons.org/licenses/by-sa/2.0/\n"
        "Changes: 19-second excerpt, silent, re-encoded; provisional names and "
        "ID-fixed fictional relationship arrows over tracked animals burned into video. "
        "No bounding box outlines are shown.\n"
        "Not AI detections, verified individual names or social relationships. "
        "Unannotated or uncertain animals/segments may remain. No endorsement implied.\n"
        "This adapted video is distributed under CC BY-SA 2.0.\n"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:5189/?species=seal")
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    export(arguments.url, arguments.output)
