from reversible_redaction.cli import build_parser


def test_skill_cli_contract_supports_redact_and_restore():
    parser = build_parser()
    commands = sorted(parser._subparsers._group_actions[0].choices.keys())
    assert "redact" in commands
    assert "restore" in commands
