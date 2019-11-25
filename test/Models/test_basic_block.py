import unittest
from src.models.basic_block import BasicBlock
from ast import Expr, BoolOp


class TestBasicBlockFromAst(unittest.TestCase):
    def test_build_returns_BasicBlock(self):
        sample_ast = [Expr()]
        basic_block = BasicBlock.build_from_ast(sample_ast)
        self.assertIsInstance(basic_block, BasicBlock)

    def test_build_errors_with_incorrect_node(self):
        sample_ast = [None]
        with self.assertRaises(ValueError):
            BasicBlock.build_from_ast(sample_ast)

        sample_ast = [BoolOp()]
        with self.assertRaises(ValueError):
            BasicBlock.build_from_ast(sample_ast)
