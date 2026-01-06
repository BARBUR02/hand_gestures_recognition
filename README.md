# Hand Gesture Detector Workspace

This repository uses **[uv](https://github.com/astral-sh/uv)** for Python dependency management and **[Task](https://taskfile.dev/)** for automation. It wraps a local package that utilizes the **MediaPipe** library for hand tracking and OpenCV python for live interaction with webcam and frame processsing.

## Prerequisites
* **uv** (required)
* **Task** (recommended for convenience)

## Quick Start (with Task)
The easiest way to run the detector. This command automatically checks for the model (downloading it if missing) and runs the script.

```bash
task run-hand-detector
```

## Manual Usage (without Task)
If you prefer not to use task, you can run the steps manually (just copy over the scripts from the Taskfile):
1. Download the Model We use the MediaPipe Hand Landmarker (float16) model. It must be placed in the models/ directory.
```bash
mkdir -p models
curl -L -o models/hand_landmarker.task https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task
```
2. Run the Script Execute the package script from the workspace root using `uv`:
```bash
uv run --package hand-gesture-detector run-hand-detector
```
