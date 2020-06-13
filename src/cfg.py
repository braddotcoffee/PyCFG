from typing import List
from ast import AST, stmt
from src.models.basic_block import BasicBlock
from src.models.equivalence_classes import EquivalenceClasses


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
    def _extract_new_ast_nodes(exit_or_entrance: AST,) -> List[List[stmt]]:
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
        if len(new_blocks) == 0:
            new_blocks.append(exit_or_entrance)
        return new_blocks

    def _connect_if_disconnected(
        self, source: int, destination: int,
    ):
        if source not in self.equivalence_classes:
            self.equivalence_classes.add(source)
        if destination not in self.equivalence_classes:
            self.equivalence_classes.add(destination)

        if self.equivalence_classes.find(
            source
        ) != self.equivalence_classes.find(destination):
            self.equivalence_classes.connect(
                source, destination,
            )

    def _build_all_basic_blocks(
        self, ast_nodes: List[AST],
    ) -> List[BasicBlock]:
        basic_blocks: List[BasicBlock] = []
        (new_block, remaining_nodes,) = BasicBlock.build_first_from_ast(
            ast_nodes
        )

        if len(new_block.body) > 0:
            basic_blocks.append(new_block)
            self.equivalence_classes.add(new_block.identifier)
        if len(remaining_nodes) == 0:
            return basic_blocks

        # Build basic blocks for nested control flow
        nested_nodes = CFG._extract_new_ast_nodes(remaining_nodes[0])
        remaining_nodes = remaining_nodes[1:]
        nested_blocks: List[BasicBlock] = []
        for nested_block_nodes in nested_nodes:
            nested_blocks += self._build_all_basic_blocks(nested_block_nodes)
        unnested_blocks = self._build_all_basic_blocks(remaining_nodes)
        for i, nested_block in enumerate(nested_blocks):
            self._connect_if_disconnected(
                new_block.identifier, nested_block.identifier,
            )
            if len(unnested_blocks) > 0:
                self._connect_if_disconnected(
                    unnested_blocks[0].identifier, nested_block.identifier,
                )
            for j in range(i + 1, len(nested_blocks)):
                self._connect_if_disconnected(
                    nested_block.identifier, nested_blocks[j].identifier
                )
        basic_blocks += nested_blocks + unnested_blocks

        # Connect current block to the first block
        if new_block.identifier in self.equivalence_classes:
            self.equivalence_classes.connect(
                new_block.identifier, nested_blocks[0].identifier,
            )
        return basic_blocks
