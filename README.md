# Remove Background

Remove photo backgrounds locally using [rembg](https://github.com/danielgatis/rembg) — no cloud services, everything runs on your machine.

Two ways to use it:

- **`app.py`** — a mini GUI in your browser: drag in photos, preview results, download a PNG (or a zip for batches)
- **`remove-bg.sh`** — a CLI wrapper for a single photo or a whole folder

## 1. Install Python

You need **Python 3.10 or newer** (tested on 3.14).

### macOS

```bash
# with Homebrew (https://brew.sh)
brew install python
```

Or download the installer from [python.org/downloads](https://www.python.org/downloads/).

### Linux

```bash
# Debian / Ubuntu
sudo apt install python3 python3-venv python3-pip

# Fedora / Nobara
sudo dnf install python3 python3-pip
```

Check it worked (use `python3` everywhere below):

```bash
python3 --version
```

`pip` ships with Python — inside the virtual environment below it is always available as `.venv/bin/pip`.

## 2. Set up the project

```bash
git clone https://github.com/arnasbrad/remove-background.git
cd remove-background

# create an isolated virtual environment
python3 -m venv .venv

# install dependencies into it
.venv/bin/pip install "rembg[cli,cpu]" gradio
```

> **Note:** the first time you process a photo, rembg downloads the AI model
> (~1 GB for the default `birefnet-general`) to `~/.rembg/models/`. This
> happens once per machine.

## 3. Run the GUI app

```bash
.venv/bin/python app.py
```

Your browser opens automatically (or go to the URL it prints, usually `http://127.0.0.1:7860`). Drag in one or more photos, pick a model and edge mode, click **Remove backgrounds**.

- Single photo → download a transparent PNG
- Multiple photos → download a zip
- Nothing is ever overwritten or deleted

## 4. Or use the CLI script

```bash
./remove-bg.sh photo.jpg                  # -> photo.no-bg.png
./remove-bg.sh photo.jpg output.png       # explicit output name
./remove-bg.sh input_folder output_folder # whole folder
MODEL=u2net ./remove-bg.sh photo.jpg      # different model
```

## Models and edge modes

| Model | Good for | Size |
|---|---|---|
| `birefnet-general` (default) | best all-round quality | ~1 GB |
| `birefnet-portrait` | people / portraits | ~1 GB |
| `u2net` | faster, lighter | ~170 MB |
| `isnet-general-use` | faster, lighter | ~170 MB |

Edge modes (GUI dropdown; the CLI script uses decontaminate):

- **Decontaminate** (default) — keeps soft anti-aliased edges but removes background color fringing (the grey halo)
- **Post-process mask** — hard, fully binary edge; crispest cut for product shots
- **Alpha matting** — for genuinely soft subjects like hair or fur
- **None** — raw model output

## Troubleshooting

- **`rembg: command not found`** — you're outside the venv; use `.venv/bin/rembg`, or `source .venv/bin/activate` first.
- **Slow processing** — birefnet on CPU takes a few seconds per photo; try `u2net` for speed.
