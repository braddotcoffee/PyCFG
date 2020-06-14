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

    def test_if_body_becomes_basic_block(self):
        sample_code = "print('Test')\n"
        sample_code += "if True:\n"
        sample_code += "    x = 1\n"
        sample_code += "print('Test')\n"

        module = parse(sample_code)
        cfg = CFG(module.body)
        self.assertIsInstance(cfg.basic_blocks[1].body[0], Assign)

    def test_for_body_becomes_basic_block(self):
        sample_code = "print('Test')\n"
        sample_code += "for i in range(10):\n"
        sample_code += "    x = 1\n"
        sample_code += "print('Test')\n"

        module = parse(sample_code)
        cfg = CFG(module.body)
        self.assertIsInstance(cfg.basic_blocks[1].body[0], Assign)

    def test_else_body_becomes_basic_block(self):
        sample_code = "print('Test')\n"
        sample_code += "if True:\n"
        sample_code += "    x = 1\n"
        sample_code += "else:\n"
        sample_code += "    x = 2\n"
        sample_code += "print('Test')\n"

        module = parse(sample_code)
        cfg = CFG(module.body)
        self.assertEqual(4, len(cfg.basic_blocks))

    def test_if_elif_else(self):
        sample_code = "if True:\n"
        sample_code += "     print('Test')\n"
        sample_code += "elif True:\n"
        sample_code += "     x = 1\n"
        sample_code += "else:\n"
        sample_code += "     print('Test')\n"
        module = parse(sample_code)
        cfg = CFG(module.body)
        self.assertEqual(3, len(cfg.basic_blocks))

    def test_try_except_finally(self):
        sample_code = "try:\n"
        sample_code += "    print('Test')\n"
        sample_code += "except Exception:\n"
        sample_code += "    x = 1\n"
        sample_code += "finally:\n"
        sample_code += "    print('Test')\n"

        module = parse(sample_code)
        cfg = CFG(module.body)
        self.assertEqual(3, len(cfg.basic_blocks))
        self.assertIsInstance(cfg.basic_blocks[0].body[0], Call)

    def test_function_definition(self):
        sample_code = "def test_func():\n"
        sample_code += "    print('Test')\n"

        module = parse(sample_code)
        cfg = CFG(module.body)
        self.assertEqual(1, len(cfg.basic_blocks))

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


class TestParsedEquivalenceClasses(unittest.TestCase):
    def test_tracks_equivalence_classes(self):
        sample_code = "print('Test')\n"
        sample_code += "while True:\n"
        sample_code += "    x = 1\n"
        sample_code += "print('Test')\n"

        module = parse(sample_code)
        cfg = CFG(module.body)

        self.assertEqual(3, len(cfg.basic_blocks))
        self.assertEqual(1, cfg.equivalence_classes.count)
        for basic_block in cfg.basic_blocks:
            self.assertIn(basic_block.identifier, cfg.equivalence_classes)

    def test_try_except_connected_to_finally(self):
        sample_code = "try:\n"
        sample_code += "    print('Test')\n"
        sample_code += "except Exception:\n"
        sample_code += "    x = 1\n"
        sample_code += "finally:\n"
        sample_code += "    print('Test')\n"

        module = parse(sample_code)
        cfg = CFG(module.body)

        self.assertEqual(3, len(cfg.basic_blocks))
        self.assertEqual(1, cfg.equivalence_classes.count)
        for basic_block in cfg.basic_blocks:
            self.assertIn(basic_block.identifier, cfg.equivalence_classes)

    def test_if_elif_else_disconnected(self):
        sample_code = "if True:\n"
        sample_code += "    print('Test')\n"
        sample_code += "elif True:\n"
        sample_code += "    x = 1\n"
        sample_code += "else:\n"
        sample_code += "    print('Test')\n"

        module = parse(sample_code)
        cfg = CFG(module.body)

        self.assertEqual(3, len(cfg.basic_blocks))
        self.assertEqual(3, cfg.equivalence_classes.count)
        for basic_block in cfg.basic_blocks:
            self.assertIn(basic_block.identifier, cfg.equivalence_classes)

    def test_nested_blocks_connect_either_end(self):
        sample_code = "print('Test')\n"
        sample_code += "if True:\n"
        sample_code += "    print('Test')\n"
        sample_code += "elif True:\n"
        sample_code += "    x = 1\n"
        sample_code += "else:\n"
        sample_code += "    print('Test')\n"
        sample_code += "print('Test')\n"

        module = parse(sample_code)
        cfg = CFG(module.body)

        self.assertEqual(5, len(cfg.basic_blocks))
        self.assertEqual(1, cfg.equivalence_classes.count)
