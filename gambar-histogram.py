import streamlit as st
import subprocess
import tempfile
import os
from PIL import Image

st.title("🎨 Live TikZ LaTeX Renderer")

st.markdown("""
Type your TikZ code below (without the `\\begin{tikzpicture}` wrapper) and see it rendered.
Make sure you have `pdflatex` and `convert` (ImageMagick) installed.
""")

tikz_code = st.text_area("TikZ Code", height=200, value=r"""
\draw[thick,->] (0,0) -- (2,2);
\draw[red] (0,0) circle (1cm);
""")

if tikz_code.strip() == "":
    st.stop()

full_latex = r"""
\documentclass[tikz]{standalone}
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}
""" + tikz_code + r"""
\end{tikzpicture}
\end{document}
"""

if st.button("Render TikZ"):
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "tikz.tex")
        pdf_path = os.path.join(tmpdir, "tikz.pdf")
        png_path = os.path.join(tmpdir, "tikz.png")

        with open(tex_path, "w") as f:
            f.write(full_latex)

        try:
            subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_path], cwd=tmpdir, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Convert PDF to PNG (you need `convert` from ImageMagick)
            subprocess.run(["convert", "-density", "300", pdf_path, "-quality", "90", png_path], check=True)

            image = Image.open(png_path)
            st.image(image, caption="Rendered TikZ", use_column_width=True)

        except subprocess.CalledProcessError as e:
            st.error("Error rendering LaTeX or converting image.")
            st.text(e.stderr.decode())
