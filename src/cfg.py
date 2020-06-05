from typing import List
from ast import AST, stmt
from src.models.basic_block import BasicBlock


class CFG:
    def __init__(self, ast_nodes: List[AST]):
        self.ast_nodes = ast_nodes
        self.basic_blocks = self._build_all_basic_blocks(self.ast_nodes)

    @staticmethod
    def _extract_new_blocks(exit_or_entrance: AST) -> List[List[stmt]]:
        new_blocks: List[List[stmt]] = []
        if (
            hasattr(exit_or_entrance, "body")
            and len(exit_or_entrance.body) > 0
        ):
            new_blocks.append(exit_or_entrance.body)
        if (
            hasattr(exit_or_entrance, "orelse")
            and len(exit_or_entrance.orelse) > 0
        ):
            new_blocks.append(exit_or_entrance.orelse)
        if (
            hasattr(exit_or_entrance, "finalbody")
            and len(exit_or_entrance.finalbody) > 0
        ):
            new_blocks.append(exit_or_entrance.finalbody)
        if (
            hasattr(exit_or_entrance, "handlers")
            and len(exit_or_entrance.handlers) > 0
        ):
            new_blocks.append(exit_or_entrance.handlers)
        if len(new_blocks) == 0:
            new_blocks.append(exit_or_entrance)
        return new_blocks

    @staticmethod
    def _build_all_basic_blocks(ast_nodes: List[AST]) -> List[BasicBlock]:
        basic_blocks: List[BasicBlock] = []
        remaining_nodes = ast_nodes
        while len(remaining_nodes) > 0:
            new_block, remaining_nodes = BasicBlock.build_first_from_ast(
                remaining_nodes
            )
            if len(new_block.body) > 0:
                basic_blocks.append(new_block)
            if len(remaining_nodes) > 0:
                new_blocks = CFG._extract_new_blocks(remaining_nodes[0])
                for block in new_blocks:
                    basic_blocks += CFG._build_all_basic_blocks(block)
            remaining_nodes = remaining_nodes[1:]
        return basic_blocks
