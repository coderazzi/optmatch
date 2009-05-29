import unittest

from optmatch import CommandLine, OptMatcherHandler, OptionMatcher, UsageMode
from optmatch import UsageException, OptionMatcherException 
from optmatch import optmatcher, optset 

class Tests(unittest.TestCase):

    def assertRaiseArg(self, exception, exStr, callable, *args, **kwargs):
        try:
            callable(*args, **kwargs)
            self.fail('Expected exception not raised')
        except exception, which:
            self.assertEqual(str(which), exStr)


class InternalTests(Tests):
    '''Tests on internal OptMatcherHandler'''
    
    def test0001(self):
        '''Non getopt mode. Long flag easy'''
        
        def method(aFlag): pass
        
        m = UsageMode('-', '=')
        arg = CommandLine([None, '-a'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1])
        
    def test0002(self):
        '''Non getopt mode. Long flag not given'''
        
        def method(aFlag): pass
        
        m = UsageMode('-', '=')
        arg = CommandLine([None, '-b'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handleArg(arg)
        self.failUnless(ret)
        
    def test0003(self):
        '''Non getopt mode. Long option given'''
        
        def method(aOption): pass
        
        m = UsageMode('-', '=')
        arg = CommandLine([None, '-a=2'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == '2')
    
    def test0004(self):
        '''Providing invalid argument '-' '''
        
        def method(aOption): pass
        
        m = UsageMode('-', '=')
        self.assertRaiseArg(UsageException, 'Unexpected argument -',
                            CommandLine, [None, '-'], m, False)
    
    def test0005(self):
        '''Providing invalid argument '--' '''
        
        def method(aOption): pass
        
        m = UsageMode('--', '=')
        self.assertRaiseArg(UsageException, 'Unexpected argument --',
                            CommandLine, [None, '--'], m, False)
    
    def test0011(self):
        '''Non getopt mode. using kwargs for an option'''
        
        def method(**kwarg): pass
        
        m = UsageMode('-', '=')
        arg = CommandLine([None, '-a=2'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.kwargs == {'a':'2'})
    
    def test0012(self):
        '''Non getopt mode. using kwargs for a flag'''
        
        def method(**kwargs): pass
        
        m = UsageMode('-', '=')
        arg = CommandLine([None, '-a'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.kwargs == {'a':None})
    
    def test0021(self):
        '''Non getopt mode. prefix well given with value'''
        
        def method(DPrefix): pass
        
        m = UsageMode('-', '=')
        arg = CommandLine([None, '-Dname=value'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == [('name', 'value')])
    
    def test0022(self):
        '''Non getopt mode. prefix well given'''
        
        def method(IPrefix): pass
        
        m = UsageMode('-', '=')
        arg = CommandLine([None, '-Iname'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == [('name', None)])
    
    def test0023(self):
        '''Non getopt mode. prefix incorrect'''
        
        def method(IPrefix): pass
        
        m = UsageMode('-', '=')
        arg = CommandLine([None, '-I=name'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException,
                            'Incorrect prefix usage on argument -I=name',
                            ch.handleArg,
                            arg)
        
    def test0024(self):
        '''Prefix are not mandatory options'''
        
        def method(IPrefix):
            return "Called"
        
        ch = OptMatcherHandler(method, UsageMode('-', '='))
        self.assertEquals(ch.invoke(), "Called")
        
    def test0101(self):
        '''Non getopt mode. Long flag with alias'''
        
        def method(aFlag): pass
        
        m = UsageMode('-', '=')
        arg = CommandLine([None, '-aalias'], m, False)
        ch = OptMatcherHandler(method, m)
        ch.setAliases({'a':'aalias'})
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1])
        
    def test0103(self):
        '''Non getopt mode. Long option given with alias'''
        
        def method(aOption): pass
        
        m = UsageMode('-', '=')
        arg = CommandLine([None, '-aalias=2'], m, False)
        ch = OptMatcherHandler(method, m)
        ch.setAliases({'a':'aalias'})
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == '2')
        
    def test0111(self):
        '''Non getopt mode. prefix well given as alias, with value'''
        
        def method(DPrefix): pass
        
        m = UsageMode('-', '=')
        arg = CommandLine([None, '-definename=value'], m, False)
        ch = OptMatcherHandler(method, m)
        ch.setAliases({'D':'define'})    
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == [('name', 'value')])
        
    def test0112(self):
        '''Non getopt mode. prefix well given as alias, without value'''
        
        def method(IPrefix): pass
        
        m = UsageMode('-', '=')
        arg = CommandLine([None, '-includename'], m, False)
        ch = OptMatcherHandler(method, m)
        ch.setAliases({'I':'include'})    
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == [('name', None)])
    
    def test0201(self):
        '''getopt mode. Long flag easy'''
        
        def method(verboseFlag): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '--verbose'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1])
        
    def test0202(self):
        '''getopt mode. Long flag not given'''
        
        def method(verboseFlag): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '--qqw'], m, False)
        ch = OptMatcherHandler(method, m)
        self.failUnless(ch.handleArg(arg))
        
    def test0203(self):
        '''getopt mode. Long option given'''
        
        def method(modeOption): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '--mode=2'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == '2')
    
    def test0211(self):
        '''getopt mode. prefix well given'''
        
        def method(definePrefix): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '--definename=value'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == [('name', 'value')])
        
    def test0212(self):
        '''getopt mode. start flag prefix well given'''
        
        def method(includePrefix): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '--includename'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == [('name', None)])
    
    def test0301(self):
        '''getopt mode. Long flag with alias'''
        
        def method(vFlag): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '--verbose'], m, False)
        ch = OptMatcherHandler(method, m)
        ch.setAliases({'v':'verbose'})
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1])
    
    def test0303(self):
        '''getopt mode. Long option given with alias'''
        
        def method(vOption): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '--verbose=2'], m, False)
        ch = OptMatcherHandler(method, m)
        ch.setAliases({'v':'verbose'})
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == '2')
    
    def test0311(self):
        '''getopt mode. Short option given as long'''
        
        def method(aOption): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '--a=2'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handleArg(arg)
        return ret    
    
    def test0312(self):
        '''getopt mode. Short prefix given as long'''
        
        def method(aPrefix): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '--aValue'], m, False)
        ch = OptMatcherHandler(method, m)
        self.failUnless(ch.handleArg(arg))
    
    def test0313(self):
        '''getopt mode. Short prefix without associated value'''
        
        def method(aPrefix):pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '-a', '-Value'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException, 'Incorrect prefix a',
                            ch.handleArg, arg)
        
    def test0321(self):
        '''getopt mode. Long flag given separated'''
        
        def method(verboseOption): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '--verbose', 'value'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == 'value')
    
    def test0322(self):
        '''getopt mode. Long flag given separated but as option'''
        
        def method(verboseOption): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '--verbose', '-value'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException, 'Incorrect option verbose',
                            ch.handleArg, arg)
    
    def test0323(self):
        '''getopt mode. Long flag given separated but as name/value'''
        
        def method(verboseOption): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '--verbose', 'name=value'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException, 'Incorrect option verbose',
                            ch.handleArg, arg)
    
    def test0401(self):
        '''getopt mode. Short flag given alone'''
        
        def method(vFlag): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '-v'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] and arg.finished())
    
    def test0402(self):
        '''getopt mode. Short option given alone'''
        
        def method(vOption): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '-v1'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == '1' and arg.finished())
    
    def test0403(self):
        '''getopt mode. Short option without value'''
        
        def method(vOption): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '-v'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException, 'Incorrect option v',
                            ch.handleArg, arg)
    
    def test0404(self):
        '''getopt mode. Short option given separately'''
        
        def method(vOption): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '-v', '1'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == '1' and arg.finished())
    
    def test0405(self):
        '''getopt mode. Short option given separately but wrong'''
        
        def method(vOption): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '-v', '-a'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException, 'Incorrect option v',
                            ch.handleArg, arg)
        
    def test0406(self):
        '''getopt mode. Short option given separately, including value'''
        
        def method(vOption): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '-v', 'a=h'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertRaiseArg(UsageException, 'Incorrect option v',
                            ch.handleArg, arg)

    def test0411(self):
        '''getopt mode. A flag given, but not alone'''
        
        def method(vFlag): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '-vw'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] and arg.name == 'w')
            
    def test0501(self):
        '''getopt mode. Flag and Short options given'''
        
        def method(vOption, wFlag): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '-wv', 'q'], m, False)
        ch = OptMatcherHandler(method, m)
        self.failUnless(not ch.handleArg(arg) and not ch.handleArg(arg) 
                        and ch.provided[1] == 'q' and 
                        ch.provided[2] and arg.finished())

    def test0601(self):
        '''getopt mode. Parameter given'''
        
        def method(par1): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, 'file'], m, False)
        ch = OptMatcherHandler(method, m)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.providedPars == ['file'] 
                        and arg.finished())

    def test0602(self):
        '''getopt mode. Two parameters given'''
        
        def method(par1, par2): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, 'file', 'more'], m, False)
        ch = OptMatcherHandler(method, m)
        self.failUnless(not ch.handleArg(arg) and not ch.handleArg(arg)
                        and ch.providedPars == ['file', 'more'] 
                        and arg.finished())

    def test0603(self):
        '''getopt mode. Two parameters given, only one expected'''
        
        def method(par1): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, 'file', 'more'], m, False)
        ch = OptMatcherHandler(method, m)
        self.assertFalse(ch.handleArg(arg) and ch.handleArg(arg)) 

    def test0605(self):
        '''getopt mode. Using vararg for two arguments'''
        
        def method(*var): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, 'file', 'more'], m, False)
        ch = OptMatcherHandler(method, m)
        self.failUnless(not ch.handleArg(arg) and not ch.handleArg(arg) 
                        and arg.finished())

    def test0611(self):
        '''getopt mode. Checking gnu mode'''
        
        def method(aFlag, par1, par2): pass
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '-a', 'par1', '-v'], m, True)
        ch = OptMatcherHandler(method, m)
        self.failUnless(not ch.handleArg(arg)) 
        self.assertRaiseArg(UsageException,
                        'Unexpected argument -v after non option arguments',
                        ch.handleArg, arg)


    def test0621(self):
        '''Checking camel casing'''
        
        def method(dryRunFlag): pass 
        
        m = UsageMode('--', '=')
        arg = CommandLine([None, '--dry-run'], m, True)
        ch = OptMatcherHandler(method, m)
        self.failUnless(not ch.handleArg(arg))


class OptMatcherTests(Tests):
    '''Tests directly on the OptionMatcher interface'''

    def test1001(self):
        '''Simplest case, no args'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self):
                return True
            
        self.failUnless(Simple().process([None]))

    def test1002(self):
        '''Define an optional argument, not provided'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, par=None):
                return True
            
        self.failUnless(Simple().process([None]))

    def test1003(self):
        '''Define an optional flag, not provided'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vFlag=None):
                return True
            
        self.failUnless(Simple().process([None]))

    def test1004(self):
        '''Define an optional option, not provided'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vOption=None):
                return True
            
        self.failUnless(Simple().process([None]))

    def test1011(self):
        '''Define a required flag, not provided'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vFlag): pass
            
        self.assertRaiseArg(UsageException, 'Missing required flag v',
                            Simple().process, [None],
                            handleUsageProblems=False)

    def test1012(self):
        '''Define a required flag, provided'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vFlag):
                return True
            
        self.failUnless(Simple().process([None, '-v']))


    def test1013(self):
        '''Define a required flag, provide two flags'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vFlag): pass
            
        self.assertRaiseArg(UsageException, 'Unexpected flag o in argument -o',
                            Simple().process, [None, '-v', '-o'],
                            handleUsageProblems=False)

    def test1021(self):
        '''Use two flags, one parameter. Flags provided separately'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vFlag, oFlag, par):
                return vFlag, oFlag, par
            
        self.assertEquals(Simple().process([None, '-v', '-o', 'file']),
                          (True, True, 'file'))

    def test1022(self):
        '''Use two flags, one parameter. Flags provided together'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vFlag, oFlag, par):
                return vFlag, oFlag, par
            
        self.assertEquals(Simple().process([None, '-vo', 'file']),
                          (True, True, 'file'))

    def test1023(self):
        '''Use two flags, one parameter. Parameter provided between flags'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vFlag, oFlag, par):
                return vFlag, oFlag, par
            
        self.assertEquals(Simple().process([None, '-v', 'file', '-o']),
                          (True, True, 'file'))

    def test1024(self):
        '''Extended for GNU. Parameter provided between the flags'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vFlag, oFlag, par):
                return vFlag, oFlag, par
            
        self.assertRaiseArg(UsageException,
                        'Unexpected argument -o after non option arguments',
                        Simple().process, [None, '-v', 'file', '-o'],
                        handleUsageProblems=False, gnu=True)

    def test1025(self):
        '''Flag, option, parameter, all provided'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vFlag, oOption, par):
                return vFlag, oOption, par
            
        self.assertEquals(Simple().process([None, '-vo1', 'file']),
                          (True, '1', 'file'))

    def test1026(self):
        '''Verifying that prefixes are not required'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vFlag, oOption, dPrefix, par):
                return vFlag, oOption, dPrefix, par
            
        self.assertEquals(Simple().process([None, '-vo', '1', 'file']),
                          (True, '1', [], 'file'))

    def test1031(self):
        '''Using two matchers'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(vFlag, oOption, par): pass
            
            @optmatcher
            def handle2(self, vFlag, par):
                return vFlag, par
            
        self.assertEquals(Simple().process([None, '-v', 'file']),
                          (True, 'file'))

    def test1032(self):
        '''Two matchers, a common one'''
        
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
        
        self.assertEquals(Simple().process([None, '-v', 'file']),
                          (True, 'file'))

    def test1033(self):
        '''common matcher with flag not provided'''
        
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
            
        self.failUnless(Simple().process([None, 'file']))
        

    def test1034(self):
        '''common matcher with default flag not provided'''
        
        class Simple(OptionMatcher):
            
            @optset
            def common_options(self, vFlag=True):
                self.v = vFlag
            
            @optmatcher
            def handle(self, par):
                return self.v
            
        self.failUnless(Simple().process([None, 'file']))
        

    def test1035(self):
        '''Common matcher, not fully specified'''
        
        class Simple(OptionMatcher):
            
            @optset
            def common_options(self, vFlag, oFlag): pass
            
            @optmatcher
            def handle(self, par): pass
            
        self.assertRaiseArg(UsageException,
                            'Missing required flag v',
                            Simple().process, [None, '-o', 'file'],
                            handleUsageProblems=False)
        

    def test1036(self):
        '''Common matcher, not fully specified, forcing 2nd matcher'''
        
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
        '''Aliases test on common'''
        
        class Simple(OptionMatcher):
            
            @optset
            def common_options(self, vFlag):
                self.v = vFlag
            
            @optmatcher
            def handle(self, oOption, par):                
                return self.v, oOption, par
            
        args = [None, '--verbose', '--option=2', 'file']
        aliases = {'v':'verbose', 'o':'option'}
        self.assertEquals(Simple(aliases=aliases).process(args),
                          (True, '2', 'file'))

    def test1042(self):
        '''Aliases test on common plus varargs'''
        
        class Simple(OptionMatcher):
            
            @optset
            def common_options(self, vFlag):
                self.v = vFlag
            
            @optmatcher
            def handle(self, oOption, *ends):
                return self.v, oOption, ends
        
        args = [None, '--verbose', '--option=2', '1', '2']
        aliases = {'v':'verbose', 'o':'option'}
        self.assertEquals(Simple(aliases=aliases).process(args),
                          (True, '2', ('1', '2')))

    def test1043(self):
        '''Clashing flags by aliases definitions'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, oOption, kOption): pass
            
        self.assertRaises(OptionMatcherException,
                          Simple(aliases={'o':'k'}).process, [])

    def test1044(self):
        '''Clashing flags by aliases definitions short and long'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, oOption, optOption): pass
            
        self.assertRaises(OptionMatcherException,
                          Simple(aliases={'o':'opt'}).process, [])

    def test1045(self):
        '''Clashing flags by aliases definitions, long to short now'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, oOption, optOption): pass
            
        self.assertRaises(OptionMatcherException,
                          Simple(aliases={'opt':'o'}).process, [])

    def test1046(self):
        '''Clashing flags by aliases definitions, not getopt mode'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, oOption, vOption): pass
            
        self.assertRaises(OptionMatcherException,
                          Simple(aliases={'v':'o'}, optionPrefix='-').process,
                          [])

    def test1047(self):
        '''Aliases test, overriding some long definition'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleB(self, verboseFlag=False): pass
        
        aliases = {'v':'verbose'}
        Simple(aliases=aliases).process([None])

    def test1051(self):
        '''Integer options'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, valOptionInt):  
                return valOptionInt
            
        self.assertEquals(Simple().process([None, '--val=2']), 2) 

    def test1052(self):
        '''Integer options, string for integer'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, valOptionInt): pass
            
        self.assertRaiseArg(UsageException, 'Incorrect value for val',
                            Simple().process, [None, '--val=two'],
                            handleUsageProblems=False)

    def test1053(self):
        '''Integer options, float for integer'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, valOptionInt):
                self.ok = valOptionInt
                return True
            
        self.assertRaiseArg(UsageException, 'Incorrect value for val',
                            Simple().process, [None, '--val=2.3'],
                            handleUsageProblems=False)

    def test1054(self):
        '''Float options'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, valOptionFloat):
                return valOptionFloat
            
        self.assertEquals(Simple().process([None, '--val=2.3']), 2.3) 

    def test1055(self):
        '''Float options, string for float'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, valOptionFloat):
                self.ok = valOptionFloat
                return True
            
        self.assertRaiseArg(UsageException, 'Incorrect value for val',
                            Simple().process, [None, '--val=two'],
                            handleUsageProblems=False)

    def test1056(self):
        '''Float options, integer for float'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, valOptionFloat):
                return valOptionFloat
            
        self.assertEquals(Simple().process([None, '--val=2']), 2) 

    def test1057(self):
        '''Parameters for common and matchers'''
        
        class Simple(OptionMatcher):
            
            @optset
            def common(self, par1):
                self.par1 = par1

            @optmatcher
            def handle(self, par2):
                return self.par1, par2
            
        self.assertEquals(Simple().process([None, 'a', 'b']), ('b', 'a'))
        
    def test1101(self):
        '''Using publicNames'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, dFlag):
                return dFlag
            
        self.failUnless(Simple(publicNames={'d':'dry-run'}
                               ).process([None, '--dry-run']))
                 
    def test1102(self):
        '''Using publicNames, expected error'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, dFlag): pass
            
        self.assertRaiseArg(UsageException,
                            'Unexpected flag d in argument -d',
                            Simple(publicNames={'d':'dry-run'}).process,
                            [None, '-d'],
                            handleUsageProblems=False)

    def test1103(self):
        '''Using publicNames, expected error when overriding'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, dFlag, oFlag): pass
            
        self.assertRaiseArg(OptionMatcherException,
                            'o cannot be a public rename, already defined ' + 
                            'in method Simple.handle',
                            Simple(publicNames={'d':'o'}).process,
                            [None])

    def test1104(self):
        '''Using publicNames, expected error when overriding parameter'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, first, second): pass
            
        self.assertRaiseArg(OptionMatcherException,
                            'second cannot be a public rename, already ' + 
                            'defined as parameter in method Simple.handle',
                            Simple(publicNames={'first':'second'}).process,
                            [None])

    def test1105(self):
        '''Using publicNames and aliases'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, dFlag):
                return dFlag
            
        self.failUnless(Simple(publicNames={'d':'dry-run'},
                               aliases={'r':'dry-run'}
                               ).process([None, '-r']))                                  


    def test2001(self):
        '''Checking non getoptMode'''
    
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, oOption, arg):
                return oOption, arg
            
        self.assertEquals(Simple(optionPrefix='/', assigner=':').
                          process([None, '/o:23', 'file']),
                                           ('23', 'file')) 

    def test2002(self):
        '''non getoptMode with aliases'''
    
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, oOption, arg):
                return oOption, arg
            
        self.assertEquals(Simple(aliases={'o':'opt'},
                                 optionPrefix='/', \
                                 assigner=':').
                                 process([None, '/opt:23', 'file']),
                                           ('23', 'file')) 
            
    def test2003(self):
        '''non getoptMode with aliases way around'''
    
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, oOption, arg):
                return oOption, arg
            
        self.assertEquals(Simple(aliases={'opt':'o'},
                                 optionPrefix='/',
                                 assigner=':').
                                 process([None, '/opt:23', 'file']),
                                           ('23', 'file')) 

    def test2101(self):
        '''using several common matchers'''
        
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
        
        self.assertEquals(Simple().process([None, '-rv', 'file', '-k']),
                          (True, True, True, 'file'))

    def test2102(self):
        '''using several common matchers, not fully specified'''
        
        class Simple(OptionMatcher):
            
            @optset
            def common_options1(self, vFlag): pass
            
            @optset
            def common_options2(self, kFlag, aFlag):pass
            
            @optmatcher
            def handle(self, rFlag, par): pass

        self.assertRaiseArg(UsageException,
                            'Missing required flag a',
                            Simple().process, [None, '-rv', 'file', '-k'],
                            handleUsageProblems=False)

    def test2111(self):
        '''Defining a function twice'''
                    
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
        '''Missing optmatcher'''
                    
        class Simple(OptionMatcher):
            
            @optset
            def handle(self): pass

        self.assertRaiseArg(OptionMatcherException,
                            'No matchers defined',
                            Simple().process, [])

    def test2201(self):
        '''Using applies on optset'''
                    
        class Simple(OptionMatcher):
            
            @optset(applies='handle2')
            def set(self, vFlag): 
                pass
            
            @optmatcher
            def handle1(self):return False

            @optmatcher
            def handle2(self):return True

        self.failUnless(Simple().process([None, '-v']))


    def test2202(self):
        '''Using applies on optset, * specified'''
                    
        class Simple(OptionMatcher):
            
            @optset(applies='*')
            def set(self, vFlag): 
                pass
            
            @optmatcher
            def handle1(self):return True

            @optmatcher
            def handle2(self):return False

        self.failUnless(Simple().process([None, '-v']))

    def test2203(self):
        '''Using applies on optset, * specified'''
                    
        class Simple(OptionMatcher):
            
            @optset(applies='handle*')
            def set(self, vFlag): 
                pass
            
            @optmatcher
            def handle1(self):return True

            @optmatcher
            def handle2(self):return False

        self.failUnless(Simple().process([None, '-v']))

    def test2204(self):
        '''Using applies on optset, several specified specified'''
                    
        class Simple(OptionMatcher):
            
            @optset(applies='handle2, handle3')
            def set(self, vFlag): 
                pass
            
            @optmatcher
            def handle1(self):return False

            @optmatcher
            def handle2(self, oOption):return True

            @optmatcher
            def handle3(self):return True

        self.failUnless(Simple().process([None, '-v']))

    def test2211(self):
        '''Using exclsuive on optmatcher'''
                    
        class Simple(OptionMatcher):
            
            @optset
            def set(self, vFlag): 
                pass
            
            @optmatcher(exclusive=True)
            def handle1(self):return False

            @optmatcher
            def handle2(self):return True


        self.failUnless(Simple().process([None, '-v']))


class OptMatcherTestsOnDecoration(Tests):
    '''Tests on the OptionMatcher decorators'''

    def test3011(self):
        '''defining flag via decorator'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='o')
            def handleA(self, o):
                return True

        self.failUnless(Simple().process([None, '-o']))

    def test3012(self):
        '''defining flags via decorator'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='o, v')
            def handleA(self, o, v):
                return o and v
            
        self.failUnless(Simple().process([None, '-ov']))

    def test3013(self):
        '''defining flags exclusively via decorator'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='o, v')
            def handleA(self, o, v, wFlag):
                return o and v and wFlag == 'w'
            
        self.failUnless(Simple().process([None, '-ov', 'w']))

    def test3014(self):
        '''defining flag with as'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='verbose as v')
            def handleA(self, verbose):
                return verbose
            
        self.failUnless(Simple().process([None, '-v']))

    def test3015(self):
        '''defining flags with as, and without'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='verbose as v, o')
            def handleA(self, verbose, o):
                return verbose and o
            
        self.failUnless(Simple().process([None, '-vo']))

    def test3016(self):
        '''defining a parameter with different name'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='o', renamePars='va as file')
            def handleA(self, o, va):
                return o and va == 'f'
            
        self.failUnless(Simple().process([None, '-o', 'f']))

    def test3017(self):
        '''Renaming a parameter without as'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(renamePars='v')
            def handleA(self, v):
                return True
            
        self.assertRaiseArg(OptionMatcherException,
                            'Invalid renamePar v',
                            Simple().process, [None])

    def test3018(self):
        '''Renaming a parameter with invalid as'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(renamePars='v as v')
            def handleA(self, v):
                return True
            
        self.assertRaiseArg(OptionMatcherException,
                            'Invalid renamePar v',
                            Simple().process, [None])

    def test3019(self):
        '''Defining a non existing option'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(options='k')
            def handleA(self, o):
                return True
            
        self.assertRaiseArg(OptionMatcherException,
                            'Invalid argument: k',
                            Simple().process, [None])

    def test3020(self):
        '''Defining a non existing flag (orphan)'''
    
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, o):
                return False

            @optmatcher(flags='k')
            def handleB(self, o):
                return True
            
        self.failUnless(Simple().process([None, '-k', 'o']))

    def test3021(self):
        '''Defining a non existing flag with as'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='k as o')
            def handleB(self): 
                pass
            
        self.assertRaiseArg(OptionMatcherException,
                            'Invalid argument: k',
                            Simple().process, [None])

    def test3022(self):
        '''Defining a non existing flag with as, even if equal'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='k as k')
            def handleB(self): 
                pass
            
        self.assertRaiseArg(OptionMatcherException,
                            'Invalid argument: k',
                            Simple().process, [None])

    def test3023(self):
        '''Orphan flag are mandatory'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='k')
            def handleB(self):
                pass
            
        self.assertRaiseArg(UsageException, 'Missing required flag k',
                            Simple().process, [None],
                            handleUsageProblems=False)
        
    def test3031(self):
        '''Full decoration'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='o,v', options='w', prefixes='d as D',
                        intOptions='i', floatOptions='f',
                        renamePars='par as class', priority=1)
            def handleA(self, o, v, w, d, i, f, par):
                return o, v, w, d, i, f, par
        
        args = [None, '-oww', '-vi1', '-f', '2.3', '-Dvalue', 'class']
        self.assertEquals(Simple().process(args),
                                         (True, True, 'w', [('value', None)],
                                          1, 2.3, 'class'))

    def test3022(self):
        '''Full decoration, using also optset'''
    
        class Simple(OptionMatcher):
            
            @optset(intOptions='m as mode')
            def common(self, m):
                self.m = m
            
            @optmatcher(flags='o,v', options='w', prefixes='d as D',
                        intOptions='i', floatOptions='f',
                        renamePars='par as class', priority=1)
            def handleA(self, o, v, w, d, i, f, par):
                return self.m, o, v, w, d, i, f, par

        args = [None, '-oww', '--mode=23', '-vi1', '-f', '2.3', '-Dvalue',
              'class']
        self.assertEquals(Simple().process(args),
                          (23, True, True, 'w', [('value', None)],
                           1, 2.3, 'class'))

    def test3031(self):
        '''Setting priorities'''
    
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, oFlag):pass
            
            @optmatcher(priority=1)
            def handleB(self, oFlag):
                return True
            
            @optmatcher
            def handleC(self, oFlag): pass
            
        self.failUnless(Simple().process([None, '-o']))
 
    def test3041(self):
        '''Setting priorities on optset'''
    
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
            
        self.failUnless(Simple().process([None, '-ok']))

    def test3042(self):
        '''Setting priorities on optset, way around'''
    
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
            
        self.failIf(Simple().process([None, '-ok'])) 



class OptMatcherTestsOnErrorMessages(Tests):
    '''Tests on the OptionMatcher error messages'''

    def test4001(self):
        '''Message error: unexpected flag'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='o')
            def handleA(self, o): pass

        self.assertRaiseArg(UsageException,
                            'Unexpected flag v in argument -v',
                            Simple().process, [None, '-v'],
                            handleUsageProblems=False)

    def test4002(self):
        '''Message error: required flag'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='o')
            def handleA(self, o): pass

        self.assertRaiseArg(UsageException,
                            'Missing required flag o',
                            Simple().process, [None],
                            handleUsageProblems=False)

    def test4003(self):
        '''Message error: unexpected parameter'''
    
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self): pass

        self.assertRaiseArg(UsageException,
                            'Unexpected argument: file',
                            Simple(defaultHelp=False).process, [None, 'file'],
                            handleUsageProblems=False)

    def test4004(self):
        '''Message error: required parameter'''
    
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, name): pass

        self.assertRaiseArg(UsageException,
                            'Missing required parameter name',
                            Simple().process, [None],
                            handleUsageProblems=False)

    def test4005(self):
        '''Message error: required parameter, changed on decorator'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(renamePars='c as class')
            def handleA(self, c): pass

        self.assertRaiseArg(UsageException,
                            'Missing required parameter class',
                            Simple().process, [None],
                            handleUsageProblems=False)


    def test4011(self):
        '''Message error: coming from lower priority matcher'''
    
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, vFlag, kFlag): pass

            @optmatcher
            def handleB(self, oFlag, pOption): pass

        self.assertRaiseArg(UsageException,
                            'Missing required option p',
                            Simple().process, [None, '-o'])

    def test4011(self):
        '''Message error: coming from lower priority matcher on shorts'''
    
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, vFlag, kFlag, oFlag): pass

            @optmatcher
            def handleB(self, vFlag, pFlag, qFlag): pass

        self.assertRaiseArg(UsageException,
                            'Unexpected flag r in argument -vpr',
                            Simple().process, [None, '-vpr'],
                            handleUsageProblems=False)

    def test4012(self):
        '''Message error: higher complexity'''
    
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, vFlag, pFlag, oFlag, *args): pass

            @optmatcher
            def handleB(self, vFlag, pFlag, qFlag): pass

        self.assertRaiseArg(UsageException,
                            'Unexpected flag q in argument -q',
                            Simple().process, [None, '-vp', 'arg', '-q'],
                            handleUsageProblems=False)


class UsageTests(Tests):
    '''Tests on internal OptMatcherHandler'''
    
    def checkString(self, received, expected):
        receivedSplit = received.split('\n')
        expectedSplit = expected.split('\n')
        for i, (lineR, lineE) in enumerate(zip(receivedSplit, expectedSplit)):
            if lineR != lineE:
                print 'Line', i + 1, 'Received:', lineR
                print 'Line', i + 1, 'Expected:', lineE
                self.fail('Line ' + str(i + 1) + ' ' + lineR + 
                          '\nAnd expected: ' + lineE)
        self.failUnless(len(receivedSplit) == len(expectedSplit))
        
    def convertList(self, list):
        return ' '.join([str(l) for l in list])
        
    def test6001(self):
        '''Basic help tests'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vFlag, oOption, par1, par2): pass
    
            @optmatcher
            def handle2(self, vFlag, kFlag, par1, *args): pass
            
        usage = Simple().getUsage()
        self.failUnless(usage.getAllParameters() == 
                        'par1 par2 ...')
        self.failUnless(self.convertList(usage.getParameters(0))
                        == 'par1 par2')
        self.failUnless(self.convertList(usage.getParameters(1))
                        == 'par1 ...')
        self.failUnless(self.convertList(usage.getAllOptions()) == 
                        '-h -k -v -o O')
    
    def test6002(self):
        '''Basic help tests, added optset'''
        
        class Simple(OptionMatcher):
            
            @optset
            def other(self, vFlag, arg, rOption='r'): pass
            
            @optmatcher
            def handle(self, vFlag, oOption, par1, par2): pass
    
            @optmatcher
            def handle2(self, vFlag, kFlag, par1, *args): pass
            
        usage = Simple().getUsage()
        self.failUnless(self.convertList(usage.getParameters(0))
                        == 'par1 par2 arg')
        self.failUnless(self.convertList(usage.getParameters(1))
                        == 'par1 ...')
        self.failUnless(self.convertList(usage.getParameters(2))
                        == '')
        self.failUnless(usage.getAllParameters() == 
                        'par1 par2 arg ...')
        self.failUnless(self.convertList(usage.getAllOptions()) == 
                        '-h -k -v -o O [-r R (r)]')
    
    def test6003(self):
        '''Basic help tests, added optsetm, with exclusive on optmatcher'''
        
        class Simple(OptionMatcher):
            
            @optset
            def other(self, vFlag, arg, rOption='r'): pass
            
            @optmatcher(exclusive=True)
            def handle(self, vFlag, oOption, par1, par2): pass
    
            @optmatcher
            def handle2(self, vFlag, kFlag, par1, *args): pass
            
        usage = Simple().getUsage()
        self.failUnless(self.convertList(usage.getParameters(0))
                        == 'par1 par2')
        self.failUnless(self.convertList(usage.getParameters(1))
                        == 'par1 ...')
        self.failUnless(self.convertList(usage.getParameters(2))
                        == '')
        self.failUnless(usage.getAllParameters() == 
                        'par1 par2 ...')
        self.failUnless(self.convertList(usage.getAllOptions()) == 
                        '-h -k -v -o O [-r R (r)]')
    
    def test6004(self):
        '''Global help test'''
        
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
                '''Executes this program repeatedly until everybody is tired''' 
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
        
        
        aliases = {'v':'verbose',
                   'f':'filename',
                   'i':'include',
                   'D':'define',
                   'm':'mode'}
        info = {'v':'lot of useless info is output',
              'D': 'create a new prefix',
              'f':'write output to FILE',
              'm':'interaction mode: novice, intermediate, or ' + 
                    'expert [default: intermediate]'}
        vars = {'d':'DX', 'i':'IN', 'f':'FILE'}
        usage = Simple(aliases=aliases, optionsHelp=info,
                     optionVarNames=vars, defaultHelp=False).getUsage()    
        
        expected = '''Usage: [common options] arg1 arg2 arg3 addpar ...

options:
  -b
  --common
  --common2
  -p
  --super
  -v, --verbose         lot of useless info is output
  -w
  --common-opt=COMMON_OPT
  -D DEFINE, --define=DEFINE
                        create a new prefix
  -d DX
  -f FILE, --filename=FILE
                        write output to FILE
  -i IN, --include=IN
  -m MODE, --mode=MODE  interaction mode: novice, intermediate, or
                        expert [default: intermediate]

alternatives:

* -b --common -D DEFINE -d DX -f FILE [--common-opt=COMMON_OPT (23)]
  [-i IN (34)] [-w (True)] one [two (2)] ...
                        Executes this program repeatedly until everybody
                        is tired

* -b --common --common2 -d DX -m MODE -p [--common-opt=COMMON_OPT (23)]
  [-i IN (68)] [-v (False)] one [commonPar (po)] [addpar (3)]

* --common2 -p [-i IN (68)] [-v (False)] one three four [addpar (3)]

* -b --common -d DX --super [--common-opt=COMMON_OPT (23)]
  [commonPar (po)]'''
        
        self.checkString(usage.getUsageString(), expected)
        
    def test6005(self):
        '''Additional global help test'''
        
        class Simple(OptionMatcher):
            
            @optset
            def other(self, vFlag, arg, rOption='r'): pass
            
            @optmatcher(exclusive=True)
            def handle(self, vFlag, oOption, par1, par2): pass
    
            @optmatcher
            def handle2(self, vFlag, kFlag, par1, *args): pass
            
        aliases = {'v':'verbose',
                   'o':'open'}
        info = {'v':'lot of useless info is output',
                'o':'sets open mode'}
        vars = {'o':'MODE'}
        usage = Simple(aliases=aliases, optionsHelp=info,
                     optionVarNames=vars, defaultHelp=True).getUsage()
        expected = '''Usage: [common options] par1
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
     -r R'''

        self.checkString(usage.getUsageString(width=30, column=15, ident=5,
                         includeAlternatives=False), expected)
    
    def test6006(self):
        '''Verifying optionality on arguments'''
        
        class Simple(OptionMatcher):
            
            @optset
            def other(self, mandatoryPar): pass
            
            @optmatcher
            def handle(self, par1, optionalPar='o'): pass
    
            @optmatcher(exclusive=True)
            def handle2(self, par1, optionalPar='o'): pass
    
        usage = Simple().getUsage()
        #note that optionalPar in handle is not treated as optional anymore
        self.failUnless(self.convertList(usage.getParameters(0))
                        == 'par1 optionalPar mandatoryPar')
        self.failUnless(self.convertList(usage.getParameters(1))
                        == 'par1 [optionalPar (o)]')

    def test6011(self):
        '''Checking default help'''

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self):pass

            def printHelp(self):
                return True

        self.failUnless(Simple().process([None, '-h']))

    def test6012(self):
        '''Checking default help using alias'''

        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self):pass

            def printHelp(self):
                return True

        self.failUnless(Simple().process([None, '--help']))

    def test6013(self):
        '''Checking default help, non getopt mode'''

        class Simple(OptionMatcher):

            @optmatcher
            def handle(self):pass

            def printHelp(self):
                return True

        self.failUnless(Simple(optionPrefix='-').process([None, '-help']))




        
if __name__ == '__main__':
    unittest.main()
