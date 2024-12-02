from threading import Thread, Lock
import helpscripts

class MyThread(Thread):
    def __init__(self, pool, keyword, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        self.args = args
        self.kwargs = kwargs
        self.pool = pool
        self.keyword = keyword

    def run(self) -> None:
        total_files = 0
        total_find = 0
        for filename in self.pool:
            text = helpscripts.get_text(filename)
            if text:
                results = helpscripts.boyer_moore_search(text, self.keyword)
                total_find += results
            total_files += 1
            with lock:
                thread_stats[self.name] = {"files": total_files, "finds": total_find}

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

    lock = Lock() # Для котнроля одновременного доступа к thread_stats{}
    thread_stats = {}
    threads = []
    for id, pool in enumerate(files_pools):
        thread = MyThread(pool=pool, keyword=keyword, name=f"Поток-{id + 1}")
        thread.start()
        threads.append(thread)

    # Ожидаем завершения потоков
    for thread in threads:
        thread.join()

    print("\n")
    for name, stats in thread_stats.items():
        print(f"{name}: Обработано файлов: {stats['files']}, Всего вхождений: {stats['finds']}")
    print("Поиск завершен.\n")