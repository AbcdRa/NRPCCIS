import glob
import os

file_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Models', '*.h5')
models = [os.path.basename(model) for model in glob.glob(file_dir)]
