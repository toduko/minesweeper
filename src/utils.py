'''
Utilities module
'''


def get_image_from_tile_char(char: str):
    '''
    Get image filename from char representation of tile
    '''
    if char == '#':
        return "hidden"
    if char == 'P':
        return "flag"
    if char == '*':
        return "mine"
    if char == ' ':
        return "0"
    return char


def get_top_k_scores(k: int, difficulty: str):
    '''
    Renders the top scores of screen
    '''
    with open(difficulty, "r", encoding="utf-8") as file:
        return sorted(list(map(float, filter(lambda x: x.replace(
            '.', '', 1).isdigit(), file.read().split("\n")))))[:k]
