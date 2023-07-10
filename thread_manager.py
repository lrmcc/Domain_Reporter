from threading import Thread

class ThreadManager():
    
    thread_dict = {}
    threads_to_del = []

    @staticmethod
    def create_thread(name, thread_function, arg):
        thread = Thread(target=thread_function, args=(arg,))
        thread.start()
        ThreadManager.thread_dict[name] = thread

    @staticmethod
    def destroy_all_threads():
        for key in ThreadManager.thread_dict.keys():
            ThreadManager.destroy_thread(key)
            ThreadManager.threads_to_del.append(key)
        for name in ThreadManager.threads_to_del:
            del ThreadManager.thread_dict[name]
        ThreadManager.threads_to_del = []
        
    @staticmethod
    def destroy_thread(name):
        thread = ThreadManager.thread_dict[name]
        if thread.is_alive():
            thread.join()