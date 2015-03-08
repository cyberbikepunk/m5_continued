""" Miscellaneous utility classes decorators and functions """

import shapefile
import matplotlib.pyplot as plt

from matplotlib.collections import PolyCollection
from collections import namedtuple
from datetime import datetime
from os.path import splitext, join, getctime, isdir
from os import mkdir
from glob import iglob
from re import sub
from random import sample

from m5.settings import FILL, USER, OUTPUT, DATABASE, DOWNLOADS, TEMP, LOG, SKIP, CENTER, DBF, PLZ


# --------------------- NAMED TUPLES


Stamped = namedtuple('Stamped', ['stamp', 'data'])
Stamp = namedtuple('Stamp', ['date', 'uuid'])
Tables = namedtuple('Tables', ['clients', 'orders', 'checkpoints', 'checkins'])

# --------------------- DECORATORS


def log_me(f):
    return f


def time_me(f):
    return f


# --------------------- FUNCTIONS


def unique_file(name: str) -> str:
    """ Return a unique path in the output folder. """

    (base, extension) = splitext(name)
    stamp = sub(r'[:]|[-]|[_]|[.]|[\s]', '', str(datetime.now()))
    unique = base.ljust(20, FILL) + stamp + extension
    path = join(OUTPUT, unique)

    return path


def latest_file(folder: str):
    """ Return the most recent file inside the folder. """
    return min(iglob(join(folder, '*.sqlite')), key=getctime)


def check_install():
    """ Create user folders if needed. """

    folders = (USER, OUTPUT, DATABASE, DOWNLOADS, TEMP, LOG)

    for folder in folders:
        if not isdir(folder):
            # Don't handle IO exception
            # to get deeper feedback.
            mkdir(folder, mode=775)
            print('Created {dir}.'.format(dir=folder))


def check_shapefile():

    shp = open(SHP, 'rb')
    dbf = open(DBF, 'rb')
    sf = shapefile.Reader(shp=shp, dbf=dbf)

    shapes = sf.shapes()
    records = sf.records()

    # READER OBJECT
    print(SKIP)
    print('{title:{fill}{align}100}'.format(title='READER OBJECT (.SHP + .DBF)', fill=FILL, align=CENTER, end=SKIP))
    print('Reader.numRecords = %s' % sf.numRecords)
    print('Reader.bbox = %s' % sf.bbox)
    print('Reader.fields = %s' % sf.fields)
    print('Reader.shp = %s' % sf.shp)
    print('Reader.dbf = %s' % sf.dbf)
    print('Reader.shx = %s' % sf.shx)
    print('Reader.shapeType = %s' % sf.shapeType)
    print('Reader.shpLength = %s' % sf.shpLength)

    # SHAPES OBJECTS
    print(SKIP)
    print('{title:{fill}{align}100}'.format(title='SHAPE OBJECTS (.SHP FILE)', fill=FILL, align=CENTER, end=SKIP))
    print('Reader.shapes() = %s' % type(shapes))
    print('len(Reader.shapes()) = %s' % len(shapes))
    print('Sample(10) iteration through shapes:')
    for s in sample(list(sf.iterShapes()), 10):
        print('    s.shapeType = %s, s.bbox = %s, s.points = %s' % (s.shapeType, s.bbox, s.points))

    # RECORD OBJECTS
    print(SKIP)
    print('{title:{fill}{align}100}'.format(title='RECORD OBJECTS (.DBF FILE)', fill=FILL, align=CENTER, end=SKIP))
    print('Reader.records() = %s' % type(records))
    print('len(Reader.records()) = %s' % len(records))
    print('Sample(10) iteration through records:')
    for r in sample(list(sf.iterRecords()), 10):
        print('   r = %s' % r)

    # MERGE INTO MATPLOTLIB
    vertices = None
    colors = None
    if False:
        coll = PolyCollection(vertices, array=colors, cmap=plt.jet, edgecolors='none')

        fig, ax = plt.subplots()
        ax.add_collection(coll)
        ax.autoscale_view()
        fig.colorbar(coll, ax=ax)
        plt.show()


if __name__ == '__main__':
    print('M5 utilities module:', end=SKIP)
    print('Latest database = %s' % latest_file(DATABASE))
    print('Unique output file: %s' % unique_file('example.unique'))
    check_shapefile()