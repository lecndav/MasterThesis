import matplotlib.pylab as plt
from random import randint

def main():
    prediction = {'x': range(0,15), 'y': map(lambda v : v - randint(-10, 10), range(0, 90, 6))}

    classification1 = {'x': range(0,15), 'y': map(lambda v : randint(0, 100), range(0, 15))}

    classification2 = {'x': range(16,30), 'y': map(lambda v : randint(0, 100), range(1, 15))}

    cluster1 = {'x': range(0,20), 'y': map(lambda v : randint(0, 20), range(0, 20))}
    cluster2 = {'x': range(15,35), 'y': map(lambda v : randint(25, 45), range(0, 20))}
    cluster3 = {'x': range(30,50), 'y': map(lambda v : randint(5, 25), range(0, 20))}

    plt.figure(num=None, figsize=(18,5))

    pp = plt.subplot(131)
    plt.title('Prediction')
    pp.plot(list(prediction['x']), list(prediction['y']), 'bo')
    pp.plot(range(0,15), range(0, 90, 6), 'r')
    pp.set_ylabel('y')
    pp.set_xlabel('x')
    pp.spines['top'].set_visible(False)
    pp.spines['right'].set_visible(False)
    pp.grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.5)

    pcl = plt.subplot(132)
    plt.title('Classification')
    pcl.plot(list(classification1['x']), list(classification1['y']), 'bo')
    pcl.plot(list(classification2['x']), list(classification2['y']), 'go')
    pcl.plot([15, 15], [0, 100], 'r')
    pcl.set_ylabel('y')
    pcl.set_xlabel('x')
    pcl.spines['top'].set_visible(False)
    pcl.spines['right'].set_visible(False)
    pcl.grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.5)

    pc = plt.subplot(133)
    plt.title('Clustering')
    pc.plot(list(cluster1['x']), list(cluster1['y']), 'bo')
    pc.plot(list(cluster2['x']), list(cluster2['y']), 'go')
    pc.plot(list(cluster3['x']), list(cluster3['y']), 'yo')
    c1 = plt.Circle((10, 10), 12, color='b', alpha=0.3)
    c2 = plt.Circle((25, 35), 12, color='g', alpha=0.3)
    c3 = plt.Circle((40, 15), 12, color='y', alpha=0.3)
    pc.add_patch(c1)
    pc.add_patch(c2)
    pc.add_patch(c3)
    pc.set_ylabel('y')
    pc.set_xlabel('x')
    pc.spines['top'].set_visible(False)
    pc.spines['right'].set_visible(False)
    pc.grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.5)

    plt.savefig('../Thesis/images/ml_problem_types.png', bbox_inches='tight')

main()
