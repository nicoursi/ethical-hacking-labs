#!/usr/bin/env python3
# It returns the first occurence o a string in a string list
def search_iface_by_prefx(search_string, string_list):
    matches = [item for item in string_list if search_string in item]
    return matches[0]
