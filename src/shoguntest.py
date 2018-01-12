from modshogun import StringCharFeatures, BinaryLabels
from modshogun import LibSVM, SubsequenceStringKernel, RAWBYTE
from modshogun import ErrorRateMeasure


def get_kernel_shogun_lib(docs, n, lam):
    # print docs
    feats_train=StringCharFeatures(docs, RAWBYTE)

    kernel=SubsequenceStringKernel(feats_train, feats_train, 2, 0.5);

    km_train=kernel.get_kernel_matrix()
    return km_train[0, 1]
