from unittest import mock

import pytest

from qn.store import Store


def test_add_existing_name_raises_error(tmp_path):
    root = tmp_path
    shell = mock.MagicMock()

    store = Store(root=root, shell=shell)

    file_name = "foo.md"
    existing_file = root.joinpath(file_name)
    existing_file.touch()

    with pytest.raises(FileExistsError) as e:
        store.add(file_name)

    assert f"'{file_name}' already exists" in str(e.value)


def test_add_invokes_shell(tmp_path):
    root = tmp_path
    shell = mock.MagicMock()

    store = Store(root=root, shell=shell)

    store.add("foo.md")

    shell.open.assert_called()


def test_open_nonexistent_name_raises_error(tmp_path):
    root = tmp_path
    shell = mock.MagicMock()

    store = Store(root=root, shell=shell)

    with pytest.raises(FileNotFoundError) as e:
        file_names = ("foo.md",)
        store.open(file_names)

    assert f"'{file_names[0]}' does not exist" in str(e.value)


def test_open_invokes_shell(tmp_path):
    root = tmp_path
    shell = mock.MagicMock()

    store = Store(root=root, shell=shell)

    file_names = ("foo.md", "bar.md")
    for file_name in file_names:
        existing_file = root.joinpath(file_name)
        existing_file.touch()

    store.open(file_names)

    shell.open.assert_called()


def test_list(tmp_path):
    root = tmp_path
    shell = mock.MagicMock()

    store = Store(root=root, shell=shell)

    file_names = ["foo.md", "bar.md", "baz.md"]
    for file_name in file_names:
        existing_file = root.joinpath(file_name)
        existing_file.touch()

    entries = store.list()

    assert sorted(file_names) == entries


def test_delete_nonexistent_name_raises_error(tmp_path):
    root = tmp_path
    shell = mock.MagicMock()

    store = Store(root=root, shell=shell)

    with pytest.raises(FileNotFoundError) as e:
        file_names = ("foo.md",)
        store.delete(file_names)

    assert f"'{file_names[0]}' does not exist" in str(e.value)


def test_delete_invokes_shell(tmp_path):
    root = tmp_path
    shell = mock.MagicMock()

    store = Store(root=root, shell=shell)

    file_names = ("foo.md", "bar.md", "baz.md")
    paths = []
    for file_name in file_names:
        path = root.joinpath(file_name)
        path.touch()
        paths.append(path)

    store.delete(file_names)

    assert all(not path.exists() for path in paths)
