from reversible_redaction.redactor import redact_text
from reversible_redaction.restore import restore_text


def test_redact_and_restore_round_trip():
    original = "IP 10.1.2.3 belongs to kpw_proxy_72"
    redacted, mappings = redact_text(original)
    restored = restore_text(redacted, mappings)
    assert restored == original
