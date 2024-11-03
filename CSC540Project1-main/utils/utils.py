def print_list_as_table(headings, rows):
    # Calculate the width for each column based on the longest item in each column
    col_widths = [max(len(str(item)) for item in column) for column in zip(headings, *rows)]
    
    # Create a horizontal separator line based on the column widths
    separator = "+".join("-" * (width + 2) for width in col_widths)
    
    # Print the header row
    header = " | ".join(f"{heading.ljust(width)}" for heading, width in zip(headings, col_widths))
    print(separator)
    print(f"| {header} |")
    print(separator)
    
    # Print each row
    for row in rows:
        formatted_row = " | ".join(f"{str(item).ljust(width)}" for item, width in zip(row, col_widths))
        print(f"| {formatted_row} |")
    
    # Print the closing separator
    print(separator)

# Example usage:
headings = ["Name", "Age", "Country"]
rows = [
    ["Alice", 30, "United States"],
    ["Bob", 22, "Canada"],
    ["Charlie", 35, "United Kingdom"]
]

print_list_as_table(headings, rows)
