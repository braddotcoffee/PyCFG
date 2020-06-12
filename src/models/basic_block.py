from typing import List, Tuple
from ast import (
    AST,
    Call,
    Expr,
    AsyncFunctionDef,
    ClassDef,
    FunctionDef,
    Return,
    For,
    While,
    If,
    Try,
    ExceptHandler,
)
from lazy import lazy


class BasicBlock:
    """A BasicBlock encapsulates a straight line code sequence"""

    invalid_ast_nodes = {
        FunctionDef,
        AsyncFunctionDef,
        ClassDef,
        Return,
        For,
        While,
        If,
        Try,
        ExceptHandler,
    }
    _next_id = 0

    def __init__(
        self, body: List[AST] = None,
    ):
        self.identifier = BasicBlock._next_id
        BasicBlock._next_id += 1
        self.body = body if body is not None else list()

    def __hash__(self):
        return self.identifier

    @lazy
    def function_calls(self) -> List[Call]:
        """All of the function calls which are a part of the body

        Returns:
            (List[Call]): Calls which are a prt of the body
        """
        return list(
            filter(lambda ast_node: isinstance(ast_node, Call), self.body)
        )

    @staticmethod
    def _validate_ast_node(ast: List[any]) -> List[AST]:
        """Ensure that ast_node is an instance of AST"""
        for ast_node in ast:
            if not isinstance(ast_node, AST):
                raise ValueError("Invalid AST node provided")
        return ast

    @staticmethod
    def _build_body(ast: List[AST],) -> Tuple[List[AST], List[AST]]:
        """
        Build body of first basic block within list of expr or stmt nodes
        """
        body: List[AST] = []
        for i, ast_node in enumerate(ast):
            if type(ast_node) in BasicBlock.invalid_ast_nodes:
                return body, ast[i:]
            elif isinstance(ast_node, Expr):
                body.append(ast_node.value)
            else:
                body.append(ast_node)
        return body, []

    @staticmethod
    def build_first_from_ast(
        ast: List[AST],
    ) -> Tuple["BasicBlock", List[AST]]:
        """Builds the first block from its AST

        Args:
            ast (List[AST]): List of AST nodes to parse first basic block from

        Returns:
            Tuple[BasicBlock, List[AST]]: The new basic block and the
            remaining AST nodes to be parsed

        Raises:
            ValueError: If attempting to parse an object that is not
            an instance of AST
        """
        ast = BasicBlock._validate_ast_node(ast)
        body, remaining_nodes = BasicBlock._build_body(ast)

        return BasicBlock(body=body), remaining_nodes
