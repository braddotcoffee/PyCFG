import unittest
from src.models.basic_block import BasicBlock
from ast import Expr, parse, Call, Constant


class TestBasicBlockFromAst(unittest.TestCase):
    def test_build_returns_BasicBlock(self):
        sample_ast = [Expr(Constant())]
        basic_block = BasicBlock.build_from_ast(sample_ast)
        self.assertIsInstance(basic_block, BasicBlock)

    def test_build_errors_with_non_ast(self):
        sample_ast = [None]
        with self.assertRaises(ValueError):
            BasicBlock.build_from_ast(sample_ast)

        sample_ast = [[]]
        with self.assertRaises(ValueError):
            BasicBlock.build_from_ast(sample_ast)

    def test_build_single_expression(self):
        sample_code = "print('Hello, world!')"
        module = parse(sample_code)
        function_call = module.body[0].value
        basic_block = BasicBlock.build_from_ast(module.body)
        self.assertIsInstance(basic_block, BasicBlock)
        self.assertEqual(len(basic_block.body), 1)
        self.assertEqual(basic_block.body[0], function_call)
        self.assertIsInstance(basic_block.body[0], Call)

    def test_build_multiple_expressions(self):
        sample_code = "print('Hello Number 1')\n"
        sample_code += "print('Hello World 2')\n"
        sample_code += "print('Hello World 3')"
        module = parse(sample_code)
        basic_block = BasicBlock.build_from_ast(module.body)
        self.assertIsInstance(basic_block, BasicBlock)
        self.assertEqual(len(basic_block.body), 3)


class TestBasicBlockFunctionCalls(unittest.TestCase):
    def test_function_calls_returns_only_calls(self):
        sample_code = "print('Hello Number 1')\n"
        sample_code += "print('Hello World 2')\n"
        sample_code += "def testFunc():\n"
        sample_code += "    pass"

        module = parse(sample_code)
        basic_block = BasicBlock.build_from_ast(module.body)
        self.assertEqual(len(basic_block.function_calls), 2)
        self.assertIsInstance(basic_block.function_calls[0], Call)
        self.assertIsInstance(basic_block.function_calls[1], Call)
