import streamlit as st

st.set_page_config(page_title="TikZJax SVG Saver", layout="centered")

st.title("📐 TikZ Diagram Renderer + SVG Saver")

st.markdown("""
Enter your **TikZ code** below. Click **Render** to see the diagram, or **Save as SVG** to download it!
""")

default_tikz = r"""
\begin{tikzpicture}
  \draw[->, thick] (0,0) -- (2,0) node[right] {x};
  \draw[->, thick] (0,0) -- (0,2) node[above] {y};
  \draw (0,0) circle (1);
  \draw[red, thick] (0,0) -- (1,1) node[right] {r};
\end{tikzpicture}
"""

tikz_code = st.text_area("Enter TikZ code here:", value=default_tikz, height=200)

# HTML with TikZJax and Save button
html = f"""
<script src="https://tikzjax.com/v1/tikzjax.js"></script>

<pre><code id="tikz-code" type="text/tikz">
{tikz_code}
</code></pre>

<br>
<button onclick="downloadSVG()">💾 Save as SVG</button>

<script>
function downloadSVG() {{
    const svgEl = document.querySelector("svg");
    if (!svgEl) {{
        alert("SVG not yet rendered!");
        return;
    }}
    const serializer = new XMLSerializer();
    const source = serializer.serializeToString(svgEl);
    const blob = new Blob([source], {{type: "image/svg+xml;charset=utf-8"}});
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "diagram.svg";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}}
</script>
"""

st.components.v1.html(html, height=500)
