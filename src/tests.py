from optmatch import _CommandLine, _CommandHandler, OptionMatcher

def testCH0001Ok():
    '''Non getopt mode. Long flag easy'''
    
    def method(aFlag):
        pass
    
    getoptMode = False
    arg = _CommandLine([None, '-a'], '-', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1]
    
    
def testCH0002Nok():
    '''Non getopt mode. Long flag not given'''
    
    def method(aFlag):
        pass
    
    getoptMode = False
    arg = _CommandLine([None, '-b'], '-', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret
    
    
def testCH0003Ok():
    '''Non getopt mode. Long option given'''
    
    def method(aOption):
        pass
    
    getoptMode = False
    arg = _CommandLine([None, '-a=2'], '-', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == '2'
    
    
    
def testCH0011Ok():
    '''Non getopt mode. using kwargs for an option'''
    
    def method(**kwarg):
        pass
    
    getoptMode = False
    arg = _CommandLine([None, '-a=2'], '-', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.kwargs == {'a':'2'}
    
    
def testCH0012Ok():
    '''Non getopt mode. using kwargs for a flag'''
    
    def method(**kwargs):
        pass
    
    getoptMode = False
    arg = _CommandLine([None, '-a'], '-', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.kwargs == {'a':None}
    
    
def testCH0021Ok():
    '''Non getopt mode. prefix well given with value'''
    
    def method(DPrefix):
        pass
    
    getoptMode = False
    arg = _CommandLine([None, '-Dname=value'], '-', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == [('name', 'value')]
    
    
def testCH0022Ok():
    '''Non getopt mode. prefix well given'''
    
    def method(IPrefix):
        pass
    
    getoptMode = False
    arg = _CommandLine([None, '-Iname'], '-', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == [('name', None)]
    
    
def testCH0023Exception():
    '''Non getopt mode. prefix incorrect'''
    
    def method(IPrefix):
        pass
    
    getoptMode = False
    arg = _CommandLine([None, '-I=name'], '-', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    #return ret and ch.provided[1]==[('name',None)]
    
    
def testCH0024Ok():
    '''Prefix are not mandatory options'''
    
    def method(IPrefix):
        return "Yeah, called"
    
    getoptMode = False
    ch = _CommandHandler(method, getoptMode)
    ret = ch.isInvokable() and ch.invoke()
    return ret=="Yeah, called"
    
    
    
    
    
def testCH0101Ok():
    '''Non getopt mode. Long flag with alias'''
    
    def method(aFlag):
        pass
    
    getoptMode = False
    arg = _CommandLine([None, '-aalias'], '-', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ch.setAliases({'a':'aalias'})
    ret = ch.handleArg(arg)
    return ret and ch.provided[1]
    
    
def testCH0103Ok():
    '''Non getopt mode. Long option given with alias'''
    
    def method(aOption):
        pass
    
    getoptMode = False
    arg = _CommandLine([None, '-aalias=2'], '-', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ch.setAliases({'a':'aalias'})
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == '2'
    
    
    
def testCH0111Ok():
    '''Non getopt mode. prefix well given as alias, with value'''
    
    def method(DPrefix):
        pass
    
    getoptMode = False
    arg = _CommandLine([None, '-definename=value'], '-', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ch.setAliases({'D':'define'})    
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == [('name', 'value')]
    
    
def testCH0112Ok():
    '''Non getopt mode. prefix well given as alias, without value'''
    
    def method(IPrefix):
        pass
    
    getoptMode = False
    arg = _CommandLine([None, '-includename'], '-', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ch.setAliases({'I':'include'})    
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == [('name', None)]
    
    
    
    

    
    
def testCH0201Ok():
    '''getopt mode. Long flag easy'''
    
    def method(verboseFlag):
        pass
    
    getoptMode = False
    arg = _CommandLine([None, '--verbose'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1]
    
    
def testCH0202Nok():
    '''getopt mode. Long flag not given'''
    
    def method(verboseFlag):
        pass
    getoptMode = True
    arg = _CommandLine([None, '--qqw'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret
    
    
def testCH0203Ok():
    '''getopt mode. Long option given'''
    
    def method(modeOption):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, '--mode=2'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == '2'
    

def testCH0211Ok():
    '''getopt mode. prefix well given'''
    
    def method(definePrefix):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, '--definename=value'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == [('name', 'value')]
    
    
def testCH0212Ok():
    '''getopt mode. start flag prefix well given'''
    
    def method(includePrefix):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, '--includename'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == [('name', None)]
    
    
def testCH0301Ok():
    '''getopt mode. Long flag with alias'''
    
    def method(vFlag):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, '--verbose'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ch.setAliases({'v':'verbose'})
    ret = ch.handleArg(arg)
    return ret and ch.provided[1]
    
    
def testCH0303Ok():
    '''getopt mode. Long option given with alias'''
    
    def method(vOption):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, '--verbose=2'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ch.setAliases({'v':'verbose'})
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == '2'
    

def testCH0311Nok():
    '''getopt mode. Short option given as long'''
    
    def method(aOption):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, '--a=2'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret
    
    
def testCH0312Nok():
    '''getopt mode. Short prefix given as long'''
    
    def method(aPrefix):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, '--aValue'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret
    
    
    
def testCH0313Exception():
    '''getopt mode. Short prefix without associated value'''
    
    def method(aPrefix):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, '-a', '-Value'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret
    
    
    
def testCH0321Ok():
    '''getopt mode. Long flag given separated'''
    
    def method(verboseOption):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, '--verbose', 'value'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == 'value'
    
    
def testCH0322Exception():
    '''getopt mode. Long flag given separated but as option'''
    
    def method(verboseOption):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, '--verbose', '-value'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ch.handleArg(arg)
    
def testCH0323Exception():
    '''getopt mode. Long flag given separated but as name/value'''
    
    def method(verboseOption):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, '--verbose', 'name=value'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ch.handleArg(arg)
    
def testCH0401Ok():
    '''getopt mode. Short flag given alone'''
    
    def method(vFlag):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, '-v'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] and arg.finished()
    
def testCH0402Ok():
    '''getopt mode. Short option given alone'''
    
    def method(vOption):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, '-v1'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == '1' and arg.finished()
    
def testCH0403Exception():
    '''getopt mode. Short option without value'''
    
    def method(vOption):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, '-v'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ch.handleArg(arg)
    
    
def testCH0404Ok():
    '''getopt mode. Short option given separately'''
    
    def method(vOption):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, '-v', '1'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] == '1' and arg.finished()
    
def testCH0405Exception():
    '''getopt mode. Short option given separately, wrong'''
    
    def method(vOption):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, '-v', '-a'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ch.handleArg(arg)
    
    
def testCH0406Exception():
    '''getopt mode. Short option given separately, including value'''
    
    def method(vOption):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, '-v', 'a=h'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    
    
    
    
def testCH0411Ok():
    '''getopt mode. A flag given, but not alone'''
    
    def method(vFlag):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, '-vw'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.provided[1] and arg.name == 'w'
    
    
def testCH0501Ok():
    '''getopt mode. Flag and Short options given'''
    
    def method(vOption, wFlag):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, '-wv', 'q'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg) and ch.handleArg(arg)
    return ret and ch.provided[1] == 'q' and ch.provided[2] and arg.finished()


def testCH0601Ok():
    '''getopt mode. Parameter given'''
    
    def method(par1):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, 'file'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg)
    return ret and ch.providedPars == ['file'] and arg.finished()


def testCH0602Ok():
    '''getopt mode. Two parameters given'''
    
    def method(par1, par2):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, 'file', 'more'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg) and ch.handleArg(arg) 
    return ret and ch.providedPars == ['file', 'more'] and arg.finished()

def testCH0603Nok():
    '''getopt mode. Two parameters given, only one expected'''
    
    def method(par1):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, 'file', 'more'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg) and ch.handleArg(arg) 
    return ret

def testCH0605Ok():
    '''getopt mode. Using vararg for two arguments'''
    
    def method(*var):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, 'file', 'more'], '--', '=', False)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg) and ch.handleArg(arg) and arg.finished()
    return ret

def testCH0611Ok():
    '''getopt mode. Checkin gnu mode'''
    
    def method(aFlag, par1, par2):
        pass
    
    getoptMode = True
    arg = _CommandLine([None, '-a', 'par1', '-v'], '--', '=', True)
    ch = _CommandHandler(method, getoptMode)
    ret = ch.handleArg(arg) and ch.handleArg(arg) and ch.handleArg(arg) and arg.finished()
    return ret




def testG0001Ok():
    '''Simple test, no args'''
    
    class Simple(OptionMatcher):
        
        def handle(self):
            self.ok = True
            return True
        
    s = Simple()
    return s.process([None]) and s.ok

def testG0002Ok():
    '''Simple test, one optional parameter, not given'''
    
    class Simple(OptionMatcher):
        
        def handle(self, par=None):
            self.ok = True
            return True
        
    s = Simple()
    return s.process([None]) and s.ok

def testG0003Ok():
    '''Simple test, one optional flag, not given'''
    
    class Simple(OptionMatcher):
        
        def handle(self, vFlag=None):
            self.ok = True
            return True
        
    s = Simple()
    return s.process([None]) and s.ok

def testG0004Ok():
    '''Simple test, one optional option, not given'''
    
    class Simple(OptionMatcher):
        
        def handle(self, vOption=None):
            self.ok = True
            return True
        
    s = Simple()
    return s.process([None]) and s.ok


def testG0011Exception():
    '''Simple test, one flag, not given'''
    
    class Simple(OptionMatcher):
        
        def handle(self, vFlag):
            pass
        
    return Simple().process([None])


def testG0012Ok():
    '''Simple test, one flag, given'''
    
    class Simple(OptionMatcher):
        
        def handle(self, vFlag):
            self.ok = True
            return True
        
    s = Simple()
    return s.process([None, '-v']) and s.ok


def testG0013Exception():
    '''Simple test, one flag, two given'''
    
    class Simple(OptionMatcher):
        
        def handle(vFlag):
            pass
        
    return Simple().process([None, '-vw'])


def testG0021Ok():
    '''More complex test, two flags, one parameter'''
    
    class Simple(OptionMatcher):
        
        def handle(self, vFlag, oFlag, par):
            self.ok = str(vFlag) + str(oFlag) + par
            return True
        
    s = Simple()
    return s.process([None, '-vo', 'file']) and s.ok == 'TrueTruefile'


def testG0022Ok():
    '''More complex test, one flag, one option, one parameter'''
    
    class Simple(OptionMatcher):
        
        def handle(self, vFlag, oOption, par):
            self.ok = str(vFlag) + oOption + par
            return True
        
    s = Simple()
    return s.process([None, '-vo1', 'file']) and s.ok == 'True1file'


def testG0023Ok():
    '''More complex test, one flag, one separated option, one parameter'''
    
    class Simple(OptionMatcher):
        
        def handle(self, vFlag, oOption, par):
            self.ok = str(vFlag) + oOption + par
            return True
        
    s = Simple()
    return s.process([None, '-vo', '1', 'file']) and s.ok == 'True1file'


def testG0024Ok():
    '''Verifying that prefixes are not required'''
    
    class Simple(OptionMatcher):
        
        def handle(self, vFlag, oOption, dPrefix, par):
            self.ok = str(vFlag) + oOption + par + str(dPrefix)
            return True
        
    s = Simple()
    return s.process([None, '-vo', '1', 'file']) and s.ok == 'True1file[]'


def testG0031Ok():
    '''More complex test, two possible handlers'''
    
    class Simple(OptionMatcher):
        
        def handle(vFlag, oOption, par):
            pass
        
        def handle2(self, vFlag, par):
            self.ok = str(vFlag) + par
            return True
        
    s = Simple()
    return s.process([None, '-v', 'file']) and s.ok == 'Truefile'


def testG0032Ok():
    '''More complex test, two possible handlers and a common one'''
    
    class Simple(OptionMatcher):
        
        def common_options(self, vFlag):
            self.v = str(vFlag)
        
        def handle(self, oOption, par):
            return False
        
        def handle2(self, par):
            self.ok = self.v + par
            return True
        
    s = Simple()
    return s.process([None, '-v', 'file']) and s.ok == 'Truefile'


def testG0033Exception():
    '''More complex test, two possible handlers and a common one, not given'''
    
    class Simple(OptionMatcher):
        
        def common_options(self, vFlag):
            pass
        
        def handle(self, oOption, par):
            pass
        
        def handle2(self, par):
            pass
        
    return Simple().process([None, 'file'])


def testG0041Ok():
    '''Aliases test using common'''
    
    class Simple(OptionMatcher):
        
        def common_options(self, vFlag):
            self.v = str(vFlag)
        
        def handle(self, oOption, par):
            self.ok = self.v + oOption + par
            return True
        
    s = Simple()
    return s.process([None, '--verbose', '--option=2', 'file'],
                     aliases={'v':'verbose', 'o':'option'}) and s.ok == 'True2file'


def testG0042Ok():
    '''Aliases test using common, varargs'''
    
    class Simple(OptionMatcher):
        
        def common_options(self, vFlag):
            self.v = str(vFlag)
        
        def handle(self, oOption, *ends):
            self.ok = self.v + oOption + str(ends)
            return True
        
    s = Simple()
    return s.process([None, '--verbose', '--option=2', '1', '2'],
                     aliases={'v':'verbose', 'o':'option'}) and s.ok == "True2('1', '2')"



def testG0043Exception():
    '''Aliases test, overriding some definition'''
    
    class Simple(OptionMatcher):
        
        def handle(self, oOption, kOption):
            pass
        
    s = Simple()    
    return s.process([], aliases={'o':'k'})


def testG0044Exception():
    '''Aliases test, overriding some definition'''
    
    class Simple(OptionMatcher):
        
        def handle(self, oOption, optOption):
            pass
        
    s = Simple()    
    return s.process([], aliases={'o':'opt'})



def testG0045Exception():
    '''Aliases test, overriding some definition, way round'''
    
    class Simple(OptionMatcher):
        
        def handle(self, oOption, optOption):
            pass
        
    s = Simple()    
    return s.process([], aliases={'opt':'o'})

def testG0046Exception():
    '''Aliases test, overriding some definition, not getopt mode'''
    
    class Simple(OptionMatcher):
        
        def handle(self, oOption, vOption):
            pass
        
    s = Simple()    
    return s.process([], aliases={'v':'o'}, option='-')



def testG0051Ok():
    '''Integer options'''
    
    class Simple(OptionMatcher):
        
        def handle(self, valOptionInt):
            self.ok = valOptionInt
            return True
        
    s = Simple()
    return s.process([None, '--val=2']) and s.ok == 2


def testG0052Exception():
    '''Integer options, string for integer'''
    
    class Simple(OptionMatcher):
        
        def handle(self, valOptionInt):
            self.ok = valOptionInt
            return True
        
    s = Simple()
    return s.process([None, '--val=two']) and s.ok == 2

def testG0053Exception():
    '''Integer options, string for integer'''
    
    class Simple(OptionMatcher):
        
        def handle(self, valOptionInt):
            self.ok = valOptionInt
            return True
        
    s = Simple()
    return s.process([None, '--val=2.3']) and s.ok == 2


def testG0054Ok():
    '''Float options'''
    
    class Simple(OptionMatcher):
        
        def handle(self, valOptionFloat):
            self.ok = valOptionFloat
            return True
        
    s = Simple()
    return s.process([None, '--val=2.3']) and s.ok == 2.3


def testG0055Exception():
    '''Float options, string for float'''
    
    class Simple(OptionMatcher):
        
        def handle(self, valOptionFloat):
            self.ok = valOptionFloat
            return True
        
    s = Simple()
    return s.process([None, '--val=two']) and s.ok == 2

def testG0056Ok():
    '''Float options, integer for float'''
    
    class Simple(OptionMatcher):
        
        def handle(self, valOptionFloat):
            self.ok = valOptionFloat
            return True
        
    s = Simple()
    return s.process([None, '--val=2']) and s.ok == 2



def testP0001Ok():
    '''API test: setNonGetoptMode'''

    class Simple(OptionMatcher):
        
        def handle(self, oOption, arg):
            self.ok = oOption + arg
            return True
        
    s = Simple()
    return s.process([None, '/o:23', 'file'], 
                     option='/', delimiter=':') and s.ok == "23file"

def testP0002Ok():
    '''API test: setNonGetoptMode with aliases'''

    class Simple(OptionMatcher):
        
        def handle(self, oOption, arg):
            self.ok = oOption + arg
            return True
        
    s = Simple()
    return s.process([None, '/opt:23', 'file'],
                     aliases={'o':'opt'},
                     option='/', delimiter=':') and s.ok == "23file"

def testP0003Ok():
    '''API test: setNonGetoptMode with aliases way around'''

    class Simple(OptionMatcher):
        
        def handle(self, oOption, arg):
            self.ok = oOption + arg
            return True
        
    s = Simple()
    return s.process([None, '/opt:23', 'file'],
                     aliases={'o':'opt'},
                     option='/', delimiter=':') and s.ok == "23file"


def testP0011Ok():
    '''API test: specifying external common handler'''
    
    class Any(object):
        
        @staticmethod
        def specificCommonHandler(oOption):
            Any.oOption = oOption
        
    class Simple(OptionMatcher):
        
        def handle(self, arg):
            self.ok = Any.oOption + arg
            return True
        
    s = Simple()
    return s.process([None, '-o23', 'file'], common=Any.specificCommonHandler) and s.ok == "23file"



def testP0012Ok():
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


def testP0021Ok():
    '''API test: specifying static method as command handler'''
    
    class Simple(object):
        
        @staticmethod        
        def handle(f):
            return f
        
    ah = OptionMatcher()
    return ah.process([None, 'ok'], matchers=[Simple.handle])=='ok'


def testP0022Exception():
    '''API test: specifying incorrect flags on command handler'''
    
    def work(aFlag, aOption):
        pass
    
    ah = OptionMatcher()
    return ah.process([None], matchers=[work])






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
        handle(testCH0024Ok)
    else:
        pass
        
