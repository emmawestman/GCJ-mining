from handle_compilation_errors import *




def change_input_streams(input_file,csharp_file,root):
    file_path = os.path.join(root, csharp_file)
    print "file_path",file_path
    list_of_inregexes = ['(new StreamReader\(new FileStream\().*(,.*)','(new FileStream\().*(,\s?FileMode.Open.*)','(new (?:System.IO.)?StreamReader\()[\"@]*.*?(\))','(new (?:System.IO.)?StreamReader\().*?(\))','(File.ReadLines\().*?(\)?\))','(File.ReadAllLines\().*(\))','(System.IO.File.ReadAllText\().*?(\))','(File.ReadAllText\().*?(\))','(File.OpenText\().*?(\))']
    new_input = '\"'+input_file+'\"'
    handle_file_not_found(file_path,list_of_inregexes,new_input)
    list_of_outregex= ['(new StreamWriter\()\"?[\w+]*.?[\w+]\"?(\))','(new StreamWriter\()\"?[\w+\s]+\"?[\w]*.?[\w]*\"?(\))','(File.WriteAllText\().*(,.*)','(new StreamWriter\().*(,.*)']
    open('output.txt', 'w').close()
    new_out_put = '\"' + 'output.txt' + '\"'
    handle_file_not_found(file_path,list_of_outregex,new_out_put)