import sys
import logging
from datetime import datetime
import importlib
import traceback

logging.basicConfig(
    filename='Logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

MODULES = [
    'Module_1',
    'Module_2',
    'Module_3',
    'Module_4_5',
]

def run_module(module_name, input_data=None):
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, 'main'):
            logging.info(f"Starting execution of {module_name}")
            start_time = datetime.now()
            if input_data is None:
                output = module.main()
            else:
                output = module.main(*input_data)
            end_time = datetime.now()
            duration = end_time - start_time
            logging.info(f"Finished execution of {module_name}. Duration: {duration}")
            return output
        else:
            logging.error(f"Module {module_name} does not have a main() function")
            return None
    except Exception as e:
        logging.error(f"Error in {module_name}: {str(e)}")
        logging.error(traceback.format_exc())
        return None

def main():
    logging.info("Starting pipeline execution")
    start_time = datetime.now()

    previous_output = None
    for module in MODULES:
        output = run_module(module, previous_output)
        if output is None and module!=MODULES[-1]:
            logging.error(f"Pipeline stopped due to error in {module}")
            sys.exit(1)
        previous_output = output

    end_time = datetime.now()
    total_duration = end_time - start_time
    logging.info(f"Pipeline execution completed. Total duration: {total_duration}")

if __name__ == "__main__":
    main()