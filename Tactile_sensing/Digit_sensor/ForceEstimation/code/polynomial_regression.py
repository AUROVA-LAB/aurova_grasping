import matplotlib.pyplot as plt
import numpy as np

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

import glob
import os


def sorter(x):
    return int(x.split(".")[0].split("_")[-1])



def read_txt_file(txt):
    
    with open(txt, "r") as f:
        val = float(f.read())
    
    return val


def load_data(path):

    train_def_path = sorted(glob.glob(os.path.join(path, "train", "def_value", "*.txt")), key=sorter)
    dev_def_path = sorted(glob.glob(os.path.join(path, "dev", "def_value", "*.txt")), key=sorter)
    test_def_path = sorted(glob.glob(os.path.join(path, "test", "def_value", "*.txt")), key=sorter)

    train_f_path = sorted(glob.glob(os.path.join(path, "train", "forces", "*.txt")), key=sorter)
    dev_f_path = sorted(glob.glob(os.path.join(path, "dev", "forces", "*.txt")), key=sorter)
    test_f_path = sorted(glob.glob(os.path.join(path, "test", "forces", "*.txt")), key=sorter)

    train_def = [read_txt_file(i) for i in train_def_path]
    dev_def = [read_txt_file(i) for i in dev_def_path]
    test_def = [read_txt_file(i) for i in test_def_path]

    train_f = [read_txt_file(i) for i in train_f_path]
    dev_f = [read_txt_file(i) for i in dev_f_path]
    test_f = [read_txt_file(i) for i in test_f_path]
    
    return train_def, dev_def, test_def, train_f, dev_f, test_f


def mae_loss(pred_fs, gt_fs):
    
    losses = []

    for pred_f, gt_f in zip(pred_fs, gt_fs):
        losses.append(np.abs(pred_f-gt_f))

    return np.mean(np.asarray(losses)), np.std(np.asarray(losses))



def main():

    path = "/home/aurova/Desktop/julio/tactile_vision2force/rosbags/dataset_indenters_octubre_19/data/datasets/2nd_manually_filtered_dataset_15nov_15N"

    train_def, dev_def, test_def, train_f, dev_f, test_f = load_data(path)

    print(len(train_def), len(dev_def), len(test_def), len(train_f), len(dev_f), len(test_f))

    # def in meters, force in N
    plt.scatter(test_def, test_f, label="Test Data")
    plt.xlabel("Depth (m)")
    plt.ylabel("Force (N)")

    poly = PolynomialFeatures(degree=3, include_bias=False)
    train_poly_features = poly.fit_transform(np.asarray(train_def).reshape(-1, 1))
    test_poly_features = poly.fit_transform(np.asarray(test_def).reshape(-1, 1))

    poly_reg_model = LinearRegression()
    poly_reg_model.fit(train_poly_features, train_f)

    print(poly_reg_model.intercept_, poly_reg_model.coef_)

    #y_predicted = poly_reg_model.predict(train_poly_features)
    y_predicted_test = poly_reg_model.predict(test_poly_features)

    mean_mae_loss, std_mae_loss = mae_loss(y_predicted_test, test_f)

    print(f"{mean_mae_loss} +- {std_mae_loss}")

    plt.scatter(test_def, y_predicted_test, color='purple', label="Polynomial Fit")
    plt.legend()
    plt.show()



if __name__ == '__main__':
    main()