"""
name:Persephone
class:311
assignment:lab7
date:10/7/2026
"""

"""
Lab 7: The Collision Resolver -- starter.

Complete the three classes below. See
Lab_07_The_Collision_Resolver.md, Part B, for the full requirements.
"""

from typing import Generic, Hashable, List, Optional, Tuple, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")

_TOMBSTONE = object()  # sentinel marking a deleted open-addressing slot


class _ChainNode(Generic[K, V]):
    __slots__ = ("key", "value", "next")

    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value
        self.next: Optional["_ChainNode[K, V]"] = None


class ChainedHashMap(Generic[K, V]):
    """Separate chaining: each bucket is a linked list of (key, value)."""

    def __init__(self, initial_size: int = 16) -> None:
        self._buckets: List[Optional[_ChainNode[K, V]]] = [None] * initial_size
        self._count = 0

    def __len__(self) -> int:
        return self._count

    def insert(self, key: K, value: V) -> None:
        """Insert, or update in place if `key` already exists. Resize (double + rehash) once load factor > 0.75."""
        # TODO
        next_load = (self._count + 1) / len(self._buckets)
        if next_load > 0.75:
            old_buckets: List[Optional[_ChainNode[K, V]]] = self._buckets
            self._buckets = [None] * (2 * len(old_buckets))
            self._count = 0
            for i in range(len(old_buckets)):
                while i.key is not None:
                    self.insert(i.key,i.value)
                    i = i.next
        index = hash(key) % len(self._buckets)
        node = self._buckets[index]
        while node is not None:
            if node.key == key:
                self._buckets[node] = [key,value]
                return
            node = node.next
        new_node = _ChainNode(key, value)
        new_node.next = self._buckets[index]
        self._buckets[index] = new_node
        self._count += 1
        #raise NotImplementedError

    def get(self, key: K) -> V:
        """Return the value for `key`. Raise KeyError if missing."""
        # TODO
        index = hash(key) % len(self._buckets)
        node = self._buckets[index]
        while node is not None:
            if node.key == key: return node.value
            node = node.next
        raise KeyError(key)
        #raise NotImplementedError

    def delete(self, key: K) -> None:
        """Remove `key`. Raise KeyError if missing."""
        # TODO
        index = hash(key) % len(self._buckets)
        node = self._buckets[index]
        while node is not None:
            if node.key == key:
                self._buckets[node] = None
                self._count -= 1
                return
            node = node.next
        raise KeyError(key)
        #raise NotImplementedError


class LinearProbingHashMap(Generic[K, V]):
    """Open addressing with linear probing and tombstone deletion."""

    def __init__(self, initial_size: int = 16) -> None:
        self._keys: List[object] = [None] * initial_size
        self._values: List[Optional[V]] = [None] * initial_size
        self._count = 0

    def __len__(self) -> int:
        return self._count

    def insert(self, key: K, value: V) -> None:
        """Resize (double + rehash) once load factor > 0.7."""
        # TODO
        next_load = (self._count + 1) / len(self._keys)
        if next_load > 0.7:
            old_keys = self._keys
            old_values = self._values
            self._keys = [None] * (2 * len(old_keys))
            self._values = [None] * (2 * len(old_values))
            self._count = 0
            for i in range(len(old_keys)):
                self.insert(old_keys[i],old_values[i])
        home = hash(key) % len(self._keys)
        for offset in range(len(self._keys)):
            slot = (home + offset) % len(self._keys)
            curr_key = self._keys[slot]
            if curr_key is None:
                self._keys[slot] = key
                self._values[slot] = value
                self._count += 1
                return 
            if curr_key ==_TOMBSTONE:
                self._keys[slot] = key
                self._values[slot] = value
                self._count += 1
                return
            if curr_key == key:
                self._values[slot] = value
                return
        #raise NotImplementedError

    def search(self, key: K) -> V:
        """Return the value for `key`. Raise KeyError if missing."""
        # TODO
        home = hash(key) % len(self._keys)
        for offset in range(len(self._keys)):
            slot = (home + offset) % len(self._keys)
            if _keys(slot) == key:
                return _values(slot)
        raise KeyError(key)
        #raise NotImplementedError

    def delete(self, key: K) -> None:
        """Remove `key` using a tombstone (not None) so later probes don't stop early. Raise KeyError if missing."""
        # TODO
        home = hash(key) % len(self._keys)
        for offset in range(len(self._keys)):
            slot = (home + offset) % len(self._keys)
            if _keys(slot) == key:
                self._keys[slot] = _TOMBSTONE
                self._values[slot] = None
                self._count -= 1
        raise KeyError(key)
        #raise NotImplementedError


class QuadraticProbingHashMap(Generic[K, V]):
    """
    Open addressing with quadratic probing and tombstone deletion.

    Pitfall to design around: with a power-of-2 table size, the probe
    sequence (idx + i^2) mod size does NOT reach every slot -- it can
    cycle through only about half of them, so the table can appear
    "full" and raise/loop forever even though empty slots exist
    elsewhere. Two standard fixes, pick one:
      (a) use a PRIME table size (so the quadratic sequence covers all
          slots whenever load factor < 1), or
      (b) resize proactively -- check load factor BEFORE attempting an
          insert's probe sequence, not only after a successful insert.
    Using both is safest.
    """

    def __init__(self, initial_size: int = 17) -> None:
        self._keys: List[object] = [None] * initial_size
        self._values: List[Optional[V]] = [None] * initial_size
        self._count = 0

    def __len__(self) -> int:
        return self._count

    def insert(self, key: K, value: V) -> None:
        """Resize (grow + rehash) once load factor > 0.7 -- see the pitfall note above."""
        # TODO
        next_load = (self._count + 1) / len(self._keys)
        if next_load > 0.7:
            old_keys = self._keys
            old_values = self._values
            self._keys = [None] * (2 * len(old_keys))
            self._values = [None] * (2 * len(old_values))
            self._count = 0
            for i in range(len(old_keys)):
                self.insert(old_keys[i],old_values[i])
        home = hash(key) % len(self._keys)
        for offset in range(len(self._keys)):
            slot = (home + offset) % len(self._keys)
            curr_key = self._keys[slot]
            if curr_key is None:
                self._keys[slot] = key
                self._values[slot] = value
                self._count += 1
                return 
            if curr_key ==_TOMBSTONE:
                self._keys[slot] = key
                self._values[slot] = value
                self._count += 1
                return
            if curr_key == key:
                self._values[slot] = value
                return
        #raise NotImplementedError
        #raise NotImplementedError

    def search(self, key: K) -> V:
        """Return the value for `key`. Raise KeyError if missing."""
        # TODO
        home = hash(key) % len(self._keys)
        for offset in range(len(self._keys)):
            slot = (home + offset * offset) % len(self._keys)
            if _keys(slot) == key:
                return _values(slot)
        raise KeyError(key)
        #raise NotImplementedError

    def delete(self, key: K) -> None:
        """Remove `key` using a tombstone. Raise KeyError if missing."""
        # TODO
        home = hash(key) % len(self._keys)
        for offset in range(len(self._keys)):
            slot = (home + offset * offset) % len(self._keys)
            if _keys(slot) == key:
                self._keys[slot] = _TOMBSTONE
                self._values[slot] = none
                self._count -= 1
        raise KeyError(key)
        #raise NotImplementedError
