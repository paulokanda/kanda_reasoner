import inspect

import kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.guarded_advisory_surface_wiring_contract as module
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
    build_phase7_guarded_advisory_surface_wiring_contract,
    evaluate_phase7_guarded_advisory_surface_wiring_request,
)


def main() -> None:
    contract = build_phase7_guarded_advisory_surface_wiring_contract()
    decision = evaluate_phase7_guarded_advisory_surface_wiring_request(
        auto_use_after_router=True,
        visible_panel=True,
    )
    assert contract.policy.route_authority_enabled is False
    assert decision.may_activate_runtime_wiring is False

    source = inspect.getsource(module)
    forbidden = (
        "requests",
        "httpx",
        "urllib",
        "socket",
        "subprocess",
        "sqlite3",
        "open(",
        "Path(",
        "os.environ",
        "MLRT_113",
        "mlrt113",
    )
    for token in forbidden:
        assert token not in source, token

    print("VALIDATION OK: phase7 guarded advisory surface wiring import boundary")


if __name__ == "__main__":
    main()
