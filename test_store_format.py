import great_expectations as gx
from datetime import datetime

context = gx.get_context(mode="file")

# Check what the validation results store expects
store = context.stores.get("validation_results_store")
print(f"Store class: {type(store)}")
print(f"Store backend: {type(store.store_backend)}")
print(f"Backend config: {store.store_backend.config}")

# Try to understand the key structure
from great_expectations.data_context.types.resource_identifiers import (
    ValidationResultIdentifier,
    ExpectationSuiteIdentifier
)

# Create a simple validation result identifier
run_id = gx.RunIdentifier(run_name="test-run-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
suite_id = ExpectationSuiteIdentifier("customer_validation_suite")

vr_id = ValidationResultIdentifier(
    expectation_suite_identifier=suite_id,
    run_id=run_id,
    batch_identifier="test_batch"
)

print(f"\nValidation Result Identifier:")
print(f"  to_tuple(): {vr_id.to_tuple()}")

# Try using store.set properly
print("\n\nAttempting to store a validation result...")
# We need an actual validation result - let's create a minimal one
sample_result = {
    "success": True,
    "results": [],
    "statistics": {"evaluated_expectations": 0, "successful_expectations": 0, "unsuccessful_expectations": 0, "success_percent": 100.0},
    "meta": {"run_id": run_id.to_json_dict()}
}

try:
    store.set(key=vr_id, value=sample_result)
    print(f"✓ Successfully stored validation result!")
    
    # Check if file was created
    import os
    val_dir = "/Users/raghualapati/workspace/ge1/gx/uncommitted/validations"
    files = []
    for root, dirs, filenames in os.walk(val_dir):
        for f in filenames:
            if f.endswith('.json'):
                files.append(os.path.join(root, f))
    
    print(f"\nValidation result files found: {len(files)}")
    for f in files[:3]:
        print(f"  - {f}")
        
except Exception as e:
    print(f"✗ Error storing: {e}")
    import traceback
    traceback.print_exc()
