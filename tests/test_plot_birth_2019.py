import subprocess
import sys
from pathlib import Path


def _is_png(path: Path) -> bool:
    return path.exists() and path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n" and path.stat().st_size > 1000


def test_births_bar_chart_2019_creates_png():
    project_root = Path(__file__).resolve().parents[1]
    script = project_root / "plots" / "births_bar_chart_2019.py"
    out_png = project_root / "plots" / "business_births_top_regions_2019.png"

    if out_png.exists():
        out_png.unlink()

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=project_root,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert _is_png(out_png)
