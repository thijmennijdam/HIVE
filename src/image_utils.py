import base64
import io
from pathlib import Path
import numpy as np
from PIL import Image
from dash import html

_IMAGENET_ROOT = Path("imagenet-subset")

def _encode_image(rel_path: str) -> str:
    """Return base64 data URI for *rel_path* (relative to *_IMAGENET_ROOT* or absolute path)."""
    # Handle both old imagenet-subset paths and new hierarchical dataset paths
    if rel_path.startswith("hierchical_datasets/"):
        img_path = Path(rel_path)
    else:
        img_path = _IMAGENET_ROOT / rel_path
    
    mime = {
        ".jpeg": "jpeg",
        ".jpg": "jpeg",
        ".png": "png",
    }.get(img_path.suffix.lower(), "jpeg")

    try:
        with open(img_path, "rb") as f_img:
            enc = base64.b64encode(f_img.read()).decode()
    except FileNotFoundError:
        # If image not found, return empty string to avoid broken UI
        return ""

    return f"data:image/{mime};base64,{enc}"


def _create_img_tag(idx: int, images: np.ndarray | None) -> html.Img | html.Span:
    """Creates a base64 encoded image tag from the IMAGES dataset."""
    if images is None:
        return html.Span()

    if isinstance(images, (list, np.ndarray)) and isinstance(images[idx], (list, np.ndarray)):
        images_np = np.asarray(images)
        pil = (
            Image.fromarray((images_np[idx] * 16).astype("uint8"), mode="L")
            .resize((64, 64), Image.Resampling.NEAREST if hasattr(Image, 'Resampling') else Image.NEAREST)
        )
        buf = io.BytesIO()
        pil.save(buf, format="PNG")
        uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
        return html.Img(
            src=uri, style={"marginRight": "0.5rem", "border": "1px solid #bbb", "maxWidth": "300px", "maxHeight": "300px", "objectFit": "contain"}
        )

    try:
        img_rel = images[idx]
        uri = _encode_image(str(img_rel))  # type: ignore[arg-type]
        return html.Img(
            src=uri, style={"marginRight": "0.5rem", "border": "1px solid #bbb", "maxWidth": "300px", "maxHeight": "300px", "objectFit": "contain"}
        )
    except Exception:
        return html.Span()

def _create_content_element(idx: int, images: np.ndarray | None, points: list | None = None, meta: dict | None = None) -> html.Div | html.Img | html.Span:
    """Creates either a text element or image element based on the embedding type."""
    # If we have points data, check the embedding type
    if points and idx < len(points):
        point = points[idx]
        embedding_type = point.get("embedding_type", "")
        
        # For text embeddings, display the actual text content
        if embedding_type in ["parent_text", "child_text"]:
            synset_id = point.get("synset_id", "")
            if meta and synset_id in meta:
                if embedding_type == "parent_text":
                    text_content = meta[synset_id].get("name", "No parent text available")
                else:  # child_text
                    text_content = meta[synset_id].get("description", "No child text available")
                
                return html.Div([
                    html.P(text_content, style={
                        "margin": "0", 
                        "padding": "0.75rem", 
                        "backgroundColor": "#f8fdff",
                        "border": "1px solid #e1e8ed",
                        "borderRadius": "6px",
                        "fontFamily": "system-ui, -apple-system, sans-serif",
                        "fontSize": "0.9rem",
                        "lineHeight": "1.4",
                        "color": "#2c3e50",
                        "maxWidth": "220px",
                        "wordWrap": "break-word",
                        "boxShadow": "0 1px 3px rgba(0,0,0,0.1)"
                    })
                ], style={"marginRight": "0.5rem"})
            else:
                return html.Div([
                    html.P(f"Text content unavailable", style={
                        "margin": "0", 
                        "padding": "0.75rem", 
                        "backgroundColor": "#f8f9fa",
                        "border": "1px solid #e1e8ed",
                        "borderRadius": "6px",
                        "fontFamily": "system-ui, -apple-system, sans-serif",
                        "fontSize": "0.9rem",
                        "fontStyle": "italic",
                        "color": "#6c757d",
                        "maxWidth": "220px"
                    })
                ], style={"marginRight": "0.5rem"})
    
    # For image embeddings or when we don't have points data, fall back to image display
    return _create_img_tag(idx, images)