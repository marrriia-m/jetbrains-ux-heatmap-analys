import json
import csv
import math
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter
from matplotlib import colormaps

BASE = Path(__file__).resolve().parent
JSON_FILE = BASE / "data" / "responses.json"
SCREENS_FOLDER = BASE / "data" / "screens"
OUTPUT_FOLDER = BASE / "outputs" / "heatmaps"

SCREENS = {
    "12401": "Changed Settings",
    "12472": "Saved Settings",
    "12541": "Default Settings",
    "12610": "Main Window",
    "12624": "Code Prototype",
    "12650": "Code Not Saved",
    "12676": "Context Menu",
}


def find_image(screen_id):
    """Find the screenshot containing the screen ID."""

    matches = []

    for file in SCREENS_FOLDER.iterdir():
        if file.suffix.lower() not in {
            ".png", ".jpg", ".jpeg", ".webp"
        }:
            continue

        if re.search(
            rf"(?<!\d){screen_id}(?!\d)", file.stem
        ):
            matches.append(file)

    if len(matches) != 1:
        raise FileNotFoundError(
            f"Expected one image for screen {screen_id}, "
            f"found {len(matches)}"
        )

    return matches[0]


def extract_clicks(data):
    """Collect clicks for each screen from all respondents."""

    clicks = {screen_id: [] for screen_id in SCREENS}
    participants = {
        screen_id: set() for screen_id in SCREENS
    }

    skipped = 0

    for respondent_id, respondent in data.items():

        answers = respondent.get("answers", {})

        if not isinstance(answers, dict):
            continue

        for task in answers.values():

            if not isinstance(task, dict):
                continue

            screen_clicks = task.get("clicks", {})

            if not isinstance(screen_clicks, dict):
                continue

            for frame_id, events in screen_clicks.items():

                screen_id = frame_id.split(":")[-1]

                if screen_id not in SCREENS:
                    continue

                if not isinstance(events, list):
                    continue

                for event in events:

                    if not isinstance(event, dict):
                        skipped += 1
                        continue

                    try:
                        x = float(event["frame_click_x"])
                        y = float(event["frame_click_y"])
                    except (KeyError, ValueError, TypeError):
                        skipped += 1
                        continue

                    if not (
                        math.isfinite(x) and math.isfinite(y)
                    ):
                        skipped += 1
                        continue

                    clicks[screen_id].append((x, y))
                    participants[screen_id].add(respondent_id)

    return clicks, participants, skipped


def add_label(image, text):
    """Add a note to screens with fewer than two clicks."""

    draw = ImageDraw.Draw(image)
    width, height = image.size

    font = ImageFont.load_default(size=15)
    box = draw.textbbox((0, 0), text, font=font)

    text_width = box[2] - box[0]
    text_height = box[3] - box[1]

    padding = 10
    margin = 12

    x = width - text_width - 2 * padding - margin
    y = height - text_height - 2 * padding - margin

    draw.rounded_rectangle(
        (x, y, width - margin, height - margin),
        radius=6,
        fill=(35, 35, 35, 230)
    )

    draw.text(
        (x + padding, y + padding - box[1]),
        text,
        font=font,
        fill="white"
    )


def create_heatmap(image, points):
    """Generate a heatmap over the original screenshot."""

    image = image.convert("RGBA")
    width, height = image.size

    count = len(points)

    if count == 0:
        add_label(image, "No recorded clicks")
        return image

    points = np.asarray(points, dtype=float)

    x = points[:, 0]
    y = points[:, 1]

    valid = (
        (x >= 0) & (x < width) &
        (y >= 0) & (y < height)
    )

    if not np.all(valid):
        raise ValueError(
            "Some clicks are outside the screenshot. "
            "Check coordinate alignment."
        )

    if count == 1:

        draw = ImageDraw.Draw(image)
        cx, cy = float(x[0]), float(y[0])
        radius = 8

        draw.ellipse(
            (
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius
            ),
            outline=(255, 0, 0, 255),
            width=3
        )

        add_label(image, "One recorded click")
        return image

    density = np.zeros(
        (height, width),
        dtype=np.float32
    )

    np.add.at(
        density,
        (y.astype(int), x.astype(int)),
        1
    )

    sigma = max(
        3.0,
        min(width, height) * 0.035
    )

    density = gaussian_filter(
        density,
        sigma=sigma,
        mode="constant"
    )

    density = density / density.max()

    colors = colormaps["turbo"](density)

    opacity = 0.62 * np.sqrt(
        np.clip((density - 0.06) / 0.94, 0, 1)
    )

    colors[:, :, 3] = opacity

    overlay = Image.fromarray(
        (colors * 255).astype(np.uint8),
        "RGBA"
    )

    return Image.alpha_composite(image, overlay)


def main():

    with open(JSON_FILE, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError(
            "Expected a dictionary of respondent records."
        )

    print("Respondents:", len(data))

    clicks, participants, skipped = extract_clicks(data)

    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    summary = []

    for screen_id, screen_name in SCREENS.items():

        print(f"\nProcessing {screen_name}")

        image_path = find_image(screen_id)

        with Image.open(image_path) as source:
            image = source.convert("RGB")

        screen_points = clicks[screen_id]

        result = create_heatmap(
            image,
            screen_points
        )

        output_path = (
            OUTPUT_FOLDER / f"{screen_id}_heatmap.png"
        )

        result.save(output_path)

        summary.append({
            "screen_id": screen_id,
            "screen": screen_name,
            "clicks": len(screen_points),
            "participants": len(participants[screen_id]),
            "width": image.width,
            "height": image.height
        })

        print("Clicks:", len(screen_points))
        print("Saved:", output_path.name)

    summary_path = OUTPUT_FOLDER / "heatmap_summary.csv"

    with open(
        summary_path, "w",
        newline="", encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=list(summary[0].keys())
        )

        writer.writeheader()
        writer.writerows(summary)

    total_clicks = sum(
        len(points) for points in clicks.values()
    )

    print("\n------------------------")
    print("Total clicks:", total_clicks)
    print("Skipped invalid events:", skipped)
    print("Heatmaps created:", len(SCREENS))
    print("Output folder:", OUTPUT_FOLDER)
    print("------------------------")


if __name__ == "__main__":
    main()