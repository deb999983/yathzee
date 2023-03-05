from functools import cached_property
from display.dice import Dice


class Table:
    def __init__(self, headers: list, data: list, name: str="") -> None:
        self.COLUMNS = len(headers)
        self.ROWS = 1 + len(data)

        self.name = name
        self.header = headers
        self.body = data

        all_data = [headers, *data]
        columns = []
        for c in range(self.COLUMNS):
            column = []
            for r in range(self.ROWS):
                column.append(all_data[r][c])
            columns.append(column)

        self.columnWidths = [(max(map(lambda s: len(s), column)) + 2) for column in columns]
        self.columnWidths.append(0) # Appending a zero column length for adding the last separators
      
    def get_header(self):
        header_row = [*self.header, '']
        table_header_row = []
        for l in range(3):  # Assumes no y padding
            row_part = ''
            for index, column in enumerate(header_row):
                colWidth = self.columnWidths[index]
                if l == 0:
                    row_part += '+' + ''.join('-' * (colWidth))
                if l == 1:
                    row_part += '|' + column.center(colWidth)
                if l == 2:
                    row_part += '+' + ''.join('-' * (colWidth))
            table_header_row.append(row_part)
        return table_header_row

    def get_table_row(self, row):
        row = [*row, '']
        table_row = []
        for r in range(2):
            row_part = ''
            for index, column in enumerate(row):
                colWidth = self.columnWidths[index]
                if r == 0:
                    row_part += '|' + column.center(colWidth)
                if r == 1:
                    row_part += '+' + ''.join('-' * (colWidth))
            table_row.append(row_part)
        return table_row

    def get_body(self):
        table_body = []
        for row in self.body:
            table_row = self.get_table_row(row)
            table_body.extend(table_row)
        return table_body

    @cached_property
    def data(self):
        return [
            *self.get_header(),
            *self.get_body()            
        ]


class Display:
    def __init__(self, *tables: list[Table]):
        self.tables = tables
        self.separator = '        '

        self.max_rows = max(map(lambda t: len(t.data), self.tables))
        self.py = 0
        self.px = 10
        self.width = sum(map(lambda t: max(len(t.name), len(t.data[0])), self.tables)) + self.px + len(self.separator) * (len(self.tables) - 1)
        self._display()
    
    def _apply_y_padding(self, rows):
        rows = [
            "─" * self.width,
            " " * self.width,
            *rows,
            " " * self.width,
            "─" * self.width
        ]
        return rows
    
    def _apply_x_padding(self, rows):
        padded_rows = []
        for row in rows[1:-1]:
            r = ["|", *row[1:-1], "|"]
            padded_rows.append("".join(r))
        return [rows[0], *padded_rows, rows[-1]]

    def _get_rows(self):
        max_rows = self.max_rows
        rows = []
        header_row = []
        for i in range(len(self.tables)):
            data = self.tables[i].data
            rowWidth = max(len(self.tables[i].name), len(data[0]))
            header_row.append(self.tables[i].name.center(rowWidth))
        rows.append(self.separator.join(header_row).center(self.width))
        
        for r in range(max_rows):
            row = []
            for table in self.tables:
                t = table.data
                rowWidth = len(t[0])
                try:
                    row.append(t[r])
                except IndexError as e:
                    row.append(" "*rowWidth)
            rows.append(self.separator.join(row).center(self.width))
        return rows

    def _display(self):
        rows = self._get_rows()
        rows = self._apply_y_padding(rows)
        rows = self._apply_x_padding(rows)


        print("\n".join(rows))


def run():
    t1 = Table(
        headers=["S-No", "Title", "Value"],
        data=[
            ["1", "Only Ones", ""],
            ["2", "Only Threes", ""],
            ["3", "Only Fours", "20"],

            ["4", "Only Ones", "30"],
            ["5", "Only Threes", ""],
            ["6", "Only Fours", "24"],
        ],
        name="Player-1"
    )
    t2 = Table(
        headers=["S-No", "Title", "Value"],
        data=[
            ["1", "Only Ones", ""],
            ["2", "Only Threes", ""],
        ],
        name="Player-2"
    )  
    tg = Display(t1, t2, t1, t2)
    tg

    d1 = Dice([2,5,1,1], name="Select to Keep")
    d2 = Dice([5], name="You have Selected")
    d3 = Dice([3,6,6], name="New Rolls")

    tg = Display(d1)
    tg

    tg = Display(d2, d3)
    tg

# run()