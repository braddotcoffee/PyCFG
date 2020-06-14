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
        """Validate that an AST node has a valid body under
        the given attribute name

        Args:
            node (AST): AST node to check for statments under attribute name
            attribute (str): Name of attribute to look for

        Returns:
            bool: True if the attribute contains statements
        """
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
        """Connect two identifiers together
        if they are not already

        Args:
            source (int): Identifier of source
            destination (int): Identifier of destination
        """
        if source not in self.equivalence_classes:
            return

        if self.equivalence_classes.find(
            source
        ) != self.equivalence_classes.find(destination):
            self.equivalence_classes.connect(
                source, destination,
            )

    def _link_try_except_finally(
        self, source_idx: int, nested_blocks: List[BasicBlock]
    ):
        """Link try/except/finally bodies together as
        try -> except, try -> finally, except -> finally

        Args:
            source_idx (int): Index of the source block to link
            nested_blocks (List[BasicBlock]): List of all blocks in
            the Try
        """
        for i in range(source_idx + 1, len(nested_blocks)):
            self._connect_if_disconnected(
                nested_blocks[source_idx].identifier,
                nested_blocks[i].identifier,
            )

    def _link_nested_blocks(
        self,
        previous_block: BasicBlock,
        nested_blocks: List[BasicBlock],
        next_blocks: List[BasicBlock],
        ast_node: AST,
    ):
        """Link together the basic blocks that are part of nested control flow
        to the previous unnested block and the next unnested block

        Args:
            previous_block (BasicBlock): Block that nested control flow
            transitions from
            nested_blocks (List[BasicBlock]): Blocks that are part of nested
            control flow (if/else bodies, etc)
            next_blocks (List[BasicBlock]): The next blocks that are part of
            the same nesting level as previous_block
            ast_node (AST): The AST entrance node that was responsible for
            the nested blocks (If, Try, etc.)
        """
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

    def _build_nested_blocks(self, entrance_node: AST) -> List[BasicBlock]:
        """Build the basic blocks nested below the given entrance node

        Args:
            entrance_node (AST): AST node that signifies the start
            of a new basic block

        Returns:
            List[BasicBlock]: The basic blocks representing the statements
            embedded within the body attributes of entrance_node
        """
        nested_nodes = CFG._extract_new_ast_nodes(entrance_node)
        nested_blocks: List[BasicBlock] = []
        for nested_block_nodes in nested_nodes:
            nested_blocks += self._build_all_basic_blocks(nested_block_nodes)
        return nested_blocks

    def _build_all_basic_blocks(
        self, ast_nodes: List[AST],
    ) -> List[BasicBlock]:
        """Parse all basic blocks out of the list of nodes

        Args:
            ast_nodes (List[AST]): AST nodes containing statements
            that make up basic blocks

        Returns:
            List[BasicBlock]: All of the basic blocks that are
            formed by the given nodes
        """
        basic_blocks: List[BasicBlock] = []
        new_block, remaining_nodes = BasicBlock.build_first_from_ast(ast_nodes)

        if len(new_block.body) > 0:
            basic_blocks.append(new_block)
            self.equivalence_classes.add(new_block.identifier)
        if len(remaining_nodes) == 0:
            return basic_blocks

        # Entering new basic block
        nested_blocks = self._build_nested_blocks(remaining_nodes[0])
        unnested_blocks = self._build_all_basic_blocks(remaining_nodes[1:])
        self._link_nested_blocks(
            new_block, nested_blocks, unnested_blocks, remaining_nodes[0]
        )
        return basic_blocks + nested_blocks + unnested_blocks
