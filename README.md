# Flex

**Flex** is a lightweight Python wrapper around `pywebview` for building standalone desktop apps using **HTML, CSS, and Python**, rendered with the **native system webview**.

No Chromium. No Node.js. Just Python + web UI.

---

## Why Flex?

- Native system webview (small, fast binaries)
- Python-first
- Simple, explicit API
- Familiar HTML/CSS for UI
- No heavy abstractions

---

## Install

```bash
pip install flex
````

---

## Minimal Example

```python
import flex
from webview import Event, Window

app = flex.App("index.html", title="Snake Game Demo", stylesheet="style.css")

@app.listen("loaded")
def on_loaded():
    print("App loaded!")


if __name__ == "__main__":
    app.run()
```

---

## How It Works

```text
Python backend → Flex → System WebView → HTML/CSS/JS
```

---

## What It’s For

* Desktop tools & utilities
* Internal dashboards
* Research / scientific apps
* Lightweight cross-platform GUIs

---

## What It’s Not

* Electron
* A frontend framework
* A magic layer that hides the webview

---

## Status

Early-stage and evolving. The surface area is intentionally small.

---

## License

MIT

