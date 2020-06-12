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
        Try,
        ExceptHandler,
    }
    _next_id = 0

    def __init__(
        self,
        body: List[AST] = None,
        inbound: List["BasicBlock"] = None,
        outbound: List["BasicBlock"] = None,
    ):
        self.identifier = BasicBlock._next_id
        BasicBlock._next_id += 1
        self.body = body if body is not None else list()
        self.inbound = inbound if inbound is not None else list()
        self.outbound = outbound if outbound is not None else list()

    def __hash__(self):
        return self.identifier

    @lazy
    def function_calls(self):
        """
        All of the function calls which are a part of this BasicBlock
        """
        return list(
            filter(lambda ast_node: isinstance(ast_node, Call), self.body)
        )

    @staticmethod
    def _validate_ast_node(ast: List[any]) -> List[AST]:
        """
        Ensure that ast_node is a statement (stmt)

        :param ast_node (AST): Any AST node

        :raise: ValueError if ast_node is not a subclass of stmt
        """
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
        """
        Builds the first basic block from its AST

        :param ast (AST): AST to build BasicBlock from

        :returns: A new BasicBlock

        :raise: ValueError if ast not a list of stmt
        """
        ast = BasicBlock._validate_ast_node(ast)
        body, remaining_nodes = BasicBlock._build_body(ast)

        return BasicBlock(body=body), remaining_nodes
