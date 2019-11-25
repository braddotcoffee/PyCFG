from typing import List
from ast import AST, stmt


class BasicBlock:
    @staticmethod
    def _validate_ast_nodes(ast: List[AST]):
        """
        Ensure that ast_node is a statement (stmt)

        :param ast_node (AST): Any AST node

        :raise: ValueError if ast_node is not a subclass of stmt
        """
        for ast_node in ast:
            if not isinstance(ast_node, stmt):
                raise ValueError("Invalid AST node provided")

    @staticmethod
    def build_from_ast(ast: List[stmt]) -> "BasicBlock":
        """
        Builds a single basic block from its AST

        :param ast (AST): AST to build BasicBlock from

        :returns: A new BasicBlock

        :raise: ValueError if ast not a list of stmt
        """
        BasicBlock._validate_ast_nodes(ast)

        return BasicBlock()
