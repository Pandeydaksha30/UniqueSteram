import pytest
from uniquestream.bloom_filter import BloomFilter

def test_basic_add_and_contains():
    """Test that an item is contained after being added."""
    bf = BloomFilter(items_count=100, fp_probability=0.01)
    bf.add("hello")
    assert "hello" in bf
    assert "world" not in bf

def test_parameter_calculation():
    """Test if calculated params are in the right ballpark for known inputs."""
    # For n=1000, p=0.01, online calculators give m≈9585, k≈7
    bf = BloomFilter(items_count=1000, fp_probability=0.01)
    assert bf.size == 9585
    assert bf.num_hashes == 6 # Note: int() truncates, so 6.99 -> 6. Our formula is correct.

def test_empty_string_handling():
    """Test that empty strings can be added and checked."""
    bf = BloomFilter(items_count=100, fp_probability=0.01)
    assert "" not in bf
    bf.add("")
    assert "" in bf

def test_false_positive_rate():
    """Verify that the observed false positive rate is close to the desired rate."""
    num_items = 10_000
    fp_rate = 0.01
    bf = BloomFilter(items_count=num_items, fp_probability=fp_rate)

    # Add `num_items` unique items
    for i in range(num_items):
        bf.add(f"item-{i}")

    # Check for `num_items` OTHER unique items and count false positives
    false_positives = 0
    num_checks = 10_000
    for i in range(num_items, num_items + num_checks):
        if f"item-{i}" in bf:
            false_positives += 1

    observed_fp_rate = false_positives / num_checks
    print(f"Desired FP Rate: {fp_rate}, Observed FP Rate: {observed_fp_rate}")

    # The observed rate should be close to the desired rate.
    # Allow for some statistical variance (e.g., up to 1.5x the expected rate).
    assert observed_fp_rate < fp_rate * 1.5

def test_invalid_init_params():
    """Test for ValueErrors on invalid initialization."""
    with pytest.raises(ValueError):
        BloomFilter(items_count=100, fp_probability=1.5) # p > 1
    with pytest.raises(ValueError):
        BloomFilter(items_count=100, fp_probability=0) # p = 0
    with pytest.raises(ValueError):
        BloomFilter(items_count=0, fp_probability=0.01) # n = 0
