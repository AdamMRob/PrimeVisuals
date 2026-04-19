import plotly.graph_objects as go

TABS = [
    {
        "label": "Distribution",
        "desc": (
            "Primes are scattered along the number line with no obvious pattern. "
            "However, the Prime Number Theorem tells us they thin out predictably: "
            "roughly 1 in every ln(n) numbers near n is prime. "
            "Each dot here is a prime — hover to see its value and rank."
        ),
    },
    {
        "label": "Gaps",
        "desc": (
            "A prime gap is the difference between two consecutive primes. "
            "After 2 and 3 (gap of 1), all gaps are even. "
            "Gaps grow on average as ln(n), but their exact pattern is unpredictable — "
            "twin primes (gap 2) appear to go on forever, though this is unproven."
        ),
    },
    {
        "label": "Counting Function",
        "desc": (
            "pi(n) counts how many primes exist up to n. "
            "The Prime Number Theorem states pi(n) ~ n / ln(n). "
            "Gauss conjectured a tighter fit using the logarithmic integral Li(n), "
            "and the Riemann Hypothesis is essentially a precise bound on the error."
        ),
    },
    {
        "label": "Ulam Spiral",
        "desc": (
            "In 1963, Stanislaw Ulam doodled integers in a square spiral and circled the primes. "
            "Diagonal lines appeared — primes cluster along quadratic polynomials like 4n^2 + n + 41. "
            "No one fully understands why. Dark cells are prime, white cells are composite."
        ),
    },
    {
        "label": "Gaussian Primes",
        "desc": (
            "A Gaussian prime is a complex number a+bi that cannot be factored in the Gaussian integers. "
            "If both a and b are nonzero, a+bi is prime when a\u00b2+b\u00b2 is a rational prime. "
            "They tile the complex plane with perfect 4-fold symmetry. "
            "Height shows the modulus |z|. "
            "The unsolved Gaussian Moat Problem asks: can you walk from 0 to infinity stepping only on Gaussian primes, "
            "each step no longer than some fixed bound? No one knows."
        ),
    },
]

_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Prime Visualisations</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: #f5f5f7;
      color: #1d1d1f;
      min-height: 100vh;
    }}

    /* ── Page header ── */
    header {{
      background: #1d1d1f;
      color: #f5f5f7;
      padding: 28px 32px 24px;
    }}
    header h1 {{
      font-size: 22px;
      font-weight: 700;
      letter-spacing: -0.3px;
    }}
    header p {{
      margin-top: 6px;
      font-size: 14px;
      color: #a1a1a6;
      line-height: 1.5;
    }}

    /* ── Main content area ── */
    main {{
      max-width: 960px;
      margin: 0 auto;
      padding: 0 24px 48px;
    }}

    /* ── Tab navigation ── */
    nav {{
      display: flex;
      gap: 2px;
      margin: 24px 0 0;
      border-bottom: 1px solid #d2d2d7;
    }}
    nav button {{
      padding: 10px 18px;
      border: none;
      background: none;
      cursor: pointer;
      font-size: 14px;
      font-weight: 500;
      color: #6e6e73;
      border-bottom: 2px solid transparent;
      margin-bottom: -1px;
      border-radius: 4px 4px 0 0;
      transition: color 0.15s ease, border-color 0.15s ease;
      white-space: nowrap;
    }}
    nav button:hover {{
      color: #1d1d1f;
      background: #e8e8ed;
    }}
    nav button.active {{
      color: #0071e3;
      border-bottom-color: #0071e3;
      font-weight: 600;
    }}
    nav button:focus-visible {{
      outline: 2px solid #0071e3;
      outline-offset: 2px;
    }}

    /* ── Content panels ── */
    .panel {{ display: none; padding: 24px 0 0; }}
    .panel.active {{ display: block; }}

    /* ── Description block ── */
    .desc {{
      max-width: 700px;
      font-size: 15px;
      color: #3a3a3c;
      line-height: 1.65;
      margin-bottom: 20px;
      padding: 16px 20px;
      background: #ffffff;
      border-left: 3px solid #0071e3;
      border-radius: 0 8px 8px 0;
      box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }}

    /* ── Plot wrapper ── */
    .plot-wrap {{
      background: #ffffff;
      border-radius: 12px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.08);
      overflow: hidden;
      padding: 8px;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Prime Visualisations</h1>
    <p>Exploring the first 10,000 primes through four interactive charts.</p>
  </header>
  <main>
    <nav>{tabs}</nav>
    {panels}
  </main>
  <script>
    function show(i) {{
      document.querySelectorAll('.panel').forEach((p, j) => p.classList.toggle('active', i === j));
      document.querySelectorAll('nav button').forEach((b, j) => b.classList.toggle('active', i === j));
    }}
  </script>
</body>
</html>
"""


def build_html(figures: list[go.Figure]) -> str:
    tab_html = "".join(
        f'<button class="tab{" active" if i == 0 else ""}" onclick="show({i})">{t["label"]}</button>'
        for i, t in enumerate(TABS)
    )
    panels = []
    for i, (fig, tab) in enumerate(zip(figures, TABS)):
        plot_div = fig.to_html(full_html=False, include_plotlyjs=False)
        active = " active" if i == 0 else ""
        panels.append(
            f'<div class="panel{active}" id="panel{i}">'
            f'<p class="desc">{tab["desc"]}</p>'
            f'<div class="plot-wrap">{plot_div}</div>'
            f'</div>'
        )
    return _HTML.format(tabs=tab_html, panels="\n".join(panels))
