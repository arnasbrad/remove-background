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
brew install python@3.13
```

Or, without Homebrew: download the **Python 3.13** installer from
[python.org/downloads](https://www.python.org/downloads/) and run it.

Either way you get a `python3.13` command. Verify:

```bash
python3.13 --version
```

Use `python3.13` (not plain `python3`) in the commands below — the Mac's
built-in `python3` is often an old 3.9 that installs broken dependency
versions.

### Linux

```bash
# Debian / Ubuntu
sudo apt install python3 python3-venv python3-pip

# Fedora / Nobara
sudo dnf install python3 python3-pip
```

Check it worked:

```bash
python3 --version
```

`pip` ships with Python — inside the virtual environment below it is always available as `.venv/bin/pip`.

## 2. Set up the project

> **Important:** put the project in a folder path **without spaces**
> (e.g. `~/remove-background`, not `~/Desktop/untitled folder/...`) —
> Python virtual environments break in paths containing spaces.

```bash
git clone https://github.com/arnasbrad/remove-background.git
cd remove-background

# create an isolated virtual environment
python3.13 -m venv .venv    # macOS
python3 -m venv .venv       # Linux

# make sure the venv uses a new enough Python (3.10+)
.venv/bin/python --version

# install dependencies into it
.venv/bin/python -m pip install "rembg[cli,cpu]" gradio
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

## Updating

Double-click `update.command` in the project folder (or run `./update.command`). It pulls the latest version from GitHub.

## Optional: a Desktop launcher (macOS)

To start the GUI without opening Terminal:

1. Open **Automator** → **File → New → Application**
2. Add a **Run Shell Script** action and set its contents to (adjust the path if you cloned elsewhere):
   ```bash
   exec "$HOME/remove-background/.venv/bin/python" "$HOME/remove-background/app.py"
   ```
3. **File → Save** as `Background Remover` on your Desktop

Double-click to launch — the browser opens by itself. While it runs, a spinning gear shows in the menu bar; stop it from there to shut the app down.

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
- **`ImportError: cannot import name 'HfFolder'`** — your venv was created with an old Python (usually macOS system 3.9; the error path shows `python3.9`). Install Python 3.13 (see step 1), then rebuild the venv with the versioned command:
  `rm -rf .venv && python3.13 -m venv .venv && .venv/bin/python -m pip install "rembg[cli,cpu]" gradio`
- **venv creation fails with an `ensurepip` error, or pip crashes with `ValueError: invalid literal for int() ... in _macos.py`** — on some macOS 26 systems Python misreports the OS version and pip's SSL setup crashes. Use [uv](https://docs.astral.sh/uv/) instead of pip:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh   # then open a new terminal
  rm -rf .venv
  uv venv --python 3.13 .venv
  uv pip install "rembg[cli,cpu]" gradio
  .venv/bin/python app.py
  ```
- **venv creation fails (`ensurepip ... returned non-zero exit status`) or pip/gradio mysteriously "not found"** — check the project path for spaces (`untitled folder`, `My Stuff`, ...). Move the project to a space-free path like `~/remove-background`, delete `.venv`, and start over from step 2.
