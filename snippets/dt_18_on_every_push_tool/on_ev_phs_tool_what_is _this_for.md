# Basic run (text/JSON only)
python dev_tools/on_every_push_tool/on_ev_phs_tool.py run

# With thresholds
python dev_tools/on_every_push_tool/on_ev_phs_tool.py run --max-cx 15 --max-debt 0

# Persist a baseline to compare future debt/violations against
python dev_tools/on_every_push_tool/on_ev_phs_tool.py write-baseline

# Show latest summary
python dev_tools/on_every_push_tool/on_ev_phs_tool.py summary

