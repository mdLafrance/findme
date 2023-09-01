"""List of runnable tasks using the pyinvoke library."""
from pathlib import Path
from shutil import rmtree

from invoke import task


REPORTS_DIR = "reports"


def _print_title(*m):
    print(" >", *m)


@task
def test(c):
    _print_title("Running tests and generating coverage report")
    coverage_dir = Path(REPORTS_DIR) / "coverage"
    coverage_file = coverage_dir / ".coverage"
    coverage_xml = coverage_dir / "coverage.xml"

    c.run(f"poetry run coverage run --data-file={coverage_file} -m pytest ./src/tests/")
    c.run(f"poetry run coverage xml --data-file={coverage_file} -o {coverage_xml}")
    c.run(f"genbadge coverage -i {coverage_xml} -o {coverage_dir / 'coverage-badge.svg'}")


@task
def lint(c):
    _print_title("Running black")
    c.run("poetry run black ./src")


@task
def build(c):
    c.run("poetry build")


@task
def clean(c):
    _print_title("Cleaning reports and build artifacts")
    
    # build
    build_dir = Path("./dist")
    if build_dir.is_dir():
        print(f"Cleaning build {build_dir}")
        rmtree(build_dir)

    # reports
    reports_dir = Path("./reports/")
    if reports_dir.is_dir():
        print(f"Cleaning reports {reports_dir}")
        rmtree(reports_dir)

    # Clean poetry lock 
    poetry_lock = Path("./poetry.lock")
    poetry_lock.unlink(missing_ok=True)
    print(f"Cleaning lock file {poetry_lock}")
