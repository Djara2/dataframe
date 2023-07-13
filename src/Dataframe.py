class Dataframe:
    def __init__(self, headers: list = [], rows: list = []):
        """
        creates a dataframe that is managed by with 2 lists: a list of headers (fields) and a list of lists (rows)

        keyword arguments
        -----------------
        headers | a list of strings where each string is a field in the dataframe
        row     | a list of lists where the outer list is all the rows, and all 
                | inner lists are the values
        """
        self.headers = headers
        self.rows = rows
        self.filename = None

    def __getitem__(self, header) -> list:
        # case: getting an entire column by providing field name
        if type(header) == str:
            if not header in self.headers:
                raise KeyError(f"{header} is not a field in the dataframe.")
            
            field_index = self.headers.index(header)
            column = [self.rows[x][field_index] for x in range(0, len(self.rows))]
            return(column)
        
        # case: getting an entire row by providing row number (starts at 0)
        elif type(header) == int:
            if header >= len(self.rows):
                raise IndexError(f"{header} is out of bounds for the rows of the dataframe; there are only {len(self.rows)} rows.")
            
            row = self.rows[header]
            return(row)

    def set_column(self, header: str, values: list) -> None:
        if not header in self.headers:
            print(f"Operation failed: {header} is not a field in the dataframe.")
            return
        
        values_length = len(self.rows)
        headers_length = len(self.headers)

        # if the provided column does not meet length of existing column,
        # then have all subsequent missing values be set to None
        if values_length < headers_length:
            values += (["NA"] * (headers_length - values_length))

        field_index = self.headers.index(header)
        for x in range(0, len(self.rows)):
            self.rows[x][field_index] = values[x]

    def set_row(self, row: int, values: list) -> None:
        if row < 0:
            print("Operation failed: row number must be positive")
            return
        
        required_length = len(self.rows[0])
        provided_length = len(values)
        number_of_rows = len(self.rows)

        if row >= number_of_rows:
            print(f"Operation failed: row number ({row}) exceeds total existing number of rows ({number_of_rows} [0 - {number_of_rows - 1}])")
            return

        if provided_length > required_length:
            values = values[0 : required_length]
            print(f"Provided row truncated to first {required_length} values, because original length was too long ({provided_length} values)")

        if provided_length < required_length:
            values += (["NA"] * (required_length - provided_length))

        self.rows[row] = values

    def fill_empty(row: list, required_length: int) -> list:
        provided_length = len(row)
        difference = required_length - provided_length
        new_row = row + (["NA"] * difference)
        return(new_row)

    def add_row(self, values: list) -> None:
        provided_length = len(values)
        required_length = len(self.headers)

        if provided_length > required_length:
            values = values[:required_length]
            print("Truncated row because it contained too many values.")

        if provided_length < required_length:
            values = Dataframe.fill_empty(values, provided_length)

        self.rows.append(values)

    def add_column(self, name: str) -> None:
        if name in self.headers:
            return

        # add to headers
        self.headers.append(name)

        # account for length disparity in rows
        for x in range(len(self.rows)):
            self.rows[x].append("NA")

    def __add__(self, value: list):
        if type(value) != list:
            value = [value]
        self.add_row(value)
        return(self)

    def __len__(self) -> int:
        return(len(self.rows))

    # helper function
    def __contains_any(row: list, values: list) -> bool:
        for value in values:
            if value in row:
                return(True)

        return(False)

    # returns dataframe
    def contains_any(self, values):
        new_rows = []
        for x in range(len(self)):
            if Dataframe.__contains_any(self[x], values):
                new_rows.append(self[x])

        new_dataframe = Dataframe(self.headers, new_rows)
        return(new_dataframe)
    
    # helper function
    def __contains_all(row: list, values: list) -> bool:
        for value in values:
            if not value in row:
                return(False)

        return(True)

    # returns dataframe
    def contains_all(self, values: list):
        new_rows = []
        for x in range(len(self)):
            if(Dataframe.__contains_all(self[x], values)):
               new_rows.append(self[x])
        
        new_dataframe = Dataframe(self.headers, new_rows)
        return(new_dataframe)

    # returns dataframe
    def query(self, query_type: str, query_restraints: str, values: list):
        # makes it so you don't have to encase a single value in a list 
        if type(values) == str:
            values = [values]

        if query_type == "contains":
            if query_restraints == "any":
                result = self.contains_any(values)
            elif query_restraints == "all":
                result = self.contains_all(values)
            else:
                print("Returning none on query operation, because query restraints are undefined.")
                result = None 
            
        return(result)
    
    def export_to_csv(self, filename: str) -> None:
        representation = ",".join(self.headers)
        representation += "\n"
        for row in self.rows:
            flattened = ",".join([str(item) for item in row])
            representation += f"{flattened}\n"
        representation = representation[:len(representation)-1]
        file_handle = open(filename, "w")
        file_handle.write(representation)
        file_handle.close()

    def save(self, filename = None) -> None:
        if filename == None:
            filename = self.filename

        if filename == None:    
            print("Could not save because no file name is associated with this dataframe.")
            return
        
        self.export_to_csv(filename)

    def read_from_csv(filename: str):
        file_handle = open(filename, "r")
        contents = [line.replace("\n", "") for line in file_handle.readlines()]
        file_handle.close()
        headers = contents[0].split(",")
        values = contents[1:]
        for x in range(0, len(values)):
            values[x] = values[x].split(",")
        dataframe = Dataframe(headers, values)
        dataframe.filename = filename
        return(dataframe)
    
    def load(filename: str):
        return(Dataframe.read_from_csv(filename))

    def __get_column_width(self, column: str) -> int:
        column = [column] + [item for item in self[column]]
        lengths = [len(str(item)) for item in column]
        return(max(lengths))

    def __str__(self) -> str:
        """
        ┏
        ━
        ━━━━━
        ━
        ┳
        ━━━━━━┳━━━━
        ━
        ┓

        ┃ table ┃ name ┃ age ┃
        ┡━━━━━━━╇━━━━━━╇━━━━━┩
        │ │ │     │
        │ │ │     │
        └───────┴──────┴─────┘
        """
        widths = [self.__get_column_width(column) for column in self.headers]
        print(widths)
        MIDDLE_LIMIT = len(widths) - 1
        top_left = "┏" + ("━" * (widths[0] + 2))
        top_middle = ""
        for x in range(1, MIDDLE_LIMIT):
            top_middle += ("┳" + ("━" * (widths[x] + 2)) + "┳")
        top_right = "━" * (widths[MIDDLE_LIMIT] + 2) + "┓\n"
        
        headers = "┃" + "┃".join([f" {item} " for item in self.headers]) + "┃\n"
        header_bottom = "┡" + ("━" * (len(headers) - 3)) + "┩\n"
        representation = f"{top_left}{top_middle}{top_right}{headers}{header_bottom}"
        return(representation)
