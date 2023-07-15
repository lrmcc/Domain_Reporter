from threading import Thread

thread_dict = {}
    
def create_thread(name, thread_function, arg):
    thread = Thread(target=thread_function, args=(arg,))
    thread.start()
    thread_dict[name] = thread

def destroy_all_threads():
    threads_to_del = []
    for key in thread_dict.keys():
        destroy_thread(key)
        threads_to_del.append(key)
    for name in threads_to_del:
        del thread_dict[name]
    
def destroy_thread(name):
    thread = thread_dict[name]
    if thread.is_alive():
        thread.join()