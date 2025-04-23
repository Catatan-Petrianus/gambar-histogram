import streamlit as st
import requests

st.title("🌐 TikZ Renderer (via QuickLaTeX API)")

tikz_code = st.text_area("Enter TikZ code", height=200, value=r"""
\draw[thick,->] (0,0) -- (2,2);
\draw[red] (0,0) circle (1cm);
""")

if st.button("Render via QuickLaTeX"):
    latex_template = r"""
\documentclass[preview]{standalone}
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}
%s
\end{tikzpicture}
\end{document}
""" % tikz_code

    payload = {
        'formula': latex_template,
        'fsize': '12px',
        'fcolor': '000000',
        'mode': '0',
        'out': '1',
        'errors': '1'
    }

    response = requests.post("https://quicklatex.com/latex3.f", data=payload)

    if response.ok and 'https://quicklatex.com/cache3' in response.text:
        image_url = response.text.split()[1]
        st.image(image_url, caption="Rendered TikZ")
    else:
        st.error("Rendering failed. Try again or check your TikZ code.")
