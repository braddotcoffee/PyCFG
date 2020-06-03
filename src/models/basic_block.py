from typing import List, Union, Tuple
from ast import (
    AST,
    expr,
    stmt,
    Call,
    Expr,
    AsyncFunctionDef,
    ClassDef,
    FunctionDef,
    Return,
    For,
    While,
    If,
)
from lazy import lazy

BasicBlockASTNode = Union[expr, stmt]


class BasicBlock:
    """
    A BasicBlock encapsulates a straight line code sequence

    :param body (List[AST]): AST nodes which make up the BasicBlock

    :param inbound (List[BasicBlock]): BasicBlocks which call this one

    :param outbound (List[BasicBlock]): BasicBlocks which this one may call
    """

    invalid_ast_nodes = {
        FunctionDef,
        AsyncFunctionDef,
        ClassDef,
        Return,
        For,
        While,
        If,
    }

    def __init__(
        self,
        body: List[AST] = None,
        inbound: List["BasicBlock"] = None,
        outbound: List["BasicBlock"] = None,
    ):
        self.body = body if body is not None else list()
        self.inbound = inbound if inbound is not None else list()
        self.outbound = outbound if outbound is not None else list()

    @lazy
    def function_calls(self):
        """
        All of the function calls which are a part of this BasicBlock
        """
        return list(
            filter(lambda ast_node: isinstance(ast_node, Call), self.body)
        )

    @staticmethod
    def _validate_ast_node(ast: List[AST]) -> List[BasicBlockASTNode]:
        """
        Ensure that ast_node is a statement (stmt)

        :param ast_node (AST): Any AST node

        :raise: ValueError if ast_node is not a subclass of stmt
        """
        for ast_node in ast:
            if not isinstance(ast_node, expr) and not isinstance(
                ast_node, stmt
            ):
                raise ValueError("Invalid AST node provided")
        return ast

    @staticmethod
    def _build_body(
        ast: List[BasicBlockASTNode],
    ) -> Tuple[List[BasicBlockASTNode], List[BasicBlockASTNode]]:
        """
        Build body of first basic block within list of expr or stmt nodes
        """
        body: List[Union[expr, stmt]] = []
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
    ) -> Tuple["BasicBlock", List[BasicBlockASTNode]]:
        """
        Builds the first basic block from its AST

        :param ast (AST): AST to build BasicBlock from

        :returns: A new BasicBlock

        :raise: ValueError if ast not a list of stmt
        """
        ast = BasicBlock._validate_ast_node(ast)
        body, remaining_nodes = BasicBlock._build_body(ast)

        return BasicBlock(body=body), remaining_nodes
