import os



def create_folder (folder):
    try:
        os.makedirs(folder)
    except OSError:
         if os.path.exists(folder):
             pass
         else: 
             raise


