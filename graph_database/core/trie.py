from typing import List, Tuple
import bisect

class ObjectId:
    OBJECT_ID_NOT_FOUND = -1

# Trie index
class Trie:
    def __init__(self):
        # Tree levels
        self.prefix_lvl: List[int] = []
        self.data_lvl: List[int] = []

        # Offset indexing
        self.offsets: List[int] = []
        self.data_count: int = 0
        self.last_offset: int = 0

        # Last prefix inserted in the first level during construction
        self.invalid_object_id: int = ObjectId.OBJECT_ID_NOT_FOUND
        self.last_prefix: int = self.invalid_object_id

    # Insert an element into the tree (construction)
    def insert(self, prefix: int, data: int) -> None:
        # Check if prefix is already in the tree
        new_prefix = prefix != self.last_prefix

        # Add new prefix
        if new_prefix:
            # New prefix being inserted
            self.last_prefix = prefix

            # Store prefix
            self.prefix_lvl.append(prefix)

            # Store last offset
            self.offsets.append(self.last_offset + self.data_count)
            self.last_offset += self.data_count
            self.data_count = 0

        # Store data
        self.data_lvl.append(data)
        self.data_count += 1

    # Prepare tree for range queries (after construction)
    def end_inserts(self) -> None:
        # Store last offset
        self.offsets.append(self.last_offset + self.data_count)

    # Range query using a prefix
    def query(self, prefix: int) -> List[int]:
        # Check if prefix exists
        prefix_idx = bisect.bisect_left(self.prefix_lvl, prefix)
        found = prefix_idx != len(self.prefix_lvl) and self.prefix_lvl[prefix_idx] == prefix

        # Return empty iterator if prefix is not in the tree
        if not found:
            return []

        # Return range of results
        return self.data_lvl[self.offsets[prefix_idx]:self.offsets[prefix_idx+1]]

    # Visualize the entire tree
    def print(self) -> None:
        print("Trie: \n")

        # Prefix level
        print("L0: ", end="")
        for prefix in self.prefix_lvl:
            print(f"{prefix},", end="")
        print()

        # Data level
        offset_idx = 1
        print("L1: *", end="")
        for i, data in enumerate(self.data_lvl):
            print(data, end="")
            if i + 1 == self.offsets[offset_idx]:
                offset_idx += 1
                print("*", end="")
            else:
                print(",", end="")
        print("\n")

    # Show offsets in the data level
    def print_offsets(self) -> None:
        # Offsets
        print("Offsets: \n")
        for i, prefix in enumerate(self.prefix_lvl):
            print(f"{prefix}: ({self.offsets[i]},{self.offsets[i+1]})")
        print()