from ast import parse
from src.cfg import CFG
import unittest
from _ast import Assign, Call


class TestCFGBuildBasicBlocks(unittest.TestCase):
    def test_can_parse_multiple_basic_blocks(self):
        sample_code = "print('Test')\n"
        sample_code += "while True:\n"
        sample_code += "    x = 1\n"
        sample_code += "print('Test')\n"

        module = parse(sample_code)
        cfg = CFG(module.body)
        self.assertEqual(3, len(cfg.basic_blocks))

    def test_while_body_becomes_basic_block(self):
        sample_code = "print('Test')\n"
        sample_code += "while True:\n"
        sample_code += "    x = 1\n"
        sample_code += "print('Test')\n"

        module = parse(sample_code)
        cfg = CFG(module.body)
        self.assertIsInstance(cfg.basic_blocks[1].body[0], Assign)

    def test_nested_blocks(self):
        sample_code = "print('Test')\n"
        sample_code += "while True:\n"
        sample_code += "    x = 1\n"
        sample_code += "    while True:\n"
        sample_code += "        print('Test')\n"
        sample_code += "print('Test')\n"

        module = parse(sample_code)
        cfg = CFG(module.body)
        self.assertEqual(4, len(cfg.basic_blocks))
        self.assertIsInstance(cfg.basic_blocks[1].body[0], Assign)
        self.assertIsInstance(cfg.basic_blocks[2].body[0], Call)
