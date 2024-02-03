from torchview import draw_graph
import os


def draw_graphs(model, inputs, min_depth=1, max_depth=10, directory='./model_viz/', hide_module_functions=True):
    base_filename = directory + model.__class__.__name__ + '.'

    for i in range(min_depth, max_depth+1):
        draw_graph(
            model, 
            input_size=inputs if isinstance(inputs, tuple) else tuple(tuple(x.shape) for x in inputs),
            expand_nested=True, 
            depth=i, 
            save_graph=True, 
            graph_name=model.__class__.__name__ + '.' + f'{i}_depth',
            directory=directory,
            hide_module_functions=hide_module_functions,
        )
        
        if i > min_depth:
            current_file = base_filename + f'{i}_depth' + '.gv'
            previous_file = base_filename + f'{i-1}_depth' + '.gv'

            # open previous saved .gv file and check text is same as current one
            with open(current_file) as file:
                data_pre = file.read()
            with open(previous_file) as file:
                data_cur = file.read()

            if len(data_pre) == len(data_cur):
                # remove current file
                os.remove(base_filename + f'{i}_depth' + '.gv')
                os.remove(base_filename + f'{i}_depth' + '.gv.png')
                break

        print(f'Graph for {i} depth is saved in {directory}')
