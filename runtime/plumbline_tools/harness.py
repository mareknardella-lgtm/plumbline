def generate_conftest(nondeterminism_sources: list) -> str:
    content = [
        "import pytest",
        "import socket",
        "import random",
        "import time",
        "",
        "@pytest.fixture(autouse=True)",
        "def block_network(monkeypatch):",
        "    def guard(*args, **kwargs):",
        "        raise Exception('Network access blocked during tests')",
        "    monkeypatch.setattr(socket, 'socket', guard)",
        "",
        "@pytest.fixture(autouse=True)",
        "def seed_random():",
        "    random.seed(42)",
        "",
    ]

    if "time" in nondeterminism_sources:
        content.extend(
            [
                "@pytest.fixture(autouse=True)",
                "def freeze_time(monkeypatch):",
                "    try:",
                "        from freezegun import freeze_time as ft",
                "        with ft('2024-01-01 12:00:00'):",
                "            yield",
                "    except ImportError:",
                "        yield",
                "",
            ]
        )

    return "\n".join(content)
