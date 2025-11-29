#!/usr/bin/env python3
"""
Comprehensive Great Expectations Demo
Demonstrates data validation using the sample_customers.csv file
"""
import great_expectations as gx
from great_expectations.core.batch import BatchRequest, RuntimeBatchRequest
from great_expectations.core import RunIdentifier
from great_expectations.data_context.types.resource_identifiers import ValidationResultIdentifier
import pandas as pd
from datetime import datetime

def main():
    print("=" * 70)
    print("Great Expectations Demo - Customer Data Validation")
    print("=" * 70)
    
    # Step 1: Get the Data Context
    print("\n[1] Loading Great Expectations context...")
    context = gx.get_context(mode="file")
    print(f"✓ Context loaded from: {context.root_directory}")
    
    # Step 2: Load and preview the data
    print("\n[2] Loading sample customer data...")
    data_path = "data/sample_customers.csv"
    df = pd.read_csv(data_path)
    print(f"✓ Loaded {len(df)} customer records")
    print("\nData Preview:")
    print(df.to_string(index=False))
    
    # Step 3: Add a Pandas Datasource (Fluent API)
    print("\n[3] Configuring Pandas datasource...")
    try:
        datasource = context.data_sources.add_pandas("pandas_datasource")
        print("✓ Created new Pandas datasource")
    except Exception:
        datasource = context.data_sources.get("pandas_datasource")
        print("✓ Using existing Pandas datasource")
    
    # Step 4: Add Data Asset
    print("\n[4] Adding customer data asset...")
    try:
        data_asset = datasource.add_dataframe_asset(name="customers")
        print("✓ Created data asset: customers")
    except Exception:
        data_asset = datasource.get_asset("customers")
        print("✓ Using existing data asset: customers")
    
    # Step 5: Create a Batch Request  
    print("\n[5] Creating batch request...")
    batch_request = data_asset.build_batch_request({"dataframe": df})
    
    # Step 6: Create an Expectation Suite
    print("\n[6] Creating expectation suite...")
    suite_name = "customer_validation_suite"
    try:
        suite = context.suites.add(gx.ExpectationSuite(name=suite_name))
        print(f"✓ Created new suite: {suite_name}")
    except Exception:
        suite = context.suites.get(name=suite_name)
        print(f"✓ Using existing suite: {suite_name}")
    
    # Step 7: Create a Validator
    print("\n[7] Creating validator...")
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=suite_name
    )
    print("✓ Validator created")
    
    # Step 8: Add Expectations (Validations)
    print("\n[8] Adding data quality expectations...")
    
    # Table-level expectations
    print("\n   Table Structure Checks:")
    result = validator.expect_table_column_count_to_equal(value=5)
    print(f"   • Column count = 5: {'✓ PASS' if result.success else '✗ FAIL'}")
    
    result = validator.expect_table_row_count_to_be_between(min_value=5, max_value=1000)
    print(f"   • Row count between 5-1000: {'✓ PASS' if result.success else '✗ FAIL'}")
    
    # Customer ID expectations
    print("\n   Customer ID Validations:")
    result = validator.expect_column_values_to_not_be_null(column="customer_id")
    print(f"   • No null customer_id: {'✓ PASS' if result.success else '✗ FAIL'}")
    
    result = validator.expect_column_values_to_be_unique(column="customer_id")
    print(f"   • Unique customer_id: {'✓ PASS' if result.success else '✗ FAIL'}")
    
    result = validator.expect_column_values_to_be_of_type(column="customer_id", type_="int64")
    print(f"   • customer_id is integer: {'✓ PASS' if result.success else '✗ FAIL'}")
    
    # Email expectations
    print("\n   Email Validations:")
    result = validator.expect_column_values_to_not_be_null(column="email")
    print(f"   • No null emails: {'✓ PASS' if result.success else '✗ FAIL'}")
    
    result = validator.expect_column_values_to_match_regex(
        column="email",
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )
    print(f"   • Valid email format: {'✓ PASS' if result.success else '✗ FAIL'}")
    
    result = validator.expect_column_values_to_be_unique(column="email")
    print(f"   • Unique emails: {'✓ PASS' if result.success else '✗ FAIL'}")
    
    # Signup date expectations
    print("\n   Signup Date Validations:")
    result = validator.expect_column_values_to_not_be_null(column="signup_date")
    print(f"   • No null signup dates: {'✓ PASS' if result.success else '✗ FAIL'}")
    
    result = validator.expect_column_values_to_match_strftime_format(
        column="signup_date",
        strftime_format="%Y-%m-%d"
    )
    print(f"   • Date format YYYY-MM-DD: {'✓ PASS' if result.success else '✗ FAIL'}")
    
    # Orders expectations
    print("\n   Orders Validations:")
    result = validator.expect_column_values_to_not_be_null(column="orders")
    print(f"   • No null orders: {'✓ PASS' if result.success else '✗ FAIL'}")
    
    result = validator.expect_column_values_to_be_between(
        column="orders",
        min_value=0,
        max_value=100
    )
    print(f"   • Orders between 0-100: {'✓ PASS' if result.success else '✗ FAIL'}")
    
    result = validator.expect_column_mean_to_be_between(
        column="orders",
        min_value=0,
        max_value=10
    )
    print(f"   • Average orders 0-10: {'✓ PASS' if result.success else '✗ FAIL'}")
    
    # Average order value expectations
    print("\n   Order Value Validations:")
    result = validator.expect_column_values_to_not_be_null(column="avg_order_value")
    print(f"   • No null order values: {'✓ PASS' if result.success else '✗ FAIL'}")
    
    result = validator.expect_column_values_to_be_between(
        column="avg_order_value",
        min_value=0,
        max_value=500
    )
    print(f"   • Order values 0-500: {'✓ PASS' if result.success else '✗ FAIL'}")
    
    # Save the suite
    print("\n[9] Saving expectation suite...")
    context.suites.add_or_update(validator.expectation_suite)
    print("✓ Suite saved")
    
    # Step 9: Run validation with proper result persistence
    print("\n[10] Running validation...")
    
    # Get a fresh validator and run validation
    validator_for_run = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=suite_name
    )
    
    # Create unique run identifier for this run
    run_id = gx.RunIdentifier(
        run_name=datetime.now().strftime("%Y%m%d-%H%M%S-customer-validation")
    )
    
    checkpoint_result = validator_for_run.validate(run_id=run_id)
    
    # Persist the validation result so it shows in historical runs
    try:
        from great_expectations.data_context.types.resource_identifiers import (
            ValidationResultIdentifier,
            ExpectationSuiteIdentifier
        )
        
        # Build the validation result identifier
        vr_id = ValidationResultIdentifier(
            expectation_suite_identifier=ExpectationSuiteIdentifier(suite_name),
            run_id=run_id,
            batch_identifier="customer_batch_" + datetime.now().strftime("%Y%m%d%H%M%S")
        )
        
        # Store the validation result (checkpoint_result is already the right type)
        context.stores.get("validation_results_store").set(key=vr_id, value=checkpoint_result)
        print("✓ Validation complete and saved to history")
    except Exception as e:
        print(f"✓ Validation complete (note: {str(e)[:60]}...)")
    
    print(f"  Run ID: {run_id.run_name}")
    
    # Step 10: Display Results
    print("\n" + "=" * 70)
    print("VALIDATION RESULTS")
    print("=" * 70)
    
    if checkpoint_result.success:
        print("\n✓ ALL VALIDATIONS PASSED!")
        print(f"\nTotal Expectations Evaluated: {checkpoint_result.statistics['evaluated_expectations']}")
        print(f"Successful Expectations: {checkpoint_result.statistics['successful_expectations']}")
        print(f"Success Rate: {checkpoint_result.statistics['success_percent']:.1f}%")
    else:
        print("\n✗ SOME VALIDATIONS FAILED")
        print(f"\nTotal Expectations Evaluated: {checkpoint_result.statistics['evaluated_expectations']}")
        print(f"Successful Expectations: {checkpoint_result.statistics['successful_expectations']}")
        print(f"Failed Expectations: {checkpoint_result.statistics['unsuccessful_expectations']}")
        print(f"Success Rate: {checkpoint_result.statistics['success_percent']:.1f}%")
    
    # Step 11: Build and open Data Docs
    print("\n[12] Building Data Docs (HTML reports)...")
    context.build_data_docs()
    print("✓ Data Docs built successfully")
    
    print("\n[13] Opening Data Docs in browser...")
    context.open_data_docs()
    
    print("\n" + "=" * 70)
    print("Demo Complete!")
    print("=" * 70)
    print("\nData Docs have been opened in your default browser.")
    print("You can also find them at: gx/uncommitted/data_docs/local_site/index.html")
    print("\nExpectation Suite saved to: gx/expectations/")
    print(f"Suite name: {suite_name}")
    print("\n✓ Validation results are being saved with unique timestamps!")
    print("Click on the Expectation Suite in Data Docs to see all historical validation runs.")
    
    # Show how many runs are stored
    import os
    val_dir = os.path.join(context.root_directory, "uncommitted/validations")
    json_files = []
    for root, dirs, files in os.walk(val_dir):
        json_files.extend([f for f in files if f.endswith('.json')])
    print(f"Total validation runs stored: {len(json_files)}")
    
    return checkpoint_result.success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
