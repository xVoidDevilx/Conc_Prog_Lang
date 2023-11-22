'''
Function: decryptLetter

Purpose:
    The `decryptLetter` function is designed to decrypt a single character by
    applying a rotation cipher technique. It rotates a given character by a
    specified value within a predefined character set, which includes numbers,
    lowercase and uppercase alphabets, and common special characters along with
    space.

Parameters:
    - letter (str): A single character string that is to be decrypted.
    - rotationValue (int): An integer value that specifies the rotation
                           offset for the decryption.

Returns:
    - str: A single character string that represents the decrypted character
           after applying the rotation.

Description:
    The function uses a string, `rotationString`, that contains all the characters
    in the sequence that are considered for the rotation cipher. It finds the
    current position of the provided `letter` within `rotationString`. Then, it
    calculates the new position by adding the `rotationValue` to the current
    index and applies modulo 95 to wrap the rotation within the bounds of
    `rotationString`'s length. The function returns the character at the new
    position in the rotation string as the decrypted character.

Example:
    - decryptLetter("e", 2) would return "g".
    - decryptLetter("Z", 4) would return "$".
    - decryptLetter("1", 5) would return "6".
    - decryptLetter("!", 94) would return "Z".

Note:
    The function assumes that `letter` is a valid single character that exists
    in the `rotationString`. If `letter` is not found in `rotationString`,
    the function behavior is not defined. Ensure that `rotationValue` is an
    integer, as other types for rotationValue will result in TypeError.
'''
def decryptLetter(letters, rotationValues):
    rotationString  = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ "
    length = len(rotationString)
    # Create a dictionary for constant-time lookup
    char_index_map = {char: index for index, char in enumerate(rotationString)}

    for letter, rotationValue in zip(letters, rotationValues):
        currentPosition = char_index_map[letter]
        yield rotationString[(currentPosition + rotationValue) % length]