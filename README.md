# JetBrains UX Test: Click Heatmaps

This repository contains my solution for Task 1 of the JetBrains internship test assignment.

The goal was to generate heatmaps from real click data collected during an unmoderated UX test of a JetBrains IDE prototype and interpret the results.

## About the study

Participants were asked to:

1. Open Settings from the top-right corner of the IDE.
2. Enable the "Use contrast scrollbars" checkbox.
3. Save their changes.
4. Return to the code editor.

The prototype tested an updated settings interface, where Settings opens in an editor tab instead of a modal window, and a confirmation bar appears after changing a setting.

## What I did

I used Python to process the JSON export from the usability test.

First, I looked at the JSON structure to understand how the participant data and click coordinates were stored. Then I grouped the clicks by prototype screen and matched them with the corresponding screenshots.

I used a Gaussian filter to create the heatmaps and placed them over the original screens. Areas with more clicks appear warmer.

The script generates heatmaps for all seven screens. For the screen with no clicks, it displays the original screenshot with a note. For the screen with just one click, it shows a marker instead of generating a heatmap.

I also looked at the participants' navigation paths and task outcomes to better understand the results.

## Tools

- Python 3.13
- NumPy
- SciPy
- Matplotlib
- Pillow
- Visual Studio Code

## How to run the script

The script needs the original `responses.json` file and the seven prototype images.

The files should be placed in:

- `data/responses.json`
- `data/screens/`

Install the libraries using:

`uv pip install -r requirements.txt`

Then run:

`python generate_heatmaps.py`

The generated images and a summary CSV will be saved in `outputs/heatmaps/`.

## Results

The dataset contains 76 respondent records and 851 click events.

Only 19 participants (25%) were marked as having completed the task.

The heatmaps show concentrated interactions around the Settings icon, the "Use contrast scrollbars" checkbox, and the "Save Changes" button.

One interesting finding came from the navigation paths. Although 57 participants were marked as having given up, 44 of them visited the Saved Settings screen.

Some participants also returned to Main Window, which already displayed the code editor, instead of ending on the separate Code Prototype screen.

This made me question whether the completion criteria of the prototype fully matched the instructions given to participants.

My interpretation of the results is described in [report.md](report.md).

## Limitations

The heatmaps show where participants clicked, not where they looked.

The heatmap colors are normalized separately for each screen, so the color intensity should not be compared directly between different screens.

Also, a recorded click does not necessarily mean a participant understood the interface, and visiting a screen does not always mean the task was completed successfully.

The original participant data is not included in this repository.

## Files

- `generate_heatmaps.py` — Python script for generating the heatmaps.
- `requirements.txt` — libraries needed to run the script.
- `report.md` — interpretation of the UX experiment.
- `outputs/heatmaps/` — generated images and click summary, when sharing is permitted.
