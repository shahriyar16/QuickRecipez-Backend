import tensorflow as tf

def load_graph(frozen_graph_filename):
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def, name="prefix")
    return graph


if __name__ == '__main__':
    graph = load_graph('frozen_inference_graph.pb')
    for op in graph.get_operations():
        abc = graph.get_tensor_by_name(op.name + ":0")
        print(abc)
