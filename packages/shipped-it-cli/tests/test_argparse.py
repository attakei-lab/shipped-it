from shipped_it_cli import CliSettings


def test_simple():
    argv = "pypi oembedpy"
    args = CliSettings(_cli_parse_args=argv.split())  # ty: ignore[missing-argument,unknown-argument]
    assert args.source == "pypi"
    assert args.release == "oembedpy"
    assert len(args.extra_values) == 0


def test_extra_context_values():
    argv = [
        "pypi",
        "oembedpy",
        "--extra-values",
        "hello=world",
        "--extra-values",
        "hello2=WORLD",
    ]
    args = CliSettings(_cli_parse_args=argv)  # ty: ignore[missing-argument,unknown-argument]
    assert args.source == "pypi"
    assert args.release == "oembedpy"
    assert len(args.extra_values) == 2
    assert args.extra_values["hello"] == "world"
    assert args.extra_values["hello2"] == "WORLD"
