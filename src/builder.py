import plotly.graph_objects as go

PRIME_TABS = [
    {
        "label": "Distribution",
        "desc": (
            "Primes are distributed aperiodically across \u2115, yet the Prime Number Theorem "
            "\u2014 proved independently by Hadamard and de la Vall\u00e9e Poussin in 1896 \u2014 "
            "establishes \u03c0(x)\u2009\u223c\u2009x\u2009/\u2009ln\u2009x. "
            "Equivalently, the probability that a uniformly chosen integer near n is prime is "
            "asymptotically 1\u2009/\u2009ln\u2009n, so consecutive primes near n are spaced "
            "on average ln\u2009n apart. Each dot is a prime; hover to inspect its rank and value."
        ),
    },
    {
        "label": "Gaps",
        "desc": (
            "The prime gap g\u2099 = p\u2099\u208a\u2081 \u2212 p\u2099 is always even for n \u2265 2, "
            "since all primes beyond 2 are odd. The Prime Number Theorem implies the average gap "
            "near n grows as ln\u2009n, yet individual gaps are wildly irregular. "
            "The Twin Prime Conjecture \u2014 that g\u2099 = 2 for infinitely many n \u2014 "
            "is unproved. Zhang (2013) established the first finite bound, showing infinitely many "
            "gaps below 70\u2009000\u2009000; the Polymath project subsequently reduced this to 246."
        ),
    },
    {
        "label": "Counting Function",
        "desc": (
            "\u03c0(n) denotes the number of primes \u2264 n. "
            "The Prime Number Theorem gives \u03c0(n)\u2009\u223c\u2009n\u2009/\u2009ln\u2009n, "
            "but Gauss\u2019s logarithmic integral Li(n) = \u222b\u2082\u207f dt\u2009/\u2009ln\u2009t "
            "provides a dramatically sharper approximation. "
            "The Riemann Hypothesis \u2014 that all non-trivial zeros of \u03b6(s) satisfy "
            "Re(s) = \u00bd \u2014 is equivalent to the tight error bound "
            "|\u03c0(n) \u2212 Li(n)| = O(\u221an\u2009ln\u2009n)."
        ),
    },
    {
        "label": "Ulam Spiral",
        "desc": (
            "In 1963 Stanislaw Ulam arranged \u2115 in a square spiral and marked the primes, "
            "revealing unexpected diagonal striations. These correspond to prime-rich quadratic "
            "polynomials: e.g. 4n\u00b2 \u2212 2n + 41 is prime for n = 0, \u2026, 10. "
            "Hardy and Littlewood\u2019s Conjecture F predicts the asymptotic density of primes "
            "along such diagonals via a product of local correction factors, but the alignment "
            "remains without a complete explanation. Dark cells are prime; white cells composite."
        ),
    },
    {
        "label": "Gaussian Primes",
        "desc": (
            "The Gaussian integers \u2124[i] = {a + bi : a, b \u2208 \u2124} form a Euclidean domain "
            "with unique factorisation. A Gaussian prime \u03b1 \u2208 \u2124[i] is irreducible therein: "
            "if b = 0 then |a| must be a rational prime \u2261 3 (mod 4); "
            "if a = 0 then |b| must be a rational prime \u2261 3 (mod 4); "
            "otherwise a\u00b2 + b\u00b2 must be a rational prime. "
            "The 4-fold symmetry reflects the unit group {\u00b11, \u00b1i}. "
            "Height encodes the modulus |z|. "
            "The unsolved Gaussian Moat Problem asks whether one can walk from 0 to \u221e "
            "stepping only on Gaussian primes with uniformly bounded step size."
        ),
    },
]

PI_TABS = [
    {
        "label": "Digit Frequencies",
        "desc": (
            "\u03c0 = 3.14159\u2026 is conjectured to be normal in base 10: every digit d \u2208 {0,\u2026,9} "
            "should appear with asymptotic frequency 1/10, every k-digit string with frequency 10\u207b\u1d4f. "
            "Despite \u03c0 having been computed to over 100 trillion decimal places, normality remains unproved. "
            "By the law of large numbers the observed frequency of each digit converges to 1/10, but the rate "
            "of convergence is not rigorously controlled. The dashed line marks the uniform expectation; "
            "deviations are consistent with statistical noise."
        ),
    },
    {
        "label": "Random Walk",
        "desc": (
            "Each decimal digit d\u2099 of \u03c0 is mapped to a unit step at bearing d\u2099 \u00d7 36\u00b0 "
            "in \u211d\u00b2 (digit 0 \u2192 East, digit 5 \u2192 West, and so on across 10 equally spaced "
            "directions). If \u03c0 is normal, consecutive steps are asymptotically i.i.d. uniform on "
            "{0\u00b0, 36\u00b0, \u2026, 324\u00b0}, giving a 2D random walk with zero drift and isotropic "
            "covariance matrix \u00bdI. P\u00f3lya\u2019s theorem guarantees such a walk is recurrent in \u211d\u00b2. "
            "Colour encodes step index \u2014 earlier steps in violet, later in yellow."
        ),
    },
]


_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Prime &amp; \u03c0 Visualisations</title>
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

    /* ── Section containers ── */
    .section {{
      margin-top: 28px;
    }}
    .section-header {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 0;
    }}
    .section-label {{
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #6e6e73;
      white-space: nowrap;
      padding: 0 2px;
    }}
    .section-rule {{
      flex: 1;
      height: 1px;
      background: #d2d2d7;
    }}

    /* ── Tab navigation ── */
    nav {{
      display: flex;
      gap: 2px;
      border-bottom: 1px solid #d2d2d7;
      margin-top: 6px;
    }}
    nav button {{
      padding: 9px 16px;
      border: none;
      background: none;
      cursor: pointer;
      font-size: 13px;
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
    nav button.pi-active {{
      color: #bf5af2;
      border-bottom-color: #bf5af2;
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
      max-width: 720px;
      font-size: 14.5px;
      color: #3a3a3c;
      line-height: 1.7;
      margin-bottom: 20px;
      padding: 16px 20px;
      background: #ffffff;
      border-left: 3px solid #0071e3;
      border-radius: 0 8px 8px 0;
      box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }}
    .desc.pi-desc {{
      border-left-color: #bf5af2;
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
    <h1>Prime &amp; \u03c0 Visualisations</h1>
    <p>Interactive explorations of the first 10\u202f000 primes and 1\u202f000 decimal digits of \u03c0.</p>
  </header>
  <main>

    <!-- ── Primes section ── -->
    <div class="section">
      <div class="section-header">
        <span class="section-label">Primes</span>
        <div class="section-rule"></div>
      </div>
      <nav id="prime-nav">{prime_tabs}</nav>
    </div>

    <!-- ── Pi section ── -->
    <div class="section">
      <div class="section-header">
        <span class="section-label">\u03c0 Digits</span>
        <div class="section-rule"></div>
      </div>
      <nav id="pi-nav">{pi_tabs}</nav>
    </div>

    {panels}
  </main>

  <script>
    var totalPrime = {n_prime};
    var totalPi    = {n_pi};

    function showPrime(i) {{
      document.querySelectorAll('.panel').forEach((p, j) => p.classList.toggle('active', i === j));
      document.querySelectorAll('#prime-nav button').forEach((b, j) => b.classList.toggle('active', i === j));
      document.querySelectorAll('#pi-nav button').forEach(b => b.classList.remove('active', 'pi-active'));
    }}

    function showPi(i) {{
      var abs = totalPrime + i;
      document.querySelectorAll('.panel').forEach((p, j) => p.classList.toggle('active', abs === j));
      document.querySelectorAll('#prime-nav button').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('#pi-nav button').forEach((b, j) => {{
        b.classList.toggle('pi-active', i === j);
        b.classList.remove('active');
      }});
    }}
  </script>
</body>
</html>
"""


def build_html(prime_figures: list[go.Figure], pi_figures: list[go.Figure]) -> str:
    prime_tab_html = "".join(
        f'<button class="tab{" active" if i == 0 else ""}" onclick="showPrime({i})">{t["label"]}</button>'
        for i, t in enumerate(PRIME_TABS)
    )
    pi_tab_html = "".join(
        f'<button onclick="showPi({i})">{t["label"]}</button>'
        for i, t in enumerate(PI_TABS)
    )

    panels = []
    all_tabs = list(zip(prime_figures, PRIME_TABS)) + list(zip(pi_figures, PI_TABS))
    n_prime = len(PRIME_TABS)

    for i, (fig, tab) in enumerate(all_tabs):
        plot_div = fig.to_html(full_html=False, include_plotlyjs=False)
        active = " active" if i == 0 else ""
        is_pi = i >= n_prime
        desc_class = "desc pi-desc" if is_pi else "desc"
        panels.append(
            f'<div class="panel{active}" id="panel{i}">'
            f'<p class="{desc_class}">{tab["desc"]}</p>'
            f'<div class="plot-wrap">{plot_div}</div>'
            f'</div>'
        )

    return _HTML.format(
        prime_tabs=prime_tab_html,
        pi_tabs=pi_tab_html,
        panels="\n".join(panels),
        n_prime=n_prime,
        n_pi=len(PI_TABS),
    )
