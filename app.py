"""Mini GUI for removing photo backgrounds with rembg.

Run:  .venv/bin/python app.py
Then open the URL it prints (usually http://127.0.0.1:7860).
Drag in one or more photos, hit Remove backgrounds, download the results.
"""

import tempfile
import zipfile
from pathlib import Path

import gradio as gr
from PIL import Image
from rembg import new_session, remove

MODELS = ["birefnet-general", "birefnet-portrait", "u2net", "isnet-general-use"]
EDGE_MODES = {
    "Decontaminate (soft edge, fixes color halo)": "dc",
    "Post-process mask (hard crisp edge)": "ppm",
    "Alpha matting (soft subjects: hair, fur)": "matting",
    "None (raw model output)": "none",
}

_sessions: dict[str, object] = {}


def _session(model: str):
    if model not in _sessions:
        _sessions[model] = new_session(model)
    return _sessions[model]


def _unique(path: Path) -> Path:
    """Never overwrite: photo.no-bg.png -> photo.no-bg-2.png, -3, ..."""
    candidate = path
    n = 2
    while candidate.exists():
        candidate = path.with_stem(f"{path.stem}-{n}")
        n += 1
    return candidate


def process(files, model, edge_label, progress=gr.Progress()):
    if not files:
        raise gr.Error("Drop at least one photo first.")
    edge = EDGE_MODES[edge_label]
    out_dir = Path(tempfile.mkdtemp(prefix="rembg-gui-"))
    results = []
    for f in progress.tqdm(files, desc="Removing backgrounds"):
        src = Path(f)
        img = Image.open(src)
        cut = remove(
            img,
            session=_session(model),
            decontaminate=(edge == "dc"),
            post_process_mask=(edge == "ppm"),
            alpha_matting=(edge == "matting"),
        )
        dst = _unique(out_dir / f"{src.stem}.no-bg.png")
        cut.save(dst)
        results.append(str(dst))

    if len(results) == 1:
        download = results[0]
    else:
        download = str(out_dir / "no-bg-photos.zip")
        with zipfile.ZipFile(download, "w") as zf:
            for r in results:
                zf.write(r, arcname=Path(r).name)
    return results, download


with gr.Blocks(title="Background Remover") as demo:
    gr.Markdown("# Background Remover\nDrop photos, get transparent PNGs back.")
    with gr.Row():
        with gr.Column():
            files = gr.File(
                label="Photos",
                file_count="multiple",
                file_types=["image"],
                type="filepath",
            )
            model = gr.Dropdown(MODELS, value="birefnet-general", label="Model")
            edge = gr.Radio(
                list(EDGE_MODES), value=list(EDGE_MODES)[0], label="Edge mode"
            )
            run = gr.Button("Remove backgrounds", variant="primary")
        with gr.Column():
            gallery = gr.Gallery(label="Results", columns=2, object_fit="contain")
            download = gr.File(label="Download")

    run.click(process, inputs=[files, model, edge], outputs=[gallery, download])

if __name__ == "__main__":
    demo.launch(inbrowser=True)
