from typing import List
from ast import AST, stmt
from src.models.basic_block import BasicBlock
from _ast import While


class CFG:
    def __init__(self, ast_nodes: List[AST]):
        self.ast_nodes = ast_nodes
        self.basic_blocks = self._build_all_basic_blocks(self.ast_nodes)

    @staticmethod
    def _extract_statements(exit_or_entrance: AST) -> List[stmt]:
        if isinstance(exit_or_entrance, While):
            return exit_or_entrance.body
        return [exit_or_entrance]

    @staticmethod
    def _build_all_basic_blocks(ast_nodes: List[AST]) -> List[BasicBlock]:
        basic_blocks: List[BasicBlock] = []
        remaining_nodes = ast_nodes
        while len(remaining_nodes) > 0:
            new_block, remaining_nodes = BasicBlock.build_first_from_ast(
                remaining_nodes
            )
            basic_blocks.append(new_block)
            if len(remaining_nodes) > 0:
                basic_blocks += CFG._build_all_basic_blocks(
                    CFG._extract_statements(remaining_nodes[0])
                )
            remaining_nodes = remaining_nodes[1:]
        return basic_blocks
