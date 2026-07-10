import re
import unicodedata


def split_title_and_description(value):
    lines = [line.strip() for line in (value or "").splitlines() if line.strip()]
    if not lines:
        return "", ""
    return lines[0], "\n".join(lines[1:])


def parse_level(value):
    match = re.search(r"\d+", value or "")
    return int(match.group()) if match else 0


def make_id(name):
    ascii_name = unicodedata.normalize("NFKD", name or "").encode("ascii", "ignore").decode().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_name).strip("-")
    return slug


def parse_conditions(text, mapper, warnings, label):
    """Convert e.g. 火 2/8 into trait:fire:8, retaining only required value."""
    conditions = []
    matched_spans = []
    pattern = re.compile(r"([^\d\n/]+?)\s*\d+\s*/\s*(\d+)")
    for match in pattern.finditer(text or ""):
        trait_text = match.group(1).strip(" ：:-")
        trait_id = mapper.map(trait_text)
        if trait_id:
            conditions.append(f"trait:{trait_id}:{match.group(2)}")
        else:
            warnings.append(f"{label}：無法對應 trait「{trait_text}」。")
        matched_spans.append(match.span())
    if (text or "").strip() and not matched_spans:
        warnings.append(f"{label}：找不到「trait 目前值/需求值」格式。")
    return ";".join(conditions)


def parse_raw(raw, mapper):
    warnings = []
    summon_name, summon_description = split_title_and_description(raw.get("summonSkill", ""))
    tactic_name, tactic_description = split_title_and_description(raw.get("uniqueTactic", ""))
    traits = mapper.find_in_text(raw.get("traits", ""))
    if raw.get("traits", "").strip() and not traits:
        warnings.append("traits：無法從 OCR 文字對應任何 trait。")
    officer_id = make_id(raw.get("name", "").strip())
    if raw.get("name", "").strip() and not officer_id:
        warnings.append("id：中文名稱無法自動轉成穩定英文 id，請在互動模式補上。")
    parsed = {
        "id": officer_id,
        "name": raw.get("name", "").strip(),
        "faction": "cameo", "factionName": "客座", "level": parse_level(raw.get("level", "")),
        "playerTraits": ";".join(f"{trait}:1" for trait in traits), "supportTraits": "",
        "operationTraitName": "待補", "operationTraitDescription": "操作特性資料待補。",
        "specialWeaponDescription": "持有特武效果待補。", "limitBreakDescription": "限界突破效果待補。",
        "summonSkillName": summon_name, "summonSkillDescription": summon_description,
        "summonSkillLevel": 1, "summonUpgradeConditionType": "all",
        "summonUpgradeConditions": parse_conditions(raw.get("summonUpgradeConditions", ""), mapper, warnings, "summonUpgradeConditions"),
        "uniqueTacticName": tactic_name, "uniqueTacticDescription": tactic_description,
        "uniqueTacticConditionType": "all",
        "uniqueTacticConditions": parse_conditions(raw.get("uniqueTacticConditions", ""), mapper, warnings, "uniqueTacticConditions"),
    }
    return parsed, warnings
