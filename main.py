import webbrowser
import tempfile
import os
from src.fetcher import fetch_primes
from src.plots import distribution_fig, gaps_fig, count_fig, ulam_fig, gaussian_primes_fig
from src.pi_plots import get_pi_digits, pi_digit_freq_fig, pi_walk_fig
from src.builder import build_html

N = 10_000


def main():
    primes = fetch_primes(N)
    print("Building plots...")
    prime_figures = [
        distribution_fig(primes[:500]),
        gaps_fig(primes[:1000]),
        count_fig(primes),
        ulam_fig(primes),
        gaussian_primes_fig(),
    ]
    pi_digits = get_pi_digits(1000)
    pi_figures = [
        pi_digit_freq_fig(pi_digits),
        pi_walk_fig(pi_digits),
    ]
    html = build_html(prime_figures, pi_figures)
    path = os.path.join(tempfile.gettempdir(), "prime_visualisation.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Opening browser...")
    webbrowser.open(f"file:///{path}")


if __name__ == "__main__":
    main()
