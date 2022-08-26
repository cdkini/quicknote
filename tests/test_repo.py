import pytest

from qn.repo import Repo


def test_repo_create_no_root_raises_error(monkeypatch):
    monkeypatch.delenv("QN_ROOT", raising=False)

    with pytest.raises(ValueError) as e:
        Repo.create()

    assert "No value found for QN_ROOT env var" == str(e.value)


def test_repo_create_nonexistent_root_raises_error(monkeypatch):
    path = "this/does/not/exist"
    monkeypatch.setenv("QN_ROOT", path)

    with pytest.raises(ValueError) as e:
        Repo.create()

    assert f"QN_ROOT '{path}' does not exist" == str(e.value)


def test_repo_create_file_root_raises_error(monkeypatch, tmp_path) -> None:
    path = tmp_path / "root.md"
    path.touch()
    monkeypatch.setenv("QN_ROOT", str(path))

    with pytest.raises(ValueError) as e:
        Repo.create()

    assert f"QN_ROOT '{path}' is not a directory" == str(e.value)
