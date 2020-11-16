import sys
import os
import argparse
import glob
from random import sample


def arguments():
    ''' Handle the input parameters '''

    path = os.path.dirname(__file__)
    if not path:
        path = '.'
    def_indir = path+'/inputs/'

    parser = argparse.ArgumentParser(description='Name generator')

    parser.add_argument('-m', '--male', help='Provide a male name instead of a female name',
                        action='store_true', required=False)
    parser.add_argument('-n', '--number-of-names',
                        help='Number of names [default: 1]', type=int, default=1, required=False)
    parser.add_argument('-i', '--input-directory',
                        help='Where would the list of files be found [default: '+def_indir+']', type=str, default=def_indir, required=False)
    parser.add_argument(
        '-d', '--debug', help='Print some debug message [default: false]', action='store_true', required=False)
    parser.add_argument('-f', '--first-only', help='Povide a first (given) name  only',
                        action='store_true', required=False)
    parser.add_argument('-l', '--last-only', help='Povide a last name (surname) only',
                        action='store_true', required=False)

    try:
        options = parser.parse_args()
    except:
        sys.exit(0)

    parameters = {}

    # Debug
    parameters['debug'] = options.debug

    # Male / Female
    parameters['ismale'] = options.male
    if parameters['debug']:
        if options.male:
            print('Getting a male name')
        else:
            print('Getting a female name')

    # Number of names
    try:
        nnames = int(options.number_of_names)
    except ValueError:
        stderr.write('Number of names format error: ', options.number_of_names)
        sys.exit(1)

    if nnames < 1:
        stderr.write('Error: We should have at least one name!')
        sys.exit(1)

    parameters['nnames'] = nnames
    if parameters['debug']:
        print('Getting '+str(nnames)+" names")

    # Input directory
    if os.path.isdir(options.input_directory):
        parameters['idir'] = options.input_directory
        if parameters['debug']:
            print('Using input directory: '+options.input_directory)
    else:
        stderr.write('Error: input directory does not exists: ' +
                     options.input_directory)
        sys.exit(1)

    # Selections
    parameters['first only'] = options.first_only
    parameters['last only'] = options.last_only

    return parameters


def get_list_from_file(filename):
    ''' Opens a file and pack each line onto a set '''
    out = set()
    with open(filename, 'rt') as f:
        lname = f.readlines()
        for line in lname:
            out.add(line)
        f.close()
    return out


def get_list_from_list_of_files(pattern, debug=False):
    out = set()
    for f in glob.glob(pattern):
        if debug:
            print('Including ', f)

        o = get_list_from_file(f)
        if len(out) == 0:
            out = o
        else:
            out = out.union(o)
    return out


def get_lists(dirname, debug=False):
    ''' Get the different lists '''

    # Female lists
    female_first_name = get_list_from_list_of_files(
        dirname+'female_first_names_*.dat', debug)

    # Male lists
    male_first_name = get_list_from_list_of_files(
        dirname+'male_first_names_*.dat', debug)

    # Surname lists
    surnames = get_list_from_list_of_files(dirname+'surname_*.dat', debug)

    return (female_first_name, male_first_name, surnames)


def pick_one_from_set(setname):
    ''' Select a single element from a set '''
    if len(setname) > 0:
        return sample(setname, 1).pop().rstrip('\n')
    else:
        return ''


if __name__ == '__main__':
    ''' Main function '''
    args = arguments()

    (femfirst, mfirst, surnames) = get_lists(args['idir'], args['debug'])

    for n in range(args['nnames']):
        fname = ''
        lname = ''

        if not args['last only']:
            if args['ismale']:
                fname = pick_one_from_set(mfirst)
            else:
                fname = pick_one_from_set(femfirst)
        if not args['first only']:
            lname = pick_one_from_set(surnames)

        print(fname, lname)
