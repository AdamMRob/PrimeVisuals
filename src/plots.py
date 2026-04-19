import math
import plotly.graph_objects as go
import plotly.express as px


def distribution_fig(primes: list[int]) -> go.Figure:
    fig = px.scatter(
        x=primes, y=[1] * len(primes),
        hover_name=[f"Prime #{i+1}: {p}" for i, p in enumerate(primes)],
        labels={"x": "Value", "y": ""},
    )
    fig.update_traces(marker=dict(size=5, opacity=0.5))
    fig.update_yaxes(visible=False)
    fig.update_layout(margin=dict(t=20, b=40))
    return fig


def gaps_fig(primes: list[int]) -> go.Figure:
    gaps = [b - a for a, b in zip(primes, primes[1:])]
    fig = px.bar(
        x=primes[1:], y=gaps,
        labels={"x": "Prime", "y": "Gap"},
        color=gaps, color_continuous_scale="Viridis",
    )
    fig.update_layout(margin=dict(t=20, b=40), coloraxis_showscale=False)
    return fig


def count_fig(primes: list[int]) -> go.Figure:
    step = max(1, primes[-1] // 300)
    xs = list(range(2, primes[-1] + 1, step))
    prime_set = set(primes)
    counts, running = [], 0
    p_iter = iter(sorted(prime_set))
    next_p = next(p_iter, None)
    for x in xs:
        while next_p is not None and next_p <= x:
            running += 1
            next_p = next(p_iter, None)
        counts.append(running)
    fig = px.line(x=xs, y=counts, labels={"x": "n", "y": "pi(n)"})
    fig.update_layout(margin=dict(t=20, b=40))
    return fig


def gaussian_primes_fig() -> go.Figure:
    limit = 55

    sieve_max = limit * limit * 2 + 1
    sieve = bytearray([1]) * sieve_max
    sieve[0] = sieve[1] = 0
    for i in range(2, int(math.sqrt(sieve_max)) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(sieve[i * i :: i]))

    def is_gaussian_prime(a: int, b: int) -> bool:
        norm = a * a + b * b
        if norm == 0:
            return False
        if a == 0:
            ab = abs(b)
            return ab < sieve_max and sieve[ab] and ab % 4 == 3
        if b == 0:
            ab = abs(a)
            return ab < sieve_max and sieve[ab] and ab % 4 == 3
        return norm < sieve_max and bool(sieve[norm])

    xs, ys, zs, labels = [], [], [], []
    for a in range(-limit, limit + 1):
        for b in range(-limit, limit + 1):
            if is_gaussian_prime(a, b):
                mod = math.sqrt(a * a + b * b)
                xs.append(a)
                ys.append(b)
                zs.append(mod)
                sign_b = "+" if b >= 0 else "-"
                labels.append(f"{a}{sign_b}{abs(b)}i  |z|={mod:.2f}")

    fig = go.Figure(go.Scatter3d(
        x=xs, y=ys, z=zs,
        mode="markers",
        marker=dict(
            size=3.5,
            color=zs,
            colorscale="Plasma",
            opacity=0.85,
            colorbar=dict(title="| z |", thickness=14, len=0.6),
        ),
        text=labels,
        hovertemplate="%{text}<extra></extra>",
    ))
    fig.update_layout(
        scene=dict(
            xaxis=dict(title="Re", gridcolor="#2a2a3e", color="#aaa"),
            yaxis=dict(title="Im", gridcolor="#2a2a3e", color="#aaa"),
            zaxis=dict(title="| z |", gridcolor="#2a2a3e", color="#aaa"),
            bgcolor="#0d0d1a",
            camera=dict(eye=dict(x=1.4, y=1.4, z=0.9)),
        ),
        paper_bgcolor="#0d0d1a",
        font=dict(color="#ccccdd"),
        margin=dict(t=10, b=10, l=0, r=0),
        height=620,
    )
    return fig


def ulam_fig(primes: list[int]) -> go.Figure:
    import math
    prime_set = set(primes)
    n = len(primes)
    size = int(math.ceil(math.sqrt(n))) | 1

    pos = {}
    x = y = size // 2
    dx, dy = 1, 0
    step, step_count, turns = 1, 0, 0
    for i in range(1, size * size + 1):
        pos[i] = (y, x)
        x += dx
        y += dy
        step_count += 1
        if step_count == step:
            step_count = 0
            dx, dy = -dy, dx
            turns += 1
            if turns % 2 == 0:
                step += 1

    z = [[0] * size for _ in range(size)]
    for num, (row, col) in pos.items():
        if num in prime_set:
            z[row][col] = 1

    fig = go.Figure(go.Heatmap(
        z=z,
        colorscale=[[0, "white"], [1, "navy"]],
        showscale=False,
        hovertemplate="value=%{text}<extra></extra>",
    ))
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False, scaleanchor="x"),
        margin=dict(t=20, b=20),
        width=650, height=650,
    )
    return fig
