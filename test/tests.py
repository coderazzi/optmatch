# Tests for python 2 can be run as
# (export PYTHONPATH=../src/:$PYTHONPATH && python2.7 tests2.py)

import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'src'))
if sys.version_info.major == 2:
    optmatch = __import__('optmatch2')
else:
    optmatch = __import__('optmatch3')

CommandLine = optmatch.CommandLine
OptMatcherHandler = optmatch.OptMatcherHandler
OptionMatcher = optmatch.OptionMatcher
UsageMode = optmatch.UsageMode
UsageException = optmatch.UsageException
OptionMatcherException = optmatch.OptionMatcherException
optmatcher = optmatch.optmatcher
optset = optmatch.optset


class Tests(unittest.TestCase):

    def assertRaiseArg(self, exception, exStr, callable, *args, **kwargs):
        try:
            callable(*args, **kwargs)
            self.fail('Expected exception not raised')
        except exception as which:
            self.assertEqual(str(which), exStr)


class InternalTests(Tests):
    """Tests on internal OptMatcherHandler"""

    def test0001(self):
        """Non getopt mode. Long flag easy"""

        def method(aFlag): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-a'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1])

    def test0002(self):
        """Non getopt mode. Long flag not given"""

        def method(aFlag): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-b'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(ret)

    def test0003(self):
        """Non getopt mode. Long option given"""

        def method(aOption): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-a=2'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == '2')

    def test0004(self):
        """Providing invalid argument '-' """

        m = UsageMode('-', '=')
        self.assertRaiseArg(UsageException, 'Unexpected argument -',
                            CommandLine, [None, '-'], m, False)

    def test0005(self):
        """Providing invalid argument '--' """

        m = UsageMode('--', '=')
        self.assertRaiseArg(UsageException, 'Unexpected argument --',
                            CommandLine, [None, '--'], m, False)

    def test0011(self):
        """Non getopt mode. using kwargs for an option"""

        def method(**kwarg): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-a=2'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.kwargs == {'a': '2'})

    def test0012(self):
        """Non getopt mode. using kwargs for a flag"""

        def method(**kwargs): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-a'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.kwargs == {'a': None})

    def test0021(self):
        """Non getopt mode. prefix well given with value"""

        def method(DPrefix): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-Dname=value'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == [('name', 'value')])

    def test0022(self):
        """Non getopt mode. prefix well given"""

        def method(IPrefix): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-Iname'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == [('name', None)])

    def test0023(self):
        """Non getopt mode. prefix incorrect"""

        def method(IPrefix): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-I=name'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException,
                            'Incorrect prefix usage on argument -I=name',
                            ch.handle_arg,
                            arg)

    def test0024(self):
        """Prefix are not mandatory options"""

        def method(IPrefix):
            return "Called"

        ch = OptMatcherHandler(method, UsageMode('-', '='))
        self.assertEqual(ch.invoke(), "Called")

    def test0101(self):
        """Non getopt mode. Long flag with alias"""

        def method(aFlag): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-aalias'], m, False)
        ch = OptMatcherHandler(method, m)
        ch.set_aliases({'a': 'aalias'})
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1])

    def test0103(self):
        """Non getopt mode. Long option given with alias"""

        def method(aOption): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-aalias=2'], m, False)
        ch = OptMatcherHandler(method, m)
        ch.set_aliases({'a': 'aalias'})
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == '2')

    def test0111(self):
        """Non getopt mode. prefix well given as alias, with value"""

        def method(DPrefix): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-definename=value'], m, False)
        ch = OptMatcherHandler(method, m)
        ch.set_aliases({'D': 'define'})
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == [('name', 'value')])

    def test0112(self):
        """Non getopt mode. prefix well given as alias, without value"""

        def method(IPrefix): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-includename'], m, False)
        ch = OptMatcherHandler(method, m)
        ch.set_aliases({'I': 'include'})
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == [('name', None)])

    def test0201(self):
        """getopt mode. Long flag easy"""

        def method(verboseFlag): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--verbose'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1])

    def test0202(self):
        """getopt mode. Long flag not given"""

        def method(verboseFlag): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--qqw'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertTrue(ch.handle_arg(arg))

    def test0203(self):
        """getopt mode. Long option given"""

        def method(modeOption): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--mode=2'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == '2')

    def test0211(self):
        """getopt mode. prefix well given"""

        def method(definePrefix): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--definename=value'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == [('name', 'value')])

    def test0212(self):
        """getopt mode. start flag prefix well given"""

        def method(includePrefix): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--includename'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == [('name', None)])

    def test0301(self):
        """getopt mode. Long flag with alias"""

        def method(vFlag): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--verbose'], m, False)
        ch = OptMatcherHandler(method, m)
        ch.set_aliases({'v': 'verbose'})
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1])

    def test0303(self):
        """getopt mode. Long option given with alias"""

        def method(vOption): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--verbose=2'], m, False)
        ch = OptMatcherHandler(method, m)
        ch.set_aliases({'v': 'verbose'})
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == '2')

    def test0311(self):
        """getopt mode. Short option given as long"""

        def method(aOption): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--a=2'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        return ret

    def test0312(self):
        """getopt mode. Short prefix given as long"""

        def method(aPrefix): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--aValue'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertTrue(ch.handle_arg(arg))

    def test0313(self):
        """getopt mode. Short prefix without associated value"""

        def method(aPrefix): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '-a', '-Value'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException, 'Incorrect prefix a',
                            ch.handle_arg, arg)

    def test0321(self):
        """getopt mode. Long flag given separated"""

        def method(verboseOption): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--verbose', 'value'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == 'value')

    def test0322(self):
        """getopt mode. Long flag given separated but as option"""

        def method(verboseOption): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--verbose', '-value'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException, 'Incorrect option verbose',
                            ch.handle_arg, arg)

    def test0323(self):
        """getopt mode. Long flag given separated but as name/value"""

        def method(verboseOption): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--verbose', 'name=value'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException, 'Incorrect option verbose',
                            ch.handle_arg, arg)

    def test0401(self):
        """getopt mode. Short flag given alone"""

        def method(vFlag): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '-v'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] and arg.finished())

    def test0402(self):
        """getopt mode. Short option given alone"""

        def method(vOption): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '-v1'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == '1' and arg.finished())

    def test0403(self):
        """getopt mode. Short option without value"""

        def method(vOption): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '-v'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException, 'Incorrect option v',
                            ch.handle_arg, arg)

    def test0404(self):
        """getopt mode. Short option given separately"""

        def method(vOption): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '-v', '1'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == '1' and arg.finished())

    def test0405(self):
        """getopt mode. Short option given separately but wrong"""

        def method(vOption): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '-v', '-a'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException, 'Incorrect option v',
                            ch.handle_arg, arg)

    def test0406(self):
        """getopt mode. Short option given separately, including value"""

        def method(vOption): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '-v', 'a=h'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException, 'Incorrect option v',
                            ch.handle_arg, arg)

    def test0411(self):
        """getopt mode. A flag given, but not alone"""

        def method(vFlag): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '-vw'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] and arg.name == 'w')

    def test0501(self):
        """getopt mode. Flag and Short options given"""

        def method(vOption, wFlag): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '-wv', 'q'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertTrue(not ch.handle_arg(arg) and not ch.handle_arg(arg)
                        and ch.provided[1] == 'q' and
                        ch.provided[2] and arg.finished())

    def test0601(self):
        """getopt mode. Parameter given"""

        def method(par1): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, 'file'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided_pars == ['file']
                        and arg.finished())

    def test0602(self):
        """getopt mode. Two parameters given"""

        def method(par1, par2): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, 'file', 'more'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertTrue(not ch.handle_arg(arg) and not ch.handle_arg(arg)
                        and ch.provided_pars == ['file', 'more']
                        and arg.finished())

    def test0603(self):
        """getopt mode. Two parameters given, only one expected"""

        def method(par1): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, 'file', 'more'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertFalse(ch.handle_arg(arg) and ch.handle_arg(arg))

    def test0605(self):
        """getopt mode. Using vararg for two arguments"""

        def method(*var): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, 'file', 'more'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertTrue(not ch.handle_arg(arg) and not ch.handle_arg(arg)
                        and arg.finished())

    def test0611(self):
        """getopt mode. Checking gnu mode"""

        def method(aFlag, par1, par2): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '-a', 'par1', '-v'], m, True)
        ch = OptMatcherHandler(method, m)
        self.assertTrue(not ch.handle_arg(arg))
        self.assertRaiseArg(UsageException,
                            'Unexpected argument -v after non option arguments',
                            ch.handle_arg, arg)

    def test0621(self):
        """Checking camel casing"""

        def method(dryRunFlag): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--dry-run'], m, True)
        ch = OptMatcherHandler(method, m)
        self.assertTrue(not ch.handle_arg(arg))


class InternalTestsForUnderscoredOptions(Tests):
    """Tests on internal OptMatcherHandler"""

    def test7001(self):
        """Non getopt mode. Long flag easy"""

        def method(a_flag): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-a'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1])

    def test7002(self):
        """Non getopt mode. Long flag not given"""

        def method(a_flag): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-b'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(ret)

    def test7003(self):
        """Non getopt mode. Long option given"""

        def method(a_option): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-a=2'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == '2')

    def test7021(self):
        """Non getopt mode. prefix well given with value"""

        def method(D_prefix): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-Dname=value'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == [('name', 'value')])

    def test7022(self):
        """Non getopt mode. prefix well given"""

        def method(I_prefix): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-Iname'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == [('name', None)])

    def test7023(self):
        """Non getopt mode. prefix incorrect"""

        def method(I_prefix): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-I=name'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException,
                            'Incorrect prefix usage on argument -I=name',
                            ch.handle_arg,
                            arg)

    def test7024(self):
        """Prefix are not mandatory options"""

        def method(I_prefix):
            return "Called"

        ch = OptMatcherHandler(method, UsageMode('-', '='))
        self.assertEqual(ch.invoke(), "Called")

    def test7101(self):
        """Non getopt mode. Long flag with alias"""

        def method(a_flag): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-aalias'], m, False)
        ch = OptMatcherHandler(method, m)
        ch.set_aliases({'a': 'aalias'})
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1])

    def test7103(self):
        """Non getopt mode. Long option given with alias"""

        def method(a_option): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-aalias=2'], m, False)
        ch = OptMatcherHandler(method, m)
        ch.set_aliases({'a': 'aalias'})
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == '2')

    def test7111(self):
        """Non getopt mode. prefix well given as alias, with value"""

        def method(x_prefix): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-definename=value'], m, False)
        ch = OptMatcherHandler(method, m)
        ch.set_aliases({'x': 'define'})
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == [('name', 'value')])

    def test7112(self):
        """Non getopt mode. prefix well given as alias, without value"""

        def method(x_prefix): pass

        m = UsageMode('-', '=')
        arg = CommandLine([None, '-includename'], m, False)
        ch = OptMatcherHandler(method, m)
        ch.set_aliases({'x': 'include'})
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == [('name', None)])

    def test7201(self):
        """getopt mode. Long flag easy"""

        def method(verbose_flag): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--verbose'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1])

    def test7202(self):
        """getopt mode. Long flag not given"""

        def method(verbose_flag): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--qqw'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertTrue(ch.handle_arg(arg))

    def test7203(self):
        """getopt mode. Long option given"""

        def method(mode_option): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--mode=2'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == '2')

    def test7211(self):
        """getopt mode. prefix well given"""

        def method(define_prefix): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--definename=value'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == [('name', 'value')])

    def test7212(self):
        """getopt mode. start flag prefix well given"""

        def method(include_prefix): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--includename'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == [('name', None)])

    def test7301(self):
        """getopt mode. Long flag with alias"""

        def method(v_flag): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--verbose'], m, False)
        ch = OptMatcherHandler(method, m)
        ch.set_aliases({'v': 'verbose'})
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1])

    def test7303(self):
        """getopt mode. Long option given with alias"""

        def method(v_option): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--verbose=2'], m, False)
        ch = OptMatcherHandler(method, m)
        ch.set_aliases({'v': 'verbose'})
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == '2')

    def test7311(self):
        """getopt mode. Short option given as long"""

        def method(a_option): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--a=2'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        return ret

    def test7312(self):
        """getopt mode. Short prefix given as long"""

        def method(a_prefix): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--aValue'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertTrue(ch.handle_arg(arg))

    def test7313(self):
        """getopt mode. Short prefix without associated value"""

        def method(a_prefix): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '-a', '-Value'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException, 'Incorrect prefix a',
                            ch.handle_arg, arg)

    def test7321(self):
        """getopt mode. Long flag given separated"""

        def method(verbose_option): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--verbose', 'value'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == 'value')

    def test7322(self):
        """getopt mode. Long flag given separated but as option"""

        def method(verbose_option): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--verbose', '-value'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException, 'Incorrect option verbose',
                            ch.handle_arg, arg)

    def test7323(self):
        """getopt mode. Long flag given separated but as name/value"""

        def method(verbose_option): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--verbose', 'name=value'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException, 'Incorrect option verbose',
                            ch.handle_arg, arg)

    def test7401(self):
        """getopt mode. Short flag given alone"""

        def method(v_flag): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '-v'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] and arg.finished())

    def test7402(self):
        """getopt mode. Short option given alone"""

        def method(v_option): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '-v1'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == '1' and arg.finished())

    def test7403(self):
        """getopt mode. Short option without value"""

        def method(v_option): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '-v'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException, 'Incorrect option v',
                            ch.handle_arg, arg)

    def test7404(self):
        """getopt mode. Short option given separately"""

        def method(v_option): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '-v', '1'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] == '1' and arg.finished())

    def test7405(self):
        """getopt mode. Short option given separately but wrong"""

        def method(v_option): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '-v', '-a'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException, 'Incorrect option v',
                            ch.handle_arg, arg)

    def test7406(self):
        """getopt mode. Short option given separately, including value"""

        def method(v_option): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '-v', 'a=h'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException, 'Incorrect option v',
                            ch.handle_arg, arg)

    def test7411(self):
        """getopt mode. A flag given, but not alone"""

        def method(v_flag): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '-vw'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handle_arg(arg)
        self.assertTrue(not ret and ch.provided[1] and arg.name == 'w')

    def test7622(self):
        """Checking absence of camel casing"""

        def method(dry_run_flag): pass

        m = UsageMode('--', '=')
        arg = CommandLine([None, '--dry-run'], m, True)
        ch = OptMatcherHandler(method, m)
        self.assertTrue(not ch.handle_arg(arg))


class OptMatcherTests(Tests):
    """Tests directly on the OptionMatcher interface"""

    def test1001(self):
        """Simplest case, no args"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self):
                return True

        self.assertTrue(Simple().process([None]))

    def test1002(self):
        """Define an optional argument, not provided"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, par=None):
                return True

        self.assertTrue(Simple().process([None]))

    def test1003(self):
        """Define an optional flag, not provided"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, vFlag=None):
                return True

        self.assertTrue(Simple().process([None]))

    def test1004(self):
        """Define an optional option, not provided"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, vOption=None):
                return True

        self.assertTrue(Simple().process([None]))

    def test1011(self):
        """Define a required flag, not provided"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, vFlag): pass

        self.assertRaiseArg(UsageException, 'Missing required flag v',
                            Simple().process, [None],
                            handle_usage_problems=False)

    def test1012(self):
        """Define a required flag, provided"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, vFlag):
                return True

        self.assertTrue(Simple().process([None, '-v']))

    def test1013(self):
        """Define a required flag, provide two flags"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, vFlag): pass

        self.assertRaiseArg(UsageException, 'Unexpected flag o in argument -o',
                            Simple().process, [None, '-v', '-o'],
                            handle_usage_problems=False)

    def test1021(self):
        """Use two flags, one parameter. Flags provided separately"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, vFlag, oFlag, par):
                return vFlag, oFlag, par

        self.assertEqual(Simple().process([None, '-v', '-o', 'file']),
                         (True, True, 'file'))

    def test1022(self):
        """Use two flags, one parameter. Flags provided together"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, vFlag, oFlag, par):
                return vFlag, oFlag, par

        self.assertEqual(Simple().process([None, '-vo', 'file']),
                         (True, True, 'file'))

    def test1023(self):
        """Use two flags, one parameter. Parameter provided between flags"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, vFlag, oFlag, par):
                return vFlag, oFlag, par

        self.assertEqual(Simple().process([None, '-v', 'file', '-o']),
                         (True, True, 'file'))

    def test1024(self):
        """Extended for GNU. Parameter provided between the flags"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, vFlag, oFlag, par):
                return vFlag, oFlag, par

        self.assertRaiseArg(UsageException,
                            'Unexpected argument -o after non option arguments',
                            Simple().process, [None, '-v', 'file', '-o'],
                            handle_usage_problems=False, gnu=True)

    def test1025(self):
        """Flag, option, parameter, all provided"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, vFlag, oOption, par):
                return vFlag, oOption, par

        self.assertEqual(Simple().process([None, '-vo1', 'file']),
                         (True, '1', 'file'))

    def test1026(self):
        """Verifying that prefixes are not required"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, vFlag, oOption, dPrefix, par):
                return vFlag, oOption, dPrefix, par

        self.assertEqual(Simple().process([None, '-vo', '1', 'file']),
                         (True, '1', [], 'file'))

    def test1031(self):
        """Using two matchers"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(vFlag, oOption, par): pass

            @optmatcher
            def handle2(self, vFlag, par):
                return vFlag, par

        self.assertEqual(Simple().process([None, '-v', 'file']),
                         (True, 'file'))

    def test1032(self):
        """Two matchers, a common one"""

        class Simple(OptionMatcher):

            @optset
            def common_options(self, vFlag):
                self.v = vFlag

            @optmatcher
            def handle(self, oOption, par):
                return False

            @optmatcher
            def handle2(self, par):
                return self.v, par

        self.assertEqual(Simple().process([None, '-v', 'file']),
                         (True, 'file'))

    def test1033(self):
        """common matcher with flag not provided"""

        class Simple(OptionMatcher):

            def __init__(self):
                OptionMatcher.__init__(self)
                self.v = None

            @optset
            def common_options(self, vFlag):
                self.v = 'invoked'

            @optmatcher
            def handle(self, par):
                return self.v == None

        self.assertTrue(Simple().process([None, 'file']))

    def test1034(self):
        """common matcher with default flag not provided"""

        class Simple(OptionMatcher):

            @optset
            def common_options(self, vFlag=True):
                self.v = vFlag

            @optmatcher
            def handle(self, par):
                return self.v

        self.assertTrue(Simple().process([None, 'file']))

    def test1035(self):
        """Common matcher, not fully specified"""

        class Simple(OptionMatcher):

            @optset
            def common_options(self, vFlag, oFlag): pass

            @optmatcher
            def handle(self, par): pass

        self.assertRaiseArg(UsageException,
                            'Missing required flag v',
                            Simple().process, [None, '-o', 'file'],
                            handle_usage_problems=False)

    def test1036(self):
        """Common matcher, not fully specified, forcing 2nd matcher"""

        class Simple(OptionMatcher):

            @optset
            def common_options(self, vFlag, oFlag): pass

            @optmatcher
            def handle(self, par): pass

            @optmatcher
            def handle2(self, oFlag, par):
                return oFlag, par, '2nd!'

        self.assertEqual(Simple().process([None, '-o', 'file']),
                         (True, 'file', '2nd!'))

    def test1041(self):
        """Aliases test on common"""

        class Simple(OptionMatcher):

            @optset
            def common_options(self, vFlag):
                self.v = vFlag

            @optmatcher
            def handle(self, oOption, par):
                return self.v, oOption, par

        args = [None, '--verbose', '--option=2', 'file']
        aliases = {'v': 'verbose', 'o': 'option'}
        self.assertEqual(Simple(aliases=aliases).process(args),
                         (True, '2', 'file'))

    def test1042(self):
        """Aliases test on common plus varargs"""

        class Simple(OptionMatcher):

            @optset
            def common_options(self, vFlag):
                self.v = vFlag

            @optmatcher
            def handle(self, oOption, *ends):
                return self.v, oOption, ends

        args = [None, '--verbose', '--option=2', '1', '2']
        aliases = {'v': 'verbose', 'o': 'option'}
        self.assertEqual(Simple(aliases=aliases).process(args),
                         (True, '2', ('1', '2')))

    def test1043(self):
        """Clashing flags by aliases definitions"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, oOption, kOption): pass

        self.assertRaises(OptionMatcherException,
                          Simple(aliases={'o': 'k'}).process, [])

    def test1044(self):
        """Clashing flags by aliases definitions short and long"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, oOption, optOption): pass

        self.assertRaises(OptionMatcherException,
                          Simple(aliases={'o': 'opt'}).process, [])

    def test1045(self):
        """Clashing flags by aliases definitions, long to short now"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, oOption, optOption): pass

        self.assertRaises(OptionMatcherException,
                          Simple(aliases={'opt': 'o'}).process, [])

    def test1046(self):
        """Clashing flags by aliases definitions, not getopt mode"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, oOption, vOption): pass

        self.assertRaises(OptionMatcherException,
                          Simple(aliases={'v': 'o'}, option_prefix='-').process,
                          [])

    def test1047(self):
        """Aliases test, overriding some long definition"""

        class Simple(OptionMatcher):

            @optmatcher
            def handleB(self, verboseFlag=False): pass

        aliases = {'v': 'verbose'}
        Simple(aliases=aliases).process([None])

    def test1048(self):
        """Clash between both styles of flags"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, vFlag, v_flag, par): pass

        self.assertRaises(OptionMatcherException, Simple().process, [])

    def test1051(self):
        """Integer options"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, valOptionInt):
                return valOptionInt

        self.assertEqual(Simple().process([None, '--val=2']), 2)

    def test1052(self):
        """Integer options, string for integer"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, valOptionInt): pass

        self.assertRaiseArg(UsageException, 'Incorrect value for val',
                            Simple().process, [None, '--val=two'],
                            handle_usage_problems=False)

    def test1053(self):
        """Integer options, float for integer"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, valOptionInt):
                self.ok = valOptionInt
                return True

        self.assertRaiseArg(UsageException, 'Incorrect value for val',
                            Simple().process, [None, '--val=2.3'],
                            handle_usage_problems=False)

    def test1054(self):
        """Float options"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, valOptionFloat):
                return valOptionFloat

        self.assertEqual(Simple().process([None, '--val=2.3']), 2.3)

    def test1055(self):
        """Float options, string for float"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, valOptionFloat):
                self.ok = valOptionFloat
                return True

        self.assertRaiseArg(UsageException, 'Incorrect value for val',
                            Simple().process, [None, '--val=two'],
                            handle_usage_problems=False)

    def test1056(self):
        """Float options, integer for float"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, valOptionFloat):
                return valOptionFloat

        self.assertEqual(Simple().process([None, '--val=2']), 2)

    def test1057(self):
        """Parameters for common and matchers"""

        class Simple(OptionMatcher):

            @optset
            def common(self, par1):
                self.par1 = par1

            @optmatcher
            def handle(self, par2):
                return self.par1, par2

        self.assertEqual(Simple().process([None, 'a', 'b']), ('b', 'a'))

    def test1101(self):
        """Using public_names"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, dFlag):
                return dFlag

        self.assertTrue(Simple(public_names={'d': 'dry-run'}
                               ).process([None, '--dry-run']))

    def test1102(self):
        """Using public_names, expected error"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, dFlag): pass

        self.assertRaiseArg(UsageException,
                            'Unexpected flag d in argument -d',
                            Simple(public_names={'d': 'dry-run'}).process,
                            [None, '-d'],
                            handle_usage_problems=False)

    def test1103(self):
        """Using public_names, expected error when overriding"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, dFlag, oFlag): pass

        self.assertRaiseArg(OptionMatcherException,
                            'method Simple.handle: invalid rename o',
                            Simple(public_names={'d': 'o'}).process,
                            [None])

    def test1104(self):
        """Using public_names, expected error when overriding parameter"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, first, second): pass

        self.assertRaiseArg(OptionMatcherException,
                            'method Simple.handle: invalid rename second',
                            Simple(public_names={'first': 'second'}).process,
                            [None])

        self.assertRaiseArg(OptionMatcherException,
                            'method Simple.handle: invalid rename first',
                            Simple(public_names={'second': 'first'}).process,
                            [None])

    def test1105(self):
        """Using public_names and aliases"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, dFlag):
                return dFlag

        self.assertTrue(Simple(public_names={'d': 'dry-run'},
                               aliases={'r': 'dry-run'}
                               ).process([None, '-r']))

    def test2001(self):
        """Checking non getoptMode"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, oOption, arg):
                return oOption, arg

        self.assertEqual(Simple(option_prefix='/', assigner=':').
                         process([None, '/o:23', 'file']),
                         ('23', 'file'))

    def test2002(self):
        """non getoptMode with aliases"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, oOption, arg):
                return oOption, arg

        self.assertEqual(Simple(aliases={'o': 'opt'},
                                option_prefix='/', \
                                assigner=':').
                         process([None, '/opt:23', 'file']),
                         ('23', 'file'))

    def test2003(self):
        """non getoptMode with aliases way around"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, oOption, arg):
                return oOption, arg

        self.assertEqual(Simple(aliases={'opt': 'o'},
                                option_prefix='/',
                                assigner=':').
                         process([None, '/opt:23', 'file']),
                         ('23', 'file'))

    def test2101(self):
        """using several common matchers"""

        class Simple(OptionMatcher):

            @optset
            def common_options1(self, vFlag):
                self.v = vFlag

            @optset
            def common_options2(self, kFlag):
                self.k = kFlag

            @optmatcher
            def handle(self, oOption, par):
                return False

            @optmatcher
            def handle2(self, rFlag, par):
                return self.v, self.k, rFlag, par

        self.assertEqual(Simple().process([None, '-rv', 'file', '-k']),
                         (True, True, True, 'file'))

    def test2102(self):
        """using several common matchers, not fully specified"""

        class Simple(OptionMatcher):

            @optset
            def common_options1(self, vFlag): pass

            @optset
            def common_options2(self, kFlag, aFlag): pass

            @optmatcher
            def handle(self, rFlag, par): pass

        self.assertRaiseArg(UsageException,
                            'Missing required flag a',
                            Simple().process, [None, '-rv', 'file', '-k'],
                            handle_usage_problems=False)

    def test2111(self):
        """Defining a function twice"""

        def go():
            class Simple(OptionMatcher):

                @optset
                @optmatcher
                def handle(self): pass

            Simple()

        self.assertRaiseArg(OptionMatcherException,
                            'Cannot decorate twice the method handle',
                            go)

    def test2112(self):
        """Missing optmatcher"""

        class Simple(OptionMatcher):

            @optset
            def handle(self): pass

        self.assertRaiseArg(OptionMatcherException,
                            'No matchers defined',
                            Simple().process, [])

    def test2201(self):
        """Using applies on optset"""

        class Simple(OptionMatcher):

            @optset(applies='handle2')
            def set(self, vFlag):
                pass

            @optmatcher
            def handle1(self): return False

            @optmatcher
            def handle2(self): return True

        self.assertTrue(Simple().process([None, '-v']))

    def test2202(self):
        """Using applies on optset, * specified"""

        class Simple(OptionMatcher):

            @optset(applies='*')
            def set(self, vFlag):
                pass

            @optmatcher
            def handle1(self): return True

            @optmatcher
            def handle2(self): return False

        self.assertTrue(Simple().process([None, '-v']))

    def test2203(self):
        """Using applies on optset, * specified"""

        class Simple(OptionMatcher):

            @optset(applies='handle*')
            def set(self, vFlag):
                pass

            @optmatcher
            def handle1(self): return True

            @optmatcher
            def handle2(self): return False

        self.assertTrue(Simple().process([None, '-v']))

    def test2204(self):
        """Using applies on optset, several specified specified"""

        class Simple(OptionMatcher):

            @optset(applies='handle2, handle3')
            def set(self, vFlag):
                pass

            @optmatcher
            def handle1(self): return False

            @optmatcher
            def handle2(self, oOption): return True

            @optmatcher
            def handle3(self): return True

        self.assertTrue(Simple().process([None, '-v']))

    def test2211(self):
        """Using exclsuive on optmatcher"""

        class Simple(OptionMatcher):

            @optset
            def set(self, vFlag):
                pass

            @optmatcher(exclusive=True)
            def handle1(self): return False

            @optmatcher
            def handle2(self): return True

        self.assertTrue(Simple().process([None, '-v']))


class OptMatcherTestsOnDecoration(Tests):
    """Tests on the OptionMatcher decorators"""

    def test3011(self):
        """defining flag via decorator"""

        class Simple(OptionMatcher):

            @optmatcher(flags='o')
            def handleA(self, o):
                return True

        self.assertTrue(Simple().process([None, '-o']))

    def test3012(self):
        """defining flags via decorator"""

        class Simple(OptionMatcher):

            @optmatcher(flags='o, v')
            def handleA(self, o, v):
                return o and v

        self.assertTrue(Simple().process([None, '-ov']))

    def test3013(self):
        """defining flags exclusively via decorator"""

        class Simple(OptionMatcher):

            @optmatcher(flags='o, v')
            def handleA(self, o, v, wFlag):
                return o and v and wFlag == 'w'

        self.assertTrue(Simple().process([None, '-ov', 'w']))

    def test3014(self):
        """defining flag with as"""

        class Simple(OptionMatcher):

            @optmatcher(flags='verbose as v')
            def handleA(self, verbose):
                return verbose

        self.assertTrue(Simple().process([None, '-v']))

    def test3015(self):
        """defining flags with as, and without"""

        class Simple(OptionMatcher):

            @optmatcher(flags='verbose as v, o')
            def handleA(self, verbose, o):
                return verbose and o

        self.assertTrue(Simple().process([None, '-vo']))

    def test3016(self):
        """defining a parameter with different name"""

        class Simple(OptionMatcher):

            @optmatcher(flags='o', rename_pars='va as file')
            def handleA(self, o, va):
                return o and va == 'f'

        self.assertTrue(Simple().process([None, '-o', 'f']))

    def test3017(self):
        """Renaming a parameter without as"""

        class Simple(OptionMatcher):

            @optmatcher(rename_pars='v')
            def handleA(self, v):
                return True

        self.assertRaiseArg(OptionMatcherException,
                            'Invalid rename_par v',
                            Simple().process, [None])

    def test3018(self):
        """Renaming a parameter with invalid as"""

        class Simple(OptionMatcher):

            @optmatcher(rename_pars='v as v')
            def handleA(self, v):
                return True

        self.assertRaiseArg(OptionMatcherException,
                            'Invalid rename_par v',
                            Simple().process, [None])

    def test3019(self):
        """Defining a non existing option"""

        class Simple(OptionMatcher):

            @optmatcher(options='k')
            def handleA(self, o):
                return True

        self.assertRaiseArg(OptionMatcherException,
                            'Invalid argument: k',
                            Simple().process, [None])

    def test3020(self):
        """Defining a non existing flag (orphan)"""

        class Simple(OptionMatcher):

            @optmatcher
            def handleA(self, o):
                return False

            @optmatcher(flags='k')
            def handleB(self, o):
                return True

        self.assertTrue(Simple().process([None, '-k', 'o']))

    def test3021(self):
        """Defining a non existing flag with as"""

        class Simple(OptionMatcher):

            @optmatcher(flags='k as o')
            def handleB(self):
                pass

        self.assertRaiseArg(OptionMatcherException,
                            'Invalid argument: k',
                            Simple().process, [None])

    def test3022(self):
        """Defining a non existing flag with as, even if equal"""

        class Simple(OptionMatcher):

            @optmatcher(flags='k as k')
            def handleB(self):
                pass

        self.assertRaiseArg(OptionMatcherException,
                            'Invalid argument: k',
                            Simple().process, [None])

    def test3023(self):
        """Orphan flag are mandatory"""

        class Simple(OptionMatcher):

            @optmatcher(flags='k')
            def handleB(self):
                pass

        self.assertRaiseArg(UsageException, 'Missing required flag k',
                            Simple().process, [None],
                            handle_usage_problems=False)

    def test3031(self):
        """Full decoration"""

        class Simple(OptionMatcher):

            @optmatcher(flags='o,v', options='w', prefixes='d as D',
                        int_options='i', float_options='f',
                        rename_pars='par as class', priority=1)
            def handleA(self, o, v, w, d, i, f, par):
                return o, v, w, d, i, f, par

        args = [None, '-oww', '-vi1', '-f', '2.3', '-Dvalue', 'class']
        self.assertEqual(Simple().process(args),
                         (True, True, 'w', [('value', None)],
                          1, 2.3, 'class'))

    def test3022(self):
        """Full decoration, using also optset"""

        class Simple(OptionMatcher):

            @optset(int_options='m as mode')
            def common(self, m):
                self.m = m

            @optmatcher(flags='o,v', options='w', prefixes='d as D',
                        int_options='i', float_options='f',
                        rename_pars='par as class', priority=1)
            def handleA(self, o, v, w, d, i, f, par):
                return self.m, o, v, w, d, i, f, par

        args = [None, '-oww', '--mode=23', '-vi1', '-f', '2.3', '-Dvalue',
                'class']
        self.assertEqual(Simple().process(args),
                         (23, True, True, 'w', [('value', None)],
                          1, 2.3, 'class'))

    def test3031(self):
        """Setting priorities"""

        class Simple(OptionMatcher):

            @optmatcher
            def handleA(self, oFlag): pass

            @optmatcher(priority=1)
            def handleB(self, oFlag):
                return True

            @optmatcher
            def handleC(self, oFlag): pass

        self.assertTrue(Simple().process([None, '-o']))

    def test3041(self):
        """Setting priorities on optset"""

        class Simple(OptionMatcher):

            def __init__(self):
                OptionMatcher.__init__(self)
                self.o = False

            @optset(priority=2)
            def handleA(self, oFlag):
                self.o = oFlag

            @optset(priority=1)
            def handleB(self, kFlag):
                try:
                    self.k = self.o
                except:
                    self.k = False

            @optmatcher
            def handle(self):
                return self.k

        self.assertTrue(Simple().process([None, '-ok']))

    def test3042(self):
        """Setting priorities on optset, way around"""

        class Simple(OptionMatcher):

            def __init__(self):
                OptionMatcher.__init__(self)
                self.o = False

            @optset(priority=1)
            def handleA(self, oFlag):
                self.o = oFlag

            @optset(priority=2)
            def handleB(self, kFlag):
                try:
                    self.k = self.o
                except:
                    self.k = False

            @optmatcher
            def handle(self):
                return self.k

        self.assertFalse(Simple().process([None, '-ok']))


class OptMatcherTestsOnErrorMessages(Tests):
    """Tests on the OptionMatcher error messages"""

    def test4001(self):
        """Message error: unexpected flag"""

        class Simple(OptionMatcher):

            @optmatcher(flags='o')
            def handleA(self, o): pass

        self.assertRaiseArg(UsageException,
                            'Unexpected flag v in argument -v',
                            Simple().process, [None, '-v'],
                            handle_usage_problems=False)

    def test4002(self):
        """Message error: required flag"""

        class Simple(OptionMatcher):

            @optmatcher(flags='o')
            def handleA(self, o): pass

        self.assertRaiseArg(UsageException,
                            'Missing required flag o',
                            Simple().process, [None],
                            handle_usage_problems=False)

    def test4003(self):
        """Message error: unexpected parameter"""

        class Simple(OptionMatcher):

            @optmatcher
            def handleA(self): pass

        self.assertRaiseArg(UsageException,
                            'Unexpected argument: file',
                            Simple(default_help=False).process, [None, 'file'],
                            handle_usage_problems=False)

    def test4004(self):
        """Message error: required parameter"""

        class Simple(OptionMatcher):

            @optmatcher
            def handleA(self, name): pass

        self.assertRaiseArg(UsageException,
                            'Missing required parameter name',
                            Simple().process, [None],
                            handle_usage_problems=False)

    def test4005(self):
        """Message error: required parameter, changed on decorator"""

        class Simple(OptionMatcher):

            @optmatcher(rename_pars='c as class')
            def handleA(self, c): pass

        self.assertRaiseArg(UsageException,
                            'Missing required parameter class',
                            Simple().process, [None],
                            handle_usage_problems=False)

    def test4011(self):
        """Message error: coming from lower priority matcher"""

        class Simple(OptionMatcher):

            @optmatcher
            def handleA(self, vFlag, kFlag): pass

            @optmatcher
            def handleB(self, oFlag, pOption): pass

        self.assertRaiseArg(UsageException,
                            'Missing required option p',
                            Simple().process, [None, '-o'])

    def test4011(self):
        """Message error: coming from lower priority matcher on shorts"""

        class Simple(OptionMatcher):

            @optmatcher
            def handleA(self, vFlag, kFlag, oFlag): pass

            @optmatcher
            def handleB(self, vFlag, pFlag, qFlag): pass

        self.assertRaiseArg(UsageException,
                            'Unexpected flag r in argument -vpr',
                            Simple().process, [None, '-vpr'],
                            handle_usage_problems=False)

    def test4012(self):
        """Message error: higher complexity"""

        class Simple(OptionMatcher):

            @optmatcher
            def handleA(self, vFlag, pFlag, oFlag, *args): pass

            @optmatcher
            def handleB(self, vFlag, pFlag, qFlag): pass

        self.assertRaiseArg(UsageException,
                            'Unexpected flag q in argument -q',
                            Simple().process, [None, '-vp', 'arg', '-q'],
                            handle_usage_problems=False)


class UsageTests(Tests):
    """Tests on internal OptMatcherHandler"""

    def checkString(self, received, expected):
        receivedSplit = received.split('\n')
        expectedSplit = expected.split('\n')
        for i, (lineR, lineE) in enumerate(zip(receivedSplit, expectedSplit)):
            if lineR != lineE:
                print()
                print('Line', i + 1, 'Received:', lineR, len(lineR))
                print('Line', i + 1, 'Expected:', lineE, len(lineE))
                self.fail('Line ' + str(i + 1) + ' ' + lineR +
                          '\nAnd expected: ' + lineE)
        self.assertTrue(len(receivedSplit) == len(expectedSplit))

    def convertList(self, list):
        return ' '.join([str(l) for l in list])

    def test6001(self):
        """Basic help tests"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self, vFlag, oOption, par1, par2): pass

            @optmatcher
            def handle2(self, vFlag, kFlag, par1, *args): pass

        usage = Simple().get_usage()
        self.assertTrue(usage.get_all_parameters() ==
                        'par1 par2 ...')
        self.assertTrue(self.convertList(usage.get_parameters(0))
                        == 'par1 par2')
        self.assertTrue(self.convertList(usage.get_parameters(1))
                        == 'par1 ...')
        self.assertTrue(self.convertList(usage.get_all_options()) ==
                        '--help -k -v -o O')

    def test6002(self):
        """Basic help tests, added optset"""

        class Simple(OptionMatcher):

            @optset
            def other(self, vFlag, arg, rOption='r'): pass

            @optmatcher
            def handle(self, vFlag, oOption, par1, par2): pass

            @optmatcher
            def handle2(self, vFlag, kFlag, par1, *args): pass

        usage = Simple().get_usage()
        self.assertTrue(self.convertList(usage.get_parameters(0))
                        == 'par1 par2 arg')
        self.assertTrue(self.convertList(usage.get_parameters(1))
                        == 'par1 ...')
        self.assertTrue(self.convertList(usage.get_parameters(2))
                        == '')
        self.assertTrue(usage.get_all_parameters() ==
                        'par1 par2 arg ...')
        self.assertTrue(self.convertList(usage.get_all_options()) ==
                        '--help -k -v -o O [-r R (r)]')

    def test6003(self):
        """Basic help tests, added optsetm, with exclusive on optmatcher"""

        class Simple(OptionMatcher):

            @optset
            def other(self, vFlag, arg, rOption='r'): pass

            @optmatcher(exclusive=True)
            def handle(self, vFlag, oOption, par1, par2): pass

            @optmatcher
            def handle2(self, vFlag, kFlag, par1, *args): pass

        usage = Simple().get_usage()
        self.assertTrue(self.convertList(usage.get_parameters(0))
                        == 'par1 par2')
        self.assertTrue(self.convertList(usage.get_parameters(1))
                        == 'par1 ...')
        self.assertTrue(self.convertList(usage.get_parameters(2))
                        == '')
        self.assertTrue(usage.get_all_parameters() ==
                        'par1 par2 ...')
        self.assertTrue(self.convertList(usage.get_all_options()) ==
                        '--help -k -v -o O [-r R (r)]')

    def test6004(self):
        """Global help test"""

        class Simple(OptionMatcher):

            @optset
            def handle(self, commonFlag, dPrefix, bFlag, commonOptOption=23,
                       commonPar='po'):
                pass

            @optset(applies='handleB, handleC')
            def handle2(self, common2Flag, addpar='3'):
                pass

            @optmatcher
            def handleA(self, fOption, DPrefix, one, two='2', iOptionInt=34,
                        wFlag=True, *args):
                """Executes this program repeatedly until everybody is tired"""
                pass

            @optmatcher
            def handleB(self, pFlag, one, mOption,
                        iOptionInt=68, verboseFlag=False):
                pass

            @optmatcher(exclusive=True)
            def handleC(self, pFlag, one, three, four, iOptionInt=68,
                        verboseFlag=False):
                pass

            @optmatcher(flags='super')
            def handleD(self):
                pass

        aliases = {'v': 'verbose',
                   'f': 'filename',
                   'i': 'include',
                   'D': 'define',
                   'm': 'mode'}
        info = {'v': 'lot of useless info is output',
                'D': 'create a new prefix',
                'f': 'write output to FILE',
                'm': 'interaction mode: novice, intermediate, or ' +
                     'expert [default: intermediate]'}
        vars = {'d': 'DX', 'i': 'IN', 'f': 'FILE'}
        usage = Simple(aliases=aliases, options_help=info,
                       option_var_names=vars, default_help=False).get_usage()

        expected = """Usage: [common options] arg1 arg2 arg3 addpar ...

options:
  -b
  --common
  --common2
  -p
  --super
  -v, --verbose         lot of useless info is output
  -w
  --common-opt=COMMON_OPT
  -d DX
  -D DEFINE, --define=DEFINE
                        create a new prefix
  -f FILE, --filename=FILE
                        write output to FILE
  -i IN, --include=IN
  -m MODE, --mode=MODE  interaction mode: novice, intermediate, or
                        expert [default: intermediate]

alternatives:

* -b --common -d DX --define=DEFINE --filename=FILE
  [--common-opt=COMMON_OPT (23)] [--include=IN (34)] [-w (True)] one
  [two (2)] ...
                        Executes this program repeatedly until everybody
                        is tired

* -b --common --common2 -d DX --mode=MODE -p
  [--common-opt=COMMON_OPT (23)] [--include=IN (68)] [--verbose (False)]
  one [commonPar (po)] [addpar (3)]

* --common2 -p [--include=IN (68)] [--verbose (False)] one three four
  [addpar (3)]

* -b --common -d DX --super [--common-opt=COMMON_OPT (23)]
  [commonPar (po)]"""

        self.checkString(usage.get_usage_string(), expected)

    def test6005(self):
        """Additional global help test"""

        class Simple(OptionMatcher):

            @optset
            def other(self, vFlag, arg, rOption='r'): pass

            @optmatcher(exclusive=True)
            def handle(self, vFlag, oOption, par1, par2): pass

            @optmatcher
            def handle2(self, vFlag, kFlag, par1, *args): pass

        aliases = {'v': 'verbose',
                   'o': 'open'}
        info = {'v': 'lot of useless info is output',
                'o': 'sets open mode'}
        vars = {'o': 'MODE'}
        usage = Simple(aliases=aliases, options_help=info,
                       option_var_names=vars, default_help=True).get_usage()
        expected = """Usage: [common options] par1
par2 ...

options:
     -h, --help
               shows this help
               message
     -k
     -v, --verbose
               lot of useless
               info is output
     -o MODE, --open=MODE
               sets open mode
     -r R"""

        self.checkString(usage.get_usage_string(width=30, column=15, ident=5,
                                              include_alternatives=False), expected)

    def test6006(self):
        """Verifying optionality on arguments"""

        class Simple(OptionMatcher):

            @optset
            def other(self, mandatoryPar): pass

            @optmatcher
            def handle(self, par1, optionalPar='o'): pass

            @optmatcher(exclusive=True)
            def handle2(self, par1, optionalPar='o'): pass

        usage = Simple().get_usage()
        # note that optionalPar in handle is not treated as optional anymore
        self.assertTrue(self.convertList(usage.get_parameters(0))
                        == 'par1 optionalPar mandatoryPar')
        self.assertTrue(self.convertList(usage.get_parameters(1))
                        == 'par1 [optionalPar (o)]')

    def test6011(self):
        """Checking default help"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self): pass

            def print_help(self):
                return True

        self.assertTrue(Simple().process([None, '-h']))

    def test6012(self):
        """Checking default help using alias"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self): pass

            def print_help(self):
                return True

        self.assertTrue(Simple().process([None, '--help']))

    def test6013(self):
        """Checking default help, non getopt mode"""

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self): pass

            def print_help(self):
                return True

        print(Simple(option_prefix='-').process([None, '-help']))
        #self.assertTrue(Simple(option_prefix='-').process([None, '-help']))


if __name__ == '__main__':
    unittest.main()
