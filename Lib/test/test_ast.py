import sys, itertools, unittest
from test import test_support
import ast

def to_tuple(t):
    if t is None or isinstance(t, (basestring, int, long, complex)):
        return t
    elif isinstance(t, list):
        return [to_tuple(e) for e in t]
    result = [t.__class__.__name__]
    if hasattr(t, 'lineno') and hasattr(t, 'col_offset'):
        result.append((t.lineno, t.col_offset))
    if t._fields is None:
        return tuple(result)
    for f in t._fields:
        result.append(to_tuple(getattr(t, f)))
    return tuple(result)


# These tests are compiled through "exec"
# There should be atleast one test per statement
exec_tests = [
    # FunctionDef
    "def f(): pass",
    # ClassDef
    "class C:pass",
    # Return
    "def f():return 1",
    # Delete
    "del v",
    # Assign
    "v = 1",
    # AugAssign
    "v += 1",
    # Print
    "print >>f, 1, ",
    # For
    "for v in v:pass",
    # While
    "while v:pass",
    # If
    "if v:pass",
    # Raise
    "raise Exception, 'string'",
    # TryExcept
    "try:\n  pass\nexcept Exception:\n  pass",
    # TryFinally
    "try:\n  pass\nfinally:\n  pass",
    # Assert
    "assert v",
    # Import
    "import sys",
    # ImportFrom
    "from sys import v",
    # Exec
    "exec 'v'",
    # Global
    "global v",
    # Expr
    "1",
    # Pass,
    "pass",
    # Break
    "break",
    # Continue
    "continue",
    # Parens and BoolOp
    "(a == '') and b",
    "not (a == '') or b",
    # Parens and BinOp
    "(a - b) * c",
    # for statements with naked tuples
    "for a,b in c: pass",
    "[(a,b) for a,b in c]",
    "((a,b) for a,b in c)",
]

# These are compiled through "single"
# because of overlap with "eval", it just tests what
# can't be tested with "eval"
single_tests = [
    "1+2"
]

# These are compiled through "eval"
# It should test all expressions
eval_tests = [
  # BoolOp
  "a and b",
  # BinOp
  "a + b",
  # UnaryOp
  "not v",
  # Lambda
  "lambda:None",
  # Dict
  "{ 1:2 }",
  # ListComp
  "[a for b in c if d]",
  # GeneratorExp
  "(a for b in c if d)",
  # Yield - yield expressions can't work outside a function
  #
  # Compare
  "1 < 2 < 3",
  # Call
  "f(1,2,c=3,*d,**e)",
  # Repr
  "`v`",
  # Num
  "10L",
  # Str
  "'string'",
  # Attribute
  "a.b",
  # Subscript
  "a[b:c]",
  # Name
  "v",
  # List
  "[1,2,3]",
  # Tuple
  "1,2,3",
  # Combination
  "a.b.c.d(a.b[1:2])",

]

# TODO: expr_context, slice, boolop, operator, unaryop, cmpop, comprehension
# excepthandler, arguments, keywords, alias

class AST_Tests(unittest.TestCase):

    def _assert_order(self, ast_node, parent_pos):
        if not isinstance(ast_node, ast.AST) or ast_node._fields is None:
            return
        if isinstance(ast_node, (ast.expr, ast.stmt, ast.excepthandler)):
            node_pos = (ast_node.lineno, ast_node.col_offset)
            self.assert_(node_pos >= parent_pos)
            parent_pos = (ast_node.lineno, ast_node.col_offset)
        for name in ast_node._fields:
            value = getattr(ast_node, name)
            if isinstance(value, list):
                for child in value:
                    self._assert_order(child, parent_pos)
            elif value is not None:
                self._assert_order(value, parent_pos)

    def test_snippets(self):
        for input, output, kind in ((exec_tests, exec_results, "exec"),
                                    (single_tests, single_results, "single"),
                                    (eval_tests, eval_results, "eval")):
            for i, o in itertools.izip(input, output):
                ast_tree = compile(i, "?", kind, ast.PyCF_ONLY_AST)
                self.assertEquals(to_tuple(ast_tree), o)
                self._assert_order(ast_tree, (0, 0))

    def test_nodeclasses(self):
        x = ast.BinOp(1, 2, 3, lineno=0)
        self.assertEquals(x.left.n, 1)
        self.assertEquals(int(x.op), 2)
        self.assertEquals(x.right.n, 3)
        self.assertEquals(x.lineno, 0)

        # node raises exception when not given enough arguments
        self.assertRaises(TypeError, ast.BinOp, 1, 2)

        # can set attributes through kwargs too
        x = ast.BinOp(left=1, op=2, right=3, lineno=0)
        self.assertEquals(x.left.n, 1)
        self.assertEquals(int(x.op), 2)
        self.assertEquals(x.right.n, 3)
        self.assertEquals(x.lineno, 0)

        # this used to fail because Sub._fields was None
        x = ast.Sub()

    def test_pickling(self):
        import pickle
        mods = [pickle]
        try:
            import cPickle
            mods.append(cPickle)
        except ImportError:
            pass
        protocols = [0, 1, 2]
        for mod in mods:
            for protocol in protocols:
                for ast in (compile(i, "?", "exec", 0x400) for i in exec_tests):
                    ast2 = mod.loads(mod.dumps(ast, protocol))
                    self.assertEquals(to_tuple(ast2), to_tuple(ast))


class ASTHelpers_Test(unittest.TestCase):

    def test_parse(self):
        a = ast.parse('foo(1 + 1)')
        b = compile('foo(1 + 1)', '<unknown>', 'exec', ast.PyCF_ONLY_AST)
        self.assertEqual(ast.dump(a), ast.dump(b))

    def test_dump(self):
        node = ast.parse('spam(eggs, "and cheese")')
        self.assertEqual(ast.dump(node),
            "Module(body=[Expr(value=Call(func=Name(id='spam', ctx=Load()), "
            "args=[Name(id='eggs', ctx=Load()), Str(s='and cheese')], "
            "keywords=[], starargs=None, kwargs=None))])"
        )
        self.assertEqual(ast.dump(node, annotate_fields=False),
            "Module([Expr(Call(Name('spam', Load()), [Name('eggs', Load()), "
            "Str('and cheese')], [], None, None))])"
        )
        self.assertEqual(ast.dump(node, include_attributes=True),
            "Module(body=[Expr(value=Call(func=Name(id='spam', ctx=Load(), "
            "lineno=1, col_offset=0), args=[Name(id='eggs', ctx=Load(), "
            "lineno=1, col_offset=5), Str(s='and cheese', lineno=1, "
            "col_offset=11)], keywords=[], starargs=None, kwargs=None, "
            "lineno=1, col_offset=0), lineno=1, col_offset=0)])"
        )

    def test_copy_location(self):
        src = ast.parse('1 + 1', mode='eval')
        src.body.right = ast.copy_location(ast.Num(2), src.body.right)
        self.assertEqual(ast.dump(src, include_attributes=True),
            'Expression(body=BinOp(left=Num(n=1, lineno=1, col_offset=0), '
            'op=Add(), right=Num(n=2, lineno=1, col_offset=4), lineno=1, '
            'col_offset=0))'
        )

    def test_fix_missing_locations(self):
        src = ast.parse('write("spam")')
        src.body.append(ast.Expr(ast.Call(ast.Name('spam', ast.Load()),
                                          [ast.Str('eggs')], [], None, None)))
        self.assertEqual(src, ast.fix_missing_locations(src))
        self.assertEqual(ast.dump(src, include_attributes=True),
            "Module(body=[Expr(value=Call(func=Name(id='write', ctx=Load(), "
            "lineno=1, col_offset=0), args=[Str(s='spam', lineno=1, "
            "col_offset=6)], keywords=[], starargs=None, kwargs=None, "
            "lineno=1, col_offset=0), lineno=1, col_offset=0), "
            "Expr(value=Call(func=Name(id='spam', ctx=Load(), lineno=1, "
            "col_offset=0), args=[Str(s='eggs', lineno=1, col_offset=0)], "
            "keywords=[], starargs=None, kwargs=None, lineno=1, "
            "col_offset=0), lineno=1, col_offset=0)])"
        )

    def test_increment_lineno(self):
        src = ast.parse('1 + 1', mode='eval')
        self.assertEqual(ast.increment_lineno(src, n=3), src)
        self.assertEqual(ast.dump(src, include_attributes=True),
            'Expression(body=BinOp(left=Num(n=1, lineno=4, col_offset=0), '
            'op=Add(), right=Num(n=1, lineno=4, col_offset=4), lineno=4, '
            'col_offset=0))'
        )

    def test_iter_fields(self):
        node = ast.parse('foo()', mode='eval')
        d = dict(ast.iter_fields(node.body))
        self.assertEqual(d.pop('func').id, 'foo')

        #XXX: tests for equality between astlist and regular lists not
        #     working, breaking this test up into its components.
        #self.assertEqual(d, {'keywords': [], 'kwargs': None,
        #                     'args': [], 'starargs': None})
        assert len(d) == 4
        assert d['keywords'] is not None
        assert len(d['keywords']) == 0
        assert d['args'] is not None
        assert len(d['args']) == 0
        assert d['kwargs'] is None
        assert d['starargs'] is None

    def test_iter_child_nodes(self):
        node = ast.parse("spam(23, 42, eggs='leek')", mode='eval')
        self.assertEqual(len(list(ast.iter_child_nodes(node.body))), 4)
        iterator = ast.iter_child_nodes(node.body)
        self.assertEqual(iterator.next().id, 'spam')
        self.assertEqual(iterator.next().n, 23)
        self.assertEqual(iterator.next().n, 42)
        self.assertEqual(ast.dump(iterator.next()),
            "keyword(arg='eggs', value=Str(s='leek'))"
        )

    def test_get_docstring(self):
        node = ast.parse('def foo():\n  """line one\n  line two"""')
        self.assertEqual(ast.get_docstring(node.body[0]),
                         'line one\nline two')

    def test_literal_eval(self):
        self.assertEqual(ast.literal_eval('[1, 2, 3]'), [1, 2, 3])
        self.assertEqual(ast.literal_eval('{"foo": 42}'), {"foo": 42})
        self.assertEqual(ast.literal_eval('(True, False, None)'), (True, False, None))
        self.assertRaises(ValueError, ast.literal_eval, 'foo()')


def test_main():
    #XXX: AST pickling is left as a TODO for now.
    del AST_Tests.test_pickling

    test_support.run_unittest(AST_Tests, ASTHelpers_Test)

def main():
    if __name__ != '__main__':
        return
    if sys.argv[1:] == ['-g']:
        for statements, kind in ((exec_tests, "exec"), (single_tests, "single"),
                                 (eval_tests, "eval")):
            print kind+"_results = ["
            for s in statements:
                print repr(to_tuple(compile(s, "?", kind, 0x400)))+","
            print "]"
        print "main()"
        raise SystemExit
    test_main()

#### EVERYTHING BELOW IS GENERATED #####
exec_results = [
('Module', [('FunctionDef', (1, 0), 'f', ('arguments', [], None, None, []), [('Pass', (1, 9))], [])]),
('Module', [('ClassDef', (1, 0), 'C', [], [('Pass', (1, 8))], [])]),
('Module', [('FunctionDef', (1, 0), 'f', ('arguments', [], None, None, []), [('Return', (1, 8), ('Num', (1, 15), 1))], [])]),
('Module', [('Delete', (1, 0), [('Name', (1, 4), 'v', ('Del',))])]),
('Module', [('Assign', (1, 0), [('Name', (1, 0), 'v', ('Store',))], ('Num', (1, 4), 1))]),
('Module', [('AugAssign', (1, 0), ('Name', (1, 0), 'v', ('AugStore',)), ('Add',), ('Num', (1, 5), 1))]),
('Module', [('Print', (1, 0), ('Name', (1, 8), 'f', ('Load',)), [('Num', (1, 11), 1)], False)]),
('Module', [('For', (1, 0), ('Name', (1, 4), 'v', ('Store',)), ('Name', (1, 9), 'v', ('Load',)), [('Pass', (1, 11))], [])]),
('Module', [('While', (1, 0), ('Name', (1, 6), 'v', ('Load',)), [('Pass', (1, 8))], [])]),
('Module', [('If', (1, 0), ('Name', (1, 3), 'v', ('Load',)), [('Pass', (1, 5))], [])]),
('Module', [('Raise', (1, 0), ('Name', (1, 6), 'Exception', ('Load',)), ('Str', (1, 17), 'string'), None)]),
('Module', [('TryExcept', (1, 0), [('Pass', (2, 2))], [('ExceptHandler', (3, 0), ('Name', (3, 7), 'Exception', ('Load',)), None, [('Pass', (4, 2))])], [])]),
('Module', [('TryFinally', (1, 0), [('Pass', (2, 2))], [('Pass', (4, 2))])]),
('Module', [('Assert', (1, 0), ('Name', (1, 7), 'v', ('Load',)), None)]),
('Module', [('Import', (1, 0), [('alias', 'sys', None)])]),
('Module', [('ImportFrom', (1, 0), 'sys', [('alias', 'v', None)], 0)]),
('Module', [('Exec', (1, 0), ('Str', (1, 5), 'v'), None, None)]),
('Module', [('Global', (1, 0), ['v'])]),
('Module', [('Expr', (1, 0), ('Num', (1, 0), 1))]),
('Module', [('Pass', (1, 0))]),
('Module', [('Break', (1, 0))]),
('Module', [('Continue', (1, 0))]),
('Module', [('Expr', (1, 0), ('BoolOp', (1, 0), ('And',), [('Compare', (1, 1), ('Name', (1, 1), 'a', ('Load',)), [('Eq',)], [('Str', (1, 6), '')]), ('Name', (1, 14), 'b', ('Load',))]))]),
('Module', [('Expr', (1, 0), ('BoolOp', (1, 0), ('Or',), [('UnaryOp', (1, 0), ('Not',), ('Compare', (1, 5), ('Name', (1, 5), 'a', ('Load',)), [('Eq',)], [('Str', (1, 10), '')])), ('Name', (1, 17), 'b', ('Load',))]))]),
('Module', [('Expr', (1, 0), ('BinOp', (1, 0), ('BinOp', (1, 1), ('Name', (1, 1), 'a', ('Load',)), ('Sub',), ('Name', (1, 5), 'b', ('Load',))), ('Mult',), ('Name', (1, 10), 'c', ('Load',))))]),
('Module', [('For', (1, 0), ('Tuple', (1, 4), [('Name', (1, 4), 'a', ('Store',)), ('Name', (1, 6), 'b', ('Store',))], ('Store',)), ('Name', (1, 11), 'c', ('Load',)), [('Pass', (1, 14))], [])]),
('Module', [('Expr', (1, 0), ('ListComp', (1, 1), ('Tuple', (1, 2), [('Name', (1, 2), 'a', ('Load',)), ('Name', (1, 4), 'b', ('Load',))], ('Load',)), [('comprehension', ('Tuple', (1, 11), [('Name', (1, 11), 'a', ('Store',)), ('Name', (1, 13), 'b', ('Store',))], ('Store',)), ('Name', (1, 18), 'c', ('Load',)), [])]))]),
('Module', [('Expr', (1, 0), ('GeneratorExp', (1, 1), ('Tuple', (1, 2), [('Name', (1, 2), 'a', ('Load',)), ('Name', (1, 4), 'b', ('Load',))], ('Load',)), [('comprehension', ('Tuple', (1, 11), [('Name', (1, 11), 'a', ('Store',)), ('Name', (1, 13), 'b', ('Store',))], ('Store',)), ('Name', (1, 18), 'c', ('Load',)), [])]))]),
]
single_results = [
('Interactive', [('Expr', (1, 0), ('BinOp', (1, 0), ('Num', (1, 0), 1), ('Add',), ('Num', (1, 2), 2)))]),
]
eval_results = [
('Expression', ('BoolOp', (1, 0), ('And',), [('Name', (1, 0), 'a', ('Load',)), ('Name', (1, 6), 'b', ('Load',))])),
('Expression', ('BinOp', (1, 0), ('Name', (1, 0), 'a', ('Load',)), ('Add',), ('Name', (1, 4), 'b', ('Load',)))),
('Expression', ('UnaryOp', (1, 0), ('Not',), ('Name', (1, 4), 'v', ('Load',)))),
('Expression', ('Lambda', (1, 0), ('arguments', [], None, None, []), ('Name', (1, 7), 'None', ('Load',)))),
('Expression', ('Dict', (1, 0), [('Num', (1, 2), 1)], [('Num', (1, 4), 2)])),
('Expression', ('ListComp', (1, 1), ('Name', (1, 1), 'a', ('Load',)), [('comprehension', ('Name', (1, 7), 'b', ('Store',)), ('Name', (1, 12), 'c', ('Load',)), [('Name', (1, 17), 'd', ('Load',))])])),
('Expression', ('GeneratorExp', (1, 1), ('Name', (1, 1), 'a', ('Load',)), [('comprehension', ('Name', (1, 7), 'b', ('Store',)), ('Name', (1, 12), 'c', ('Load',)), [('Name', (1, 17), 'd', ('Load',))])])),
('Expression', ('Compare', (1, 0), ('Num', (1, 0), 1), [('Lt',), ('Lt',)], [('Num', (1, 4), 2), ('Num', (1, 8), 3)])),
('Expression', ('Call', (1, 0), ('Name', (1, 0), 'f', ('Load',)), [('Num', (1, 2), 1), ('Num', (1, 4), 2)], [('keyword', 'c', ('Num', (1, 8), 3))], ('Name', (1, 11), 'd', ('Load',)), ('Name', (1, 15), 'e', ('Load',)))),
('Expression', ('Repr', (1, 0), ('Name', (1, 1), 'v', ('Load',)))),
('Expression', ('Num', (1, 0), 10L)),
('Expression', ('Str', (1, 0), 'string')),
('Expression', ('Attribute', (1, 0), ('Name', (1, 0), 'a', ('Load',)), 'b', ('Load',))),
('Expression', ('Subscript', (1, 0), ('Name', (1, 0), 'a', ('Load',)), ('Slice', ('Name', (1, 2), 'b', ('Load',)), ('Name', (1, 4), 'c', ('Load',)), None), ('Load',))),
('Expression', ('Name', (1, 0), 'v', ('Load',))),
('Expression', ('List', (1, 0), [('Num', (1, 1), 1), ('Num', (1, 3), 2), ('Num', (1, 5), 3)], ('Load',))),
('Expression', ('Tuple', (1, 0), [('Num', (1, 0), 1), ('Num', (1, 2), 2), ('Num', (1, 4), 3)], ('Load',))),
('Expression', ('Call', (1, 0), ('Attribute', (1, 0), ('Attribute', (1, 0), ('Attribute', (1, 0), ('Name', (1, 0), 'a', ('Load',)), 'b', ('Load',)), 'c', ('Load',)), 'd', ('Load',)), [('Subscript', (1, 8), ('Attribute', (1, 8), ('Name', (1, 8), 'a', ('Load',)), 'b', ('Load',)), ('Slice', ('Num', (1, 12), 1), ('Num', (1, 14), 2), None), ('Load',))], [], None, None)),
]
main()
