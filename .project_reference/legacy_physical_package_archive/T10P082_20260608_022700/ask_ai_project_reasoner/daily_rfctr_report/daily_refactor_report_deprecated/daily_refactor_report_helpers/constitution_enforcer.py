from dev_tools.daily_refactor_report_helpers.analysis_contracts import AnalysisInputs, AnalyzerResult


def analyze_constitution(inputs: AnalysisInputs) -> AnalyzerResult:
    dep_graph = inputs.dependency_graph or {}
    rules = inputs.governance_rules or {}

    violations = []
    violation_count = 0

    domains = rules.get("domains", {})
    enforcement = rules.get("enforcement", {})

    edges = dep_graph.get("edges", [])

    for edge in edges:
        source = edge.get("from", "")
        target = edge.get("to", "")

        for domain_name, domain_rules in domains.items():
            root_pkg = domain_rules.get("root_package", "")
            forbidden = domain_rules.get("forbidden_import_prefixes", [])

            if source.startswith(root_pkg):
                for forbidden_prefix in forbidden:
                    if target.startswith(forbidden_prefix):
                        violation_count += 1
                        violations.append({
                            "type": "forbidden_import",
                            "from": source,
                            "to": target
                        })

    max_forbidden = enforcement.get("max_forbidden_edges", 0)

    compliance = "pass"
    if violation_count > max_forbidden:
        compliance = "fail"

    payload = {
        "violation_count": violation_count,
        "violations": violations,
        "compliance": compliance
    }

    return AnalyzerResult(
        name="constitution_enforcer",
        version="1.0",
        result=payload
    )