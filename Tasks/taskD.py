from collections import deque, defaultdict
from itertools import chain, combinations

from typing import List, Tuple, Optional, Set, Dict


def read_input(*types_list, input_file_name: str = "input.txt") -> tuple:
    def _format_input(line: str, expected_type):
        line = line.strip()
        if expected_type == int:
            return int(line)

        elif expected_type == list[int]:
            return list(map(int, line.split()))

    try:
        with open(input_file_name, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = [input() for _ in types_list]

    return tuple(
        _format_input(line, expected_type)
        for line, expected_type in zip(lines, types_list)
    )


def write_output(output_data, output_file_name: str = "output.txt") -> None:
    formatted_output = " ".join(map(str, output_data))

    with open(output_file_name, "w") as f:
        f.write(formatted_output)

    print(formatted_output)


class TreeNode:
    def __init__(self, list_state: List[int], choices: List[int]):
        self.list_state = list_state
        self.choices = choices
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None
        self.is_odd_node = len(choices) % 2 != 0


def build_tree_and_group_levels(
    n: int, list_state: List[int]
) -> Tuple[TreeNode, Dict[int, List[TreeNode]], Dict[TreeNode, TreeNode]]:
    level_nodes = defaultdict(list)
    parent_map: Dict[TreeNode, TreeNode] = {}

    queue = deque([(list_state, [], 0, None)])  # (state, choices, level, parent)
    root = None

    while queue:
        state, choices, level, parent = queue.popleft()
        node = TreeNode(state, choices)

        if root is None:
            root = node

        level_nodes[level].append(node)

        if parent:
            parent_map[node] = parent

        if len(state) > 1:
            tail, head = state[1:], state[:-1]
            left_choices, right_choices = choices + [state[0]], choices + [state[-1]]

            node.left = TreeNode(tail, left_choices)
            node.right = TreeNode(head, right_choices)

            queue.append((tail, left_choices, level + 1, node))
            queue.append((head, right_choices, level + 1, node))

    return root, level_nodes, parent_map


def calculate_subset_sums(choices: List[int]) -> Set[int]:
    return {
        sum(subset)
        for subset in chain.from_iterable(
            combinations(choices, r) for r in range(1, len(choices) + 1)
        )
    }


def add_solution(solution_set: Set[int], nodes: List[TreeNode]) -> None:
    for node in nodes:
        if not node:
            continue
        formatted_solution = node.choices[::2]
        all_sums = calculate_subset_sums(formatted_solution)
        if all(1 <= x <= 49 for x in all_sums):
            solution_set.update(all_sums)


def is_valid_solution(node: TreeNode) -> bool:
    if not node:
        return False

    formatted_solution = node.choices[::2]
    return any(
        1 <= sum(comb) <= 49
        for comb in chain.from_iterable(
            combinations(formatted_solution, r)
            for r in range(1, len(formatted_solution) + 1)
        )
    )


def find_solutions(input_data: Tuple[int, List[int]]) -> List[int]:
    n, coins = input_data
    if n < 3:
        return coins[:1]

    root, level_nodes, parent_map = build_tree_and_group_levels(n, coins)
    solution_set = set()

    for branch in [root.left, root.right]:
        if is_valid_solution(branch):
            add_solution(solution_set, [branch])

    for level, nodes in level_nodes.items():
        odd_length_nodes = [node for node in nodes if node.is_odd_node]
        grandchild_map = defaultdict(list)

        for current_node in odd_length_nodes:
            grandparent = parent_map.get(parent_map.get(current_node, None), None)
            if grandparent:
                grandchild_map[grandparent].append(current_node)

        for grandchildren in grandchild_map.values():
            even_values_map = defaultdict(list)

            for current_node in grandchildren:
                if not is_valid_solution(current_node):
                    continue

                even_values = tuple(current_node.choices[::2])

                for neighbor_node in even_values_map[even_values]:
                    if is_valid_solution(neighbor_node):
                        add_solution(solution_set, [current_node, neighbor_node])

                even_values_map[even_values].append(current_node)

    return sorted(solution_set)


if __name__ == "__main__":
    input_data = read_input(int, list[int])
    output_data = find_solutions(input_data)
    write_output(output_data)
