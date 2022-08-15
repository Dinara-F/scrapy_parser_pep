import csv
import datetime as dt
from collections import defaultdict
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'


class PepParsePipeline:
    def open_spider(self, spider):
        self.results = defaultdict(int)
        self.count = 0

    def process_item(self, item, spider):
        status = item['status']
        self.results[status] += 1
        self.count += 1
        return item

    def close_spider(self, spider):
        result_list = [('Статус', 'Количество')]
        result_list.extend(self.results.items())
        result_list.append(('Total', self.count))
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        file_name = f'status_summary_{now_formatted}.csv'
        file_path = results_dir / file_name
        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerows(result_list)
