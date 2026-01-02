import subprocess
import sys
from pathlib import Path


def _is_png(path: Path) -> bool:
    return (
        path.exists()
        and path.stat().st_size > 1000
        and path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
    )


def _find_plot_script(project_root: Path, must_contain: list[str]) -> Path:
    plots_dir = project_root / "plots"
    scripts = list(plots_dir.glob("*.py"))

    matches = []
    for p in scripts:
        name = p.name.lower()
        if all(token in name for token in must_contain):
            matches.append(p)

    if not matches:
        raise FileNotFoundError(
            f"No plot script found matching tokens={must_contain}. "
            f"Found scripts: {[p.name for p in scripts]}"
        )

    return sorted(matches, key=lambda x: len(x.name))[0]


def test_births_plot_2024_creates_png():
    project_root = Path(__file__).resolve().parents[1]
    plots_dir = project_root / "plots"

    script = _find_plot_script(project_root, must_contain=["birth", "2024"])

    before = {p.name for p in plots_dir.glob("*.png")}

    env = dict(**__import__("os").environ)
    env["CI"] = "true"
    env["MPLBACKEND"] = "Agg"

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=project_root,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0, result.stderr

    after = {p.name for p in plots_dir.glob("*.png")}
    new_pngs = sorted(list(after - before))

    assert new_pngs, (
        f"Script ran but produced no new PNG.\nScript: {script}\n"
        f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )

    assert any(_is_png(plots_dir / f) for f in new_pngs)
