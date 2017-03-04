from __future__ import division

class BSTError(ValueError):
    pass

class BSTNode(object):
    def __init__(self, val, parent, size):
        self.val = val
        self.parent = parent
        self.size = size
        self.left = None
        self.right = None

    def _get_right_size(self):
        return self.right.size if self.right else 0

    def _get(self, key):
        node = self
        while node and node.val != key:
            node = node.left if node.val > key else node.right

        if not node:
            raise BSTError('Could not find node with key {}'.format(key))

        return node

    def _update_size(self, node):
        while node:
            node.size -= 1
            node = node.parent

    def lower_than(self, n):
        node = self
        count = 0

        while node:
            if node.val < n:
                count += node.size - node._get_right_size()
                node = node.right
            else:
                node = node.left

        return count

    def delete(self, key):
        node = self._get(key)
        self._update_size(node)

    def __str__(self):
        return str(self.val)

    def _display(self):
        return '({}({}):{},{})'.format(
            self.val,
            self.size,
            self.left or '',
            self.right or '',
        )


class Solution(object):
    def reversePairs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if not nums:
            return 0

        sorted_nums = sorted(nums)

        lookup = self.create_bst(sorted_nums, None, 0, len(sorted_nums))

        total = 0
        for n in nums:
            lookup.delete(n)
            # TODO remove float
            total += lookup.lower_than(float(n) / 2)

        return total

    def create_bst(self, nums, parent, start, end):
        size = end - start
        if size == 0:
            return None

        if size == 1:
            return BSTNode(nums[start], parent, 1)

        # TODO undo some optimization so that this makes sense
        half = 1 << size.bit_length() - 1
        quarter = half >> 1
        pivot = start + quarter - 1 + min(size - half + 1, quarter)

        node = BSTNode(nums[pivot], parent, size)
        node.left = self.create_bst(nums, node, start, pivot)
        node.right = self.create_bst(nums, node, pivot + 1, end)

        return node
