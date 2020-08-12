import subprocess


def test_specification(module) -> str:
    """テスト仕様
    """
    return "<br/>".join(subprocess.run(
        f"pytest --collect-only --quiet {module.__file__}",
        universal_newlines=True,
        check=True,
        shell=True,
        stdout=subprocess.PIPE
        ).stdout.splitlines())