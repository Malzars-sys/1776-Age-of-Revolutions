"""Read-only regression checks against the installed game's building group hierarchy.

This checks definitions, not live-game buttons or save migration. Economic laws
continue to control nationalization and privatization as in vanilla.
"""
import json

from asset4_style_reference_audit import catalog, field


def main():
    groups = catalog("common/building_groups")
    buildings = catalog("common/buildings")
    building = buildings["building_railway"][0]
    group = field(building, "building_group")
    chain = []
    effective = {}
    while group:
        assert group not in chain, "Cyclic building group inheritance"
        chain.append(group)
        tokens = groups[group][0]
        for key in ("is_government_funded", "subsidized", "cash_reserves_max",
                    "economy_of_scale", "infrastructure_usage_per_level"):
            value = field(tokens, key)
            if value and key not in effective:
                effective[key] = value
        group = field(tokens, "parent_group")

    assert chain == ["bg_land_transport_network", "bg_private_infrastructure", "bg_infrastructure"]
    assert effective["is_government_funded"] == "no"
    assert effective["subsidized"] == "yes"  # Campaign-start default only.
    assert float(effective["cash_reserves_max"]) == 25000
    assert effective["economy_of_scale"] == "no"
    assert float(effective["infrastructure_usage_per_level"]) == 0
    assert field(building, "ownership_type") != "none"
    assert field(building, "buildable") != "no"

    native_building = catalog("common/buildings", native_only=True)["building_railway"][0]
    assert field(native_building, "building_group") == "bg_private_infrastructure"
    assert field(building, "ownership_type") == field(native_building, "ownership_type")

    print(json.dumps({"status": "PASS_STATIC_DEFINITIONS", "building": "building_railway",
                      "inheritance": chain, "effective": effective,
                      "ownership_model": "same as installed vanilla railway",
                      "limitations": "Live game and existing-save migration not exercised; economic law restrictions retained."},
                     indent=2))


if __name__ == "__main__":
    main()
