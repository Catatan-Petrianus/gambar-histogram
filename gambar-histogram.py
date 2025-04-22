import streamlit as st
import subprocess
from pathlib import Path
from PIL import Image

st.set_page_config(layout="wide")
st.title("📊 Live‑Preview TikZ Histogram Generator")

# Sidebar inputs for clarity
st.sidebar.header("Chart Data")
num_points = st.sidebar.number_input("Number of bars", min_value=1, max_value=20, value=6)
coords = []
for i in range(num_points):
    x = st.sidebar.number_input(f"x{i+1} (bar start)", value=45.0 + i*5, key=f"x{i}")
    y = st.sidebar.number_input(f"y{i+1} (frequency)", value=10.0, key=f"y{i}")
    coords.append((x, y))

# Cache the render step so we don't recompile unchanged data
@st.cache_data(show_spinner=False)
def render_histogram(coords):
    # Build LaTeX code
    latex_coords = " ".join(f"({x},{y})" for x, y in coords)
    horiz = "\n".join(
        f"\\addplot[mark=none,dashed] coordinates {{(45,{y}) ({x},{y})}};"
        for x, y in coords
    )
    xticks = ", ".join(str(x) for x, _ in coords)
    yticks = ", ".join(sorted({str(int(y)) for _, y in coords}, key=lambda v: int(v)))
    tex = f"""
\\documentclass[border=5mm,tikz,preview]{{standalone}}
\\usepackage[margin=0.5in]{{geometry}}
\\usepackage{{fontspec}}
\\setmainfont{{Times New Roman}}
\\usepackage{{pgfplots}}
\\pgfplotsset{{width=10cm,compat=1.16}}
\\begin{{document}}
\\begin{{tikzpicture}}
  \\begin{{axis}}[
    axis x line=bottom,
    axis y line=left,
    xlabel=nilai,
    ylabel=frekuensi,
    xmin=45,xmax=80,ymin=0,ymax=55,
    xtick={{ {xticks} }},ytick={{ {yticks} }}
  ]
    \\addplot[ybar interval,thick,fill=white] plot coordinates {{ {latex_coords} }};
    {horiz}
  \\end{{axis}}
\\end{{tikzpicture}}
\\end{{document}}
"""
    # Write files
    Path("histogram.tex").write_text(tex, encoding="utf-8")
    # Compile
    subprocess.run(
        ["xelatex", "-interaction=nonstopmode", "histogram.tex"],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    # Convert to PNG
    subprocess.run(
        ["convert", "-density", "300", "histogram.pdf", "-quality", "90", "histogram.png"],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return "histogram.png"

# Render and display
with st.spinner("Rendering…"):
    img_path = render_histogram(coords)
    st.image(img_path, caption="🖼️ Live TikZ Preview", use_column_width=True)
    st.download_button("📥 Download LaTeX Source", Path("histogram.tex").read_bytes(), file_name="histogram.tex")
