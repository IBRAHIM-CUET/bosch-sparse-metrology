"""Draws the four figures of the paper from figure_data/ (extracted from the dataset and the v2 notebook run).

Usage:  python make_figs.py [output_folder]      (default: the folder above this script)
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "figure_data")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)

INK, INK2, GRID, MUTED = "#0b0b0b", "#52514e", "#e3e2de", "#b8b7b2"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
MARKERS = ["o", "s", "^", "D", "v", "P"]
SEQ_BLUE = LinearSegmentedColormap.from_list("seq_blue", ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf",
                                                          "#184f95", "#0d366b"])
SEQ_ORANGE = LinearSegmentedColormap.from_list("seq_orange", ["#fde3d6", "#f7b393", "#eb6834", "#b84a1f", "#7a2e10"])
plt.rcParams.update({
    "font.size": 7.5, "axes.titlesize": 7.5, "axes.labelsize": 7.5, "legend.fontsize": 6.5, "xtick.labelsize": 6.5,
    "ytick.labelsize": 6.5, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
    "text.color": INK, "axes.linewidth": 0.6, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.5,
    "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 1.3, "lines.markersize": 3.5,
    "legend.frameon": False, "savefig.dpi": 300, "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
    "pdf.fonttype": 42, "ps.fonttype": 42, "axes.titlelocation": "left", "font.family": "DejaVu Sans",
})
R_EDGE = 90.0


def save(fig, name):
    fig.savefig(os.path.join(OUT, f"{name}.pdf"))
    fig.savefig(os.path.join(OUT, f"{name}.png"), dpi=200)
    plt.close(fig)


def wafer_axes(ax, ylabel=True):
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(100 * np.cos(th), 100 * np.sin(th), color=INK2, lw=0.6)
    ax.set_aspect("equal")
    ax.set_xlim(-108, 108)
    ax.set_ylim(-108, 108)
    ax.set_xticks([-95, 0, 95])
    ax.set_yticks([-95, 0, 95])
    if not ylabel:
        ax.set_yticklabels([])
    ax.grid(False)
    ax.set_xlabel("x (mm)")


# ------------------------------------------------------------------ Fig. 1: maps and measurement layouts
def fig_maps():
    s = pd.read_csv(os.path.join(DATA, "sites.csv"))
    lay = json.load(open(os.path.join(DATA, "layouts.json")))
    idx = {l: i for i, l in enumerate(s.label)}
    x, y, r = s.x_mm.values, s.y_mm.values, s.r_mm.values
    fig, axs = plt.subplots(1, 3, figsize=(7.16, 2.3), gridspec_kw={"width_ratios": [1, 1.2, 1]})
    ax = axs[0]
    sc = ax.scatter(x, y, c=s.mean_um, cmap=SEQ_BLUE, marker="s", s=26, linewidths=0)
    std = [idx[l] for l in lay["standard9"]]
    edge_only = [idx[l] for l in lay["edge9"] if l not in lay["standard9"]]
    learned = [idx[l] for l in lay["fsca_all_wafers_first9"][:4]]
    ax.scatter(x[std], y[std], facecolors="none", edgecolors=INK, s=48, linewidths=0.8, label="standard 9")
    ax.scatter(x[edge_only], y[edge_only], marker="D", facecolors="none", edgecolors=SERIES[5], s=38, linewidths=0.9,
               label="edge-inclusive (outer 4)")
    ax.scatter(x[learned], y[learned], marker="^", color=SERIES[1], s=34, linewidths=0.5, edgecolors="white",
               label="learned, first 4")
    for n, j in enumerate(learned, 1):
        ax.annotate(str(n), (x[j], y[j]), xytext=(-8 if x[j] > 60 else 4, 3), textcoords="offset points", fontsize=6,
                    color=INK)
    wafer_axes(ax)
    ax.set_ylabel("y (mm)")
    ax.set_title("(a) mean Si etch depth")
    cb = fig.colorbar(sc, ax=ax, fraction=0.046, pad=0.02)
    cb.set_label("depth (µm)")
    cb.outline.set_linewidth(0.4)
    ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.24), ncol=1, handletextpad=0.3, borderpad=0.1)
    ax = axs[1]
    ax.axvspan(R_EDGE, 100, color=GRID, lw=0, label=f"edge ring (r ≥ {R_EDGE:.0f} mm)")
    ax.errorbar(r, s.mean_um, yerr=s.sd_um, fmt="o", ms=2.6, color=SERIES[0], ecolor=MUTED, elinewidth=0.6, capsize=0,
                label="site mean ± s.d.")
    ax.scatter(r[std], s.mean_um.values[std], facecolors="none", edgecolors=INK, s=30, linewidths=0.8, zorder=3,
               label="standard 9")
    ax.set_xlabel("radius (mm)")
    ax.set_ylabel("Si etch depth (µm)")
    ax.set_title("(b) radial profile")
    ax.legend(loc="upper left")
    ax = axs[2]
    v = s.shape_sd_um.values
    sc = ax.scatter(x, y, c=v, cmap=SEQ_ORANGE, marker="s", s=26, linewidths=0, vmin=0, vmax=float(np.percentile(v, 98)))
    wafer_axes(ax, ylabel=False)
    ax.set_title("(c) wafer-to-wafer s.d. of shape")
    cb = fig.colorbar(sc, ax=ax, fraction=0.046, pad=0.02)
    cb.set_label("s.d. (µm)")
    cb.outline.set_linewidth(0.4)
    fig.tight_layout(w_pad=1.0)
    save(fig, "fig_maps")


# ------------------------------------------------------------------ Fig. 2: campaign audit and drift
def fig_audit():
    a = pd.read_csv(os.path.join(DATA, "audit_stepheight.csv")).sort_values("resid_sd_after_wafer_offset_um")
    pairs = pd.read_csv(os.path.join(DATA, "matched_pairs_si_etch.csv"))
    w = pd.read_csv(os.path.join(DATA, "wafer_means.csv"))
    fig, axs = plt.subplots(1, 3, figsize=(7.16, 2.05), gridspec_kw={"width_ratios": [1.05, 1, 1.05]})
    ax = axs[0]
    yy = np.arange(len(a))[::-1]
    cols = [SERIES[0] if t == "rot180" else MUTED for t in a["transform"]]
    ax.barh(yy, a.resid_sd_after_wafer_offset_um, color=cols, height=0.62)
    ax.set_yticks(yy)
    ax.set_yticklabels(a["transform"])
    ax.grid(axis="y", visible=False)
    for y_, v in zip(yy, a.resid_sd_after_wafer_offset_um):
        ax.text(v, y_, f" {v:.3f}", va="center", fontsize=6, color=INK2)
    ax.set_xlim(0, 1.85)
    ax.set_xlabel("step-height residual s.d. (µm)")
    ax.set_title("(a) grid symmetry of the 9-site file")
    ax = axs[1]
    g, b = pairs[pairs["transform"] == "identity"], pairs[pairs["transform"] == "rot180"]
    ax.scatter(g.v89, g.v9, s=4, color=MUTED, linewidths=0, label="as given")
    ax.scatter(b.v89, b.v9, s=4, color=SERIES[0], linewidths=0, label="rotated 180°")
    off = float((b.v9 - b.v89).mean())
    lo, hi = float(b.v89.min()) - 0.3, float(b.v89.max()) + 0.2
    ax.plot([lo, hi], [lo + off, hi + off], color=INK2, lw=0.8, ls="--")
    ax.set_xlabel("offline 89-site depth (µm)")
    ax.set_ylabel("in-line 9-site depth (µm)")
    ax.set_title("(b) matched sites")
    ax.legend(loc="upper left", handletextpad=0.1, borderaxespad=0.1, labelspacing=0.25, markerscale=2.5)
    ax = axs[2]
    for lot, d in w.groupby("lot"):
        d = d.sort_values("wafer")
        hl = lot in (6, 7, 8)
        ax.plot(d.wafer, d.mean_um, color=SERIES[1] if hl else MUTED, lw=0.8 if hl else 0.6, zorder=2 if hl else 1)
    agg = w.groupby("wafer").mean_um.mean()
    ax.plot(agg.index, agg.values, color=SERIES[0], marker="o", ms=3, lw=1.3, zorder=3, label="mean over lots")
    ax.plot([], [], color=MUTED, lw=0.6, label="one lot")
    ax.plot([], [], color=SERIES[1], lw=0.8, label="lots 6-8")
    ax.set_xticks(range(1, 11))
    ax.set_xlabel("wafer position in lot")
    ax.set_ylabel("wafer-mean depth (µm)")
    ax.set_title("(c) within-lot drift")
    ax.legend(loc="upper right", handlelength=1.4)
    fig.tight_layout(w_pad=0.8)
    save(fig, "fig_audit")


# ------------------------------------------------------------------ Fig. 3: error against number of sites
def curve(ax, d, label, color, marker, band=False, ls="-"):
    d = d.sort_values("k")
    if band:
        ax.fill_between(d.k, d.rmse_lo, d.rmse_hi, color=color, alpha=0.12, lw=0)
    ax.plot(d.k, d.rmse, color=color, marker=marker, ls=ls, label=label, markeredgecolor="white", markeredgewidth=0.5)


def fig_sites():
    m1 = pd.read_csv(os.path.join(DATA, "rq1_macro.csv"))
    m2 = pd.read_csv(os.path.join(DATA, "rq2_macro.csv"))
    fig, axs = plt.subplots(1, 2, figsize=(7.16, 2.25), sharey=True)
    ax = axs[0]
    kr = m1[m1.estimator == "Kriging"]
    for j, (dn, lab) in enumerate([("FSCA", "FSCA"), ("Greedy", "greedy (A-optimal)"), ("QR", "QR pivoting"),
                                   ("Random", "random (mean of 20)")]):
        curve(ax, kr[kr.design == dn], lab, SERIES[j], MARKERS[j], band=(j == 0))
    d = kr[kr.design == "Standard"].sort_values("k")
    ax.plot(d.k, d.rmse, color=SERIES[4], marker="v", ls=":", label="standard 1/5/9", markeredgecolor="white",
            markeredgewidth=0.5)
    d = kr[kr.design == "Edge-inclusive"].sort_values("k")
    ax.plot(d.k, d.rmse, color=SERIES[5], marker="P", ls=":", label="edge-inclusive 5/9", markeredgecolor="white",
            markeredgewidth=0.5)
    ax.set_xlabel("measured sites k")
    ax.set_ylabel("map RMSE (µm)")
    ax.set_title("(a) where to measure (no process data)")
    ax.legend(loc="upper right", ncol=1)
    ax = axs[1]
    g = m2[m2.design == "FSCA"]
    for j, (lv, lab) in enumerate([("none", "none (mean map)"), ("context", "context"), ("process", "machine signals"),
                                   ("context+process", "context + machine"), ("OES", "OES"),
                                   ("context+process+OES", "context + machine + OES")]):
        curve(ax, g[g.level == lv], lab, SERIES[j], MARKERS[j], band=(j == 0))
    ax.set_xlabel("measured sites k (same FSCA sites for every level)")
    ax.set_title("(b) what process information adds")
    ax.legend(loc="upper right")
    for a_ in axs:
        a_.set_xticks(range(0, 13, 2))
        a_.set_yscale("log")
        a_.set_ylim(0.04, 0.45)
        a_.set_yticks([0.05, 0.1, 0.2, 0.4])
        a_.set_yticklabels(["0.05", "0.1", "0.2", "0.4"])
        a_.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    fig.tight_layout(w_pad=1.0)
    save(fig, "fig_sites")


# ------------------------------------------------------------------ Fig. 4: error of the within-wafer CV estimate
def fig_cv():
    u = pd.read_csv(os.path.join(DATA, "uniformity_cv_errors.csv")).drop(columns="lot")
    names = {"9 standard,\nas measured": "9 standard, raw", "9 standard\n+ model": "9 standard + model",
             "3 learned\n+ model": "3 learned + model", "1 learned\n+ model": "1 learned + model",
             "0 sites,\nmean map": "0 sites, mean map", "0 sites,\nVM only": "0 sites, process prior"}
    u = u.rename(columns=names)[list(names.values())]
    fig, axs = plt.subplots(1, 2, figsize=(3.5, 1.75), sharey=True, gridspec_kw={"width_ratios": [0.55, 1]})
    rows = list(u.columns)[::-1]
    for ax, rng in ((axs[0], (-6.6, -5.0)), (axs[1], (-0.5, 0.5))):
        for i, c in enumerate(rows):
            v = u[c].dropna().values
            yj = i + (np.random.default_rng(i).random(len(v)) - 0.5) * 0.45
            ax.scatter(v, yj, s=3, color=MUTED if "raw" in c else SERIES[0], linewidths=0, alpha=0.85)
            med = np.median(v)
            if rng[0] <= med <= rng[1]:
                ax.plot([med, med], [i - 0.32, i + 0.32], color=INK, lw=1.0)
        ax.set_xlim(*rng)
        ax.axvline(0, color=INK2, lw=0.5) if rng[0] < 0 < rng[1] else None
        ax.grid(axis="y", visible=False)
    axs[0].set_yticks(range(len(rows)))
    axs[0].set_yticklabels(rows)
    axs[0].set_xticks([-6.5, -6.0, -5.5])
    axs[0].set_xticklabels(["−6.5", "−6", "−5.5"])
    axs[1].spines["left"].set_visible(False)
    axs[1].tick_params(axis="y", length=0)
    for ax, side in ((axs[0], 1), (axs[1], 0)):               # break marks between the two x ranges
        kw = dict(transform=ax.transAxes, color=INK2, clip_on=False, lw=0.6)
        ax.plot([side - 0.02 * (1 if side else -1) * 0 - 0.015, side + 0.015], [-0.03, 0.03], **kw)
    fig.text(0.62, 0.0, "estimated − true within-wafer CV (percentage points)", ha="center", va="bottom", fontsize=7)
    fig.tight_layout(w_pad=0.4, rect=(0, 0.06, 1, 1))
    save(fig, "fig_cv")


if __name__ == "__main__":
    fig_maps()
    fig_audit()
    fig_sites()
    fig_cv()
    print("figures written to", OUT)
