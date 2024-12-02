from multiprocessing import Process, Queue, current_process
import helpscripts

def worker(queue, pool, keyword):
    total_files = 0
    total_find = 0
    for filename in pool:
        text = helpscripts.get_text(filename)
        if text:
            results = helpscripts.boyer_moore_search(text, keyword)
            total_find += results
        total_files += 1
    queue.put({current_process().name: {"files": total_files, "finds": total_find}})

if __name__ == '__main__':

    filelist = helpscripts.get_file_list()
    keyword = "система"
    limit = 5 # Лимит файлов на поток

    files_pools = [] # Набираем сюда списки по 5 фалов максимум
    chunk = []
    for file in filelist:
        chunk.append(file)
        if len(chunk) == limit:  
            files_pools.append(chunk) 
            chunk = []

    queue = Queue()
    processes = []

    for id, pool in enumerate(files_pools):
        process = Process(target=worker, args=(queue, pool, keyword), name=f"Процесс-{id + 1}")
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    process_stats = {}
    while not queue.empty():
        process_stats.update(queue.get())

    print("\n")
    for name, stats in process_stats.items():
        print(f"{name}: Обработано файлов: {stats['files']}, Всего вхождений: {stats['finds']}")
    print("Поиск завершен.\n")