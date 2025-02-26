"""
Gradio-based web UI to explore the Camel dataset.
"""

import argparse
import random
from typing import Dict, List, Tuple

import gradio as gr
from loader import Datasets, load_datasets


def parse_arguments():
    """ Get command line arguments. """

    parser = argparse.ArgumentParser("Camel data explorer")
    parser.add_argument(
        '--data-path', type=str, default=None,
        help='Path to the folder with ZIP datasets containing JSONs')
    parser.add_argument('--default-dataset', type=str, default=None,
                        help='Default dataset name selected from ZIPs')
    parser.add_argument('--share', type=bool, default=False,
                        help='Expose the web UI to Gradio')
    parser.add_argument('--server-port', type=int, default=8080,
                        help='Port ot run the web page on')
    parser.add_argument('--inbrowser', type=bool, default=False,
                        help='Open the web UI in the default browser on lunch')
    parser.add_argument(
        '--concurrency-count', type=int, default=10,
        help='Number if concurrent threads at Gradio websocket queue. ' +
        'Increase to serve more requests but keep an eye on RAM usage.')
    args, unknown = parser.parse_known_args()
    if len(unknown) > 0:
        print("Unknown args: ", unknown)
    return args


def construct_app(datasets: Datasets, default_dataset: str = None):
    """ Build Gradio UI and populate with chat data from JSONs.

    Args:
        datasets (Datasets): Several parsed
        multi-JSON dataset with chats.
        default_dataset (str): Default selection of the dataset.

    Returns:
        None
    """

    if default_dataset is None:
        default_dataset = "ai_society_chat"

    misalignment_set_names = {"misalignment"}
    ordinary_datasets = [
        v for v in datasets.keys() if v not in misalignment_set_names
    ]
    misalignment_datasets = [
        v for v in datasets.keys() if v in misalignment_set_names
    ]
    default_dataset_name = default_dataset \
        if default_dataset in datasets.keys() \
        else ordinary_datasets[0] if len(ordinary_datasets) > 0 \
        else misalignment_datasets[0] if len(misalignment_datasets) > 0 \
        else ""
    dataset_names = list(datasets.keys())

    with gr.Row().style():
        with gr.Column(scale=2):
            with gr.Row():
                dataset_dd = gr.Dropdown(dataset_names, label="Select dataset",
                                         value="NODEFAULT", interactive=True)
            with gr.Row():
                disclaimer_ta = gr.Markdown(
                    "## By clicking AGREE I consent to use the dataset "
                    "for purely educational and academic purposes and "
                    "not use it for any fraudulent activity; and I take "
                    "all the responsibility if the data is used in a "
                    "malicious application.", visible=False)
            with gr.Row():
                with gr.Column(scale=1):
                    accept_disclaimer_bn = gr.Button("AGREE", visible=False)
                with gr.Column(scale=1):
                    decline_disclaimer_bn = gr.Button("DECLINE", visible=False)
            with gr.Row():
                with gr.Column(scale=3):
                    assistant_dd = gr.Dropdown([], label="ASSISTANT", value="",
                                               interactive=True)
                with gr.Column(scale=3):
                    user_dd = gr.Dropdown([], label="USER", value="",
                                          interactive=True)
        with gr.Column(scale=1):
            gr.Markdown(
                "## CAMEL: Communicative Agents for \"Mind\" Exploration"
                " of Large Scale Language Model Society\n"
                "Github repo: [https://github.com/lightaime/camel]"
                "(https://github.com/lightaime/camel)\n"
                '<div style="display:flex; justify-content:center;">'
                '<img src="https://raw.githubusercontent.com/lightaime/camel/'
                'master/misc/logo.png" alt="Logo" style="max-width:50%;">'
                '</div>')

    task_dd = gr.Dropdown([], label="Original task", value="",
                          interactive=True)
    specified_task_ta = gr.TextArea(label="Specified task", lines=2)
    chatbot = gr.Chatbot()
    accepted_st = gr.State(False)

    def set_default_dataset() -> Dict:
        """ Trigger for app load.

        Returns:
            Dict: Update dict for dataset_dd.
        """
        return gr.update(value=default_dataset_name)

    def check_if_misalignment(dataset_name: str, accepted: bool) \
            -> Tuple[Dict, Dict, Dict]:
        """ Display AGREE/DECLINE if needed.

        Returns:
            Tuple: Visibility updates for the buttons.
        """

        if dataset_name == "misalignment" and not accepted:
            return gr.update(visible=True), \
                gr.update(visible=True), gr.update(visible=True)
        else:
            return gr.update(visible=False), \
                gr.update(visible=False), gr.update(visible=False)

    def enable_misalignment() -> Tuple[bool, Dict, Dict, Dict]:
        """ Update the state of the accepted disclaimer.

        Returns:
            Tuple: New state and visibility updates for the buttons.
        """

        return True, gr.update(visible=False), \
            gr.update(visible=False), gr.update(visible=False)

    def disable_misalignment() -> Tuple[bool, Dict, Dict, Dict]:
        """ Update the state of the accepted disclaimer.

        Returns:
            Tuple: New state and visibility updates for the buttons.
        """

        return False, gr.update(visible=False), \
            gr.update(visible=False), gr.update(visible=False)

    def update_dataset_selection(dataset_name: str,
                                 accepted: bool) -> Tuple[Dict, Dict]:
        """ Update roles based on the selected dataset.

        Args:
            dataset_name (str): Name of the loaded .zip dataset.
            accepted (bool): If the disclaimer thas been accepted.

        Returns:
            Tuple[Dict, Dict]: New Assistant and User roles.
        """

        if dataset_name == "misalignment" and not accepted:
            # If used did not accept the misalignment policy,
            # keep the old selection.
            return (gr.update(value="N/A",
                              choices=[]), gr.update(value="N/A", choices=[]))

        dataset = datasets[dataset_name]
        assistant_roles = dataset['assistant_roles']
        user_roles = dataset['user_roles']
        assistant_role = random.choice(assistant_roles) \
            if len(assistant_roles) > 0 else ""
        user_role = random.choice(user_roles) if len(user_roles) > 0 else ""
        return (gr.update(value=assistant_role, choices=assistant_roles),
                gr.update(value=user_role, choices=user_roles))

    def roles_dd_change(dataset_name: str, assistant_role: str,
                        user_role: str) -> Dict:
        """ Update the displayed chat upon inputs change.

        Args:
            assistant_role (str): Assistant dropdown value.
            user_role (str): User dropdown value.

        Returns:
            Dict: New original roles state dictionary.
        """
        matrix = datasets[dataset_name]['matrix']
        if (assistant_role, user_role) in matrix:
            record: Dict[str, Dict] = matrix[(assistant_role, user_role)]
            original_task_options = list(record.keys())
            original_task = original_task_options[0]
        else:
            original_task = "N/A"
            original_task_options = []

        choices = gr.Dropdown.update(choices=original_task_options,
                                     value=original_task, interactive=True)
        return choices

    def build_chat_history(messages: Dict[int, Dict]) -> List[Tuple]:
        """ Structures chatbot contents from the loaded data.

        Args:
            messages (Dict[int, Dict]): Messages loaded from JSON.

        Returns:
            List[Tuple]: Chat history in chatbot UI element format.
        """
        history = []
        curr_qa = (None, None)
        for k in sorted(messages.keys()):
            msg = messages[k]
            content = msg['content']
            if msg['role_type'] == "USER":
                if curr_qa[0] is not None:
                    history.append(curr_qa)
                    curr_qa = (content, None)
                else:
                    curr_qa = (content, None)
            elif msg['role_type'] == "ASSISTANT":
                curr_qa = (curr_qa[0], content)
                history.append(curr_qa)
                curr_qa = (None, None)
            else:
                pass
        return history

    def task_dd_change(dataset_name: str, assistant_role: str, user_role: str,
                       original_task: str) -> Tuple[str, List]:
        """ Load task details and chatbot history into UI elements.

        Args:
            assistant_role (str): An assistan role.
            user_role (str): An user role.
            original_task (str): The original task.

        Returns:
            Tuple[str, List]: New contents of the specified task
            and chatbot history UI elements.
        """

        matrix = datasets[dataset_name]['matrix']
        if (assistant_role, user_role) in matrix:
            task_dict: Dict[str, Dict] = matrix[(assistant_role, user_role)]
            if original_task in task_dict:
                chat = task_dict[original_task]
                specified_task = chat['specified_task']
                history = build_chat_history(chat['messages'])
            else:
                specified_task = "N/A"
                history = []
        else:
            specified_task = "N/A"
            history = []
        return specified_task, history

    dataset_dd.change(check_if_misalignment, [dataset_dd, accepted_st],
                      [disclaimer_ta, accept_disclaimer_bn,
                       decline_disclaimer_bn]) \
              .then(update_dataset_selection,
                    [dataset_dd, accepted_st],
                    [assistant_dd, user_dd])

    accept_disclaimer_bn.click(enable_misalignment, None, [
        accepted_st, disclaimer_ta, accept_disclaimer_bn, decline_disclaimer_bn
    ]) \
        .then(update_dataset_selection,
              [dataset_dd, accepted_st],
              [assistant_dd, user_dd])

    decline_disclaimer_bn.click(disable_misalignment, None, [
        accepted_st, disclaimer_ta, accept_disclaimer_bn, decline_disclaimer_bn
    ]) \
        .then(update_dataset_selection,
              [dataset_dd, accepted_st],
              [assistant_dd, user_dd])

    func_args = (roles_dd_change, [dataset_dd, assistant_dd, user_dd], task_dd)
    assistant_dd.change(*func_args)
    user_dd.change(*func_args)

    task_dd.change(task_dd_change,
                   [dataset_dd, assistant_dd, user_dd, task_dd],
                   [specified_task_ta, chatbot])

    demo.load(set_default_dataset, None, dataset_dd)


if __name__ == "__main__":
    """ Entry point. """

    args = parse_arguments()

    print("Loading the dataset...")
    datasets = load_datasets(args.data_path)
    print("Dataset is loaded")

    print("Getting Data Explorer web server online...")

    with gr.Blocks() as demo:
        construct_app(datasets, args.default_dataset)

    demo.queue(args.concurrency_count)
    demo.launch(share=args.share, inbrowser=args.inbrowser,
                server_name="0.0.0.0", server_port=args.server_port)

    print("Exiting.")
