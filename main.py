from flask import Flask, render_template
import fault_tree_framework as FTF
import os
import numpy as np


app = Flask(__name__)


@app.route('/')
def index():
    print('STARTING')
    cwd = os.getcwd()
    SIZE = 1000
    OPERATING_CYCLE = 1000
    linspace = np.linspace(0, 100, 1000)

    original_fault_tree = FTF.create_fault_tree()
    original_fault_tree.export_to_png(cwd + '/static/images/Original_FT.png')
    FTF.generate_export_time_series(original_fault_tree, SIZE, 'ts.txt')
    reconstructed_fault_tree = FTF.reconstruct_fault_tree('ts.txt')
    FTF.run_reconstruction_analysis(reconstructed_fault_tree, OPERATING_CYCLE)
    FTF.run_theoretical_analysis(original_fault_tree, linspace, OPERATING_CYCLE)
    reconstructed_fault_tree.export_to_png(cwd + '/static/images/Reconstructed_FT.png')
    FTF.create_plots(reconstructed_fault_tree, original_fault_tree)
    print('END')

    original_events = [original_fault_tree.top_event]
    original_events.extend(original_fault_tree.get_basic_events())
    reconstructed_events = [reconstructed_fault_tree.top_event]
    reconstructed_events.extend(reconstructed_fault_tree.get_basic_events())

    return render_template("index.html", orignal_events=original_events, reconstructed_events=reconstructed_events)


if __name__ == "__main__":
    app.run(debug=True)
