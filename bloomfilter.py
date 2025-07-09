
---

### **3. Core Logic Implementation**

#### **`uniquestream/__init__.py`**

This file can be empty. Its presence makes the `uniquestream` directory a Python package.

#### **`uniquestream/bloom_filter.py`**

This is our custom, from-scratch implementation.

```python
import math
import mmh3

class BloomFilter:
    """
    A custom Bloom Filter implementation.

    This class is designed for educational purposes to show the inner workings
    of a Bloom Filter. For production use, a C-optimized library like
    `pybloom-live` is recommended for better performance.
    """

    def __init__(self, items_count: int, fp_probability: float):
        """
        Initializes the Bloom Filter.

        Args:
            items_count (int): The expected number of items to be stored (n).
            fp_probability (float): The desired false positive probability (p), e.g., 0.01 for 1%.
        """
        if not (0 < fp_probability < 1):
            raise ValueError("False positive probability must be between 0 and 1.")
        if not items_count > 0:
            raise ValueError("Items count must be greater than 0.")
        
        # Calculate optimal filter size (m) and hash count (k)
        self._size = self._get_size(items_count, fp_probability)
        self._num_hashes = self._get_hash_count(self._size, items_count)
        
        # The bit array
        self.bit_array = [False] * self._size

    @property
    def size(self):
        """Returns the size of the bit array."""
        return self._size

    @property
    def num_hashes(self):
        """Returns the number of hash functions."""
        return self._num_hashes

    def add(self, item: str):
        """
        Adds an item to the filter.

        The item is hashed multiple times, and the bits at the resulting
        indices in the bit array are set to True.
        """
        for i in range(self._num_hashes):
            # Use different seeds for each hash function
            digest = mmh3.hash(item, i) % self._size
            self.bit_array[digest] = True

    def __contains__(self, item: str) -> bool:
        """
        Checks if an item may be in the set using the `in` operator.

        Returns:
            bool: False if the item is definitely not in the set.
                  True if the item might be in the set (with a given fp_probability).
        """
        for i in range(self._num_hashes):
            digest = mmh3.hash(item, i) % self._size
            if not self.bit_array[digest]:
                # If any bit is False, the item is definitely not present
                return False
        # If all bits are True, the item is possibly present
        return True

    @staticmethod
    def _get_size(n: int, p: float) -> int:
        """
        Calculates the optimal bit array size (m).
        m = - (n * log(p)) / (log(2)^2)
        """
        m = - (n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    @staticmethod
    def _get_hash_count(m: int, n: int) -> int:
        """
        Calculates the optimal number of hash functions (k).
        k = (m/n) * log(2)
        """
        k = (m / n) * math.log(2)
        return int(k)
