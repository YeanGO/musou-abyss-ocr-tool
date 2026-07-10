import csv
import json
from pathlib import Path

FIELDS = ["id", "name", "faction", "factionName", "level", "playerTraits", "supportTraits", "operationTraitName", "operationTraitDescription", "specialWeaponDescription", "limitBreakDescription", "summonSkillName", "summonSkillDescription", "summonSkillLevel", "summonUpgradeConditionType", "summonUpgradeConditions", "uniqueTacticName", "uniqueTacticDescription", "uniqueTacticConditionType", "uniqueTacticConditions"]


def write_drafts(raw, parsed, warnings, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "officer-draft.json", "w", encoding="utf-8") as handle:
        json.dump({"rawOcr": raw, "parsed": parsed, "warnings": warnings}, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    with open(output_dir / "officer-draft.csv", "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerow(parsed)
