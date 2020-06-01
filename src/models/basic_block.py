from typing import List, Union
from ast import AST, expr, stmt, Call, Expr
from lazy import lazy


class BasicBlock:
    """
    A BasicBlock encapsulates a straight line code sequence

    :param body (List[AST]): AST nodes which make up the BasicBlock

    :param inbound (List[BasicBlock]): BasicBlocks which call this one

    :param outbound (List[BasicBlock]): BasicBlocks which this one may call
    """

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
    def _validate_ast_node(ast: List[AST]) -> List[Union[expr, stmt]]:
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
    def _build_body(ast: List[Union[expr, stmt]]):
        body = []
        for ast_node in ast:
            if isinstance(ast_node, Expr):
                body.append(ast_node.value)
            else:
                body.append(ast_node)
        return body

    @staticmethod
    def build_from_ast(ast: List[AST]) -> "BasicBlock":
        """
        Builds a single basic block from its AST

        :param ast (AST): AST to build BasicBlock from

        :returns: A new BasicBlock

        :raise: ValueError if ast not a list of stmt
        """
        ast = BasicBlock._validate_ast_node(ast)
        body = BasicBlock._build_body(ast)

        return BasicBlock(body=body)
