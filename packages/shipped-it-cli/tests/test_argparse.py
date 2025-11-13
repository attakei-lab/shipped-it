from shipped_it_cli import CliSettings


def test_simple():
    argv = "pypi oembedpy"
    args = CliSettings(_cli_parse_args=argv.split())  # ty: ignore[missing-argument,unknown-argument]
    assert args.source == "pypi"
    assert args.release == "oembedpy"
