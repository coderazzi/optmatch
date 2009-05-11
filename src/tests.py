from optmatch import CommandLine, OptMatcherHandler, OptionMatcher, optmatcher, optcommon

def test0001Ok():
    '''Non getopt mode. Long flag easy'''
    
    def method(aFlag):
        pass
    
    getoptMode = False
    arg = CommandLine([None, '-a'], '-', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1]
    
    
def test0002Nok():
    '''Non getopt mode. Long flag not given'''
    
    def method(aFlag):
        pass
    
    getoptMode = False
    arg = CommandLine([None, '-b'], '-', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret
    
    
def test0003Ok():
    '''Non getopt mode. Long option given'''
    
    def method(aOption):
        pass
    
    getoptMode = False
    arg = CommandLine([None, '-a=2'], '-', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == '2'
    
    
    
def test0011Ok():
    '''Non getopt mode. using kwargs for an option'''
    
    def method(**kwarg):
        pass
    
    getoptMode = False
    arg = CommandLine([None, '-a=2'], '-', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.kwargs == {'a':'2'}
    
    
def test0012Ok():
    '''Non getopt mode. using kwargs for a flag'''
    
    def method(**kwargs):
        pass
    
    getoptMode = False
    arg = CommandLine([None, '-a'], '-', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.kwargs == {'a':None}
    
    
def test0021Ok():
    '''Non getopt mode. prefix well given with value'''
    
    def method(DPrefix):
        pass
    
    getoptMode = False
    arg = CommandLine([None, '-Dname=value'], '-', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == [('name', 'value')]
    
    
def test0022Ok():
    '''Non getopt mode. prefix well given'''
    
    def method(IPrefix):
        pass
    
    getoptMode = False
    arg = CommandLine([None, '-Iname'], '-', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == [('name', None)]
    
    
def test0023Exception():
    '''Non getopt mode. prefix incorrect'''
    
    def method(IPrefix):
        pass
    
    getoptMode = False
    arg = CommandLine([None, '-I=name'], '-', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    #return ret and ch.provided[1]==[('name',None)]
    
    
def test0024Ok():
    '''Prefix are not mandatory options'''
    
    def method(IPrefix):
        return "Yeah, called"
    
    getoptMode = False
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.isInvokable() and ch.invoke()
    return ret=="Yeah, called"
    
    
    
    
    
def test0101Ok():
    '''Non getopt mode. Long flag with alias'''
    
    def method(aFlag):
        pass
    
    getoptMode = False
    arg = CommandLine([None, '-aalias'], '-', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ch.setAliases({'a':'aalias'})
    ret = ch.handleArg(arg)
    return ret and ch.provided[1]
    
    
def test0103Ok():
    '''Non getopt mode. Long option given with alias'''
    
    def method(aOption):
        pass
    
    getoptMode = False
    arg = CommandLine([None, '-aalias=2'], '-', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ch.setAliases({'a':'aalias'})
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == '2'
    
    
    
def test0111Ok():
    '''Non getopt mode. prefix well given as alias, with value'''
    
    def method(DPrefix):
        pass
    
    getoptMode = False
    arg = CommandLine([None, '-definename=value'], '-', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ch.setAliases({'D':'define'})    
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == [('name', 'value')]
    
    
def test0112Ok():
    '''Non getopt mode. prefix well given as alias, without value'''
    
    def method(IPrefix):
        pass
    
    getoptMode = False
    arg = CommandLine([None, '-includename'], '-', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ch.setAliases({'I':'include'})    
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == [('name', None)]
    
    
    
    

    
    
def test0201Ok():
    '''getopt mode. Long flag easy'''
    
    def method(verboseFlag):
        pass
    
    getoptMode = False
    arg = CommandLine([None, '--verbose'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1]
    
    
def test0202Nok():
    '''getopt mode. Long flag not given'''
    
    def method(verboseFlag):
        pass
    getoptMode = True
    arg = CommandLine([None, '--qqw'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret
    
    
def test0203Ok():
    '''getopt mode. Long option given'''
    
    def method(modeOption):
        pass
    
    getoptMode = True
    arg = CommandLine([None, '--mode=2'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == '2'
    

def test0211Ok():
    '''getopt mode. prefix well given'''
    
    def method(definePrefix):
        pass
    
    getoptMode = True
    arg = CommandLine([None, '--definename=value'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == [('name', 'value')]
    
    
def test0212Ok():
    '''getopt mode. start flag prefix well given'''
    
    def method(includePrefix):
        pass
    
    getoptMode = True
    arg = CommandLine([None, '--includename'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == [('name', None)]
    
    
def test0301Ok():
    '''getopt mode. Long flag with alias'''
    
    def method(vFlag):
        pass
    
    getoptMode = True
    arg = CommandLine([None, '--verbose'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ch.setAliases({'v':'verbose'})
    ret = ch.handleArg(arg)
    return ret and ch.provided[1]
    
    
def test0303Ok():
    '''getopt mode. Long option given with alias'''
    
    def method(vOption):
        pass
    
    getoptMode = True
    arg = CommandLine([None, '--verbose=2'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ch.setAliases({'v':'verbose'})
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == '2'
    

def test0311Nok():
    '''getopt mode. Short option given as long'''
    
    def method(aOption):
        pass
    
    getoptMode = True
    arg = CommandLine([None, '--a=2'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret
    
    
def test0312Nok():
    '''getopt mode. Short prefix given as long'''
    
    def method(aPrefix):
        pass
    
    getoptMode = True
    arg = CommandLine([None, '--aValue'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret
    
    
    
def test0313Exception():
    '''getopt mode. Short prefix without associated value'''
    
    def method(aPrefix):
        pass
    
    getoptMode = True
    arg = CommandLine([None, '-a', '-Value'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret
    
    
    
def test0321Ok():
    '''getopt mode. Long flag given separated'''
    
    def method(verboseOption):
        pass
    
    getoptMode = True
    arg = CommandLine([None, '--verbose', 'value'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == 'value'
    
    
def test0322Exception():
    '''getopt mode. Long flag given separated but as option'''
    
    def method(verboseOption):
        pass
    
    getoptMode = True
    arg = CommandLine([None, '--verbose', '-value'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ch.handleArg(arg)
    
def test0323Exception():
    '''getopt mode. Long flag given separated but as name/value'''
    
    def method(verboseOption):
        pass
    
    getoptMode = True
    arg = CommandLine([None, '--verbose', 'name=value'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ch.handleArg(arg)
    
def test0401Ok():
    '''getopt mode. Short flag given alone'''
    
    def method(vFlag):
        pass
    
    getoptMode = True
    arg = CommandLine([None, '-v'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] and arg.finished()
    
def test0402Ok():
    '''getopt mode. Short option given alone'''
    
    def method(vOption):
        pass
    
    getoptMode = True
    arg = CommandLine([None, '-v1'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == '1' and arg.finished()
    
def test0403Exception():
    '''getopt mode. Short option without value'''
    
    def method(vOption):
        pass
    
    getoptMode = True
    arg = CommandLine([None, '-v'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ch.handleArg(arg)
    
    
def test0404Ok():
    '''getopt mode. Short option given separately'''
    
    def method(vOption):
        pass
    
    getoptMode = True
    arg = CommandLine([None, '-v', '1'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == '1' and arg.finished()
    
def test0405Exception():
    '''getopt mode. Short option given separately, wrong'''
    
    def method(vOption):
        pass
    
    getoptMode = True
    arg = CommandLine([None, '-v', '-a'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ch.handleArg(arg)
    
    
def test0406Exception():
    '''getopt mode. Short option given separately, including value'''
    
    def method(vOption):
        pass
    
    getoptMode = True
    arg = CommandLine([None, '-v', 'a=h'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    
    
    
    
def test0411Ok():
    '''getopt mode. A flag given, but not alone'''
    
    def method(vFlag):
        pass
    
    getoptMode = True
    arg = CommandLine([None, '-vw'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] and arg.name == 'w'
    
    
def test0501Ok():
    '''getopt mode. Flag and Short options given'''
    
    def method(vOption, wFlag):
        pass
    
    getoptMode = True
    arg = CommandLine([None, '-wv', 'q'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg) and ch.handleArg(arg)
    return ret and ch.provided[1] == 'q' and ch.provided[2] and arg.finished()


def test0601Ok():
    '''getopt mode. Parameter given'''
    
    def method(par1):
        pass
    
    getoptMode = True
    arg = CommandLine([None, 'file'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.providedPars == ['file'] and arg.finished()


def test0602Ok():
    '''getopt mode. Two parameters given'''
    
    def method(par1, par2):
        pass
    
    getoptMode = True
    arg = CommandLine([None, 'file', 'more'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg) and ch.handleArg(arg) 
    return ret and ch.providedPars == ['file', 'more'] and arg.finished()

def test0603Nok():
    '''getopt mode. Two parameters given, only one expected'''
    
    def method(par1):
        pass
    
    getoptMode = True
    arg = CommandLine([None, 'file', 'more'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg) and ch.handleArg(arg) 
    return ret

def test0605Ok():
    '''getopt mode. Using vararg for two arguments'''
    
    def method(*var):
        pass
    
    getoptMode = True
    arg = CommandLine([None, 'file', 'more'], '--', '=', False)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg) and ch.handleArg(arg) and arg.finished()
    return ret

def test0611Ok():
    '''getopt mode. Checkin gnu mode'''
    
    def method(aFlag, par1, par2):
        pass
    
    getoptMode = True
    arg = CommandLine([None, '-a', 'par1', '-v'], '--', '=', True)
    ch = OptMatcherHandler(method, getoptMode)
    ret = ch.handleArg(arg) and ch.handleArg(arg) and ch.handleArg(arg) and arg.finished()
    return ret




def test1001Ok():
    '''Simple test, no args'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self):
            self.ok = True
            return True
        
    s = Simple()
    return s.process([None]) and s.ok

def test1002Ok():
    '''Simple test, one optional parameter, not given'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, par=None):
            self.ok = True
            return True
        
    s = Simple()
    return s.process([None]) and s.ok

def test1003Ok():
    '''Simple test, one optional flag, not given'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, vFlag=None):
            self.ok = True
            return True
        
    s = Simple()
    return s.process([None]) and s.ok

def test1004Ok():
    '''Simple test, one optional option, not given'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, vOption=None):
            self.ok = True
            return True
        
    s = Simple()
    return s.process([None]) and s.ok


def test1011Exception():
    '''Simple test, one flag, not given'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, vFlag):
            pass
        
    return Simple().process([None])


def test1012Ok():
    '''Simple test, one flag, given'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, vFlag):
            self.ok = True
            return True
        
    s = Simple()
    return s.process([None, '-v']) and s.ok


def test1013Exception():
    '''Simple test, one flag, two given'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(vFlag):
            pass
        
    return Simple().process([None, '-vw'])


def test1021Ok():
    '''More complex test, two flags, one parameter'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, vFlag, oFlag, par):
            self.ok = str(vFlag) + str(oFlag) + par
            return True
        
    s = Simple()
    return s.process([None, '-vo', 'file']) and s.ok == 'TrueTruefile'


def test1022Ok():
    '''More complex test, one flag, one option, one parameter'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, vFlag, oOption, par):
            self.ok = str(vFlag) + oOption + par
            return True
        
    s = Simple()
    return s.process([None, '-vo1', 'file']) and s.ok == 'True1file'


def test1023Ok():
    '''More complex test, one flag, one separated option, one parameter'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, vFlag, oOption, par):
            self.ok = str(vFlag) + oOption + par
            return True
        
    s = Simple()
    return s.process([None, '-vo', '1', 'file']) and s.ok == 'True1file'


def test1024Ok():
    '''Verifying that prefixes are not required'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, vFlag, oOption, dPrefix, par):
            self.ok = str(vFlag) + oOption + par + str(dPrefix)
            return True
        
    s = Simple()
    return s.process([None, '-vo', '1', 'file']) and s.ok == 'True1file[]'


def test1031Ok():
    '''More complex test, two possible handlers'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(vFlag, oOption, par):
            pass
        
        @optmatcher
        def handle2(self, vFlag, par):
            self.ok = str(vFlag) + par
            return True
        
    s = Simple()
    return s.process([None, '-v', 'file']) and s.ok == 'Truefile'


def test1032Ok():
    '''More complex test, two possible handlers and a common one'''
    
    class Simple(OptionMatcher):
        
        @optcommon
        def common_options(self, vFlag):
            self.v = str(vFlag)
        
        @optmatcher
        def handle(self, oOption, par):
            return False
        
        @optmatcher
        def handle2(self, par):
            self.ok = self.v + par
            return True
        
    s = Simple()
    return s.process([None, '-v', 'file']) and s.ok == 'Truefile'


def test1033Exception():
    '''More complex test, two possible handlers and a common one, not given'''
    
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
        
    return Simple().process([None, 'file'])


def test1041Ok():
    '''Aliases test using common'''
    
    class Simple(OptionMatcher):
        
        @optcommon
        def common_options(self, vFlag):
            self.v = str(vFlag)
        
        @optmatcher
        def handle(self, oOption, par):
            self.ok = self.v + oOption + par
            return True
        
    s = Simple()
    return s.process([None, '--verbose', '--option=2', 'file'],
                     aliases={'v':'verbose', 'o':'option'}) and s.ok == 'True2file'


def test1042Ok():
    '''Aliases test using common, varargs'''
    
    class Simple(OptionMatcher):
        
        @optcommon
        def common_options(self, vFlag):
            self.v = str(vFlag)
        
        @optmatcher
        def handle(self, oOption, *ends):
            self.ok = self.v + oOption + str(ends)
            return True
        
    s = Simple()
    return s.process([None, '--verbose', '--option=2', '1', '2'],
                     aliases={'v':'verbose', 'o':'option'}) and s.ok == "True2('1', '2')"



def test1043Exception():
    '''Aliases test, overriding some definition'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, oOption, kOption):
            pass
        
    s = Simple()    
    return s.process([], aliases={'o':'k'})


def test1044Exception():
    '''Aliases test, overriding some definition'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, oOption, optOption):
            pass
        
    s = Simple()    
    return s.process([], aliases={'o':'opt'})



def test1045Exception():
    '''Aliases test, overriding some definition, way round'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, oOption, optOption):
            pass
        
    s = Simple()    
    return s.process([], aliases={'opt':'o'})

def test1046Exception():
    '''Aliases test, overriding some definition, not getopt mode'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, oOption, vOption):
            pass
        
    s = Simple()    
    return s.process([], aliases={'v':'o'}, option='-')



def test1051Ok():
    '''Integer options'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, valOptionInt):
            self.ok = valOptionInt
            return True
        
    s = Simple()
    return s.process([None, '--val=2']) and s.ok == 2


def test1052Exception():
    '''Integer options, string for integer'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, valOptionInt):
            self.ok = valOptionInt
            return True
        
    s = Simple()
    return s.process([None, '--val=two']) and s.ok == 2

def test1053Exception():
    '''Integer options, float for integer'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, valOptionInt):
            self.ok = valOptionInt
            return True
        
    s = Simple()
    return s.process([None, '--val=2.3']) and s.ok == 2


def test1054Ok():
    '''Float options'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, valOptionFloat):
            self.ok = valOptionFloat
            return True
        
    s = Simple()
    return s.process([None, '--val=2.3']) and s.ok == 2.3


def test1055Exception():
    '''Float options, string for float'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, valOptionFloat):
            self.ok = valOptionFloat
            return True
        
    s = Simple()
    return s.process([None, '--val=two']) and s.ok == 2

def test1056Ok():
    '''Float options, integer for float'''
    
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, valOptionFloat):
            self.ok = valOptionFloat
            return True
        
    s = Simple()
    return s.process([None, '--val=2']) and s.ok == 2



def test2001Ok():
    '''API test: setNonGetoptMode'''

    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, oOption, arg):
            self.ok = oOption + arg
            return True
        
    s = Simple()
    return s.process([None, '/o:23', 'file'], 
                     option='/', delimiter=':') and s.ok == "23file"

def test2002Ok():
    '''API test: setNonGetoptMode with aliases'''

    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, oOption, arg):
            self.ok = oOption + arg
            return True
        
    s = Simple()
    return s.process([None, '/opt:23', 'file'],
                     aliases={'o':'opt'},
                     option='/', delimiter=':') and s.ok == "23file"

def test2003Ok():
    '''API test: setNonGetoptMode with aliases way around'''

    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, oOption, arg):
            self.ok = oOption + arg
            return True
        
    s = Simple()
    return s.process([None, '/opt:23', 'file'],
                     aliases={'o':'opt'},
                     option='/', delimiter=':') and s.ok == "23file"


def test2011Ok():
    '''API test: specifying external common handler'''
    
    class Any(object):
        
        @staticmethod
        def specificCommonHandler(oOption):
            Any.oOption = oOption
        
    class Simple(OptionMatcher):
        
        @optmatcher
        def handle(self, arg):
            self.ok = Any.oOption + arg
            return True
        
    s = Simple()
    return s.process([None, '-o23', 'file'], common=Any.specificCommonHandler) and s.ok == "23file"



def test2012Ok():
    '''API test: specifying external handlers as methods'''
    
    class Any(object):
        
        @staticmethod
        def myOwnHandler(oOption, par):
            Any.o = oOption
            Any.p = par
            return True
        
    ah = OptionMatcher()
    return ah.process([None, '-o23', 'file'],
                      matchers=[Any.myOwnHandler]) and Any.o == '23' and Any.p == 'file'


def test2021Ok():
    '''API test: specifying static method as command handler'''
    
    class Simple(object):
        
        @staticmethod        
        def handle(f):
            return f
        
    ah = OptionMatcher()
    return ah.process([None, 'ok'], matchers=[Simple.handle])=='ok'


def test2022Exception():
    '''API test: specifying incorrect flags on command handler'''
    
    def work(aFlag, aOption):
        pass
    
    ah = OptionMatcher()
    return ah.process([None], matchers=[work])



def test3011Ok():
    '''API test: defining flag via decorator'''

    class Simple(OptionMatcher):
        
        @optmatcher(flags='o')
        def handleA(self, o):
            self.ok=True
            return True
        
    s = Simple()
    return s.process([None, '-o']) and s.ok


def test3012Ok():
    '''API test: defining flags via decorator'''

    class Simple(OptionMatcher):
        
        @optmatcher(flags='o, v')
        def handleA(self, o, v):
            self.ok=o and v
            return True
        
    s = Simple()
    return s.process([None, '-ov']) and s.ok


def test3013Ok():
    '''API test: defining flags exclusively via decorator'''

    class Simple(OptionMatcher):
        
        @optmatcher(flags='o, v')
        def handleA(self, o, v, wFlag):
            self.ok=o and v and wFlag=='w'
            return True
        
    s = Simple()
    return s.process([None, '-ov','w']) and s.ok


def test3014Ok():
    '''API test: defining flag with as, exclusively via decorator'''

    class Simple(OptionMatcher):
        
        @optmatcher(flags='verbose as v')
        def handleA(self, verbose):
            self.ok=verbose
            return True
        
    s = Simple()
    return s.process([None, '-v']) and s.ok


def test3015Ok():
    '''API test: defining flags with as, exclusively via decorator'''

    class Simple(OptionMatcher):
        
        @optmatcher(flags='verbose as v, o')
        def handleA(self, verbose, o):
            self.ok=verbose and o
            return True
        
    s = Simple()
    return s.process([None, '-vo']) and s.ok


def test3016Ok():
    '''API test: defining a parameter with different name'''

    class Simple(OptionMatcher):
        
        @optmatcher(flags='o', parameters='va as file')
        def handleA(self, o, va):
            self.ok=o and va=='f'
            return True
        
    s = Simple()
    return s.process([None, '-o', 'f']) and s.ok


def test3021Ok():
    '''API test: defining all via decorator'''

    class Simple(OptionMatcher):
        
        @optmatcher(flags='o,v', options='w', prefixes='d as D',
                    intOptions='i', floatOptions='f', parameters='par as class', 
                    priority=1)
        def handleA(self, o, v, w, d, i, f, par):
            self.ok=o and v and (w=='w') and (d==[('value',None)]) and (i==1) and (f==2.3) and (par=='class') 
            return True
        
    s = Simple()
    return s.process([None, '-oww', '-vi1', '-f', '2.3', '-Dvalue', 'class']) and s.ok


def test3022Ok():
    '''API test: defining all via decorator, using also optcommon'''

    class Simple(OptionMatcher):
        
        @optcommon(intOptions='m as mode')
        def common(self, m):
            self.m=m
        
        @optmatcher(flags='o,v', options='w', prefixes='d as D',
                    intOptions='i', floatOptions='f', parameters='par as class', 
                    priority=1)
        def handleA(self, o, v, w, d, i, f, par):
            self.ok=self.m==23 and o and v and (w=='w') and (d==[('value',None)]) and (i==1) and (f==2.3) and (par=='class') 
            return True
        
    s = Simple()
    return s.process([None, '-oww', '--mode=23', '-vi1', '-f', '2.3', '-Dvalue', 'class']) and s.ok


def test3031Ok():
    '''API test: setting priorities'''

    class Simple(OptionMatcher):
        
        @optmatcher
        def handleA(self, oFlag):
            pass
        
        @optmatcher(priority=1)
        def handleB(self, oFlag):
            self.ok = True
            return True
        
        @optmatcher
        def handleC(self, oFlag):
            pass
        
    s = Simple()
    return s.process([None, '-o']) and s.ok


def test3032Ok():
    '''API test: setting priorities on optcommon'''

    class Simple(OptionMatcher):
        
        @optcommon(priority=1)
        def handleA(self, oFlag):
            print 'Called'
        
        @optcommon(priority=2)
        def handleB(self, oFlag):
            self.o=oFlag
        
        @optmatcher
        def handleC(self, *args):
            self.ok = self.o and len(args)==3
            return True
        
        
    s = Simple()
    return s.process([None, '-o','1','2','3']) and s.ok





def handle(*what):
    failures = 0
    for each in what:
        name = each.__name__        
        reason = ''
        try:
            ok = each()
            if ok:
                if not name.endswith('Ok'):
                    ok = False
            elif name.endswith('Nok'):
                ok = True
        except Exception, r:
            if name.endswith('Exception'):
                ok = True
            else:
                raise
                ok = False
            reason = '===>' + str(r)
        print ok, ':', each.__name__, ':', each.__doc__, reason
        if not ok:
            failures += 1
    return failures
            



    
def handleAll():
    import inspect
    current = __import__(inspect.getmodulename(__file__))
    total, failures = 0, 0
    for each in dir(current):
        if each.startswith('test'):
            total+=1
            failures+=handle(getattr(current, each))
    print '=========================='
    print 'Total:   ',total
    print 'Failures:',failures
    
if __name__ == '__main__':
    if True:
        handleAll()
    elif True:
        handle(test3032Ok)
    else:
        pass
