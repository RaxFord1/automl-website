import json
import logging
import os


def find_tuner_path(result_dataset_folder_path):
    root_dataset_folders = os.listdir(result_dataset_folder_path)
    for folder in root_dataset_folders:
        if "tuner" not in folder:
            continue
        else:
            return os.path.join(result_dataset_folder_path, folder)

    return None


tf_size_guidance = {
    'compressedHistograms': 10,
    'images': 0,
    'scalars': 100,
    'histograms': 1
}


# used in flask env
def get_results_info_for_all_experiment_from_summary_file(tuner_path):
    result = {}
    models = os.listdir(tuner_path)
    if len(models) <= 1:
        return result

    for model in models:
        model_path = os.path.join(tuner_path, model)
        if len(os.listdir(model_path)) == 0:
            continue

        result[model] = {}

        eval_folder = os.path.join(model_path, "eval")
        if not os.path.exists(eval_folder):
            continue
        history_file = os.listdir(eval_folder)
        if len(history_file) != 0:
            history_file = history_file[0]
            full_history_file_path = os.path.join(eval_folder, history_file)
            # event_acc = EventAccumulator(full_history_file_path, tf_size_guidance)
            # event_acc.Reload()
            result[model]['accuracy'] = 1  # event_acc.Scalars('accuracy')[0].value
            result[model]['auc_pr'] = 1  # event_acc.Scalars('auc_pr')[-1].value
            result[model]['auc_roc'] = 1  # event_acc.Scalars('auc_roc')[-1].value
            result[model]['loss'] = 1  # event_acc.Scalars('loss')[-1].value
            result[model]['num_parameters'] = 1  # event_acc.Scalars('num_parameters')[-1].value


# used in train.py
def get_results_info_for_all_experiment(tuner_path):
    from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

    result = {}
    models = os.listdir(tuner_path)
    if len(models) <= 1:
        return result

    for model in models:
        model_path = os.path.join(tuner_path, model)
        if len(os.listdir(model_path)) == 0:
            continue

        result[model] = {}

        eval_folder = os.path.join(model_path, "eval")
        if not os.path.exists(eval_folder):
            continue
        history_file = os.listdir(eval_folder)
        if len(history_file) != 0:
            history_file = history_file[0]
            full_history_file_path = os.path.join(eval_folder, history_file)
            event_acc = EventAccumulator(full_history_file_path, tf_size_guidance)
            event_acc.Reload()
            result[model]['accuracy'] = event_acc.Scalars('accuracy')[0].value
            result[model]['auc_pr'] = event_acc.Scalars('auc_pr')[-1].value
            result[model]['auc_roc'] = event_acc.Scalars('auc_roc')[-1].value
            result[model]['loss'] = event_acc.Scalars('loss')[-1].value
            result[model]['num_parameters'] = 1  # event_acc.Scalars('num_parameters')[-1].value


def generate_images(event_acc, results_dataset_folder_path):
    import matplotlib.pyplot as plt
    tags = event_acc.Tags()['scalars']
    save_dir = os.path.join(results_dataset_folder_path, 'tensorboard_graphs')
    os.makedirs(save_dir, exist_ok=True)

    for tag in tags:
        # Get the scalar events
        events = event_acc.Scalars(tag)
        steps = [event.step for event in events]
        values = [event.value for event in events]

        # Plot the data
        plt.figure()
        plt.plot(steps, values)
        plt.xlabel('Steps')
        plt.ylabel(tag)
        plt.title(tag)

        # Save the graph
        save_path = os.path.join(save_dir, f'{tag}.png')
        plt.savefig(save_path)
        plt.close()


def generate_results(result_dataset_path):
    tuner_path = find_tuner_path(result_dataset_path)
    results = get_results_info_for_all_experiment(tuner_path)

    out_file = os.path.join(result_dataset_path, "summary.json")

    with open(out_file, 'w') as json_file:
        json.dump(results, json_file, indent=4)

    logging.log(logging.INFO, "Results to Expirement have successfully been written")
