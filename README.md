# dataframe

This is a lightweight dataframe implementation intended to be used in the Python interpreter.

It exports to and reads from CSV files very easily allowing you to quickly start a Python interpreter session and manipulate your data.

You can access entire columns of the data frame using the syntax `df["name"]` or alternatively an entire row (counting from 0) using the syntax `df[0]`

This implementation uses lists rather than arrays. This was a design consideration at first, but ultimately lists are used so that rows can immediately be assigned to the results of list comprehensions when using the Python interpreter. This also allows for the usage of list methods on the rows of the dataframe.

To create a dataframe from a CSV file, use the syntax `df = Dataframe.load("file.csv")`. Alternatively, you can also use the syntax `df = Dataframe.read_from_csv("file.csv")` as they are the same.

To a dataframe to a file, use the syntax `df.save("file.csv")` or just `df.save()` if the dataframe already has a file associated with it (it will automatically have a file associated with it if you create the dataframe from a CSV using the `Dataframe.load("file.csv")` syntax or the `Dataframe.read_from_csv("file.csv")` syntax). You can also use the `export_to_csv()` method instead of the `save()` method (they are the same)
