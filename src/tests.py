import unittest

from optmatch import CommandLine, OptMatcherHandler, OptionMatcher 
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
#    def test4001(self):
#        '''API test: defining flag via decorator'''
#    
#        class Simple(OptionMatcher):
#            
#            @optmatcher
#            def handleA(self, vFlag, kFlag): pass
#
#            @optmatcher
#            def handleB(self, oFlag, pOption): pass
#
#        self.assertRaiseArg(UsageException,
#                            'Missing required parameter class',
#                            Simple().process, [None, '-o'])
#
#class Tests:
class Tests(unittest.TestCase):

    def assertRaiseArg(self, exception, exStr, callable, *args, **kwargs):
        try:
            callable(*args, **kwargs)
            self.fail('Expected exception not raised')
        except exception, which:
            self.assertEqual(str(which), exStr)

    def test1011(self):
        '''Simple test, one flag, not given'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, vFlag): pass
            
        self.assertRaiseArg(UsageException, 'Missing required flag v',
                            Simple().process, [None])

class InternalTests(Tests):
    '''Tests on internal OptMatcherHandler'''
    
    def test0001Ok(self):
        '''Non getopt mode. Long flag easy'''
        
        def method(aFlag): pass
        
        getoptMode = False
        arg = CommandLine([None, '-a'], '-', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1])
        
    def test0002(self):
        '''Non getopt mode. Long flag not given'''
        
        def method(aFlag): pass
        
        getoptMode = False
        arg = CommandLine([None, '-b'], '-', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ret = ch.handleArg(arg)
        self.failUnless(ret)
        
    def test0003(self):
        '''Non getopt mode. Long option given'''
        
        def method(aOption): pass
        
        getoptMode = False
        arg = CommandLine([None, '-a=2'], '-', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == '2')
    
    def test0011(self):
        '''Non getopt mode. using kwargs for an option'''
        
        def method(**kwarg): pass
        
        getoptMode = False
        arg = CommandLine([None, '-a=2'], '-', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.kwargs == {'a':'2'})
    
    def test0012(self):
        '''Non getopt mode. using kwargs for a flag'''
        
        def method(**kwargs): pass
        
        getoptMode = False
        arg = CommandLine([None, '-a'], '-', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.kwargs == {'a':None})
    
    def test0021(self):
        '''Non getopt mode. prefix well given with value'''
        
        def method(DPrefix): pass
        
        getoptMode = False
        arg = CommandLine([None, '-Dname=value'], '-', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == [('name', 'value')])
    
    def test0022(self):
        '''Non getopt mode. prefix well given'''
        
        def method(IPrefix): pass
        
        getoptMode = False
        arg = CommandLine([None, '-Iname'], '-', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == [('name', None)])
    
    def test0023(self):
        '''Non getopt mode. prefix incorrect'''
        
        def method(IPrefix): pass
        
        getoptMode = False
        arg = CommandLine([None, '-I=name'], '-', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        self.assertRaiseArg(UsageException, 
                            'Incorrect prefix usage on argument -I=name',
                            ch.handleArg, 
                            arg)
        
    def test0024(self):
        '''Prefix are not mandatory options'''
        
        def method(IPrefix):
            return "Called"
        
        getoptMode = False
        ch = OptMatcherHandler(method, getoptMode)
        self.assertEquals(ch.invoke(), "Called")
        
    def test0101(self):
        '''Non getopt mode. Long flag with alias'''
        
        def method(aFlag): pass
        
        getoptMode = False
        arg = CommandLine([None, '-aalias'], '-', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ch.setAliases({'a':'aalias'})
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1])
        
    def test0103(self):
        '''Non getopt mode. Long option given with alias'''
        
        def method(aOption): pass
        
        getoptMode = False
        arg = CommandLine([None, '-aalias=2'], '-', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ch.setAliases({'a':'aalias'})
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == '2')
        
    def test0111(self):
        '''Non getopt mode. prefix well given as alias, with value'''
        
        def method(DPrefix): pass
        
        getoptMode = False
        arg = CommandLine([None, '-definename=value'], '-', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ch.setAliases({'D':'define'})    
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == [('name', 'value')])
        
    def test0112(self):
        '''Non getopt mode. prefix well given as alias, without value'''
        
        def method(IPrefix): pass
        
        getoptMode = False
        arg = CommandLine([None, '-includename'], '-', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ch.setAliases({'I':'include'})    
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == [('name', None)])
    
    def test0201(self):
        '''getopt mode. Long flag easy'''
        
        def method(verboseFlag): pass
        
        getoptMode = False
        arg = CommandLine([None, '--verbose'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1])
        
    def test0202(self):
        '''getopt mode. Long flag not given'''
        
        def method(verboseFlag): pass
        
        getoptMode = True
        arg = CommandLine([None, '--qqw'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        self.failUnless(ch.handleArg(arg))
        
    def test0203(self):
        '''getopt mode. Long option given'''
        
        def method(modeOption): pass
        
        getoptMode = True
        arg = CommandLine([None, '--mode=2'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == '2')
    
    def test0211(self):
        '''getopt mode. prefix well given'''
        
        def method(definePrefix): pass
        
        getoptMode = True
        arg = CommandLine([None, '--definename=value'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == [('name', 'value')])
        
    def test0212(self):
        '''getopt mode. start flag prefix well given'''
        
        def method(includePrefix): pass
        
        getoptMode = True
        arg = CommandLine([None, '--includename'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == [('name', None)])
    
    def test0301(self):
        '''getopt mode. Long flag with alias'''
        
        def method(vFlag): pass
        
        getoptMode = True
        arg = CommandLine([None, '--verbose'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ch.setAliases({'v':'verbose'})
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1])
    
    def test0303(self):
        '''getopt mode. Long option given with alias'''
        
        def method(vOption): pass
        
        getoptMode = True
        arg = CommandLine([None, '--verbose=2'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ch.setAliases({'v':'verbose'})
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == '2')
    
    def test0311(self):
        '''getopt mode. Short option given as long'''
        
        def method(aOption): pass
        
        getoptMode = True
        arg = CommandLine([None, '--a=2'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ret = ch.handleArg(arg)
        return ret    
    
    def test0312(self):
        '''getopt mode. Short prefix given as long'''
        
        def method(aPrefix): pass
        
        getoptMode = True
        arg = CommandLine([None, '--aValue'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        self.failUnless(ch.handleArg(arg))
    
    def test0313(self):
        '''getopt mode. Short prefix without associated value'''
        
        def method(aPrefix):pass
        
        getoptMode = True
        arg = CommandLine([None, '-a', '-Value'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        self.assertRaiseArg(UsageException, 'Incorrect prefix a',
                            ch.handleArg, arg)
        
    def test0321(self):
        '''getopt mode. Long flag given separated'''
        
        def method(verboseOption): pass
        
        getoptMode = True
        arg = CommandLine([None, '--verbose', 'value'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == 'value')
    
    def test0322(self):
        '''getopt mode. Long flag given separated but as option'''
        
        def method(verboseOption): pass
        
        getoptMode = True
        arg = CommandLine([None, '--verbose', '-value'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        self.assertRaiseArg(UsageException, 'Incorrect option verbose',
                            ch.handleArg, arg)
    
    def test0323(self):
        '''getopt mode. Long flag given separated but as name/value'''
        
        def method(verboseOption): pass
        
        getoptMode = True
        arg = CommandLine([None, '--verbose', 'name=value'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        self.assertRaiseArg(UsageException, 'Incorrect option verbose',
                            ch.handleArg, arg)
    
    def test0401(self):
        '''getopt mode. Short flag given alone'''
        
        def method(vFlag): pass
        
        getoptMode = True
        arg = CommandLine([None, '-v'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] and arg.finished())
    
    def test0402(self):
        '''getopt mode. Short option given alone'''
        
        def method(vOption): pass
        
        getoptMode = True
        arg = CommandLine([None, '-v1'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == '1' and arg.finished())
    
    def test0403(self):
        '''getopt mode. Short option without value'''
        
        def method(vOption): pass
        
        getoptMode = True
        arg = CommandLine([None, '-v'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        self.assertRaiseArg(UsageException, 'Incorrect option v',
                            ch.handleArg, arg)
    
    def test0404(self):
        '''getopt mode. Short option given separately'''
        
        def method(vOption): pass
        
        getoptMode = True
        arg = CommandLine([None, '-v', '1'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] == '1' and arg.finished())
    
    def test0405(self):
        '''getopt mode. Short option given separately but wrong'''
        
        def method(vOption): pass
        
        getoptMode = True
        arg = CommandLine([None, '-v', '-a'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        self.assertRaiseArg(UsageException, 'Incorrect option v',
                            ch.handleArg, arg)
        
    def test0406(self):
        '''getopt mode. Short option given separately, including value'''
        
        def method(vOption): pass
        
        getoptMode = True
        arg = CommandLine([None, '-v', 'a=h'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        self.assertRaiseArg(UsageException, 'Incorrect option v',
                            ch.handleArg, arg)

    def test0411(self):
        '''getopt mode. A flag given, but not alone'''
        
        def method(vFlag): pass
        
        getoptMode = True
        arg = CommandLine([None, '-vw'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.provided[1] and arg.name == 'w')
    
    def test0501(self):
        '''getopt mode. Flag and Short options given'''
        
        def method(vOption, wFlag): pass
        
        getoptMode = True
        arg = CommandLine([None, '-wv', 'q'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        self.failUnless(not ch.handleArg(arg) and not ch.handleArg(arg) 
                        and ch.provided[1] == 'q' and 
                        ch.provided[2] and arg.finished())

    def test0601(self):
        '''getopt mode. Parameter given'''
        
        def method(par1): pass
        
        getoptMode = True
        arg = CommandLine([None, 'file'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        ret = ch.handleArg(arg)
        self.failUnless(not ret and ch.providedPars == ['file'] 
                        and arg.finished())

    def test0602(self):
        '''getopt mode. Two parameters given'''
        
        def method(par1, par2): pass
        
        getoptMode = True
        arg = CommandLine([None, 'file', 'more'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        self.failUnless(not ch.handleArg(arg) and not ch.handleArg(arg)
                        and ch.providedPars == ['file', 'more'] 
                        and arg.finished())

    def test0603(self):
        '''getopt mode. Two parameters given, only one expected'''
        
        def method(par1): pass
        
        getoptMode = True
        arg = CommandLine([None, 'file', 'more'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        self.assertFalse(ch.handleArg(arg) and ch.handleArg(arg)) 

    def test0605(self):
        '''getopt mode. Using vararg for two arguments'''
        
        def method(*var): pass
        
        getoptMode = True
        arg = CommandLine([None, 'file', 'more'], '--', '=', False)
        ch = OptMatcherHandler(method, getoptMode)
        self.failUnless(not ch.handleArg(arg) and not ch.handleArg(arg) 
                        and arg.finished())

    def test0611(self):
        '''getopt mode. Checking gnu mode'''
        
        def method(aFlag, par1, par2): pass
        
        getoptMode = True
        arg = CommandLine([None, '-a', 'par1', '-v'], '--', '=', True)
        ch = OptMatcherHandler(method, getoptMode)
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
        '''More complex test, one flag, one separated option, one parameter'''
        
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
        '''More complex test, two possible handlers and a common one, not given
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
        self.assertEquals(Simple().process(args, aliases=aliases),
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
        self.assertEquals(Simple().process(args, aliases=aliases),
                          (True, '2', ('1', '2')))

    def test1043(self):
        '''Aliases test, overriding some definition'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, oOption, kOption): pass
            
        self.assertRaises(OptionMatcherException,
                          Simple().process, [], aliases={'o':'k'})

    def test1044(self):
        '''Aliases test, overriding some definition'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, oOption, optOption): pass
            
        self.assertRaises(OptionMatcherException,
                          Simple().process, [], aliases={'o':'opt'})

    def test1045(self):
        '''Aliases test, overriding some definition, way round'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, oOption, optOption): pass
            
        self.assertRaises(OptionMatcherException,
                          Simple().process, [], aliases={'opt':'o'})

    def test1046(self):
        '''Aliases test, overriding some definition, not getopt mode'''
        
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, oOption, vOption): pass
            
        self.assertRaises(OptionMatcherException,
                          Simple().process, [], aliases={'v':'o'}, option='-')

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

    def test2001(self):
        '''API test: non getoptMode'''
    
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, oOption, arg):
                return oOption, arg
            
        self.assertEquals(Simple().process([None, '/o:23', 'file'],
                                           option='/',
                                           delimiter=':'), ('23', 'file')) 

    def test2002(self):
        '''API test: non getoptMode with aliases'''
    
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, oOption, arg):
                return oOption, arg
            
        self.assertEquals(Simple().process([None, '/opt:23', 'file'],
                                           aliases={'o':'opt'},
                                           option='/',
                                           delimiter=':'), ('23', 'file')) 
            
    def test2003(self):
        '''API test: non getoptMode with aliases way around'''
    
        class Simple(OptionMatcher):
            
            @optmatcher
            def handle(self, oOption, arg):
                return oOption, arg
            
        self.assertEquals(Simple().process([None, '/opt:23', 'file'],
                                           aliases={'opt':'o'},
                                           option='/',
                                           delimiter=':'), ('23', 'file')) 

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
            
        self.assertEquals(Simple().process([None, '-o23', 'file'],
                                           common=Any.specificCommonHandler),
                                           ('23', 'file')) 

    def test2012(self):
        '''API test: specifying external handlers as methods'''
        
        class Any(object):
            
            @staticmethod
            def myOwnHandler(oOption, par):
                return oOption, par
            
        self.assertEquals(OptionMatcher().process([None, '-o23', 'file'],
                                           matchers=[Any.myOwnHandler]),
                                           ('23', 'file')) 

    def test2021(self):
        '''API test: specifying static method as command handler'''
        
        class Simple(object):
            
            @staticmethod        
            def handle(f):
                return f
            
        self.assertEquals(OptionMatcher().process([None, 'ok'],
                                           matchers=[Simple.handle]), 'ok')

    def test2022(self):
        '''API test: specifying incorrect flags on command handler'''
        
        def work(aFlag, aOption): pass
        
        self.assertRaiseArg(OptionMatcherException,
                            'Repeated option "a" in function work',
                            OptionMatcher().process, [None], matchers=[work])


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
            
            @optmatcher(flags='o', parameters='va as file')
            def handleA(self, o, va):
                return o and va == 'f'
            
        self.failUnless(Simple().process([None, '-o', 'f']))

    def test3021(self):
        '''API test: defining all via decorator'''
    
        class Simple(OptionMatcher):
            
            @optmatcher(flags='o,v', options='w', prefixes='d as D',
                        intOptions='i', floatOptions='f', 
                        parameters='par as class', priority=1)
            def handleA(self, o, v, w, d, i, f, par):
                return o, v, w, d, i, f, par
        
        args=[None, '-oww', '-vi1', '-f', '2.3', '-Dvalue', 'class']
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
                        parameters='par as class', priority=1)
            def handleA(self, o, v, w, d, i, f, par):
                return self.m, o, v, w, d, i, f, par

        args=[None, '-oww', '--mode=23', '-vi1', '-f', '2.3', '-Dvalue', 
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
            
            @optmatcher(parameters='c as class')
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


if __name__ == '__main__':
    unittest.main()
