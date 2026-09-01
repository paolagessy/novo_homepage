# -*- coding: utf-8 -*-
"""Fluxo medido da flare em funcao do tempo, nas quatro bandas do SPARC4.

Le o CSV de curvas produzido pelo notebook `sparc4_flares_aumic.ipynb` e
desenha C(t) = f(t)/q(t) — o fluxo do alvo dividido pelas comparacoes e
normalizado pelo quiescente — banda a banda. C = 1 e a estrela em repouso;
C = 1.18 e um excesso de 18% (180 ppt), que foi o pico desta flare em g.

Uso:  python plota_flare_4bandas.py
"""
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ── configuracao ────────────────────────────────────────────────────────────
BASE   = r"C:/Users/paola/Desktop/Doutorado/Codigos-doc/Flares-/novo_homepage/Sparc4-data"
OUTDIR = os.path.join(BASE, "resultados_flares")
FLARE  = "aumic_flares_20260815_F01"

BANDAS = ["g", "r", "i", "z"]
CORES  = {"g": "#3b6ea5", "r": "#3f8f4f", "i": "#c06a2a", "z": "#8b3a5a"}
LAMBDA = {"g": 457, "r": 614, "i": 753, "z": 894}     # nm, comprimento efetivo

MOSTRA_MODELO = True      # sobrepoe o ajuste de corpo negro (Heinzel+2026)

# ── dados ───────────────────────────────────────────────────────────────────
csv = os.path.join(OUTDIR, f"{FLARE}_curvas.csv")
d   = pd.read_csv(csv)
t   = d["minutos"].to_numpy(float)

# ── figura: um painel por banda, mesmo eixo de tempo ────────────────────────
fig, axs = plt.subplots(4, 1, figsize=(8.5, 9), sharex=True)

for ax, b in zip(axs, BANDAS):
    C   = d[f"C_{b}"].to_numpy(float)
    sig = d[f"sigC_{b}"].to_numpy(float)

    ax.axhline(1.0, color="0.6", lw=0.8, zorder=0)              # quiescente
    ax.errorbar(t, C, yerr=sig, fmt="o", ms=3.5, lw=0, elinewidth=0.9,
                capsize=0, color=CORES[b], ecolor=CORES[b], alpha=0.85,
                zorder=2)
    if MOSTRA_MODELO and f"modelo_IIb_{b}" in d:
        ax.plot(t, d[f"modelo_IIb_{b}"], "-", lw=1.4, color="k", alpha=0.55,
                zorder=3)

    # rotulo direto: a identidade da banda nao depende so da cor
    ax.text(0.985, 0.88, f"{b}   {LAMBDA[b]} nm", transform=ax.transAxes,
            ha="right", va="top", fontsize=12, fontweight="bold",
            color=CORES[b])

    amp = (np.nanmax(C) - 1.0) * 1e3
    ax.text(0.985, 0.70, f"amp = {amp:.0f} ppt", transform=ax.transAxes,
            ha="right", va="top", fontsize=9, color="0.35")

    ax.set_ylabel("C = f / q")
    ax.grid(alpha=0.18, lw=0.6)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)

axs[-1].set_xlabel("tempo desde o inicio da janela [min]")
axs[0].set_title(f"AU Mic · flare {FLARE.split('_')[-1]} · 2026-08-15 22:38:10 UTC\n"
                 "fluxo medido nas quatro bandas do SPARC4", fontsize=12, pad=12)
fig.align_ylabels(axs)
fig.tight_layout()

png = os.path.join(OUTDIR, f"{FLARE}_4bandas.png")
fig.savefig(png, dpi=160)
print(f"figura -> {png}")

# ── tabela: quando e quanto cada banda mediu ────────────────────────────────
print(f"\n{'banda':>6} {'lambda':>8} {'t pico':>9} {'amp':>10} {'S/R pico':>10}")
print(f"{'':>6} {'[nm]':>8} {'[min]':>9} {'[ppt]':>10}")
for b in BANDAS:
    C, sig = d[f"C_{b}"].to_numpy(float), d[f"sigC_{b}"].to_numpy(float)
    k = int(np.nanargmax(C))
    print(f"{b:>6} {LAMBDA[b]:>8} {t[k]:>9.2f} {(C[k]-1)*1e3:>10.1f} "
          f"{(C[k]-1)/sig[k]:>10.1f}")

plt.show()
