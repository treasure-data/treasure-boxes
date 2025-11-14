"""
Test script for CJO Profile Viewer

This script tests the core functionality of the application without the Streamlit interface.
"""

import json
import pandas as pd
from column_mapper import CJOColumnMapper
from flowchart_generator import CJOFlowchartGenerator


def test_components():
    """Test the core components of the application."""
    print("Testing CJO Profile Viewer Components...")

    # Load test data
    try:
        print("\n1. Loading test data...")
        with open('/Users/wei.chen/Documents/td/cjo/211205_journey.json', 'r') as f:
            api_response = json.load(f)
        print(f"   ✓ API response loaded - Journey: {api_response['data']['attributes']['name']}")

        profile_data = pd.read_csv('/Users/wei.chen/Documents/td/cjo/profiles.csv')
        print(f"   ✓ Profile data loaded - Shape: {profile_data.shape}")
        print(f"   ✓ Columns: {len(profile_data.columns)} total")

    except Exception as e:
        print(f"   ✗ Error loading data: {e}")
        return False

    # Test Column Mapper
    try:
        print("\n2. Testing Column Mapper...")
        column_mapper = CJOColumnMapper(api_response)
        print("   ✓ Column mapper initialized")

        # Test some column mappings
        test_columns = [
            'cdp_customer_id',
            'intime_journey',
            'intime_stage_0',
            'intime_stage_0_milestone'
        ]

        # Add actual columns from the data
        actual_columns = [col for col in profile_data.columns if col.startswith('intime_stage_0_')][:5]
        test_columns.extend(actual_columns)

        mappings = column_mapper.get_all_column_mappings(test_columns)
        print(f"   ✓ Mapped {len(mappings)} columns")

        for col, display in list(mappings.items())[:5]:
            print(f"     {col} -> {display}")

    except Exception as e:
        print(f"   ✗ Error in column mapper: {e}")
        return False

    # Test Flowchart Generator
    try:
        print("\n3. Testing Flowchart Generator...")
        generator = CJOFlowchartGenerator(api_response, profile_data)
        print("   ✓ Flowchart generator initialized")

        summary = generator.get_journey_summary()
        print(f"   ✓ Journey summary: {summary['journey_name']}")
        print(f"     - Total profiles: {summary['total_profiles']}")
        print(f"     - Journey entries: {summary['journey_entry_count']}")
        print(f"     - Stages: {summary['stage_count']}")

        # Test stage counts
        stage_counts = summary['stage_counts']
        print(f"   ✓ Stage profile counts:")
        for stage_idx, count in stage_counts.items():
            stage_name = generator.stages[stage_idx].name if stage_idx < len(generator.stages) else f"Stage {stage_idx}"
            print(f"     - {stage_name}: {count} profiles")

    except Exception as e:
        print(f"   ✗ Error in flowchart generator: {e}")
        return False

    # Test profile retrieval
    try:
        print("\n4. Testing profile retrieval...")

        # Test with a sample step column
        sample_columns = [col for col in profile_data.columns if col.startswith('intime_stage_0_') and profile_data[col].notna().sum() > 0]

        if sample_columns:
            test_column = sample_columns[0]
            profiles = generator.get_profiles_in_step(test_column)
            print(f"   ✓ Retrieved {len(profiles)} profiles for column: {test_column}")

            if profiles:
                print(f"     Sample profiles: {profiles[:3]}...")
        else:
            print("   ! No suitable test columns found with profile data")

    except Exception as e:
        print(f"   ✗ Error in profile retrieval: {e}")
        return False

    # Test data analysis
    try:
        print("\n5. Analyzing journey structure...")

        journey_stages = api_response['data']['attributes']['journeyStages']
        print(f"   ✓ Journey has {len(journey_stages)} stages")

        for i, stage in enumerate(journey_stages):
            stage_name = stage['name']
            step_count = len(stage.get('steps', {}))
            print(f"     Stage {i}: {stage_name} ({step_count} steps)")

            # Analyze step types
            step_types = {}
            for step_id, step_data in stage.get('steps', {}).items():
                step_type = step_data.get('type', 'Unknown')
                step_types[step_type] = step_types.get(step_type, 0) + 1

            for step_type, count in step_types.items():
                print(f"       - {step_type}: {count}")

    except Exception as e:
        print(f"   ✗ Error in journey analysis: {e}")
        return False

    print("\n✅ All tests passed! The application should work correctly.")
    return True


def analyze_profile_data():
    """Analyze the profile data to understand its structure."""
    print("\n6. Analyzing profile data structure...")

    try:
        profile_data = pd.read_csv('/Users/wei.chen/Documents/td/cjo/profiles.csv')

        # Analyze column patterns
        column_patterns = {
            'journey': [col for col in profile_data.columns if 'journey' in col],
            'stage': [col for col in profile_data.columns if col.startswith('intime_stage_') or col.startswith('outtime_stage_')],
            'milestone': [col for col in profile_data.columns if 'milestone' in col],
            'other': [col for col in profile_data.columns if not any(pattern in col for pattern in ['journey', 'stage', 'milestone'])]
        }

        for pattern, columns in column_patterns.items():
            print(f"   {pattern.title()} columns ({len(columns)}):")
            if columns:
                for col in columns[:5]:  # Show first 5
                    non_null_count = profile_data[col].notna().sum()
                    print(f"     - {col}: {non_null_count} profiles")
                if len(columns) > 5:
                    print(f"     ... and {len(columns) - 5} more")

        # Profile data summary
        total_profiles = len(profile_data)
        journey_entries = profile_data['intime_journey'].notna().sum() if 'intime_journey' in profile_data.columns else 0

        print(f"\n   Summary:")
        print(f"   - Total rows: {total_profiles}")
        print(f"   - Journey entries: {journey_entries}")
        print(f"   - Data completion rate: {journey_entries/total_profiles*100:.1f}%")

    except Exception as e:
        print(f"   ✗ Error analyzing profile data: {e}")


if __name__ == "__main__":
    success = test_components()
    analyze_profile_data()

    if success:
        print("\n🚀 Ready to run the Streamlit app!")
        print("   Run: streamlit run streamlit_app.py")
    else:
        print("\n❌ Issues found. Please fix the errors before running the app.")