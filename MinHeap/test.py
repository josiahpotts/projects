import min_heap

h = min_heap.MinHeap()
da = min_heap.DynamicArray([-25779, 51403, -67454, 45578, -25779, 13625, 99732, 8899])
da1 = min_heap.DynamicArray([-38814, -17011, -98750, 77808, 40471, 77808, -94155, -90608, 20816])

h.build_heap(da1)

print(h)
