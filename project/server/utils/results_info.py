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


# tf_size_guidance = {
#     'compressedHistograms': 10,
#     'images': 0,
#     'scalars': 100,
#     'histograms': 1
# }

summary_file_name = "summary.json"


# used in flask env
def get_results_info_for_all_experiment_from_summary_file(result_dataset_path):
    result = {}
    file_name = os.path.join(result_dataset_path, summary_file_name)
    if os.path.exists(result_dataset_path):
        with open(file_name, 'r') as json_file:
            result = json.load(json_file)

    return result

    # models = os.listdir(tuner_path)
    # if len(models) <= 1:
    #     return result
    #
    # for model in models:
    #     model_path = os.path.join(tuner_path, model)
    #     if len(os.listdir(model_path)) == 0:
    #         continue
    #
    #     result[model] = {}
    #
    #     eval_folder = os.path.join(model_path, "eval")
    #     if not os.path.exists(eval_folder):
    #         continue
    #     history_file = os.listdir(eval_folder)
    #     if len(history_file) != 0:
    #         history_file = history_file[0]
    #         full_history_file_path = os.path.join(eval_folder, history_file)
    #         # event_acc = EventAccumulator(full_history_file_path, tf_size_guidance)
    #         # event_acc.Reload()
    #         result[model]['accuracy'] = 1  # event_acc.Scalars('accuracy')[0].value
    #         result[model]['auc_pr'] = 1  # event_acc.Scalars('auc_pr')[-1].value
    #         result[model]['auc_roc'] = 1  # event_acc.Scalars('auc_roc')[-1].value
    #         result[model]['loss'] = 1  # event_acc.Scalars('loss')[-1].value
    #         result[model]['num_parameters'] = 1  # event_acc.Scalars('num_parameters')[-1].value


def model_summary(trainer, result_model_path):
    import tensorflow as tf
    result = []

    model_saves_path = os.path.join(result_model_path, "saved_model")
    if not os.path.exists(model_saves_path):
        logging.log(logging.ERROR, f"path not exists {model_saves_path}")
        return result

    saved_models = os.listdir(model_saves_path)
    if len(saved_models) == 0:
        logging.log(logging.ERROR, f"no saved_models found {model_saves_path}")
        return result

    folders = [item for item in saved_models if os.path.isdir(os.path.join(model_saves_path, item))]
    # Return the first folder if it exists
    folder = None
    if folders:
        for _folder in folders:
            if ".env" in _folder:
                continue
            folder = _folder

    if folder is None:
        logging.log(logging.ERROR, f"{result_model_path} found no saved models")
        return result
    model_path = os.path.join(model_saves_path, folder)

    loaded = tf.saved_model.load(model_path)  # r'F:\docker_backup\tuner-1\7\saved_model\1718972892'

    for idx, v in enumerate(loaded.variables):
        for s in trainer._spec.blocks_to_use:
            if s in v.name:
                result.append({"name": str(v.name), "shape": str(v.shape)})

    return result






# used in train.py
def set_results_info_for_all_experiment(result_dataset_path, tuner_path, trainer):
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

        result[model]['val_images'], result[model]['images'] = generate_images_all(
            model_path,
            result_dataset_path,
            model
        )

        eval_folder = os.path.join(model_path, "eval")
        if not os.path.exists(eval_folder):
            continue
        history_file = os.listdir(eval_folder)
        if len(history_file) != 0:
            history_file = history_file[0]
            full_history_file_path = os.path.join(eval_folder, history_file)
            event_acc = EventAccumulator(full_history_file_path)  # , tf_size_guidance)
            event_acc.Reload()

            # result[model]['val_images'] = generate_images(event_acc, result_dataset_path, model)  # just names of images
            # result[model]['images'] = generate_images(event_acc, result_dataset_path, model)  # just names of images

            result[model]['accuracy'] = event_acc.Scalars('accuracy')[0].value
            result[model]['auc_pr'] = event_acc.Scalars('auc_pr')[-1].value
            result[model]['auc_roc'] = event_acc.Scalars('auc_roc')[-1].value
            result[model]['loss'] = event_acc.Scalars('loss')[-1].value
            result[model]['num_parameters'] = event_acc.Scalars('num_parameters')[-1].value

            result[model]["architecture"] = model_summary(trainer, model_path)

    out_file = os.path.join(result_dataset_path, summary_file_name)
    with open(out_file, 'w') as json_file:
        json.dump(result, json_file, indent=4)

    return result


def generate_images_all(results_dataset_path: str, save_path: str,
                        model: str, train_event_acc=None, val_event_acc=None):
    from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

    if train_event_acc is None:
        for file in os.listdir(results_dataset_path):
            if "tfevents" in file:
                full_file_path = os.path.join(results_dataset_path, file)
                train_event_acc = EventAccumulator(full_file_path)  # , tf_size_guidance)
                train_event_acc.Reload()

    if val_event_acc is None:
        eval_folder = os.path.join(results_dataset_path, "eval")
        if os.path.exists(eval_folder):
            files = os.listdir(eval_folder)
            if len(files) != 0:
                file = files[0]
                full_file_path = os.path.join(eval_folder, file)

                val_event_acc = EventAccumulator(full_file_path)  # , tf_size_guidance)
                val_event_acc.Reload()

    val_images = generate_images(val_event_acc, save_path, model, prefix='val-')
    train_images = generate_images(train_event_acc, save_path, model, prefix='train-')

    return val_images, train_images


def generate_images(event_acc, results_dataset_folder_path, model, prefix=""):
    if event_acc is None:
        logging.log(logging.ERROR, f"got None event_acc for prefix = {prefix}")
        return []

    import matplotlib.pyplot as plt

    tags = event_acc.Tags()['scalars']
    save_dir = os.path.join(results_dataset_folder_path, 'tensorboard_graphs', model)
    os.makedirs(save_dir, exist_ok=True)

    images = []

    for tag in tags:
        events = event_acc.Scalars(tag)

        steps = [event.step for event in events]
        values = [event.value for event in events]

        logging.log(logging.ERROR, f"{prefix}{tag} steps")
        logging.log(logging.ERROR, steps)
        logging.log(logging.ERROR, f"{prefix}{tag} values")
        logging.log(logging.ERROR, values)

        plt.figure()
        plt.plot(steps, values)
        plt.xlabel('Steps')
        plt.ylabel(tag)
        plt.title(tag)

        image_name = f'{prefix}{tag}.png'
        save_path = os.path.join(save_dir, image_name)

        plt.savefig(save_path)
        plt.close()

        images.append(image_name)

    return images


def generate_results(trainer, result_dataset_path):
    tuner_path = find_tuner_path(result_dataset_path)
    set_results_info_for_all_experiment(result_dataset_path, tuner_path, trainer)

    logging.log(logging.INFO, "Results to experiment have successfully been written")
