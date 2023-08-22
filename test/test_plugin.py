import pytest

from sphinxcontrib.bibtex.plugin import find_plugin, register_plugin


def test_plugin_bad_group() -> None:
    with pytest.raises(ImportError, match="plugin group blablabla not found"):
        find_plugin("blablabla", "boo")
    with pytest.raises(ImportError, match="plugin group blablabla not found"):
        register_plugin("blablabla", "boo", type(None))


def test_plugin_register_not_forced() -> None:
    class Plugin:
        pass

    assert not register_plugin(
        "sphinxcontrib.bibtex.style.referencing", "label", Plugin
    )
    assert find_plugin("sphinxcontrib.bibtex.style.referencing", "label") is not Plugin


def test_plugin_register_forced() -> None:
    class PluginOld:
        pass

    class PluginNew:
        pass

    assert register_plugin(
        "sphinxcontrib.bibtex.style.referencing",
        "xxx_test_plugin_register_forced",
        PluginOld,
    )
    assert (
        find_plugin(
            "sphinxcontrib.bibtex.style.referencing", "xxx_test_plugin_register_forced"
        )
        is PluginOld
    )
    assert not register_plugin(
        "sphinxcontrib.bibtex.style.referencing",
        "xxx_test_plugin_register_forced",
        PluginNew,
    )
    assert (
        find_plugin(
            "sphinxcontrib.bibtex.style.referencing", "xxx_test_plugin_register_forced"
        )
        is PluginOld
    )
    assert register_plugin(
        "sphinxcontrib.bibtex.style.referencing",
        "xxx_test_plugin_register_forced",
        PluginNew,
        force=True,
    )
    assert (
        find_plugin(
            "sphinxcontrib.bibtex.style.referencing", "xxx_test_plugin_register_forced"
        )
        is PluginNew
    )
