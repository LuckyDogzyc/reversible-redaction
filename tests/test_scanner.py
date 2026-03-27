from reversible_redaction.scanner import scan_entities


def test_scan_entities_detects_ips_and_hosts():
    text = "Server 10.1.2.3 runs kpw_proxy_72 and backup 10.1.2.3"
    entities = scan_entities(text)
    kinds = [e.kind for e in entities]
    assert "ip" in kinds
    assert "hostname" in kinds
    assert len([e for e in entities if e.original == "10.1.2.3"]) == 1
