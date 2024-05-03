from email.policy import default
import pytest
import numpy as np

from anopt.predictor import Predictor, NUMPredictor
from anopt.utils.generator import generate_network, generate_random_flows


def test_num_predictor():
    network = generate_network(mode='linear', n=3, default_bw=1000)
    flows = generate_random_flows(network, mode='ordered')
    flow_routes = network.get_routes(flows)
    predictor = NUMPredictor(network, flow_routes, 0, np.zeros((0, len(flows))))
    tputs, grads = predictor.predict([])
    assert len(tputs) == predictor.n
    assert grads is None

    # Print the inputs: network, flow_routes, and predictor
    print(f"network: {network}")
    print(f"flow_routes: {flow_routes}")
    print(f"predictor: {predictor}")

    # Print the outputs: tputs and grads
    print(f"tputs: {tputs}")
    print(f"grads: {grads}")

test_num_predictor()