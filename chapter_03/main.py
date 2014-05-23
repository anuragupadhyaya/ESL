#!/usr/bin/env python

import pandas as pd
import numpy as np

import chapter_03.data as data
import chapter_03.regression as regression

from common.ui import print_title


def training_data_correlations():
    """ Print the correlations in training data """
    print_title("Data correlations")
    prostate_data = data.read_prostate_data()
    training_data = prostate_data[prostate_data.train == 'T'].drop('train', 1)
    print training_data.corr().to_string(float_format=lambda x: '%.3f' % x)


def training_data_regression():
    """ Run least squares regression on the training data """
    print_title("Least squares regression")
    prostate_data = data.read_prostate_data()

    # Select corresponding columns
    yraw = prostate_data.lpsa
    train = prostate_data.train
    Xraw = prostate_data.drop(['lpsa', 'train'], 1)

    # Normalize data
    Xraw = (Xraw - Xraw.mean()) / np.sqrt(Xraw.var())

    # Insert intercept column
    Xraw.insert(0, 'intercept', 1.0)

    # Select training set
    y = yraw[train == 'T']
    X = Xraw[train == 'T']

    # Regresion
    least_squares = regression.LeastSquaresRegression(X, y)
    # betahat, errors = regression.least_squares_regression_with_std_errors(X.values, y.values)

    result = pd.DataFrame({
        'Coefficient': least_squares.betahat,
        'Std. Error': least_squares.std_errors
    }, index=X.columns)

    result['Z Score'] = result['Coefficient'] / result['Std. Error']

    print result.to_string(float_format=lambda x: '%.2f' % x)


def shrinkage_methods():
    """ Test various shrinkage methods """
    print_title("Shrinkage methods")
    prostate_data = data.read_prostate_data()

    # Select corresponding columns
    yraw = prostate_data.lpsa
    train = prostate_data.train
    Xraw = prostate_data.drop(['lpsa', 'train'], 1)

    # Normalize data
    Xraw = (Xraw - Xraw.mean()) / np.sqrt(Xraw.var())

    # Insert intercept column
    Xraw.insert(0, 'intercept', 1.0)

    # Select training set
    y = yraw[train == 'T']
    X = Xraw[train == 'T']

    # Select test set
    ytest = yraw[train == 'F']
    Xtest = Xraw[train == 'F']

    #############################################################
    # Ordinary least squares
    least_squares = regression.LeastSquaresRegression(X, y)
    test_error, std_error = regression.test_error(least_squares, Xtest, ytest)

    ls_series = pd.Series(least_squares.betahat, index=X.columns)
    ls_series.set_value('Test Error', test_error)
    ls_series.set_value('Std Error', std_error)

    #############################################################
    # Best subset selection
    best_subset_parameter = 2  # These parameters where chosen by the authors of the book

    subset_model = regression.BestSubsetSelection(X, y, best_subset_parameter)
    test_error, std_error = regression.test_error(subset_model, Xtest, ytest)

    best_subset_series = pd.Series(subset_model.betahat, index=X.columns[subset_model.best_combination])
    best_subset_series.set_value('Test Error', test_error)
    best_subset_series.set_value('Std Error', std_error)

    #############################################################
    # Print results
    result = pd.DataFrame({
        'LS': ls_series,
        'Best Subset': best_subset_series
    },
        index=ls_series.index,
        columns=['LS', 'Best Subset']
    )

    print result.to_string(float_format=lambda x: '---' if np.isnan(x) else '%.3f' % x)


if __name__ == '__main__':
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>"
    print "Running code for chapter 3"
    training_data_correlations()
    training_data_regression()
    shrinkage_methods()
