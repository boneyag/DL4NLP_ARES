from eval_data_reader import get_instances_eval_file

def create_input_lemmas():
    get_instances_eval_file('senseval2', 'senseval2.data.xml')
    
def main():
    create_input_lemmas()
    
if __name__ == '__main__':
    main()