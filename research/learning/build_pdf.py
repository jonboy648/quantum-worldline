# RETRACTION NOTICE (2026-08-17): the force exponent alpha = 3.92 +/- 0.16 stated in this document is an ESTIMATOR ARTIFACT (95.8% of the fit objective sits on one point). The measured value is 2.6 +/- 0.2 and the channel is open. Interpretations built on alpha = 4 (graviton / stress-tensor exchange) are withdrawn. See research/ERRATA.md and the Zenodo v5 correction, doi:10.5281/zenodo.22080720.
"""Convert the three learning guides to a single styled HTML with embedded images."""
import markdown
import base64
import os
import re

DOCS = [
    ("intuitive-guide.md", "Part I"),
    ("physics-guide.md", "Part II"),
    ("connections-guide.md", "Part III"),
]

# Image insertions: (doc_index, after_heading_text, image_file, caption)
IMAGES = [
    (0, "## 3. MERA: A Hierarchy of Seeing", "frosted_glass_diagram.png",
     "The frosted glass metaphor mapped to MERA: boundary qubits on the surface, pattern-recognition layers creating depth, emergent AdS geometry behind the glass."),
    (0, "## 3. MERA: A Hierarchy of Seeing", "figure1_mera_schematic.png",
     "MERA circuit schematic: disentanglers (triangles) remove short-range entanglement, isometries (trapezoids) coarse-grain. Each layer halves the number of sites. The causal cone (shaded) shows which boundary sites influence a given bulk point."),
    (1, "## 2. MERA: The Architecture", "figure1_mera_schematic.png",
     "Figure 1: Binary MERA architecture with 3 layers of disentanglers and isometries."),
    (1, "## 8. The Interaction Energy F(dr)", "figure4_force_worldline.png",
     "Figure 4: Holographic force profile F(dr) on log-log scale. Blue dots: 12 measured points. Red line: power-law fit with alpha = 3.92. Dashed lines: stress-tensor reference (alpha = 4) and scalar reference (alpha = 2). The data clearly follows the stress-tensor prediction."),
    (1, "## 10. Causal Transport and Geodesics", "figure3_transport_trace.png",
     "Figure 3: Transport trace showing spin density rho(t) across boundary sites. Signal enters at site 0 (peak), disappears into the bulk (dip), and re-emerges at the antipodal point. Transport time T = 2.250 vs prediction 2.266."),
    (1, "## 12. The Z2 Problem and ALM+Projection", "figure2_alm_convergence.png",
     "Figure 2: ALM+Projection convergence. Phase 1 (ALM) escapes the ferromagnetic trap over 8 rounds. Phase 2 (projected L-BFGS-B) refines to the chi=2 energy floor."),
    (2, "## 6. What Comes Next", "figure5_helios_error_budget.png",
     "Figure 5: Quantinuum Helios circuit layout and error budget. 57 CX gates, 0.57% accumulated error - well within the hardware capability demonstrated by Perlin et al. (2132 gates)."),
]

CSS = """
@page { size: letter; margin: 1in 0.85in; }
body {
    font-family: 'Segoe UI', Calibri, Arial, sans-serif;
    font-size: 11.5pt;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 100%;
}
h1 {
    font-size: 22pt;
    color: #1a3a5c;
    border-bottom: 2px solid #1a3a5c;
    padding-bottom: 8px;
    margin-top: 40px;
    page-break-before: always;
}
h1:first-of-type { page-break-before: avoid; }
h2 {
    font-size: 15pt;
    color: #2a5a8c;
    margin-top: 28px;
    border-bottom: 1px solid #ddd;
    padding-bottom: 4px;
}
h3 { font-size: 12.5pt; color: #3a6a9c; margin-top: 20px; }
h4 { font-size: 11.5pt; color: #4a7aac; }
blockquote {
    border-left: 4px solid #2a5a8c;
    background: #f0f5fa;
    margin: 16px 0;
    padding: 12px 16px;
    font-style: italic;
    color: #333;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 16px 0;
    font-size: 10.5pt;
}
th, td {
    border: 1px solid #ccc;
    padding: 6px 10px;
    text-align: left;
}
th { background: #e8eef5; font-weight: 600; }
tr:nth-child(even) { background: #f8f9fa; }
code {
    background: #f0f0f0;
    padding: 2px 5px;
    border-radius: 3px;
    font-size: 10pt;
}
hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 30px 0;
}
.part-label {
    text-align: center;
    font-size: 10pt;
    color: #888;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 60px;
    margin-bottom: -30px;
}
.cover {
    text-align: center;
    padding-top: 200px;
    page-break-after: always;
}
.cover h1 {
    font-size: 28pt;
    border: none;
    color: #1a3a5c;
    page-break-before: avoid;
}
.cover .subtitle {
    font-size: 14pt;
    color: #666;
    margin-top: 20px;
}
.cover .author {
    font-size: 12pt;
    color: #888;
    margin-top: 40px;
}
.cover .date {
    font-size: 10pt;
    color: #aaa;
    margin-top: 10px;
}
.figure {
    text-align: center;
    margin: 24px 0;
    page-break-inside: avoid;
}
.figure img {
    max-width: 90%;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
.figure .caption {
    font-size: 9.5pt;
    color: #555;
    font-style: italic;
    margin-top: 8px;
    max-width: 85%;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.4;
}
"""

DIR = os.path.dirname(os.path.abspath(__file__))


def img_to_base64(filename):
    path = os.path.join(DIR, filename)
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{data}"


def make_figure_html(image_file, caption):
    b64 = img_to_base64(image_file)
    return f'''<div class="figure">
<img src="{b64}" alt="{caption[:60]}">
<div class="caption">{caption}</div>
</div>'''


def insert_after_heading(html, heading_text, insert_html):
    """Insert HTML after the first occurrence of a heading containing the given text."""
    # Find h2 tags and match by content
    pattern = r'(<h2[^>]*>.*?' + re.escape(heading_text.replace('## ', '')) + r'.*?</h2>)'
    match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
    if match:
        pos = match.end()
        return html[:pos] + '\n' + insert_html + '\n' + html[pos:]
    # Fallback: try finding the text directly
    idx = html.find(heading_text.replace('## ', ''))
    if idx > 0:
        # Find the end of the enclosing tag
        close = html.find('</h2>', idx)
        if close > 0:
            pos = close + 5
            return html[:pos] + '\n' + insert_html + '\n' + html[pos:]
    print(f"  WARNING: Could not find heading '{heading_text}' for image insertion")
    return html


# Build cover page
html_parts_raw = [f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="cover">
<h1>Understanding Your Research</h1>
<div class="subtitle">A Layered Learning Guide to Holographic Physics,<br>
MERA Tensor Networks, and Emergent Geometry</div>
<div class="author">Prepared for Jon Cackler<br>Independent Researcher</div>
<div class="date">March 2026</div>
</div>
"""]

md = markdown.Markdown(extensions=['tables', 'fenced_code'])

doc_htmls = []
for filename, part_label in DOCS:
    path = os.path.join(DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    md.reset()
    html_content = md.convert(text)
    doc_htmls.append((part_label, html_content))

# Insert images into the right documents
for doc_idx, heading_text, image_file, caption in IMAGES:
    part_label, html_content = doc_htmls[doc_idx]
    fig_html = make_figure_html(image_file, caption)
    html_content = insert_after_heading(html_content, heading_text, fig_html)
    doc_htmls[doc_idx] = (part_label, html_content)
    print(f"  Inserted {image_file} into {DOCS[doc_idx][0]} after '{heading_text[:40]}...'")

# Assemble
for part_label, html_content in doc_htmls:
    html_parts_raw.append(f'<div class="part-label">{part_label}</div>')
    html_parts_raw.append(html_content)

html_parts_raw.append("</body></html>")
full_html = "\n".join(html_parts_raw)

out_path = os.path.join(DIR, "learning-guide.html")
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"\nHTML written to: {out_path}")
print(f"Size: {len(full_html):,} chars")
print(f"Images embedded as base64 (self-contained)")
