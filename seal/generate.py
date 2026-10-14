import argparse
import json
import sys
from itertools import pairwise
from pathlib import Path


def make_frames(
    boxes, frame_count=44, fps=11, source="manual-visible-extent", track_index=1
):
    frames = []
    for frame_index in range(frame_count):
        timestamp = frame_index / fps
        observations = []
        if frame_index in boxes:
            observations.append(
                {
                    "timestamp": timestamp,
                    "track_id": f"Seal {track_index:02d}",
                    "individual_id": f"seal_track_{track_index:02d}",
                    "bbox": boxes[frame_index],
                    "confidence": None,
                    "bbox_source": source,
                }
            )
        frames.append(
            {
                "frame_index": frame_index,
                "timestamp": timestamp,
                "observations": observations,
            }
        )
    return frames


def interpolate(keyframes):
    boxes = dict(keyframes)
    for (start, first), (end, last) in pairwise(keyframes):
        for frame_index in range(start + 1, end):
            weight = (frame_index - start) / (end - start)
            boxes[frame_index] = [
                round(left + weight * (right - left))
                for left, right in zip(first, last)
            ]
    return boxes


def generate(research_source):
    sys.path.insert(0, str(research_source.resolve()))
    from pipeline import pair_history
    from prepare_pages import sanitized

    destination = Path(__file__).parent / "data"
    video_id = "seal_030615ch3_short"
    boxes = {
        4: [0, 460, 120, 576],
        5: [0, 310, 140, 576],
        6: [0, 145, 195, 576],
        7: [0, 0, 240, 576],
        8: [0, 0, 305, 576],
        9: [0, 0, 365, 576],
        10: [0, 0, 445, 576],
        11: [0, 0, 610, 576],
        12: [0, 0, 610, 576],
        13: [0, 0, 704, 576],
        14: [0, 0, 704, 576],
        15: [0, 0, 635, 576],
        16: [0, 0, 600, 576],
        17: [0, 0, 645, 576],
        18: [0, 0, 630, 576],
        19: [0, 0, 615, 576],
        20: [75, 0, 595, 576],
        21: [120, 0, 555, 576],
        22: [125, 0, 565, 576],
        23: [145, 0, 555, 576],
        24: [105, 0, 565, 576],
        25: [90, 0, 630, 576],
        26: [165, 0, 645, 576],
        27: [205, 0, 670, 440],
        28: [255, 0, 685, 290],
        29: [170, 0, 610, 195],
        30: [165, 0, 260, 95],
    }
    frames = make_frames(boxes)
    bundle = {
        "video_id": video_id,
        "mode": "gt",
        "frames": frames,
        "relations": pair_history(frames, 704, 576, 1 / 11),
        "identity_scope": "temporary track within this clip only; no SealID match",
    }
    catalog = {
        "videos": [
            {
                "video_id": video_id,
                "width": 704,
                "height": 576,
                "fps": 11,
                "frame_count": 44,
                "annotation_stride": 1,
                "strict_split": "01・近くを通過",
                "recording_date": "2015_06_03",
            }
        ],
        "notice": "Manual boxes and temporary track ID; no verified identity or social relationship",
        "metrics": {
            "reid": {
                "gt_crop_rank1": None,
                "test_known_coverage": None,
                "encoder": "not used",
                "gallery_individuals": [],
            },
            "videos": [],
        },
        "reference_available": False,
        "mapped_demo_available": False,
    }
    extras = [
        (
            "seal_030615ch3_return",
            "2015_06_03",
            "02・逆向きの通過",
            44,
            11,
            [
                (2, [620, 0, 704, 40]),
                (3, [520, 0, 680, 85]),
                (4, [440, 0, 625, 180]),
                (5, [370, 0, 655, 300]),
                (6, [350, 0, 680, 365]),
                (7, [315, 0, 680, 415]),
                (8, [290, 0, 704, 480]),
                (9, [260, 0, 704, 576]),
                (10, [190, 0, 704, 576]),
                (11, [205, 0, 704, 576]),
                (12, [190, 0, 704, 576]),
                (13, [165, 0, 704, 576]),
                (14, [140, 0, 685, 576]),
                (15, [105, 0, 625, 576]),
                (16, [95, 0, 610, 576]),
                (17, [60, 0, 575, 576]),
                (18, [90, 0, 560, 576]),
                (19, [70, 0, 550, 576]),
                (20, [145, 75, 465, 576]),
                (21, [190, 190, 420, 576]),
                (22, [225, 310, 405, 576]),
                (23, [225, 445, 400, 576]),
                (24, [245, 535, 340, 576]),
            ],
        ),
        (
            "seal_260515ch1_swim",
            "2015_05_26",
            "03・別日の全身遊泳",
            72,
            12,
            [
                (0, [135, 530, 190, 576]),
                (5, [85, 365, 205, 576]),
                (10, [60, 240, 295, 576]),
                (15, [60, 160, 505, 535]),
                (20, [35, 130, 470, 520]),
                (25, [60, 115, 625, 380]),
                (30, [100, 80, 640, 355]),
                (35, [290, 0, 510, 340]),
                (40, [325, 0, 490, 400]),
                (45, [400, 10, 660, 430]),
                (50, [425, 95, 704, 560]),
                (55, [375, 215, 630, 576]),
                (60, [390, 305, 630, 576]),
                (65, [285, 410, 420, 576]),
                (70, [295, 515, 390, 576]),
                (71, [300, 540, 360, 576]),
            ],
        ),
    ]
    outputs = [(f"{video_id}.gt.json", bundle)]
    for identity, date, title, count, fps, keyframes in extras:
        frames = make_frames(
            interpolate(keyframes), count, fps, "manual-keyframes-linear-interpolation"
        )
        catalog["videos"].append(
            dict(
                catalog["videos"][0],
                video_id=identity,
                recording_date=date,
                strict_split=title,
                frame_count=count,
                fps=fps,
            )
        )
        outputs.append(
            (
                f"{identity}.gt.json",
                dict(
                    bundle,
                    video_id=identity,
                    frames=frames,
                    relations=pair_history(frames, 704, 576, 1 / fps),
                ),
            )
        )
    pair_id = "seal_harbor_pair"
    pair_tracks = [
        [
            (0, [295, 230, 400, 286]),
            (5, [332, 225, 434, 300]),
            (10, [352, 210, 430, 279]),
            (15, [350, 218, 405, 285]),
            (19, [325, 221, 390, 281]),
        ],
        [
            (0, [0, 145, 104, 191]),
            (5, [112, 150, 208, 195]),
            (10, [220, 169, 325, 211]),
            (15, [290, 200, 377, 235]),
            (19, [359, 235, 420, 277]),
        ],
    ]
    pair_frames = make_frames(
        interpolate(pair_tracks[0]), 20, 10, "manual-keyframes-linear-interpolation"
    )
    second_frames = make_frames(
        interpolate(pair_tracks[1]),
        20,
        10,
        "manual-keyframes-linear-interpolation",
        track_index=2,
    )
    for first, second in zip(pair_frames, second_frames):
        first["observations"].extend(second["observations"])
    source = {
        "title": "The Lamb Family · Harbor seals (Phoca vitulina)",
        "url": "https://commons.wikimedia.org/wiki/File:Harbor_seals_(Phoca_vitulina).webm",
        "license": "CC BY-SA 2.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/2.0/",
    }
    catalog["videos"].append(
        dict(
            catalog["videos"][0],
            video_id=pair_id,
            width=960,
            height=540,
            frame_count=20,
            fps=10,
            strict_split="04・2頭の同時遊泳",
            recording_date="2016_01_04",
            track_ids=["seal_track_01", "seal_track_02"],
            source=source,
        )
    )
    outputs.append(
        (
            f"{pair_id}.gt.json",
            dict(
                bundle,
                video_id=pair_id,
                frames=pair_frames,
                relations=pair_history(pair_frames, 960, 540, 0.1),
                source=source,
            ),
        )
    )
    long_tracks = [
        [
            (0, [363, 282, 655, 401]),
            (10, [270, 268, 481, 359]),
            (20, [245, 245, 398, 313]),
            (30, [295, 230, 400, 286]),
            (40, [352, 210, 430, 279]),
            (50, [315, 218, 390, 292]),
            (60, [270, 224, 328, 276]),
            (70, [240, 210, 281, 256]),
            (80, [215, 205, 255, 250]),
            (90, [190, 190, 223, 239]),
            (100, [108, 172, 149, 225]),
            (110, [47, 160, 166, 207]),
        ],
        [
            (30, [0, 142, 80, 181]),
            (40, [219, 169, 325, 212]),
            (50, [353, 238, 438, 280]),
            (60, [409, 272, 505, 316]),
            (70, [481, 297, 573, 334]),
            (80, [557, 307, 666, 350]),
            (90, [641, 301, 760, 346]),
            (100, [680, 300, 805, 341]),
            (110, [728, 270, 856, 315]),
            (120, [800, 198, 920, 268]),
            (130, [872, 138, 960, 207]),
            (135, [526, 255, 621, 307]),
            (140, [513, 235, 636, 311]),
            (150, [528, 165, 653, 294]),
            (160, [607, 70, 756, 219]),
            (170, [750, 0, 895, 112]),
        ],
        [
            (60, [520, 98, 580, 145]),
            (70, [556, 119, 607, 178]),
            (80, [587, 159, 640, 225]),
            (90, [596, 191, 637, 266]),
            (100, [557, 194, 598, 293]),
            (110, [529, 229, 564, 295]),
            (120, [526, 239, 566, 321]),
            (130, [524, 247, 590, 315]),
            (135, [897, 139, 960, 200]),
            (140, [850, 145, 910, 192]),
            (150, [739, 178, 815, 230]),
            (160, [659, 214, 785, 275]),
            (170, [540, 245, 731, 307]),
            (180, [316, 286, 600, 373]),
            (189, [80, 285, 442, 373]),
        ],
    ]
    long_frames = make_frames({}, 190, 10)
    for track_index, keyframes in enumerate(long_tracks, start=1):
        track_frames = make_frames(
            interpolate(keyframes),
            190,
            10,
            "manual-keyframes-linear-interpolation",
            track_index,
        )
        for frame, track_frame in zip(long_frames, track_frames):
            frame["observations"].extend(track_frame["observations"])
    long_id = "seal_harbor_19s"
    catalog["videos"].insert(
        0,
        dict(
            catalog["videos"][-1],
            video_id=long_id,
            frame_count=190,
            strict_split="05・19秒の群れの遊泳",
            track_ids=["seal_track_01", "seal_track_02", "seal_track_03"],
            preview_time=4,
        ),
    )
    outputs.append(
        (
            f"{long_id}.gt.json",
            dict(
                bundle,
                video_id=long_id,
                frames=long_frames,
                relations=pair_history(long_frames, 960, 540, 0.1),
                source=source,
                annotation_scope="Partial manual tracks; unlabelled animals and uncertain/off-screen segments are excluded",
            ),
        )
    )
    outputs.append(("catalog.json", catalog))
    destination.mkdir(exist_ok=True)
    for filename, data in outputs:
        (destination / filename).write_text(
            json.dumps(sanitized(data), ensure_ascii=False, separators=(",", ":"))
            + "\n"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--research-source", type=Path, required=True)
    generate(parser.parse_args().research_source)
