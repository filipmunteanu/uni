from mnist import MNIST
from argparse import ArgumentParser
from cascor import *
MNIST_PATH = "./MNIST"

def preprocess(train_imgs, test_imgs):
    avg = np.mean(train_imgs)
    dev = np.std(train_imgs)

    train_imgs -= avg
    train_imgs /= dev
    test_imgs -= avg
    test_imgs /= dev


def load_mnist():
    mnist_data = MNIST(MNIST_PATH)
    train_imgs, train_labels = mnist_data.load_training()
    test_imgs, test_labels = mnist_data.load_testing()
    data = {}
    data["train_imgs"] = np.array(train_imgs, dtype="f").reshape(60000, 784, 1)
    data["test_imgs"] = np.array(test_imgs, dtype="f").reshape(10000, 784, 1)
    data["train_labels"] = np.array(train_labels)
    data["test_labels"] = np.array(test_labels)

    preprocess(data["train_imgs"], data["test_imgs"])

    data["train_no"] = 60000
    data["test_no"] = 10000

    return data


def eval_nn(nn, imgs, labels, maximum = 0):
    confusion_matrix = np.zeros((10, 10))
    correct_no = 0
    how_many = imgs.shape[0] if maximum == 0 else maximum
    
    for i in range(imgs.shape[0])[:how_many]:
        y = np.argmax(nn.forward(imgs[i]))
        t = labels[i]
        if y == t:
            correct_no += 1
        confusion_matrix[t-1][y-1] += 1

    return float(correct_no) / float(how_many), confusion_matrix


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--learning_rate", type = float, default = 0.01,
                        help="Learning rate")
    parser.add_argument("--eval_every", type = int, default = 200,
                        help="Learning rate")
    args = parser.parse_args()

    mnist = load_mnist()
    input_size = mnist["train_imgs"][0].size
    outp_size = 10

    nn = CascNet(input_size, outp_size, learn_rate=args.learning_rate)
    nn.train_netw(mnist, (mnist['train_imgs'])[:10000], (mnist["train_labels"])[:10000])
