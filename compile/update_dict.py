import re

def get_user_id(path) :
    return path.split('/')[-1]

def set_column_in_user_dict(user_dict,column,value):
    user_dict[column] = str(value)

def set_exe_size(user_dict, size):
    set_column_in_user_dict(user_dict,'exe_size', size)

def set_compile_exitcode(user_dict,exit_code) :
    set_column_in_user_dict(user_dict,'compiled',exit_code)

def set_compiler_version(user_dict,version) :
    set_column_in_user_dict(user_dict,'compiler_version',version)

def remove_unwanted_chars(msg):
    if '\t' in msg :
        print 'found tab'
        msg = msg.replace('\t', ' ')
    if '^' in msg :
        msg = msg.replace('^', ' ')
    if ',' in msg :
        msg = msg.replace(';', ' ')
    return msg

def python_format(msg) :
    if 'Errno 2' in msg :
        return 'File or Dir not found'
    elif 'SyntaxError' in msg :
        return 'SyntaxError'
    elif 'TypeError' in msg :
        return 'TypeError'
    elif 'ValueError' in msg :
        return 'ValueError'
    elif 'ImportError' in msg :
        return 'ImportError'
    elif 'IndexError' in msg :
        return 'IndexError'
    elif 'AssertionError' in msg :
        return 'AssertionError'
    else :
        return 'Unknown'

def cpp_formating_compile(msg) :
    if 'expected primary-expression' in msg :
        return 'expected primary-expression'
    elif 'redeclaration' in msg :
        return'redeclaration'
    elif 'redeclared' in msg :
        return 'redeclared'
    elif 'No such file' in msg :
        return 'No such file or directory'
    elif 'not declared' in msg :
        return 'not declared'
    elif 'reference' in msg and 'ambiguous' in msg :
        return 'reference is ambiguous'
    elif 'Usage' in msg :
        return 'Usage'
    elif 'Bad address' in msg :
        return 'Bad address'
    elif 'Assertion failed' in msg :
        return 'Assertion failed'
    elif 'Abort trap' in msg :
        return 'Abort trap'
    else :
        return 'Unknown error'

def java_format_compile(msg) :
    if 'unmappable character for encoding UTF8' in msg :
        return 'unmappable character for encoding UTF8'
    elif 'not a statement' in msg :
        return 'not a statement'
    elif 'Syntax error' in msg :
        return 'Syntax error'
    elif 'package' in msg :
        return 'package does not exist'
    elif 'cannot find symbol' in msg :
        return 'cannot find symbol'
    elif '<identifier> expected' in msg :
        msg = 'expected ;'
    else :
        return 'Unknown error'

def format_error_msg(msg, lang) :
    if lang == 'C++' :
        return cpp_formating_compile(msg)
    elif lang == 'Java' :
        return java_format_compile(msg)
    else :
        msg = remove_unwanted_chars(msg)
        if '\n' in msg :
            msg = msg.replace('\n', ' ')
        if  'error' in msg :
             index1 = msg.find('error')
             index2 = msg[index1:].find(':')
             msg = msg[index1+index2:]
        if len(msg) > 80 :
            msg = msg[0:80]
        if len(msg) == 0 : 
            msg = 'Unknown'
        return msg

def cpp_formating_run(msg) :
    if 'Segmentation fault' in msg :
        return 'Segmentation fault'
    elif 'Assertion' in msg:
        return 'Assertion failed'
    elif 'underflow error reading the file' in msg :
        return 'underflow error reading the file'
    elif 'invalid pointer' in msg :
        return 'invalid pointer'
    else :
        return 'Unknown error'

def format_run_msg(msg, lang) :
    # remove last two lines, cotains mesured data
    lines = msg.split('\n')
    lines = lines[:-2]
    msg = ' '.join(lines)
    if lang == 'Java':
        index1 = msg.find('java')
        index2 = msg[index1:].find(' ')
        msg = msg[index1:index2]
    elif lang == 'Python':
        msg = python_format(msg)
    elif lang == 'C++' or lang == 'C':
        msg = cpp_formating_run(msg)
    else :
        index1 = msg.find(':')
        index2 = msg[index1+1:].find(':')
        msg = msg[index1:index1+index2+1]
    if len(msg) > 80 :
        msg = msg[0:80]
    return msg


def set_compile_error_msg(user_dict, msg, exit_code, lang):
    if str(exit_code) == '0' :
        msg = '-'
    elif str(exit_code) == '-15' :
        msg = 'Timeout'
    elif str(exit_code) == '127':
        msg = 'Command not found'
    else:
        msg = format_error_msg(msg, lang)
    print 'Writing: ' + msg
    set_column_in_user_dict(user_dict,'compile_error_msg', msg)

def set_run_error_msg(user_dict, msg, exit_code, lang):
    if str(exit_code) == '-15' :
        msg = 'Timeout'
    elif str(exit_code) == '127':
        msg = 'Command not found'
    elif str(exit_code) == '0':
        msg = '-'
    else :
        msg = format_run_msg(msg, lang)
        if len(msg) == 0 :
            msg = '-'
            
    print 'Writing: ' + msg
    set_column_in_user_dict(user_dict,'run_error_msg', msg)

def get_mesurments(errors) :
    regex = "\,\d?\.?\d*"
    res = []
    output = re.findall(regex, errors)
    print errors
    #remove first comma
    for s in output :
        res.append(s[1:])
    return res

def write_to_user_dict(user_dict, exit_code, mesurments):
    user_dict['exit_code'] = exit_code
    if not len(mesurments) == 10 :
        user_dict['wall_clock'] = '-'
        user_dict['user_time'] = '-'
        user_dict['system_time'] = '-'
        user_dict['avg_memory'] = '-'
        user_dict['max_RAM'] = '-'
        user_dict['avg_RAM'] = '-'
        user_dict['nbr_page_faults'] = '-'
        user_dict['nbr_file_out'] = '-'
        user_dict['nbr_file_in'] = '-'
        user_dict['swap_main_memory'] = '-'
    else :
        user_dict['wall_clock'] = mesurments[0]
        user_dict['user_time'] = mesurments[1]
        user_dict['system_time'] = mesurments[2]
        user_dict['avg_memory'] = mesurments[3]
        user_dict['max_RAM'] = mesurments[4]
        user_dict['avg_RAM'] = mesurments[5]
        user_dict['nbr_page_faults'] = mesurments[6]
        user_dict['nbr_file_out'] = mesurments[7]
        user_dict['nbr_file_in'] = mesurments[8]
        user_dict['swap_main_memory'] = mesurments[9]
    return dict

def set_run_mesurments(exit_code, errors, user_dict) :
    mesurments = get_mesurments(errors)
    return write_to_user_dict(user_dict, exit_code, mesurments)

'''
c_sharp_compile = '/home/useruser/datacollection/solutions_2453486_1/C#/Akira/Program.cs(4,22): error CS0234: The type or namespace name `Forms does not exist in the namespace `System.Windows. Are you missing `System.Windows.Forms assembly reference? /home/useruser/datacollection/solutions_2453486_1/C#/Akira/Form1.cs(4,14): error CS0234: The type or namespace name `Data does not exist in the namespace `System. Are you missing `System.Data assembly reference? /home/useruser/datacollection/solutions_2453486_1/C#/Akira/Form1.cs(8,22): error CS0234: The type or namespace name `Forms does not exist in the namespace `System.Windows. Are you missing `System.Windows.Forms assembly reference? /home/useruser/datacollection/solutions_2453486_1/C#/Akira/Form1.cs(12,34): error CS0246: The type or namespace name `Form could not be found. Are you missing an assembly reference?'
c_sharp_run = 'Unhandled Exception: System.TypeInitializationException: An exception was thrown by the type initializer for codeJam2013QRnd.FileOPS ---> System.IO.FileNotFoundException: Could not find file /home/useruser/GCJ-mining/compile/C:\Users\dkulkarni1\Downloads\A-large.in. File name: /home/useruser/GCJ-mining/compile/C:\Users\dkulkarni1\Downloads\A-large.in at System.IO.FileStream..ctor (System.String path, FileMode mode, FileAccess access, FileShare share, Int32 bufferSize, Boolean anonymous, FileOptions options) [0x00000] in <filename unknown>:0 at System.IO.FileStream..ctor (System.String path, FileMode mode, FileAccess access, FileShare share) [0x00000] in <filename unknown>:0 at (wrapper remoting-invoke-with-check) System.IO.FileStream:.ctor (string,System.IO.FileMode,System.IO.FileAccess,System.IO.FileShare) at System.IO.File.OpenRead (System.String path) [0x00000] in <filename unknown>:0 at System.IO.StreamReader..ctor (System.String path, System.Text.Encoding encoding, Boolean detectEncodingFromByteOrderMarks, Int32 bufferSize) [0x00000] in <filename unknown>:0 at System.IO.StreamReader..ctor (System.String path) [0x00000] in <filename unknown>:0 at (wrapper remoting-invoke-with-check) System.IO.StreamReader:.ctor (string) at System.IO.File.OpenText (System.String path) [0x00000] in <filename unknown>:0 at System.IO.File.ReadAllLines (System.String path) [0x00000] in <filename unknown>:0 at codeJam2013QRnd.FileOPS..cctor () [0x00000] in <filename unknown>:0 --- End of inner exception stack trace --- at codeJam2013QRnd.Program.Main (System.String[] args) [0x00000] in <filename unknown>:0 [ERROR] FATAL UNHANDLED EXCEPTION: System.TypeInitializationException: An exception was thrown by the type initializer for codeJam2013QRnd.FileOPS ---> System.IO.FileNotFoundException: Could not find file /home/useruser/GCJ-mining/compile/C:\Users\dkulkarni1\Downloads\A-large.in. File name: /home/useruser/GCJ-mining/compile/C:\Users\dkulkarni1\Downloads\A-large.in at System.IO.FileStream..ctor (System.String path, FileMode mode, FileAccess access, FileShare share, Int32 bufferSize, Boolean anonymous, FileOptions options) [0x00000] in <filename unknown>:0 at System.IO.FileStream..ctor (System.String path, FileMode mode, FileAccess access, FileShare share) [0x00000] in <filename unknown>:0 at (wrapper remoting-invoke-with-check) System.IO.FileStream:.ctor (string,System.IO.FileMode,System.IO.FileAccess,System.IO.FileShare) at System.IO.File.OpenRead (System.String path) [0x00000] in <filename unknown>:0 at System.IO.StreamReader..ctor (System.String path, System.Text.Encoding encoding, Boolean detectEncodingFromByteOrderMarks, Int32 bufferSize) [0x00000] in <filename unknown>:0 at System.IO.StreamReader..ctor (System.String path) [0x00000] in <filename unknown>:0 at (wrapper remoting-invoke-with-check) System.IO.StreamReader:.ctor (string) at System.IO.File.OpenText (System.String path) [0x00000] in <filename unknown>:0 at System.IO.File.ReadAllLines (System.String path) [0x00000] in <filename unknown>:0 at codeJam2013QRnd.FileOPS..cctor () [0x00000] in <filename unknown>:0 --- End of inner exception stack trace --- at codeJam2013QRnd.Program.Main (System.String[] args) [0x00000] in <filename unknown>:0 Command exited with non-zero status 1'

java_compile = '/home/useruser/datacollection/solutions_2458486_1/java/Kurenai/Treasure.java:35: error: cannot find symbol private static ArrayList<ChestOpener> getChests(String aFileName) throws FileNotFoundException, IOException { ^ symbol: class ChestOpener location: class Treasure /home/useruser/datacollection/solutions_2458486_1/java/Kurenai/Treasure.java:12: error: cannot find symbol ArrayList<ChestOpener> chests = getChests("C:\\Users\\Patri\\Downloads\\D-large.in"); ^ symbol: class ChestOpener location: class Treasure /home/useruser/datacollection/solutions_2458486_1/java/Kurenai/Treasure.java:16: error: cannot find symbol ChestOpener chest = chests.get(0); ^ symbol: class ChestOpener location: class Treasure /home/useruser/datacollection/solutions_2458486_1/java/Kurenai/Treasure.java:36: error: cannot find symbol ArrayList<ChestOpener> chestOpeners = new ArrayList<ChestOpener>(); ^ symbol: class ChestOpener location: class Treasure /home/useruser/datacollection/solutions_2458486_1/java/Kurenai/Treasure.java:36: error: cannot find symbol ArrayList<ChestOpener> chestOpeners = new ArrayList<ChestOpener>(); ^ symbol: class ChestOpener location: class Treasure /home/useruser/datacollection/solutions_2458486_1/java/Kurenai/Treasure.java:42: error: cannot find symbol ArrayList<Chest> chests = new ArrayList<Chest>(); ^ symbol: class Chest location: class Treasure /home/useruser/datacollection/solutions_2458486_1/java/Kurenai/Treasure.java:42: error: cannot find symbol ArrayList<Chest> chests = new ArrayList<Chest>(); ^ symbol: class Chest location: class Treasure /home/useruser/datacollection/solutions_2458486_1/java/Kurenai/Treasure.java:59: error: cannot find symbol chests.add(new Chest(chestArray[0], chestKeys)); ^ symbol: class Chest location: class Treasure /home/useruser/datacollection/solutions_2458486_1/java/Kurenai/Treasure.java:62: error: cannot find symbol chestOpeners.add(new ChestOpener(chests, keys)); ^ symbol: class ChestOpener location: class Treasure 9 errors'
java_run = 'at java.lang.ClassLoader.defineClass1(Native Method) at java.lang.ClassLoader.defineClass(ClassLoader.java:803) at java.security.SecureClassLoader.defineClass(SecureClassLoader.java:142) at java.net.URLClassLoader.defineClass(URLClassLoader.java:442) at java.net.URLClassLoader.access$100(URLClassLoader.java:64) at java.net.URLClassLoader$1.run(URLClassLoader.java:354) at java.net.URLClassLoader$1.run(URLClassLoader.java:348) at java.security.AccessController.doPrivileged(Native Method) at java.net.URLClassLoader.findClass(URLClassLoader.java:347) at java.lang.ClassLoader.loadClass(ClassLoader.java:425) at sun.misc.Launcher$AppClassLoader.loadClass(Launcher.java:308) at java.lang.ClassLoader.loadClass(ClassLoader.java:358) at sun.launcher.LauncherHelper.checkAndLoadMain(LauncherHelper.java:482) Command exited with non-zero status 1'
cpp_copile = '/home/useruser/datacollection/solutions_2755486_1/C++/Echo80313/c.cpp: In function int main(): /home/useruser/datacollection/solutions_2755486_1/C++/Echo80313/c.cpp:87:35: error: kase was not declared in this scope printf();  /home/useruser/datacollection/solutions_2755486_1/C++/Echo80313/c.cpp: At global scope: /home/useruser/datacollection/solutions_2755486_1/C++/Echo80313/c.cpp:89:1: error: expected declaration before } token } '

print 'c# compile: ' + format_error_msg(c_sharp_compile)
print ' '
print 'java compile: ' + format_error_msg(java_compile)
print ' '
print 'c++ compile: ' + format_error_msg(cpp_copile)
print ' '
print 'c# run: ' + format_run_msg(c_sharp_run, 'C#')
print ' '
print 'java run: ' + format_run_msg(java_run, 'Java')
'''








