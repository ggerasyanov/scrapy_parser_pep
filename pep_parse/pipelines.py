import csv
import datetime as dt
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'


class PepParsePipeline:

    count_status = defaultdict(int)
    total = 0
    result = []

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.count_status[item['status']] += 1
        self.total += 1
        return item

    def close_spider(self, spider):
        self.result.append(('Статус', 'Количество'))
        for status, count in self.count_status.items():
            self.result.append(
                (status, count)
            )

        self.result.append(
            ('Total', self.total)
        )

        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)

        with open(
            BASE_DIR / 'results' / f'status_summary_{now_formatted}.csv',
            'w',
            encoding='utf-8'
        ) as f:
            write = csv.writer(f, dialect='unix')
            write.writerows(self.result)
