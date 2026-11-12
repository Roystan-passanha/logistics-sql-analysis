import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import run_analysis  # noqa: E402


def setup_module():
    subprocess.run([sys.executable, str(ROOT / "generate_data.py")], check=True)


def test_every_query_runs_and_returns_rows(tmp_path):
    con = run_analysis.build_db(tmp_path / "t.db")
    for file in sorted((ROOT / "sql").glob("0*.sql"))[1:]:
        cols, rows = run_analysis.run(con, file.name)
        assert cols and rows, file.name


def test_on_time_pct_is_a_percentage(tmp_path):
    con = run_analysis.build_db(tmp_path / "t.db")
    _, rows = run_analysis.run(con, "03_on_time_by_region.sql")
    assert len(rows) == 4
    assert all(0 <= r[3] <= 100 for r in rows)


def test_cancelled_deliveries_excluded_from_view(tmp_path):
    con = run_analysis.build_db(tmp_path / "t.db")
    total = con.execute("SELECT COUNT(*) FROM deliveries").fetchone()[0]
    delivered = con.execute("SELECT COUNT(*) FROM v_delivered").fetchone()[0]
    cancelled = con.execute("SELECT COUNT(*) FROM deliveries WHERE status='Cancelled'").fetchone()[0]
    assert delivered == total - cancelled
