import unittest

from optmatch import CommandLine, OptMatcherHandler, OptionMatcher, UsageMode
from optmatch import UsageException, OptionMatcherException 
from optmatch import optmatcher, optcommon 

#class MandatoryTests(unittest.TestCase):
#
#    def assertRaiseArg(self, exception, exStr, callable, *args, **kwargs):
#        try:
#            callable(*args, **kwargs)
#            self.fail('Expected exception not raised')
#        except exception, which:
#            self.assertEqual(str(which), exStr)
#            
#    def test1042(self):
#        '''Aliases test using common, varargs'''
#        
#        class Simple(OptionMatcher):
#            
#            @optcommon
#            def common_options(self, vFlag):
#                self.v = vFlag
#            
#            @optmatcher
#            def handle(self, oOption, *ends):
#                return self.v, oOption, ends
#        
#        args = [None, '--verbose', '--option=2', '1', '2']
#        aliases = {'v':'verbose', 'o':'option'}
#        self.assertEquals(Simple(aliases=aliases).process(args),
#                          (True, '2', ('1', '2')))
#
#
#class Tests:
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
        self.failUnless(not ch.handleArg(arg) and not ch.handleArg(arg) 
                        and not ch.handleArg(arg) and arg.finished())


class OptMatcherTests(Tests):
    '''Tests directly on the OptionMatcher interface'''

    def test1001(self):
        '''Simple test, no args'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self):
                return True
            
        self.failUnless(Simple().process([None]))

    def test1002(self):
        '''Simple test, one optional parameter, not given'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, par=None):
                return True
            
        self.failUnless(Simple().process([None]))

    def test1003(self):
        '''Simple test, one optional flag, not given'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vFlag=None):
                return True
            
        self.failUnless(Simple().process([None]))

    def test1004(self):
        '''Simple test, one optional option, not given'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vOption=None):
                return True
            
        self.failUnless(Simple().process([None]))

    def test1011(self):
        '''Simple test, one flag, not given'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vFlag): pass
            
        self.assertRaiseArg(UsageException, 'Missing required flag v',
                            Simple().process, [None])

    def test1012(self):
        '''Simple test, one flag, given'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vFlag):
                return True
            
        self.failUnless(Simple().process([None, '-v']))


    def test1013(self):
        '''Simple test, one flag, two given'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vFlag): pass
            
        self.assertRaiseArg(UsageException, 'Missing required flag v',
                            Simple().process, [None])

    def test1021(self):
        '''More complex test, two flags, one parameter'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vFlag, oFlag, par):
                return vFlag, oFlag, par
            
        self.assertEquals(Simple().process([None, '-vo', 'file']),
                          (True, True, 'file'))

    def test1022(self):
        '''More complex test, one flag, one option, one parameter'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vFlag, oOption, par):
                return vFlag, oOption, par
            
        self.assertEquals(Simple().process([None, '-vo1', 'file']),
                          (True, '1', 'file'))

    def test1023(self):
        '''More complex test, a flag, a separated option, one parameter'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vFlag, oOption, par):
                return vFlag, oOption, par
            
        self.assertEquals(Simple().process([None, '-vo1', 'file']),
                          (True, '1', 'file'))

    def test1024(self):
        '''Verifying that prefixes are not required'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vFlag, oOption, dPrefix, par):
                return vFlag, oOption, dPrefix, par
            
        self.assertEquals(Simple().process([None, '-vo', '1', 'file']),
                          (True, '1', [], 'file'))

    def test1031(self):
        '''More complex test, two possible handlers'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(vFlag, oOption, par): pass
            
            @optmatcher
            def handle2(self, vFlag, par):
                return vFlag, par
            
        self.assertEquals(Simple().process([None, '-v', 'file']),
                          (True, 'file'))

    def test1032(self):
        '''More complex test, two possible handlers and a common one'''
        
        class Simple(OptionMatcher):
            
            @optcommon
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
        '''More complex test, two possible handlers and a common, not given
        '''
        
        class Simple(OptionMatcher):
            
            @optcommon
            def common_options(self, vFlag):
                pass
            
            @optmatcher
            def handle(self, oOption, par):
                pass
            
            @optmatcher
            def handle2(self, par):
                pass
            
        self.assertRaiseArg(UsageException, 'Missing required flag v',
                            Simple().process, [None, 'file'])

    def test1041(self):
        '''Aliases test using common'''
        
        class Simple(OptionMatcher):
            
            @optcommon
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
        '''Aliases test using common, varargs'''
        
        class Simple(OptionMatcher):
            
            @optcommon
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
        '''Aliases test, overriding some definition'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, oOption, kOption): pass
            
        self.assertRaises(OptionMatcherException,
                          Simple(aliases={'o':'k'}).process, [])

    def test1044(self):
        '''Aliases test, overriding some definition -long '''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, oOption, optOption): pass
            
        self.assertRaises(OptionMatcherException,
                          Simple(aliases={'o':'opt'}).process, [])

    def test1045(self):
        '''Aliases test, overriding some definition, way round'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, oOption, optOption): pass
            
        self.assertRaises(OptionMatcherException,
                          Simple(aliases={'opt':'o'}).process, [])

    def test1046(self):
        '''Aliases test, overriding some definition, not getopt mode'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, oOption, vOption): pass
            
        self.assertRaises(OptionMatcherException,
                          Simple(aliases={'v':'o'}, optionPrefix='-').process, [])

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
                            Simple().process, [None, '--val=two'])

    def test1053(self):
        '''Integer options, float for integer'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, valOptionInt):
                self.ok = valOptionInt
                return True
            
        self.assertRaiseArg(UsageException, 'Incorrect value for val',
                            Simple().process, [None, '--val=2.3'])

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
                            Simple().process, [None, '--val=two'])

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
            
            @optcommon
            def common(self, par1):
                self.par1 = par1

            @optmatcher
            def handle(self, par2):
                return self.par1, par2
            
        self.assertEquals(Simple().process([None, 'a', 'b']), ('a', 'b')) 

    def test2001(self):
        '''API test: non getoptMode'''
    
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, oOption, arg):
                return oOption, arg
            
        self.assertEquals(Simple(optionPrefix='/', assigner=':').
                          process([None, '/o:23', 'file']),
                                           ('23', 'file')) 

    def test2002(self):
        '''API test: non getoptMode with aliases'''
    
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
        '''API test: non getoptMode with aliases way around'''
    
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, oOption, arg):
                return oOption, arg
            
        self.assertEquals(Simple(aliases={'opt':'o'},
                                 optionPrefix='/',
                                 assigner=':').
                                 process([None, '/opt:23', 'file']),
                                           ('23', 'file')) 

    def test2011(self):
        '''API test: specifying external common handler'''
        
        class Any(object):
            
            @staticmethod
            def specificCommonHandler(oOption):
                Any.oOption = oOption
            
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, arg):
                return Any.oOption, arg
            
        s = Simple()
        s.setMatchers(None, Any.specificCommonHandler)
        self.assertEquals(s.process([None, '-o23', 'file']), ('23', 'file')) 

    def test2012(self):
        '''API test: specifying external handlers as methods'''
        
        class Any(object):
            
            @staticmethod
            def myOwnHandler(oOption, par):
                return oOption, par
            
        s = OptionMatcher()
        s.setMatchers([Any.myOwnHandler])
        self.assertEquals(s.process([None, '-o23', 'file']), ('23', 'file')) 

    def test2021(self):
        '''API test: specifying static method as command handler'''
        
        class Simple(object):
            
            @staticmethod        
            def handle(f):
                return f
            
        s = OptionMatcher()
        s.setMatchers([Simple.handle])
        self.assertEquals(s.process([None, 'ok']), 'ok')

    def test2022(self):
        '''API test: specifying incorrect flags on command handler'''
        
        def work(aFlag, aOption): pass
        
        s = OptionMatcher()
        s.setMatchers([work])
        self.assertRaiseArg(OptionMatcherException,
                            'Repeated option "a" in function work',
                            s.process, [None])


class OptMatcherTestsOnDecoration(Tests):
    '''Tests on the OptionMatcher decorators'''

    def test3011(self):
        '''API test: defining flag via decorator'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='o')
            def handleA(self, o):
                return True

        self.failUnless(Simple().process([None, '-o']))

    def test3012(self):
        '''API test: defining flags via decorator'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='o, v')
            def handleA(self, o, v):
                return o and v
            
        self.failUnless(Simple().process([None, '-ov']))

    def test3013(self):
        '''API test: defining flags exclusively via decorator'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='o, v')
            def handleA(self, o, v, wFlag):
                return o and v and wFlag == 'w'
            
        self.failUnless(Simple().process([None, '-ov', 'w']))

    def test3014(self):
        '''API test: defining flag with as, exclusively via decorator'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='verbose as v')
            def handleA(self, verbose):
                return verbose
            
        self.failUnless(Simple().process([None, '-v']))

    def test3015(self):
        '''API test: defining flags with as, exclusively via decorator'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='verbose as v, o')
            def handleA(self, verbose, o):
                return verbose and o
            
        self.failUnless(Simple().process([None, '-vo']))

    def test3016(self):
        '''API test: defining a parameter with different name'''
    
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
        '''Defining a non existing flag'''
    
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
        '''Non existing flag are required'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='k')
            def handleB(self):
                pass
            
        self.assertRaiseArg(UsageException, 'Missing required flag k',
                            Simple().process, [None])
        
    def test3031(self):
        '''API test: defining all via decorator'''
    
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

    def test3022O(self):
        '''API test: defining all via decorator, using also optcommon'''
    
        class Simple(OptionMatcher):
            
            @optcommon(intOptions='m as mode')
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
        '''API test: setting priorities'''
    
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, oFlag):pass
            
            @optmatcher(priority=1)
            def handleB(self, oFlag):
                return True
            
            @optmatcher
            def handleC(self, oFlag): pass
            
        self.failUnless(Simple().process([None, '-o']))

    def test3032(self):
        '''API test: setting priorities on optcommon'''
    
        class Simple(OptionMatcher):
            
            @optcommon(priority=1)
            def handleA(self, oFlag): pass
            
            @optcommon(priority=2)
            def handleB(self, oFlag):
                self.o = oFlag
            
            @optmatcher
            def handleC(self, *args):
                return self.o, args
            
            
        self.assertEquals(Simple().process([None, '-o', '1', '2', '3']),
                          (True, ('1', '2', '3')))

class OptMatcherTestsOnErrorMessages(Tests):
    '''Tests on the OptionMatcher error messages'''

    def test4001(self):
        '''Message error: unexpected flag'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='o')
            def handleA(self, o): pass

        self.assertRaiseArg(UsageException,
                            'Unexpected flag v in argument -v',
                            Simple().process, [None, '-v'])

    def test4002(self):
        '''Message error: required flag'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='o')
            def handleA(self, o): pass

        self.assertRaiseArg(UsageException,
                            'Missing required flag o',
                            Simple().process, [None])

    def test4003(self):
        '''Message error: unexpected parameter'''
    
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self): pass

        self.assertRaiseArg(UsageException,
                            'Unexpected argument: file',
                            Simple().process, [None, 'file'])

    def test4004(self):
        '''Message error: required parameter'''
    
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, name): pass

        self.assertRaiseArg(UsageException,
                            'Missing required parameter name',
                            Simple().process, [None])

    def test4005(self):
        '''Message error: required parameter, changed on decorator'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(renamePars='c as class')
            def handleA(self, c): pass

        self.assertRaiseArg(UsageException,
                            'Missing required parameter class',
                            Simple().process, [None])


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
                            Simple().process, [None, '-vpr'])

    def test4012(self):
        '''Message error: higher complexity'''
    
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, vFlag, pFlag, oFlag, *args): pass

            @optmatcher
            def handleB(self, vFlag, pFlag, qFlag): pass

        self.assertRaiseArg(UsageException,
                            'Unexpected flag q in argument -q',
                            Simple().process, [None, '-vp', 'arg', '-q'])


class OptMatcherTestsWrongSyntax(Tests):
    '''Tests to verify incorrect syntax'''

    def test5001(self):
        '''Matchers are required'''
        class Simple(OptionMatcher):
            pass
            
        self.assertRaiseArg(OptionMatcherException,
                            'No matchers defined',
                            Simple(defaultHelp=False).check)

    def test5002(self):
        '''Matchers are required. optcommon, not enough'''
        class Simple(OptionMatcher):
            
            @optcommon
            def common(self): pass
            
        self.assertRaiseArg(OptionMatcherException,
                            'No matchers defined',
                            Simple(defaultHelp=False).check)

    def test5003(self):
        '''Matchers are required, given in any way'''
        class Simple(OptionMatcher):
            
            def handle(self): pass 
                
        
        s = Simple()
        s.setMatchers([s.handle])
        s.check()
        self.assert_(True)
        
    def test5011(self):
        '''Problems with common handler accepting varargs'''
        
        class Simple(OptionMatcher):
            
            @optcommon
            def handleA(self, *args): pass

            @optmatcher
            def handleB(self, arg): pass

        self.assertRaiseArg(OptionMatcherException,
                            'method Simple.handleB cannot be invoked: ' + 
                            'common handler accepts varargs',
                            Simple().check)

    def test5012(self):
        '''Common handler can accept varargs (if matchers have no pars)'''
        class Simple(OptionMatcher):
            
            @optcommon
            def handleA(self, *args): pass

            @optmatcher
            def handleB(self): pass

        Simple(defaultHelp=False).check()
        self.assert_(True)

    def test5013(self):
        '''common handler can accept varargs (if matchers have only options)'''
        class Simple(OptionMatcher):
            
            @optcommon
            def handleA(self, *args): pass

            @optmatcher
            def handleB(self, kFlag): pass

        Simple(defaultHelp=False).check()
        self.assert_(True)

    def test5014(self):
        '''common handler can accept varargs (if matchers have default pars)'''
        class Simple(OptionMatcher):
            
            @optcommon
            def handleA(self, *args): pass

            @optmatcher
            def handleB(self, par='file'): pass

        Simple(defaultHelp=False).check()
        self.assert_(True)

    def test5021(self):
        '''Problem with kwargs in common handler'''
        class Simple(OptionMatcher):
            
            @optcommon
            def handleA(self, **args): pass

            @optmatcher
            def handleB(self, kFlag): pass

        self.assertRaiseArg(OptionMatcherException,
                            'method Simple.handleB cannot be invoked: ' + 
                            'common handler accepts kwargs',
                            Simple(optionPrefix='-').check)

    def test5022(self):
        '''No Problem with kwargs in common in getopt mode'''
        class Simple(OptionMatcher):
            
            @optcommon
            def handleA(self, **args): pass

            @optmatcher
            def handleB(self, kFlag): pass

        Simple().check()
        self.assert_(True)

    def test5023(self):
        '''No Problem with kwargs in common if matchers have defaults'''
        class Simple(OptionMatcher):
            
            @optcommon
            def handleA(self, **args): pass

            @optmatcher
            def handleB(self, kFlag=False): pass

        Simple(optionPrefix='-', defaultHelp=False).check()
        self.assert_(True)

    def test5031(self):
        '''Problem on two handles with same parameters (None)'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self): pass

            @optmatcher
            def handleB(self): pass

        self.assertRaiseArg(OptionMatcherException,
                        'method Simple.handleB cannot be invoked: ' + 
                        'method Simple.handleA will be always invoked first',
                         Simple().check)

    def test5032(self):
        '''Problem on two handles with same parameters (a flag)'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, kFlag): pass

            @optmatcher
            def handleB(self, kFlag): pass

        self.assertRaiseArg(OptionMatcherException,
                        'method Simple.handleB cannot be invoked: ' + 
                        'method Simple.handleA will be always invoked first',
                         Simple().check)

    def test5034(self):
        '''Problem on two handles with same parameters (an option)'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, kOption): pass

            @optmatcher
            def handleB(self, kOption): pass

        self.assertRaiseArg(OptionMatcherException,
                        'method Simple.handleB cannot be invoked: ' + 
                        'method Simple.handleA will be always invoked first',
                         Simple().check)

    def test5036(self):
        '''No problem on two handles with same parameters if 2. optional'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, kFlag): pass

            @optmatcher
            def handleB(self, kFlag=True): pass

        Simple().check()
        self.assert_(True)

    def test5037(self):
        '''problem on two handles with same parameters if 1. optional'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, kFlag=True): pass

            @optmatcher
            def handleB(self, kFlag): pass

        self.assertRaiseArg(OptionMatcherException,
                        'method Simple.handleB cannot be invoked: ' + 
                        'method Simple.handleA will be always invoked first',
                         Simple().check)

    def test5041(self):
        '''problem on two handles with same n. mandatory parameters'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, one, two): pass

            @optmatcher
            def handleB(self, one, two): pass

        self.assertRaiseArg(OptionMatcherException,
                        'method Simple.handleB cannot be invoked: ' + 
                        'method Simple.handleA will be always invoked first',
                         Simple().check)

    def test5042(self):
        '''problem on two handles with less mandatory parameters'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, one): pass

            @optmatcher
            def handleB(self, one, two): pass

        Simple().check()
        self.assert_(True)

    def test5043(self):
        '''problem on two handles with more mandatory parameters'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, one, two): pass

            @optmatcher
            def handleB(self, one): pass

        Simple().check()
        self.assert_(True)

    def test5044(self):
        '''problem on two handles with same n. mandatory, less optional'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, one, two): pass

            @optmatcher
            def handleB(self, one, two, third='o'): pass

        Simple().check()
        self.assert_(True)

    def test5045(self):
        '''problem on two handles with less mandatory &optional parameters'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, one): pass

            @optmatcher
            def handleB(self, one, two, third='o'): pass

        Simple().check()
        self.assert_(True)

    def test5046(self):
        '''problem on two handles with more mandatory, less optional'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, one, two): pass

            @optmatcher
            def handleB(self, one, third='o'): pass

        Simple().check()
        self.assert_(True)

    def test5047(self):
        '''problem on two handles with same n. mandatory, more optional'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, one, two, third='o'): pass

            @optmatcher
            def handleB(self, one, two): pass

        self.assertRaiseArg(OptionMatcherException,
                        'method Simple.handleB cannot be invoked: ' + 
                        'method Simple.handleA will be always invoked first',
                         Simple().check)

    def test5048(self):
        '''problem on two handles with less mandatory , more parameters'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, one, third='o'): pass

            @optmatcher
            def handleB(self, one, two): pass

        self.assertRaiseArg(OptionMatcherException,
                        'method Simple.handleB cannot be invoked: ' + 
                        'method Simple.handleA will be always invoked first',
                         Simple().check)

    def test5049(self):
        '''problem on two handles with more mandatory &  optional'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, one, two, third='o'): pass

            @optmatcher
            def handleB(self, one, third='o'): pass

        Simple().check()
        self.assert_(True)


    def test5050(self):
        '''problem on two handles/parameters'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, one, two, third='o'): pass

            @optmatcher
            def handleB(self, one, two='a', third='a'): pass

        Simple().check()
        self.assert_(True)


    def test5061(self):
        '''problem on clashing options with common'''
        class Simple(OptionMatcher):
            
            @optcommon
            def handleA(self, kFlag, oFlag): pass

            @optmatcher
            def handleB(self, kFlag, pFlag): pass

        self.assertRaiseArg(OptionMatcherException,
                        'method Simple.handleB defines clashing options ' + 
                        'with the common matcher method Simple.handleA : k',
                         Simple().check)

    def test5062(self):
        '''problem on clashing options with common. type is dismissed'''
        class Simple(OptionMatcher):
            
            @optcommon
            def handleA(self, kFlag, oFlag): pass

            @optmatcher
            def handleB(self, kOption, pFlag): pass

        self.assertRaiseArg(OptionMatcherException,
                        'method Simple.handleB defines clashing options ' + 
                        'with the common matcher method Simple.handleA : k',
                         Simple().check)

    def test5063(self):
        '''problem on clashing options with common. alias apply'''
        class Simple(OptionMatcher):
            
            @optcommon
            def handleA(self, cFlag, oFlag): pass

            @optmatcher
            def handleB(self, courierOption, pFlag): pass

        self.assertRaiseArg(OptionMatcherException,
                        'method Simple.handleB defines clashing options ' + 
                        'with the common matcher method Simple.handleA : c',
                         Simple(aliases={'c':'courier'}).check)

    def test5071(self):
        '''problem on defining an option on different ways'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, kFlag): pass

            @optmatcher
            def handleB(self, kOption): pass

        self.assertRaiseArg(OptionMatcherException,
                           'Flag k in method Simple.handleA is defined as ' + 
                           'Option in method Simple.handleB',
                           Simple().check)

    def test5072(self):
        '''problem on defining an option on different ways, through aliases'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, kFlag): pass

            @optmatcher
            def handleB(self, koOption): pass

        self.assertRaiseArg(OptionMatcherException,
                           'Flag k in method Simple.handleA is defined as ' + 
                           'Option in method Simple.handleB',
                           Simple(aliases={'k':'ko'}).check)

    def test5081(self):
        '''problem on defining help for multiple aliases of an option'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, kFlag): pass

        self.assertRaiseArg(OptionMatcherException,
                           'optionsHelp defines information for aliases k, ko',
                           Simple(aliases={'k':'ko'},
                                  optionsHelp={'k':'', 'ko':''}).check)

    def test5082(self):
        '''problem on defining help for unknown option'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self): pass

        self.assertRaiseArg(OptionMatcherException,
                           'optionsHelp defines information for unknown: k',
                           Simple(optionsHelp={'k':''}).check)

    def test5083(self):
        '''problem on defining vars for multiple aliases of an option'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self, kFlag): pass

        self.assertRaiseArg(OptionMatcherException,
                    'optionVarNames defines information for aliases k, ko',
                    Simple(aliases={'k':'ko'},
                    optionVarNames={'k':'', 'ko':''}).check)

    def test5084(self):
        '''problem on defining vars for unknown option'''
        class Simple(OptionMatcher):
            
            @optmatcher
            def handleA(self): pass

        self.assertRaiseArg(OptionMatcherException,
                           'optionVarNames defines information for unknown: k',
                           Simple(optionVarNames={'k':''}).check)


class UsageTests(Tests):
    '''Tests on internal OptMatcherHandler'''
    
    def test6001(self):
        '''Global help test'''
        
        class Simple(OptionMatcher):
            
            @optcommon
            def handle(self, commonFlag, dPrefix, bFlag, commonOptOption=23, 
                       commonPar='po' , *gh): 
                pass
            
            @optmatcher
            def handleA(self, fOption, DPrefix, one, two, iOptionInt=34, 
                        wFlag=True, *args):
                '''Executes this program repeatedly until everybody is tired''' 
                pass
        
            @optmatcher
            def handleB(self, pFlag, one, mOption, 
                        iOptionInt=68, verboseFlag=False): 
                pass
        
            @optmatcher
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
        info={'v':'lot of useless info is output', 
              'D': 'create a new prefix',
              'f':'write output to FILE', 
              'm':'interaction mode: novice, intermediate, or '+
                    'expert [default: intermediate]'}
        vars={'d':'DX', 'i':'IN', 'f':'FILE'}
        usage=Simple(aliases=aliases, optionsHelp=info, 
                     optionVarNames=vars, defaultHelp=False).getUsage()    
        
        expected='''Usage: [common options] commonPar ...

options:
  -b
  --common
  -p
  --super
  -v, --verbose         lot of useless info is output
  -w
  --commonOpt=COMMONOPT
  -d DX
  -D DEFINE, --define=DEFINE
                        create a new prefix
  -f FILE, --filename=FILE
                        write output to FILE
  -i IN, --include=IN
  -m MODE, --mode=MODE  interaction mode: novice, intermediate, or
                        expert [default: intermediate]

alternatives:

* [--commonOpt=COMMONOPT (23)] [-i IN (34)] [-w (True)] -b --common
  -d DX -D DEFINE -f FILE [commonPar (po)] ...
                        Executes this program repeatedly until everybody
                        is tired

* [--commonOpt=COMMONOPT (23)] [-i IN (68)] [-v (False)] -b --common
  -d DX -m MODE -p [commonPar (po)] ...

* [--commonOpt=COMMONOPT (23)] [-i IN (68)] [-v (False)] -b --common
  -d DX -p [commonPar (po)] ...

* [--commonOpt=COMMONOPT (23)] -b --common -d DX --super
  [commonPar (po)] ...'''
        
#        for a, b in zip(usage.getUsageString(), expected):
#            print a, b
#        print len(usage.getUsageString()), len(expected)
        self.assertEqual(usage.getUsageString(), expected)
        
    def test6011(self):
        '''Checking default help'''

        class Simple(OptionMatcher):

            def printHelp(self):
                return True

        self.failUnless(Simple().process([None, '-h']))

    def test6012(self):
        '''Checking default help using alias'''

        class Simple(OptionMatcher):

            def printHelp(self):
                return True

        self.failUnless(Simple().process([None, '--help']))

    def test6013(self):
        '''Checking default help, non getopt mode'''

        class Simple(OptionMatcher):

            def printHelp(self):
                return True

        self.failUnless(Simple(optionPrefix='-').process([None, '-help']))



        
if __name__ == '__main__':
    unittest.main()
