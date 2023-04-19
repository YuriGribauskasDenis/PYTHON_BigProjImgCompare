from Stuff.GenerateStuff import get_folder_adr

adr = get_folder_adr(__file__).parent
print(adr)
ttf_fold = get_folder_adr(__file__).parent / 'Constants'
print(ttf_fold)