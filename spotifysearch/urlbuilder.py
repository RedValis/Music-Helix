
# THIS FILE IS RESPONSABLE FOR BUILDING DYNAMIC URLS

def search_endpoint(keywords:str, allowed_types:list, 
filters:dict, market:str, limit:int, offset:int):
    endpoint = 'https://api.spotify.com/v1/search?'
    
    # FORMAT QUERRY ITEMS AND FILTERS
    querry_items = keywords.split(' ')   
    for filter, value in filters.items():
        value = value.replace(' ', '%20')
        item = f'{filter}:{value}'
        querry_items.append(item)

    # REQUIRED ARGUMENTS
    querry = 'q=' + '%20'.join(querry_items)
    types = 'type=' + ','.join(allowed_types)
    arguments = [querry, types]
    
    # OPTIONAL ARGUMENTS
    if market: 
        arguments.append(f'market={market}')
    if limit: 
        arguments.append(f'limit={limit}')  
    if offset: 
        arguments.append(f'offset={offset}')
    
    return endpoint + '&'.join(arguments)
