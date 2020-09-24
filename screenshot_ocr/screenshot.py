import time

import pytesseract
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from pathlib import Path
from os.path import join, splitext


class OnMyWatch:
    # Set the directory on watch 

    def __init__(self):
        self.observer = Observer()
        home = str(Path.home())
        self.watchDirectory = join(home, 'Desktop', 'screenshots')

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):

    def on_created(self, event: FileCreatedEvent):
        filename = event.src_path

        if not event.is_directory:
            new_filename, ext = splitext(filename)
            if ext in ['.png', '.jpg']:
                result = pytesseract.image_to_string(filename, lang='eng')
                new_filename += '.txt'
                with open(new_filename, 'w+') as f:
                    f.write(result)
                    print(f"Write result to the file {new_filename}")


if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()
