# Flex

**Flex** is a lightweight Python wrapper around `pywebview` for building standalone desktop apps using **HTML, CSS, and Python**, rendered with the **native system webview**.

No Chromium. No Node.js. Just Python + web UI.

## Why Flex?

- Native system webview (small, fast binaries)
- Python-first
- Simple, explicit API
- Familiar HTML/CSS for UI
- No heavy abstractions

## Install

```bash
pip install git+https://github.com/jnsougata/flex
````

## Minimal Example

```python
import flex
from webview import Event, Window

app = flex.App("index.html", title="Chat App", stylesheet="style.css")

@app.listen("loaded")
def on_loaded():
    print("App loaded!")


if __name__ == "__main__":
    app.run()
```

## How It Works

```text
Python backend → Flex → System WebView → HTML/CSS/JS
```

## What It’s Not

* Electron
* A frontend framework
* A magic layer that hides the webview

## Status

Early-stage and evolving. The surface area is intentionally small.

## Demo App Window

<img width="912" height="712" alt="Screenshot 2026-01-10 at 12 43 00 AM" src="https://github.com/user-attachments/assets/984e4b16-d568-45f0-902c-d2d3a0374f1d" />


