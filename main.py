from uniquestream.bloom_filter import BloomFilter
from pybloom_live import BloomFilter as ProdBloomFilter

def check_post(filter, post: str):
    """Helper function to check and print the status of a post."""
    print(f'Checking post: "{post}"')
    if post in filter:
        print(" -> Result: Potential Duplicate. Flag for review.\n")
    else:
        print(" -> Result: Unique Content. Approved.\n")

def run_custom_filter_demo():
    """Demonstrates the custom-built Bloom Filter."""
    print("--- 1. UniqueStream Demo (Custom Python Implementation) ---")
    
    # Configure filter for 1 million posts with a 0.1% false positive rate
    expected_posts = 1_000_000
    fp_rate = 0.001
    custom_filter = BloomFilter(items_count=expected_posts, fp_probability=fp_rate)

    print(f"Filter configured for {expected_posts:,} items.")
    print(f"Memory size (m): {custom_filter.size:,} bits")
    print(f"Hash functions (k): {custom_filter.num_hashes}\n")

    # Sample posts
    post1 = "Check out this amazing sunset! #nofilter"
    post2 = "My thoughts on the latest Python features."
    post3_duplicate = "Check out this amazing sunset! #nofilter"
    post4_unique = "Just finished a great workout at the gym."

    # Add initial posts
    print("Adding initial posts to the stream...")
    custom_filter.add(post1)
    custom_filter.add(post2)
    print("-------------------------------------------\n")

    # Check posts for uniqueness
    check_post(custom_filter, post4_unique)
    check_post(custom_filter, post3_duplicate)


def run_production_filter_demo():
    """Demonstrates the production-ready pybloom-live library."""
    print("\n--- 2. UniqueStream Demo (Production-Ready `pybloom-live`) ---")
    
    expected_posts = 1_000_000
    fp_rate = 0.001
    # The library handles the parameters automatically
    prod_filter = ProdBloomFilter(capacity=expected_posts, error_rate=fp_rate)

    print(f"Filter configured for {prod_filter.capacity:,} items with a {prod_filter.error_rate} error rate.")
    print(f"Memory size: {prod_filter.num_bits:,} bits")
    print(f"Hash functions: {prod_filter.num_hashes}\n")

    # Sample posts
    post1 = "Check out this amazing sunset! #nofilter"
    post2 = "My thoughts on the latest Python features."
    post3_duplicate = "Check out this amazing sunset! #nofilter"
    post4_unique = "Just finished a great workout at the gym."

    # The library's `add` method returns True if the item was already present
    prod_filter.add(post1.encode('utf-8')) # Requires bytes
    prod_filter.add(post2.encode('utf-8'))

    # Check posts
    check_post(prod_filter, post4_unique.encode('utf-8'))
    check_post(prod_filter, post3_duplicate.encode('utf-8'))


if __name__ == "__main__":
    run_custom_filter_demo()
    run_production_filter_demo()
