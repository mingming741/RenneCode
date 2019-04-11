# This is a script to determine whether given images are cartoons

import os
import os.path
import skimage.io
# please import other necessary packages needed by your algorithm


def is_cartoon(im):
    """Return True if the input image im is considered as a cartoon image,

       or False, if the input is considered as a natural image.
    """

    # It is in general a good practice to break an algorithm into
    # multiple components, implemented in different functions.
    # Then you may call those functions here to get to
    # the final decision.

    # the "return True" statement is here only as a placeholder, you
    # should use your algorithm to make the judgment.
    return True


def eval_performance(setname, dirpath, verbose=2):
    """Evaluate performance over a directory"""

    # collect the file names of testing images

    cartoon_dir = os.path.join(dirpath, "Cartoon")
    natural_dir = os.path.join(dirpath, "Natural")

    if not os.path.exists(cartoon_dir):
        raise IOError("The directory %s does not exist" % cartoon_dir)

    if not os.path.exists(natural_dir):
        raise IOError("The directory %s does not exist" % natural_dir)

    cartoon_files = [f for f in os.listdir(cartoon_dir) if f.endswith(".jpg")]
    natural_files = [f for f in os.listdir(natural_dir) if f.endswith(".jpg")]

    num_cartoons = len(cartoon_files)
    num_naturals = len(natural_files)

    if verbose >= 2:
        print "%s: %d cartoon images, %d natural images." % \
              (setname, num_cartoons, num_naturals)

    cartoon_corrects = 0   # the number of correct predictions on the cartoon set
    natural_corrects = 0   # the number of correct predictions on the cartoon set

    # perform testing and collect the statistics of predictions
    for f in cartoon_files:
        fpath = os.path.join(cartoon_dir, f)
        im = skimage.io.imread(fpath)
        pred = is_cartoon(im)
        if pred:
            cartoon_corrects += 1
        if verbose >= 2:
            print "Cartoon/%s ==> %d" % (f, pred)

    for f in natural_files:
        fpath = os.path.join(natural_dir, f)
        im = skimage.io.imread(fpath)
        pred = is_cartoon(im)
        if not pred:
            natural_corrects += 1
        if verbose >= 2:
            print "Natural/%s ==> %d" % (f, pred)

    # show summary of results
    correct_rate = (cartoon_corrects + natural_corrects) * 1.0 / (num_cartoons + num_naturals)
    if verbose >= 1:
        print "Cartoon: %d / %d corrects" % (cartoon_corrects, num_cartoons)
        print "Natural: %d / %d corrects" % (natural_corrects, num_naturals)
        print "Overall correct rate = %.4f" % correct_rate


if __name__ == '__main__':

    data_dir = os.path.join(os.path.dirname(__file__), 'dev_imgs')
    eval_performance("Development set", data_dir)

