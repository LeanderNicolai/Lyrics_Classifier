from func_base import dir_creation, input_format, get_links_create_files

# Creation of Directory and Lyric Retrieval
base_folder_name, base_folder_loc = dir_creation()


space_format, base, domain, n_songs, base_folder_name, base_folder_loc = input_format(
    base_folder_name, base_folder_loc)

artist_links = get_links_create_files(
    space_format, base, domain, n_songs, base_folder_name, base_folder_loc)
