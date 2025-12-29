"""
ACES Data Integrity Verification Script

Run this after ingestion to verify that no data was lost.
"""

from django.db.models import Count, Q
from apps.autocare.models.aces import (
    AcesApp,
    AcesAppVehicle,
    AcesQualifier,
    AcesRawAttribute,
    AcesVehicleType,
)


def verify_aces_integrity(source_file: str, verbose: bool = True):
    """
    Verify that all data from the ACES file was properly imported.

    Returns dict with verification results.
    """

    results = {
        "apps_total": 0,
        "apps_with_vehicles": 0,
        "apps_with_parts": 0,
        "apps_with_part_types": 0,
        "apps_with_qualifiers": 0,
        "apps_with_notes": 0,
        "apps_with_raw_attrs": 0,
        "total_notes": 0,
        "total_qualifiers": 0,
        "total_raw_attrs": 0,
        "total_vehicle_types": 0,
        "missing_vehicle_records": [],
        "missing_parts": [],
        "issues": [],
    }

    if verbose:
        print("\n" + "=" * 70)
        print("  ACES DATA INTEGRITY VERIFICATION")
        print("=" * 70)
        print(f"\nSource file: {source_file}")
        print("\n[1/5] Checking core application records...")

    # Get all apps from this source file
    apps = AcesApp.objects.filter(source_file=source_file)
    results["apps_total"] = apps.count()

    if verbose:
        print(f"      ✓ Found {results['apps_total']:,} applications")

    if results["apps_total"] == 0:
        results["issues"].append("No applications found for this source file!")
        return results

    # Check vehicle records
    if verbose:
        print("\n[2/5] Verifying vehicle records...")

    apps_with_vehicles = apps.filter(acesappvehicle__isnull=False).count()
    results["apps_with_vehicles"] = apps_with_vehicles

    if apps_with_vehicles != results["apps_total"]:
        missing = apps.filter(acesappvehicle__isnull=True)
        results["missing_vehicle_records"] = list(missing.values_list("app_id", flat=True))
        results["issues"].append(
            f"{results['apps_total'] - apps_with_vehicles} apps missing vehicle records!"
        )
        if verbose:
            print(f"      ⚠ WARNING: {len(results['missing_vehicle_records'])} apps missing vehicle records")
            print(f"        App IDs: {results['missing_vehicle_records'][:10]}...")
    else:
        if verbose:
            print(f"      ✓ All {results['apps_total']:,} apps have vehicle records")

    # Check required fields
    if verbose:
        print("\n[3/5] Verifying required fields...")

    apps_with_parts = apps.exclude(Q(part_number__isnull=True) | Q(part_number="")).count()
    apps_with_part_types = apps.filter(part_type_id__isnull=False).count()

    results["apps_with_parts"] = apps_with_parts
    results["apps_with_part_types"] = apps_with_part_types

    if apps_with_parts != results["apps_total"]:
        missing_parts = results["apps_total"] - apps_with_parts
        results["issues"].append(f"{missing_parts} apps missing part numbers!")
        if verbose:
            print(f"      ⚠ WARNING: {missing_parts} apps missing part numbers")
    else:
        if verbose:
            print(f"      ✓ All apps have part numbers")

    if apps_with_part_types != results["apps_total"]:
        missing_part_types = results["apps_total"] - apps_with_part_types
        results["issues"].append(f"{missing_part_types} apps missing part types!")
        if verbose:
            print(f"      ⚠ WARNING: {missing_part_types} apps missing part types")
    else:
        if verbose:
            print(f"      ✓ All apps have part types")

    # Check qualifiers
    if verbose:
        print("\n[4/5] Verifying qualifiers and notes...")

    qualifier_stats = AcesQualifier.objects.filter(
        app__source_file=source_file
    ).aggregate(
        total=Count('id'),
        distinct_apps=Count('app', distinct=True)
    )

    results["total_qualifiers"] = qualifier_stats["total"]
    results["apps_with_qualifiers"] = qualifier_stats["distinct_apps"]

    if verbose:
        print(f"      ✓ Found {results['total_qualifiers']:,} qualifiers")
        print(f"        on {results['apps_with_qualifiers']:,} applications")

    # Check notes
    note_stats = AcesRawAttribute.objects.filter(
        app__source_file=source_file,
        attr_name="note"
    ).aggregate(
        total=Count('id'),
        distinct_apps=Count('app', distinct=True)
    )

    results["total_notes"] = note_stats["total"]
    results["apps_with_notes"] = note_stats["distinct_apps"]

    if verbose:
        print(f"      ✓ Found {results['total_notes']:,} notes")
        print(f"        on {results['apps_with_notes']:,} applications")

    # Check vehicle types
    vehicle_type_stats = AcesVehicleType.objects.filter(
        app__source_file=source_file
    ).aggregate(
        total=Count('id'),
        distinct_apps=Count('app', distinct=True)
    )

    results["total_vehicle_types"] = vehicle_type_stats["total"]

    if verbose and results["total_vehicle_types"] > 0:
        print(f"      ✓ Found {results['total_vehicle_types']:,} vehicle type assignments")

    # Check raw attributes (non-notes)
    raw_attr_stats = AcesRawAttribute.objects.filter(
        app__source_file=source_file
    ).exclude(
        attr_name="note"
    ).aggregate(
        total=Count('id'),
        distinct_apps=Count('app', distinct=True)
    )

    results["total_raw_attrs"] = raw_attr_stats["total"]
    results["apps_with_raw_attrs"] = raw_attr_stats["distinct_apps"]

    if results["total_raw_attrs"] > 0:
        if verbose:
            print(f"\n      ℹ INFO: {results['total_raw_attrs']:,} attributes stored in raw_attribute table")
            print(f"        These are fields without dedicated typed tables yet.")

        # Show breakdown by attribute name
        raw_breakdown = AcesRawAttribute.objects.filter(
            app__source_file=source_file
        ).exclude(
            attr_name="note"
        ).values('attr_name').annotate(
            count=Count('id')
        ).order_by('-count')

        if verbose:
            print("\n        Top unmapped attributes:")
            for item in raw_breakdown[:10]:
                print(f"          • {item['attr_name']}: {item['count']:,}")

    # Final summary
    if verbose:
        print("\n[5/5] Summary:")
        print("=" * 70)

        if results["issues"]:
            print("\n  ⚠ ISSUES FOUND:")
            for issue in results["issues"]:
                print(f"    • {issue}")
        else:
            print("\n  ✓ NO ISSUES FOUND - All data successfully imported!")

        print(f"\n  Total Applications: {results['apps_total']:,}")
        print(f"  Applications with vehicles: {results['apps_with_vehicles']:,}")
        print(f"  Applications with qualifiers: {results['apps_with_qualifiers']:,}")
        print(f"  Applications with notes: {results['apps_with_notes']:,}")
        print(f"  Total qualifiers: {results['total_qualifiers']:,}")
        print(f"  Total notes: {results['total_notes']:,}")

        if results["total_vehicle_types"] > 0:
            print(f"  Total vehicle types: {results['total_vehicle_types']:,}")

        if results["total_raw_attrs"] > 0:
            print(f"  Unmapped attributes: {results['total_raw_attrs']:,}")

        print("=" * 70 + "\n")

    return results


def verify_application_completeness(app_id: int, source_file: str):
    """
    Verify a single application record has all its data.

    Useful for debugging specific records.
    """

    try:
        app = AcesApp.objects.get(app_id=app_id, source_file=source_file)
    except AcesApp.DoesNotExist:
        print(f"\nApplication {app_id} not found in {source_file}")
        return None

    print(f"\n{'=' * 70}")
    print(f"  APPLICATION {app_id} VERIFICATION")
    print(f"{'=' * 70}")

    print(f"\nCore Fields:")
    print(f"  Action: {app.action}")
    print(f"  Validate: {app.validate}")
    print(f"  Part Number: {app.part_number}")
    print(f"  Part Type ID: {app.part_type_id}")
    print(f"  Quantity: {app.quantity}")
    print(f"  Position ID: {app.position_id}")

    if app.brand_aaiaid:
        print(f"  Brand AAIAID: {app.brand_aaiaid}")
    if app.subbrand_aaiaid:
        print(f"  Sub-Brand AAIAID: {app.subbrand_aaiaid}")
    if app.mfr_label:
        print(f"  Mfr Label: {app.mfr_label}")

    # Vehicle record
    try:
        vehicle = app.acesappvehicle
        print(f"\nVehicle Record:")
        print(f"  Base Vehicle ID: {vehicle.base_vehicle_id}")
        print(f"  Make ID: {vehicle.make_id}")
        print(f"  Model ID: {vehicle.model_id}")
        print(f"  Submodel ID: {vehicle.submodel_id}")
        print(f"  Year From: {vehicle.year_from}")
        print(f"  Year To: {vehicle.year_to}")
        print(f"  Engine Base ID: {vehicle.engine_base_id}")
        print(f"  Engine Block ID: {vehicle.engine_block_id}")
    except AcesAppVehicle.DoesNotExist:
        print(f"\n  ⚠ WARNING: No vehicle record found!")

    # Qualifiers
    qualifiers = app.qualifiers.all()
    if qualifiers:
        print(f"\nQualifiers ({qualifiers.count()}):")
        for q in qualifiers:
            print(f"  • ID {q.qual_id}: {q.qual_text}")
            if q.param_1:
                print(f"    Param 1: {q.param_1}")
            if q.param_2:
                print(f"    Param 2: {q.param_2}")
            if q.param_3:
                print(f"    Param 3: {q.param_3}")

    # Notes
    notes = app.raw_attributes.filter(attr_name="note")
    if notes:
        print(f"\nNotes ({notes.count()}):")
        for note in notes.order_by('idx'):
            if note.attr_id:
                print(f"  [{note.attr_id}] {note.attr_value}")
            else:
                print(f"  • {note.attr_value}")

    # Other raw attributes
    other_attrs = app.raw_attributes.exclude(attr_name="note")
    if other_attrs:
        print(f"\nRaw Attributes ({other_attrs.count()}):")
        for attr in other_attrs:
            if attr.attr_id:
                print(f"  • {attr.attr_name} (ID {attr.attr_id})")
            else:
                print(f"  • {attr.attr_name}: {attr.attr_value}")

    # Vehicle types
    vehicle_types = app.vehicle_types.all()
    if vehicle_types:
        print(f"\nVehicle Types ({vehicle_types.count()}):")
        for vt in vehicle_types.order_by('idx'):
            print(f"  • Vehicle Type ID: {vt.vehicle_type_id}")

    print(f"\n{'=' * 70}\n")

    return app


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python verify_aces_integrity.py <source_file_path>")
        print("   or: python verify_aces_integrity.py <source_file_path> <app_id>")
        sys.exit(1)

    source_file = sys.argv[1]

    if len(sys.argv) == 3:
        # Verify specific application
        app_id = int(sys.argv[2])
        verify_application_completeness(app_id, source_file)
    else:
        # Verify entire file
        verify_aces_integrity(source_file, verbose=True)