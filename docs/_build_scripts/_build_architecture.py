import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm

BG = "#08080A"
PANEL = "#151517"
BORDER = "#33333a"
ACCENT = "#D4AF37"
TEXT = "#EDEDED"
DIM = "#9a9a9f"
POS = "#16C784"

fig, ax = plt.subplots(figsize=(12, 7.5), dpi=150)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 12)
ax.set_ylim(0, 7.5)
ax.axis("off")

def box(x, y, w, h, label, sublabel=None, color=PANEL, edge=ACCENT, textcolor=TEXT, fontsize=10.5):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                        linewidth=1.4, edgecolor=edge, facecolor=color, zorder=2)
    ax.add_patch(b)
    if sublabel:
        ax.text(x + w/2, y + h*0.62, label, ha="center", va="center",
                 color=textcolor, fontsize=fontsize, fontweight="bold", zorder=3)
        ax.text(x + w/2, y + h*0.30, sublabel, ha="center", va="center",
                 color=DIM, fontsize=fontsize-2.5, zorder=3)
    else:
        ax.text(x + w/2, y + h/2, label, ha="center", va="center",
                 color=textcolor, fontsize=fontsize, fontweight="bold", zorder=3)
    return (x, y, w, h)

def arrow(p1, p2, color=ACCENT, style="-|>", curve=0.0):
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=14,
                         linewidth=1.6, color=color, zorder=1,
                         connectionstyle=f"arc3,rad={curve}")
    ax.add_patch(a)

# Title
ax.text(0.15, 7.15, "FORBES 2000", color=ACCENT, fontsize=17, fontweight="bold", family="serif")
ax.text(0.15, 6.85, "Repository Architecture & Data Flow", color=DIM, fontsize=10.5)

# Row 1: Raw data
raw = box(0.3, 5.6, 2.3, 0.85, "Raw Dataset", "data/raw/*.csv", color="#1a1510", edge="#8a6d00")

# Cleaning script
clean = box(3.2, 5.6, 2.5, 0.85, "Cleaning Pipeline", "scripts/clean_forbes_2000.py")
arrow((2.6, 6.02), (3.2, 6.02))

# Outputs: processed csv + report
proc = box(6.3, 6.15, 2.5, 0.7, "Cleaned Dataset", "data/processed/*.csv")
rep = box(6.3, 5.35, 2.5, 0.7, "Quality Report", "data/reports/*.txt")
arrow((5.7, 6.15), (6.3, 6.45))
arrow((5.7, 5.9), (6.3, 5.65))

# Tests
tests = box(9.3, 5.6, 2.4, 0.85, "Automated Tests", "tests/test_data_quality.py", edge=POS)
arrow((8.8, 6.5), (9.3, 6.1), curve=-0.15)
arrow((8.8, 5.7), (9.3, 5.95), curve=0.1)

# Row 2: consumers of cleaned data
nb = box(3.2, 3.9, 2.5, 0.85, "EDA Notebook", "notebooks/exploratory_analysis.ipynb")
dash = box(6.3, 3.9, 2.5, 0.85, "Dashboard Build", "embed cleaned data as inline JSON")
arrow((7.5, 6.15), (4.45, 4.75), curve=0.25)
arrow((7.5, 6.15), (7.5, 4.75))

# Row 3: dashboard files
idx = box(5.0, 2.5, 1.55, 0.75, "index.html", color="#151725", edge="#6C8EBF")
css = box(6.75, 2.5, 1.55, 0.75, "style.css", color="#151725", edge="#6C8EBF")
js = box(8.5, 2.5, 1.55, 0.75, "script.js\n(data embedded)", color="#151725", edge="#6C8EBF", fontsize=9.5)
arrow((7.0, 3.9), (5.77, 3.25), curve=0.15)
arrow((7.55, 3.9), (7.52, 3.25))
arrow((8.1, 3.9), (9.27, 3.25), curve=-0.15)

# Row 4: deployment
gha = box(5.0, 1.2, 2.5, 0.75, "GitHub Actions", ".github/workflows/deploy.yml", edge=POS)
pages = box(8.0, 1.2, 2.5, 0.75, "GitHub Pages", "live public dashboard URL", edge=POS)
arrow((6.75, 2.5), (6.25, 1.95))
arrow((7.5, 1.575), (8.0, 1.575))

# Docs branch off the report/tests
docs = box(9.3, 3.9, 2.4, 0.85, "Documentation", "docs/*.pdf, README.md")
arrow((10.5, 5.6), (10.5, 4.75))

# Footer credit
ax.text(0.15, 0.35, "Ging (Gabriel Alegre Caña) · Forbes Global 2000 (2026) Analytics Project",
         color=DIM, fontsize=8.5)

plt.tight_layout()
plt.savefig("Architecture.png", facecolor=BG, dpi=150, bbox_inches="tight")
print("Architecture.png created")
