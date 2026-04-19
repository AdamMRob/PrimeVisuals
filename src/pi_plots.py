import math
import plotly.graph_objects as go
import plotly.express as px

# First 1000 decimal digits of pi (after the decimal point)
_PI_STR = (
    "1415926535897932384626433832795028841971693993751058209749445923078164"
    "0628620899862803482534211706798214808651328230664709384460955058223172"
    "5359408128481117450284102701938521105559644622948954930381964428810975"
    "6659334461284756482337867831652712019091456485669234603486104543266482"
    "1339360726024914127372458700660631558817488152092096282925409171536436"
    "7892590360011330530548820466521384146951941511609433057270365759591953"
    "0921861173819326117931051185480744623799627495673518857527248912279381"
    "8301194912983367336244065664308602139494639522473719070217986094370277"
    "0539217176293176752384674818467669405132000568127145263560827785771342"
    "7577896091736371787214684409012249534301465495853710507922796892589235"
    "4201995611212902196086403441815981362977477130996051870721134999999837"
    "2978049951059731732816096318595024459455346908302642522308253344685035"
    "2619311881710100031378387528865875332083814206171776691473035982534904"
    "2875546873115956286388235378759375195778185778053217122680661300192787"
    "6611195909216420198938095257201065485863278865936153381827968230301952"
)


def get_pi_digits(n: int = 1000) -> list[int]:
    return [int(d) for d in _PI_STR[:n]]


def pi_digit_freq_fig(digits: list[int]) -> go.Figure:
    counts = [digits.count(d) for d in range(10)]
    n = len(digits)
    expected = n / 10

    colors = px.colors.sample_colorscale("Viridis", [i / 9 for i in range(10)])
    fig = go.Figure(go.Bar(
        x=[str(d) for d in range(10)],
        y=counts,
        marker_color=colors,
        text=counts,
        textposition="outside",
        hovertemplate="Digit %{x}: %{y} occurrences<extra></extra>",
    ))
    fig.add_hline(
        y=expected,
        line_dash="dash",
        line_color="#0071e3",
        annotation_text=f"Uniform expectation: {expected:.0f}",
        annotation_position="top right",
    )
    fig.update_layout(
        xaxis=dict(title="Digit d", tickmode="linear"),
        yaxis=dict(title="Frequency", range=[0, max(counts) * 1.12]),
        margin=dict(t=30, b=40),
        showlegend=False,
    )
    return fig


def pi_walk_fig(digits: list[int]) -> go.Figure:
    xs, ys = [0.0], [0.0]
    for d in digits:
        angle = math.radians(d * 36.0)
        xs.append(xs[-1] + math.cos(angle))
        ys.append(ys[-1] + math.sin(angle))

    steps = list(range(len(xs)))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=xs, y=ys,
        mode="lines",
        line=dict(width=0.9, color="rgba(130,130,160,0.35)"),
        hoverinfo="skip",
        showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=xs, y=ys,
        mode="markers",
        marker=dict(
            size=3,
            color=steps,
            colorscale="Plasma",
            showscale=True,
            colorbar=dict(title="Step", thickness=14, len=0.6),
        ),
        hovertemplate="Step %{marker.color}: (%{x:.3f}, %{y:.3f})<extra></extra>",
        showlegend=False,
    ))
    fig.update_layout(
        xaxis=dict(title="x", scaleanchor="y", scaleratio=1),
        yaxis=dict(title="y"),
        margin=dict(t=20, b=40),
        height=600,
    )
    return fig
