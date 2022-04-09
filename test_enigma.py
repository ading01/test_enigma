from unittest.mock import Mock, patch
from attr import validate
import pytest

from machine import Enigma
from components import Rotor, Plugboard, Reflector

@pytest.fixture
def enigma():
    return Enigma(key="BED", swaps=[('O', 'Z'), ('E', 'Q')], rotor_order=['II', 'I', 'V'])


from curses import window
import pytest
from machine import Enigma
from components import *
from unittest.mock import Mock, patch

@pytest.fixture
def enigma():
    return Enigma(key="BED", swaps=[('O', 'Z'), ('E', 'Q')], rotor_order=['II', 'I', 'V'])

def test_alphabet():
    assert ALPHABET == 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def test_1(capsys):
    position_key = "ABC"
    mach = Enigma(key='AAA')
    mach.set_rotor_position(position_key, printIt=True) #== "Rotor position successfully updated. Now using ABC."
    captured = capsys.readouterr()
    assert mach.key == "ABC"
    assert captured.out == 'Rotor position successfully updated. Now using ABC.\n'

def test_1_1():
    position_key = "ABC"
    mach = Enigma(key='AAA')
    mach.set_rotor_position(position_key, printIt=False) 
    assert mach.key == "ABC"

def test_2(capsys):
    position_key = 111
    # self, key='AAA', swaps=None, rotor_order=['I', 'II', 'III']):
    mach = Enigma(key='AAA')
    mach.set_rotor_position(position_key, printIt=True) #== "Rotor position successfully updated. Now using ABC."
    captured = capsys.readouterr()
    assert captured.out == 'Please provide a three letter position key such as AAA.\n'

# testing roter order

def test_3():
    rotor_order = ['II', 'I', 'III']
    mach = Enigma()
    mach.set_rotor_order(rotor_order)
    assert mach.l_rotor.rotor_num == 'II'
    assert mach.m_rotor.rotor_num == "I"
    assert mach.r_rotor.rotor_num == "III"
    
# what if order has repeating rotor e.g. ['II', 'I', 'III']

def test_repeating_rotors():
    break_order = ['II', 'I', 'II']
    mach = Enigma(rotor_order=break_order)
    assert mach.l_rotor.rotor_num == 'II'

def test_4(capsys):
    mach = Enigma()
    return_letter = mach.encode_decode_letter(letter='E')
    print(return_letter)
    captured = capsys.readouterr()
    assert captured.out == 'F\n'
    assert return_letter == 'F'


#check to make sure that swaps are uppercase?
def test_uppercase():
    mach = Enigma()
    return_letter = mach.encode_decode_letter(letter='e')
    assert return_letter == 'F'

def test_plugboard():
    swaps = ['AB', 'XR']
    pboard = Plugboard(swaps)
    assert pboard.swaps['A'] == 'B'
    assert pboard.swaps['X'] == 'R'

def test_repr_plugboard(capsys):
    swaps = ['AB', 'XR']
    pboard = Plugboard(swaps)
    print(pboard)
    captured = capsys.readouterr()
    assert captured.out == 'A <-> B\nX <-> R\n'
# must test three cases: replace = False , or replace = True, replace = False, but goes over 6.


#this one is test 15
def test_encode_if_swapped():
    mach = Enigma(key='ABC', swaps = ['AB', 'XR'], rotor_order = ['II', 'I', 'III'])
    resp = mach.encode_decode_letter('a')
    assert resp == 'H'

def test_encode_if_space():
    mach = Enigma(key='ABC', swaps = ['AB', 'XR'], rotor_order = ['II', 'I', 'III'])
    resp = mach.encipher('banana is great')
    assert resp == 'XMPDHPOHBMGZB'

def test_encode_decode_letter_with_space():
    with pytest.raises(ValueError):
        mach = Enigma(key='ABC', swaps = ['AB', 'XR'], rotor_order = ['II', 'I', 'III'])
        resp = mach.encode_decode_letter(' ')
        resp == None
    
def test_encode_decode():
    mach = Enigma(key='ABC', swaps = ['AB', 'XR'], rotor_order = ['II', 'I', 'III'])
    resp = mach.encipher('banana')

    mach2 = Enigma(key='ABC', swaps = ['AB', 'XR'], rotor_order = ['II', 'I', 'III'])
    resp2 = mach2.decipher(resp)
    assert resp2 == 'BANANA'

def test_encode_letter_with_space():
    with pytest.raises(ValueError):
        starting_rotor_num = 'III'
        start_window_letter = 'a'
        myrot = Rotor(starting_rotor_num, start_window_letter)
        myrot.encode_letter(' ')

def test_encode_decode_letter_without_strip():
    mach = Enigma(key='ABC', swaps = ['AB', 'XR'], rotor_order = ['II', 'I', 'III'])
    resp = mach.encipher(' hey  ')
    assert resp == 'AJX'

def test_encipher_without_replace():
    mach = Enigma(key='ABC', swaps = ['AB', 'XR'], rotor_order = ['II', 'I', 'III'])
    resp = mach.encipher('banana is great')
    assert resp == 'XMPDHPOHBMGZB'

def test_update_swaps1():
    swaps = ['AB', 'XR']
    pboard = Plugboard(swaps)
    additional_swaps = ['CD', 'YZ']
    pboard.update_swaps(additional_swaps)
    assert len(pboard.swaps) == 8
    assert pboard.swaps['C'] == 'D'

def test_capacity_swaps():
    swaps = {}
    pboard = Plugboard(swaps)
    additional_swaps = ['AB', 'KI', 'TJ', 'XY', 'UM', 'EG']
    pboard.update_swaps(additional_swaps)
    assert len(pboard.swaps) == 12
    assert pboard.swaps['K'] == 'I'

def test_overcapacity_swaps(capsys):
    swaps = {}
    pboard = Plugboard(swaps)
    additional_swaps = ['AB', 'KI', 'TJ', 'XY', 'UM', 'EG', 'BP']
    pboard.update_swaps(additional_swaps)
    captured = capsys.readouterr()
    assert captured.out == 'Only a maximum of 6 swaps is allowed.\n'
    assert len(pboard.swaps) == 0

def test_update_swaps_with_replace():
    swaps = ['AB', 'XR']
    pboard = Plugboard(swaps)
    additional_swaps = ['CD', 'YZ']
    pboard.update_swaps(additional_swaps, replace=True)
    assert len(pboard.swaps) == 4
    assert pboard.swaps['C'] == 'D'

def test_update_swaps_with_false():
    swaps = ['AB', 'XR']
    pboard = Plugboard(swaps)
    additional_swaps = None
    pboard.update_swaps(additional_swaps, replace=True)
    assert len(pboard.swaps) == 0

def test_init():
    starting_rotor_num = 'III'
    start_window_letter = 'a'
    myrot = Rotor(starting_rotor_num, start_window_letter)
    assert myrot.offset == 0

def test_print_enigma(enigma, capsys):
    print(enigma)
    captured = capsys.readouterr()
    assert captured.out == "Keyboard <-> Plugboard <->  Rotor II <-> Rotor  I <-> Rotor  V <-> Reflector \nKey:  + BED\n"


def test_not_init(capsys):
    with pytest.raises(ValueError):
        starting_rotor_num = 'IV'
        start_window_letter = 'a'
        myrot = Rotor(starting_rotor_num, start_window_letter)

def test__repr__(capsys):
    starting_rotor_num = 'III'
    start_window_letter = 'a'
    myrot = Rotor(starting_rotor_num, start_window_letter)
    print(myrot)
    captured = capsys.readouterr()
    assert captured.out == "Wiring:\n{'forward': 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'backward': 'TAGBPCSDQEUFVNZHYIXJWLRKOM'}\nWindow: A\n"

#does rotor init require a check for the window to make sure that it is a letter?

def test_reflector(capsys):
    myreflector = Reflector()
    assert myreflector.wiring['A'] == 'Y'
    assert myreflector.wiring['B'] == 'R'
    print(myreflector)
    captured = capsys.readouterr()
    assert captured.out == "Reflector wiring: \n{'A': 'Y', 'B': 'R', 'C': 'U', 'D': 'H', 'E': 'Q', 'F': 'S', 'G': 'L', 'H': 'D', 'I': 'P', 'J': 'X', 'K': 'N', 'L': 'G', 'M': 'O', 'N': 'K', 'O': 'M', 'P': 'I', 'Q': 'E', 'R': 'B', 'S': 'F', 'T': 'Z', 'U': 'C', 'V': 'W', 'W': 'V', 'X': 'J', 'Y': 'A', 'Z': 'T'}\n"

# may need to have argument for if foward=False
def test_encode(capsys):
    starting_rotor_num = 'III'
    start_window_letter = 'a'
    myrot = Rotor(starting_rotor_num, start_window_letter)
    letter = myrot.encode_letter('a', return_letter=True, printit=True)
    captured = capsys.readouterr()
    assert letter == 'B'
    assert captured.out == 'Rotor III: input = A, output = B\n'


#this test needs some updates 
def test_step():
    rot1 = 'III'
    start1 = 'c'
    myrot = Rotor(rot1, start1)

    rot2 = 'V'
    start2 = 'd'
    myrot2 = Rotor(rot2, start2, prev_rotor=myrot)
    myrot2.step()
    assert myrot2.prev_rotor == myrot

def test_swaps_with_windows_equals_notch(capsys):
    starting_rotor_num = 'III'
    start_window_letter = 'v'
    next_rotor = Rotor('II', 't')
    myrot = Rotor(starting_rotor_num, start_window_letter, next_rotor= next_rotor)
    myrot.step()
    assert myrot.offset == 22
    assert myrot.window == ALPHABET[22]

def test_swaps_with_windows_equals_notch_second_branch(capsys):
    starting_rotor_num = 'III'
    start_window_letter = 's'
    next_rotor = Rotor('II', 'e')
    myrot = Rotor(starting_rotor_num, start_window_letter, next_rotor= next_rotor)
    myrot.step()
    assert myrot.offset == 19
    assert myrot.window == ALPHABET[19]
    assert next_rotor.offset == 5
    assert next_rotor.window == ALPHABET[5]
# more machine tests

def test_more_than_3():
    with pytest.raises(ValueError):
        mach = Enigma(key='ABCD')

def test_enigma_repr(capsys):
    mach = Enigma(key='ABC', swaps = ['AB', 'XR'], rotor_order = ['II', 'I', 'III'])
    print(mach)
    captured = capsys.readouterr()
    assert captured.out == 'Keyboard <-> Plugboard <->  Rotor II <-> Rotor  I <-> Rotor  III <-> Reflector \nKey:  + ABC\n'

def test_encipher():
    mach = Enigma(key='ABC', swaps = ['AB', 'XR'], rotor_order = ['II', 'I', 'III'])
    resp = mach.encipher('banana')
    assert resp == 'XMPDHP'

#do i need to assert the printed string?
def test_encipher_with_num():
    with pytest.raises(ValueError):
        mach = Enigma(key='ABC', swaps = ['AB', 'XR'], rotor_order = ['II', 'I', 'III'])
        resp = mach.encipher('banana1')
        

def test_decipher():
    mach = Enigma(key='ABC', swaps = ['AB', 'XR'], rotor_order = ['II', 'I', 'III'])
    resp = mach.decipher('XMPDHP')
    assert resp == 'BANANA'

def test_set_plugs(capsys):
    mach = Enigma(key='ABC', swaps = ['AB', 'XR'], rotor_order = ['II', 'I', 'III'])
    swaps = ['BC']
    mach.set_plugs(swaps, replace=True, printIt=True)
    captured = capsys.readouterr()
    assert captured.out == 'Plugboard successfully updated. New swaps are:\nB <-> C\n'

def test_set_plugs_woPrintIt():
    mach = Enigma(key='ABC', swaps = ['AB', 'XR'], rotor_order = ['II', 'I', 'III'])
    swaps = ['BC']
    mach.set_plugs(swaps, replace=True, printIt=False)
    assert mach.plugboard.swaps == {'B': 'C', 'C': 'B'}


def test_set_plugs_woReplace(capsys):
    mach = Enigma(key='ABC', swaps = ['AB', 'XR'], rotor_order = ['II', 'I', 'III'])
    swaps = ['CD']
    mach.set_plugs(swaps, replace=False, printIt=True)
    captured = capsys.readouterr()
    assert captured.out == 'Plugboard successfully updated. New swaps are:\nA <-> B\nX <-> R\nC <-> D\n'

def test_encode_decode_letter():
    with pytest.raises(ValueError):
        mach = Enigma(key='ABC', swaps = ['AB', 'XR'], rotor_order = ['II', 'I', 'III'])
        mach.encode_decode_letter('1')
        

def test_all_rotors():
    myEnigma = Enigma()
    assert myEnigma.l_rotor.rotor_num == 'I'
    assert myEnigma.m_rotor.rotor_num == 'II'
    assert myEnigma.r_rotor.rotor_num == 'III'
    assert myEnigma.l_rotor.offset == 0
    assert myEnigma.m_rotor.offset == 0
    assert myEnigma.r_rotor.offset == 0

def test_all_rotors_again():
    rotor_ord = ['II', 'III', 'I']
    myEnigma = Enigma('RCB', rotor_order=rotor_ord)
    assert myEnigma.l_rotor.rotor_num == 'II'
    assert myEnigma.m_rotor.rotor_num == 'III'
    assert myEnigma.r_rotor.rotor_num == 'I'
    assert myEnigma.l_rotor.offset == 17
    assert myEnigma.m_rotor.offset == 2
    assert myEnigma.r_rotor.offset == 1

def test_all_rotors_w_changes():
    myEnigma = Enigma(key='ABC', swaps = ['AB', 'XR'], rotor_order = ['II', 'I', 'III'])
    assert myEnigma.l_rotor.rotor_num == 'II'
    assert myEnigma.m_rotor.rotor_num == 'I'
    assert myEnigma.r_rotor.rotor_num == 'III'
    assert myEnigma.l_rotor.offset == 0
    assert myEnigma.m_rotor.offset == 1
    assert myEnigma.r_rotor.offset == 2

def test_rotor_init():
    rotor_num = 'I'
    window_letter = 'R'
    mynext_rotor = 'II'
    myprev_rotor = None
    myrot = Rotor(rotor_num, window_letter, next_rotor=mynext_rotor)
    assert myrot.rotor_num == 'I'
    assert myrot.offset == 17
    assert myrot.wiring['forward'] == 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'
    assert myrot.wiring['backward'] == 'UWYGADFPVZBECKMTHXSLRINQOJ'
    assert myrot.notch == 'Q'
    assert myrot.next_rotor == 'II'
    assert myrot.prev_rotor == None

def test_encode_long_paragraph():
    mach = Enigma(key='ABC', swaps = ['AB', 'XR'], rotor_order = ['II', 'I', 'III'])
    resp = mach.encipher("This is a very long string of letters that I am going to use for this project This needs to be long enough to test that all rotors rotate at least once so that I can check my output This sentence also cannot contain any punctuation or any other characters other than whitespace and letters from the alphabet I am going to make this insanely long because if its not i will not be able to tell and that would be bad")
    assert resp == 'PZFCVHVRSMPSVTBXUKDMSXTKPCUDUHDJTSVLWSHWBADNQWHQTNZVVHZVYZQGIEMFZCVOFURJGQPMCZWZCSIFQTJWINXLGCLBQAYPEJPKIXDQBDEMQLTIAEMOIYDCWRPQBQNFWNHNOZZUDPUOMWXMTPKAHSBOUAXIRSXRLHJQRVHZHKFXCDBVDKDJUIISTAGMVMVVEBEBBOPXEDNDMMDUDMWEYWFSLYDBOWABFWGXRCGVVCHMIORHSEDJSSRDGFIUZMPRUJYMMLJDKTNYEOQJWJSMVJNYVGIJDXJARINWXGOHKQOQRYUMSOYRKCSEPRAMSXMWETAHGGDC'


def test_more_than_letter():
    with pytest.raises(ValueError):
        mach = Enigma()
        return_letter = mach.encode_decode_letter(letter='ds')

#this is test 5
def test_encipher_multiple_times():
    mach = Enigma(key='ABC', swaps = ['AB', 'XR'], rotor_order = ['II', 'I', 'III'])
    resp = mach.encipher('hello')
    assert resp == 'AJMWJ'
    assert mach.key == 'ABC'
    assert mach.l_rotor.window == 'A'
    assert mach.m_rotor.window == 'B'
    mach.l_rotor.change_setting('C')
    assert mach.l_rotor.window == 'C'
    resp2 = mach.encipher('HEY')
    assert resp2 == 'KVX'


def test_rotor_wirings():
    one = ROTOR_WIRINGS['I']
    two = ROTOR_WIRINGS['II']
    three = ROTOR_WIRINGS['III']
    four = ROTOR_WIRINGS['V']
    assert one['forward'] == 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'
    assert one['backward'] == 'UWYGADFPVZBECKMTHXSLRINQOJ'
    assert two['forward'] == 'AJDKSIRUXBLHWTMCQGZNPYFVOE'
    assert two['backward'] == 'AJPCZWRLFBDKOTYUQGENHXMIVS'
    assert three['forward'] == 'BDFHJLCPRTXVZNYEIWGAKMUSQO'
    assert three['backward'] == 'TAGBPCSDQEUFVNZHYIXJWLRKOM'
    assert four['forward'] == 'VZBRGITYUPSDNHLXAWMJQOFECK'
    assert four ['backward'] == 'QCYLXWENFTZOSMVJUDKGIARPHB'


def test_rotor_notches():
    assert ROTOR_NOTCHES['I'] == 'Q'
    assert ROTOR_NOTCHES['II'] == 'E'
    assert ROTOR_NOTCHES['III'] == 'V' 
    assert ROTOR_NOTCHES['V'] == 'Z'

def test_setrotorposition_1():
    mach = Enigma()
    mach.set_rotor_position('CZD')
    assert mach.l_rotor.window == 'C'
    assert mach.l_rotor.offset == 2
    assert mach.m_rotor.window == 'Z'
    assert mach.m_rotor.offset == 25
    assert mach.r_rotor.window == 'D'
    assert mach.r_rotor.offset == 3

def test_set_rotor_with_step():
    mach = Enigma()
    mach.set_rotor_position('PEV')
    mach.l_rotor.step()
    assert mach.l_rotor.window == 'Q'
    assert mach.l_rotor.offset == 16
    assert mach.m_rotor.window == 'E'
    assert mach.m_rotor.offset == 4
    assert mach.r_rotor.window == 'V'
    assert mach.r_rotor.offset == 21
    mach.l_rotor.step()
    assert mach.l_rotor.window == 'R'
    assert mach.l_rotor.offset == 17
    assert mach.m_rotor.window == 'E'
    assert mach.m_rotor.offset == 4
    assert mach.r_rotor.window == 'V'
    assert mach.r_rotor.offset == 21


def test_connected_rotors():
    r1 = Rotor('I', 'F')
    r2 = Rotor('II', 'E')
    r3 = Rotor('III', 'A')
    r4 = Rotor('V', 'F')

    r1.next_rotor == r2
    r1.prev_rotor == r4
    r2.prev_rotor == r1
    r2.next_rotor == r3
    r3.prev_rotor == r2
    r3.next_rotor == r4
    r4.prev_rotor == r3

    r1.step()

    assert r1.offset == 6
    assert r1.window == 'G'

    assert r2.offset == 4
    assert r2.window == 'E'

    assert r3.offset == 0
    assert r3.window == 'A'  

    assert r4.offset == 5
    assert r4.window == 'F'  



def test_long(capsys):
    r1 = Rotor('I', 'F')
    r2 = Rotor('II', 'E')
    r3 = Rotor('III', 'A')
    r4 = Rotor('V', 'F')

    r1.next_rotor == r2
    r2.prev_rotor == r1
    r2.next_rotor == r3
    r3.prev_rotor == r2
    r3.next_rotor == r4
    r4.prev_rotor == r3

    assert r1.encode_letter('A', True, True, True) == 'B'
    assert r1.encode_letter('A', False, True, True) == 'Y'
    assert r1.encode_letter('A', True, False, True) == 1
    assert r1.encode_letter('A', True, True, False) == 'B'
    assert r1.encode_letter('A', False, False, True) == 24
    assert r1.encode_letter('A', True, False, False) == 1
    assert r1.encode_letter('A', False, True, False) == 'Y'
    assert r1.encode_letter('A', False, False, False) == 24
    captured = capsys.readouterr()
    assert captured.out == "Rotor I: input = F, output = G\nRotor I: input = F, output = D\nRotor I: input = F, output = G\nRotor I: input = F, output = D\n"


def test_m_encipher(enigma):
    with pytest.raises(ValueError) as e:
        enigma.encipher("#2(*124")
    with pytest.raises(ValueError) as e:
        enigma.encipher("+")
    with pytest.raises(ValueError) as e:
        enigma.encipher("@")
    assert str(e.value) == 'Please provide a string containing only the characters a-zA-Z and spaces.'

    assert(enigma.encipher("this better work") == "CCWBPXUJGNQCDI")
    assert(enigma.encipher("this better work") == "MBACNKAODYQGBA")
    assert(enigma.encipher("this better work") == "ZWGATWEYPMUHED")

    with patch.object(enigma, "encode_decode_letter") as mock:
        enigma.encipher("this better work")
    assert mock.call_count == 14

