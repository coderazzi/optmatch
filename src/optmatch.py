import re
import types

class _CommandLine(object):
    '''Class to handle the Command Line arguments, splitting them as 
          required.  It allows handling arguments one by one, even for 
          short options, where -cov could mean -c -o -v
       Available instance attributes:
          arg    : String, the whole argument, without the prefix option
                   if the argument were '--option', arg would be 'option'
          name   : String, the name of the current argument
                   if the argument were '--op=2', name would be 'op'
          value  : String, the value of the current argument
                   if the argument were '--op=2', name would be '2'
          option : Bool, true if the current argument is an option
          isShort: Bool, true if the current arg is a short option
    ''' 
       
    def __init__(self, args, optionPrefix, delimiter, gnuMode):
        '''args: the list of arguments to handle (first is dismissed)
           optionPrefix: the prefix for the options. If '--', it will
                         be enabled the usage of short options with '-'.
                         Must be escaped for RE purposes
           delimiter: the string to be used as separator between
                      names and values. Must be escaped for RE purposes
           gnuMode: if true, after a non option argument, all remaining
                    arguments will be treated as non options 
        '''
        self.args = args
        self.reShort = (optionPrefix == '--') and re.compile('-(.+)$')
        self.reOption = re.compile(optionPrefix + '(.+)$')
        self.reSeparation = re.compile('(.+?)' + delimiter + '(.+)$')
        self.gnuMode = gnuMode
        self.canBeOption = True  
        self.reset()
        
    def reset(self):
        self.next = 1
        if len(self.args) > 1:
            self._next()
        
    def finished(self):
        return self.next == 1
    
    def separate(self, what):
        '''Separates the passed string into name and value
           Returns a tuple (status, name, value) where status is True
             if the string was separated
        '''
        m = self.reSeparation.match(what)
        return m and (True, m.group(1), m.group(2)) or (False, what, None)
        
    def setArgHandled(self):
        '''Reports that the current argument has been handled.
           It returns True if there are no more arguments to handle or the 
              next argument is an option
        '''
        if self.next >= len(self.args):
            self.next = 1
        return (self.next == 1) or self._next()
            
    def setShortArgHandled(self):
        '''Reports that the current (short!) argument has been handled.'''
        if self.value:
            self.name, self.value = self.value[0], self.value[1:]
        else:
            self.setArgHandled()
    
    def _next(self):
        '''Handles the next argument, returing True if it is an option'''
        self.arg = self.args[self.next]
        self.next += 1
        self.option = False
        if self.canBeOption:
            match = self.reOption.match(self.arg)
            if match:
                self.option, self.isShort = True, False
                self.arg = match.group(1)
            else:               
                match = self.reShort and self.reShort.match(self.arg)
                if match:
                    self.arg = match.group(1)
                    self.name, self.value = self.arg[0], self.arg[1:]
                    self.option, self.isShort, self.split = True, True, False
                    return True
                self.canBeOption = not self.gnuMode
        self.split, self.name, self.value = self.separate(self.arg)
        return self.option

        
class _CommandHandler(object):
    '''Internal class, representing each specific command handler.
       A command handler is each separate method or function that 
          can handle one or more arguments'''
        
    INT_TYPE=1
    FLOAT_TYPE=2
    FLAG_PATTERN = re.compile('(.+?)(Flag|Option|' + 
                              'OptionInt|OptionFloat|Prefix)$')
        
    def __init__(self, function, getoptMode):
        '''The constructor requires a function or bound method.
           getoptMode is a boolean parameter that specifies whether
             to use getoptMode or not. In getoptMode, there is specific
             support for short/long options; in addition, kwargs
             parameters cannot be supported.
        '''
        self.func = function
        self.defs = set()       #definitions (flags/options/prefixes)
        self.flags = {}         #mapping known flag to argument index
        self.options = {}       #mapping known option to argument index
        self.checks = {}        #type checking on options
        self.prefixes = {}      #mapping known prefix to argument index
        self.pars = {}          #parametrs: mapping from index to name
        self.vararg = False     #whether it supports varargs 
        self.kwargs = False     #whether it supports kwargs (a dict if it does) 
        self.defaults = {}      #default values for flags and options
        self.provided = {}      #definitions given by the user
        self.providedPars = []  #what has been provided as parameters
        self.lastArg = 1        #number of arguments. 
        self.getoptMode = getoptMode

        #With getoptMode, in addition to the normal definitions, users
        # can specify short options, stored in sortedDefs 
        if getoptMode:
            self.shortDefs = set()    
        else:
            self.shortDefs = self.defs
        
        #Note that all arg indexes start with 1. When accessing the dicts 
        # (self.flags, etc) it simplifies testing for key existence
        for name, default in self._parseFunction(function):
            self._setupParameter(name, self.lastArg)
            if default is not self:
                self.defaults[self.lastArg] = default
            self.lastArg += 1
            
    def getUsageInformation(self):
        '''Returns all usage information as a tuple of 3 elements
           1- The options, as a list of tuples, where each tuple defines the
                 equivalent options. I.e: [[m, mode], [h, help]]. 
           2- The positional argument names
           3- A tuple (varg, kw), to define the support for varg and kwargs
        '''
        options={}
        for group in self.flags, self.options, self.prefixes:
            for name, index in group.items():
                options.setdefault(index, []).append(name)
        pars=self.pars.keys()
        pars.sort()        
        return options.values(), [self.pars[i] for i in pars],\
               (self.vararg>0, self.kwargs!=False)
                                        
    def setAliases(self, aliases):
        '''Sets aliases between option definitions.
           Aliases affect to all possible options (flags/options/prefixes).
           In getoptMode, aliases must map short and long options, 
             that is, options with 1 character and options with more 
             than 1 character
        '''
        for s, l in aliases.items():
            if self.getoptMode:
                #aliases are from short to long mode, or viceversa
                s, l = self._getShortAndLongAliases(s, l)
                self._setAlias(l, s, self.defs, self.shortDefs)
            elif l in self.defs:
                #if alias 'l' is already known, we try setting from s->l
                s, l = l, s
            self._setAlias(s, l, self.shortDefs, self.defs)
            
    def _getShortAndLongAliases(self, s, l):
        '''Returns (short option, long option), only for getopt mode'''
        if len(s) != 1:
            if len(l) == 1:
                return l, s
        elif len(l) > 1:
            return s, l
        raise OptionMatcherException('Bad alias:' + s + '/' + l)
                                                
    def _setAlias(self, a, b, aSet, bSet):
        '''Defines b as an alias in bSet of a, if a is defined in aSet
           As a result, any option defined as 'a' will be used if the 
              user specifies the 'b'
        '''
        if a in aSet:
            if b in bSet:
                raise OptionMatcherException(
                    'Bad alias:' + a + '/' + b + ' for ' + self._describe())
            bSet.add(b)
            for group in self.flags, self.options, self.prefixes:
                try:
                    group[b] = group[a]
                except KeyError:
                    pass

    def reset(self):
        self.provided, self.providedPars = {}, []
                
    def invoke(self):
        '''Invokes the underlying function.
           It is invoked using the options/parameters/defaults 
              already setup
           It is an error to invoke this method if isInvokable 
              returned False
        '''
        args, kwargs = self._getInvokingPars()
        return self.func(*args, **kwargs)
    
    def isInvokable(self):
        '''Verifies whether the underlying function can be invoked.
           It can be invoked if all the options/parameters are specified
              or have default values
        '''
        return self._getInvokingPars() != None
        
    def _getInvokingPars(self):
        '''Returns the parameters required to invoke the underlying function.
           The parameters are returned as a tuple (*args, **kwargs), 
        '''
        args, parameters = [], self.providedPars[:]
        for i in range(1, self.lastArg):
            try:
                value = self.provided[i] #read first the provided value
            except KeyError:
                #otherwise, the current index could refer to a parameter,
                #which are stored separately
                if i in self.pars and parameters:
                    value = parameters.pop(0) 
                else:
                    #this argument were not provided: try the default value
                    try:
                        value = self.defaults[i]
                    except KeyError:
                        #Neither, this function cannot be invoked
                        return None
            args.append(value)
        #if the function defined a *arg parameter, it can handle the 
        #  remaining provided parameters
        args.extend(parameters)
        return args, self.kwargs or {}
                        
    def handleArg(self, commandLine):
        '''Handles one argument in the command line.
           This handling can imply, under getopt mode, consuming more 
             than one argument in the command line, or just a portion
             of one, if a short option was specified
        '''
        if commandLine.option:
            if commandLine.isShort:
                return self._handleShortArg(commandLine)
            return self._handleLongArg(commandLine)
        if self.vararg or (len(self.providedPars) < len(self.pars)):
            self.providedPars.append(commandLine.arg)
            commandLine.setArgHandled()
            return True
        return False
    
    def _handleLongArg(self, cmd):
        '''Handles one long argument in the command line.'''
        name = cmd.name
        #only check the name if defined (and not defined as a short option)
        okName = name in self.defs
        if okName and self._handleOption(cmd):
            return True
        
        flag = okName and self.flags.get(name, None)
        if flag:
            if cmd.split: #flag, but user specified a value
                raise UsageException('Incorrect flag ' + name)
            self.provided[flag] = True
        else:
            prefix, name = self._splitPrefix(name)
            if prefix:
                if not name:
                    #perhaps is given as -D=value(bad) or separate (getoptMode)
                    if cmd.split or not self.getoptMode or cmd.setArgHandled():
                        raise UsageException('Incorrect prefix ' + cmd.arg)
                    #note that cmd.value is the value of next argument now
                    name = cmd.name 
                self.provided[prefix].append((name, cmd.value))
            else: #try now the self.kwargs, if possible
                try:
                    self.kwargs[cmd.name] = cmd.value
                except TypeError:
                    return False #no kwargs, this argument cannot be used                    
        cmd.setArgHandled()
        return True
            
    def _handleShortArg(self, command):
        '''Handles one argument in the command line, given as a short argument
           This method is only called for getopt mode
        '''
        name = command.name
        if not name in self.shortDefs:
            #in shorts, name is just one letter, so not inclusion 
            #in shortDefs means that is neither a prefix
            return False
        flag = self.flags.get(name, None)
        if flag:
            self.provided[flag] = True
            command.setShortArgHandled()
        elif not self._handleOption(command):
            prefix = self.prefixes.get(name, None)
            #no flag, no option, but in shortDefs->is a prefix! 
            if not command.value:
                #given separately                    
                if command.setArgHandled():
                    raise UsageException('Incorrect prefix ' + name)
                command.value = command.arg
            self.provided[prefix].append(command.separate(command.value)[1:])
            command.setArgHandled()            
        return True
                
    def _handleOption(self, cmd):
        '''Checks if the command is a valid option, handling it if so'''
        #the normal case, -name=value, implies command.value
        name=cmd.name
        option = self.options.get(name, None)
        if option:
            if cmd.value:
                value=cmd.value
            else:
                #under getoptMode, this is still valid if the value is
                #provided as a separate argument (no option, no split)                
                if not self.getoptMode or cmd.setArgHandled() or cmd.split:
                    raise UsageException('Incorrect option ' + name)
                value = cmd.arg
            check = self.checks.get(option, 0)
            try:
                if check==self.INT_TYPE:
                    value=int(value)
                elif check==self.FLOAT_TYPE:
                    value=float(value)
            except ValueError:
                raise UsageException('Incorrect value for ' + name)
            self.provided[option] = value
            cmd.setArgHandled()
        return option
                        
    def _splitPrefix(self, name):
        '''Splits an existing prefix from the given name.
           It does not apply to short prefixes (getopt mode)
           It returns the tuple (prefix, rest), or (None, None) if not found
        '''
        for each in self.prefixes:
            if each in self.defs and name.startswith(each):
                return self.prefixes[each], name[len(each):]
        return None, None
                            
    def _describe(self):
        '''Describes the underlying method'''
        try:
            name = 'method ' + self.func.im_self.__class__.__name__ + '.'
        except AttributeError:
            name = 'function '
        return name + self.func.__name__
            
    def _parseFunction(self, function):
        '''Obtains the parameters and default values in the function.
           It handles specially the parameters self, *args, **kwargs
           Self parameter, for bound methods, is discarded.
           If *arg parameter is present, self.vararg is set to True
           If *kwargs parameter is present, and is not getopt mode,
              self.kwargs is set to {}
           The returned value is a a list of tuples (name, default value)           
        '''
        flags = function.func_code.co_flags
        vars = function.func_code.co_varnames
        #dismiss *args and **kwargs
        self.vararg = flags & 0x0004 
        if self.vararg: vars = vars[:-1]
        if flags & 0x0008:
            vars = vars[:-1]
            #only on non getoptMode we can properly support kwargs
            self.kwargs = not self.getoptMode and {}
        #we set impossible value 'self' as value for not default
        defs = list(function.func_defaults or [])
        ret = zip(vars, [self] * (len(vars) - len(defs)) + defs)
        try:
            if not function.im_self:
                raise OptionMatcherException('Unbound ' + self._describe())
            ret = ret[1:] #dismiss first argument
        except AttributeError:
            pass
        return ret
    
    def _setupParameter(self, name, index):
        '''Setups the parameter with given name.
           The setup depends of the name suffix
        '''
        match = self.FLAG_PATTERN.match(name)
        if match:
            useName = match.group(1)
            self._newDefinition(useName)
            what = match.group(2)
            if what == 'Flag':
                self.flags[useName] = index
            elif what == 'Prefix':
                self.prefixes[useName] = index
                self.provided[index] = []
            else:
                self.options[useName] = index
                if what == 'OptionInt':
                    self.checks[index]=self.INT_TYPE
                elif what == 'OptionFloat':
                    self.checks[index]=self.FLOAT_TYPE
        else:
            self.pars[index]=name

    def _newDefinition(self, name):
        '''Adds the new option definition (into shortDefs or defs)'''
        if len(name) == 1:
            #note that, in non getopt mode, shortDefs points to defs
            defSet=self.shortDefs
        else:
            defSet=self.defs
        if name in defSet: #for example, defining kFlag and kOption
            raise OptionMatcherException('Repeated option "' + name + 
                                         '" in ' + self._describe())
        defSet.add(name)
    
        
class OptionMatcherException(Exception):
    '''Exception raised when a problem happens during handling setup'''

        
class UsageException(OptionMatcherException):
    '''Exception raised while handling an argument'''
            

class OptionMatcher (object):
    ''' 
        Class to handle command line arguments by matching the
           parameters expected in specific methods. It supports
           naturally the handling of mutually exclusive options.
           
        For example, a OptionMatcher subclass could define the methods:
        
           def handle(suffixOption, file, verboseFlag=None, DPrefix=None):
              pass
           
           def handleHelp(usageFlag):
              pass
              
           This class would support one of the following inputs:
              [--verbose] --suffix=value [-Done ...] filename
              Or
              [--usage]

        It is possible to specify one or more functions or methods -from
           now called matchers- to process command line arguments. 
           The name of the parameters identify whether it is a flag, 
           and option, a prefix, or a simple non option argument.
           
        If there is one matcher that can handle every command line
           arguments, it is invoked with the appropiate arguments. 
           If there were more than one match, the first one is invoked.
           
        It is also possible to specify a single matcher to handle options
           which are common to every other possible matcher.
           
        By default, the matchers are all methods of this class with
           prefix 'handle', sorted alphabetically. If the class contains
           a 'common_options' method, it is used as common matcher.
    '''
    
    HANDLE_PATTERN = re.compile('handle.*$')
    COMMON = 'common_options'

    def process(self, args, matchers=None, common=None, aliases=None,
                option='--', gnu=False, delimiter='='):
        '''Processes the given command line arguments
           matchers define the instances/methods/functions to handle 
              the command line. If a matcher is an instance, all 
              its methods with prefix 'handle' are automatically used.
           common can be used to specify a matcher to handle common options 
              If it is not specified, and the passed matchers contain 
              one single element, which is an instance defining a method
              'commonOptions', this method it is automatically used to 
              handle the common options
           aliases is a map, allowing setting option aliases. 
              In getopt mode, all aliases must be defined between a short
              (1 character length) option and a long (>1 character length)
              option   
           option defines the prefix used to characterize an argument
              as an option. If is defined as '--', it implies 
              automatically getopt mode, which enables the usage of 
              short options with prefix -
           gnu determines gnu behaviour. Is True, 
              no-option arguments can be only specified latest
           delimiter defines the character separating options' name 
              and value
        '''
        getoptMode = option == '--'
        
        def handleCreator(function):
            ret = _CommandHandler(function, getoptMode)
            if aliases:
                ret.setAliases(aliases)                
            return ret
            
        matchers = matchers or [self] #use self if no matchers specified
        commandLine = _CommandLine(args, option, delimiter, gnu)
        commonHandler, handlers = self._getCommandHandlers(
               common, matchers, handleCreator) 
        
        for handler in handlers:
            if commonHandler:
                commonHandler.reset()
            if self._validHandlers(commonHandler, handler, commandLine):
                if commonHandler:
                    commonHandler.invoke()
                return handler.invoke()
            commandLine.reset()
        raise UsageException ('Invalid command line input')

    def _validHandlers(self, commonHandler, commandHandler, commandLine):
        '''Checks if the specified handlers can process the command line.
           If so, it returns True, letting the handlers ready to be invoked 
        '''
        while not commandLine.finished():
            if commonHandler:
                if commonHandler.handleArg(commandLine):
                    continue
            if not commandHandler.handleArg(commandLine):
                return False
        if commonHandler and not commonHandler.isInvokable():
            return False
        return commandHandler.isInvokable()
               
    def _getCommandHandlers(self, common, funcs, handleCreator):
        '''Creates all required _CommandHandler instances
           It returns the handler for the common options, and a list
              with handlers for all suitable function/methods
           funcs refers to any specified function/bound method or 
              class instance. In the latest case, all non static methods
              with prefix handle are used to create handlers
           If the parameter common is None, and funcs contain one only
              element, and is a class instance, it is observed to check
              if it contain a common_options method. If so, it will be 
              used as _CommandHandler for the common options                    
        '''
        handlers = []
        for each in funcs:
            if self._asFunction(each):
                handlers.append(handleCreator(each))
            else: #treat as instance: extract handlers
                for att in dir(each):
                    if self.HANDLE_PATTERN.match(att):
                        f = getattr(each, att)
                        if self._asFunction(f):
                            handlers.append(handleCreator(f))
        if not common and len(funcs) == 1 and hasattr(funcs[0], self.COMMON):             
            common = self._asFunction(getattr(funcs[0], self.COMMON))
        return (common and handleCreator(common)), handlers
    
    def _createHandler(self, function, getoptMode, aliases):
        '''Creates a _CommandHandler for the specified function
           It setups correctly the _CommandHandler, with the specified aliases
        '''
        ret = _CommandHandler(function, getoptMode)
        ret.setAliases(aliases)
        return ret
        
    def _asFunction(self, what):
        '''It returns the passed argument If it is a function or bound method.
           Otherwise, it returns False
        ''' 
        return (isinstance(what, types.FunctionType) or
               (isinstance(what, types.MethodType) and what.im_self) and what)
    
