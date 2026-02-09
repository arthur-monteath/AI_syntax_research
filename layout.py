def layout_tree(tree, x=0, y=0, level_gap=80, sibling_gap=30):
    positions = {}

    def helper(node, depth, x_offset, y_offset):
        if not node.children:
            positions[node] = (x_offset, y_offset + depth * level_gap)
            return x_offset + sibling_gap

        child_x = x_offset
        child_centers = []

        for child in node.children:
            child_x = helper(child, depth + 1, child_x, y_offset)
            child_centers.append(positions[child][0])

        center_x = sum(child_centers) / len(child_centers)
        positions[node] = (center_x, y_offset + depth * level_gap)
        return child_x

    helper(tree, 0, x, y)
    return positions