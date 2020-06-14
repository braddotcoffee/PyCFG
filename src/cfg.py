from typing import List
from ast import AST, stmt
from src.models.basic_block import BasicBlock
from src.models.equivalence_classes import EquivalenceClasses
from _ast import Try


class CFG:
    """Class representing the control-flow graph of a program
    """

    def __init__(
        self, ast_nodes: List[AST],
    ):
        """Instantiate Control Flow Graph by parsing list of AST nodes

        Args:
            ast_nodes (List[AST]): AST nodes of program to generate graph for
        """
        self.ast_nodes = ast_nodes
        self.equivalence_classes = EquivalenceClasses()
        self.basic_blocks = self._build_all_basic_blocks(self.ast_nodes)

    @staticmethod
    def _validate_block_attribute(node: AST, attribute: str,) -> bool:
        return hasattr(node, attribute,) and len(getattr(node, attribute,)) > 0

    @staticmethod
    def _extract_new_ast_nodes(exit_or_entrance: AST) -> List[List[stmt]]:
        """Pull body out of AST node representing newe basic block

        Args:
            exit_or_entrance (AST): AST node containing statements that
            make up a new basic block

        Returns:
            List[List[stmt]]: An array of the bodies of each branch
            of the AST Node. Example: try/except/finally will return
            [[try_body], [except_body], [finally_body]]
        """
        new_blocks: List[List[stmt]] = []
        block_attributes = [
            "body",
            "orelse",
            "handlers",
            "finalbody",
        ]

        for attr in block_attributes:
            if CFG._validate_block_attribute(exit_or_entrance, attr,):
                new_blocks.append(getattr(exit_or_entrance, attr,))
        return new_blocks

    def _connect_if_disconnected(
        self, source: int, destination: int,
    ):
        if source not in self.equivalence_classes:
            return

        if self.equivalence_classes.find(
            source
        ) != self.equivalence_classes.find(destination):
            self.equivalence_classes.connect(
                source, destination,
            )

    def _link_try_except_finally(
        self, current_idx: int, nested_blocks: List[BasicBlock]
    ):
        for i in range(current_idx + 1, len(nested_blocks)):
            self._connect_if_disconnected(
                nested_blocks[current_idx].identifier,
                nested_blocks[i].identifier,
            )

    def _link_nested_nodes(
        self,
        previous_block: BasicBlock,
        nested_blocks: List[BasicBlock],
        next_blocks: List[BasicBlock],
        ast_node: AST,
    ):
        for i, nested_block in enumerate(nested_blocks):
            self._connect_if_disconnected(
                previous_block.identifier, nested_block.identifier,
            )
            if len(next_blocks) > 0:
                self._connect_if_disconnected(
                    next_blocks[0].identifier, nested_block.identifier,
                )
            if isinstance(ast_node, Try):
                self._link_try_except_finally(i, nested_blocks)

    def _build_all_basic_blocks(
        self, ast_nodes: List[AST],
    ) -> List[BasicBlock]:
        basic_blocks: List[BasicBlock] = []
        new_block, remaining_nodes = BasicBlock.build_first_from_ast(ast_nodes)

        if len(new_block.body) > 0:
            basic_blocks.append(new_block)
            self.equivalence_classes.add(new_block.identifier)
        if len(remaining_nodes) == 0:
            return basic_blocks

        # Entering new basic block
        entrance_node = remaining_nodes[0]
        nested_nodes = CFG._extract_new_ast_nodes(entrance_node)
        remaining_nodes = remaining_nodes[1:]
        nested_blocks: List[BasicBlock] = []
        for nested_block_nodes in nested_nodes:
            nested_blocks += self._build_all_basic_blocks(nested_block_nodes)
        unnested_blocks = self._build_all_basic_blocks(remaining_nodes)
        self._link_nested_nodes(
            new_block, nested_blocks, unnested_blocks, entrance_node
        )
        basic_blocks += nested_blocks + unnested_blocks

        # Connect current block to the first nested block
        if new_block.identifier in self.equivalence_classes:
            self.equivalence_classes.connect(
                new_block.identifier, nested_blocks[0].identifier,
            )
        return basic_blocks
