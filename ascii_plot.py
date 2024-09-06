def ascii_table(row_names: list, column_names: list, per_row_values: list, width_of_screen: int) -> str:
    assert len(per_row_values) == len(row_names)
    assert len(row_names) > 0
    assert len(column_names) > 0
    assert all([len(row) == len(column_names) for row in per_row_values])
    row_cnt = len(row_names)
    column_cnt = len(column_names)
    retval = ''
    # Get max of width inside.
    # Every column should have a max width.
    # len(column_names) + 1 columns in total.
    max_width = max(
        max([len(str(x)) for x in row_names]), max(
        [max(len(str(column_names[i])), max([len(str(x[i])) for x in per_row_values])) for i in range(column_cnt)]
        )
    )
    assert max_width > 0
    # Then align to a number that fits into screen.
    # Note that it can shrink.
    max_width = min(max_width, width_of_screen // (column_cnt + 1))
    def divide_line(column_number: int, max_width: int) -> str:
        assert column_number > 0
        line_str = '+'
        line_str += '+'.join(['-' * max_width for _ in range(column_number)])
        line_str += '+\n'
        return line_str
    def content_line(row_name: str, row_values: list, max_width: int) -> str:
        assert len(row_values) == column_cnt
        # Check how wide it is first.
        c_max_len = max(len(row_name), max([len(str(x)) for x in row_values]), max_width)
        rows_of_this_line = (c_max_len + max_width - 1) // max_width
        remaining_index_start = [0 for _ in range(column_cnt + 1)]
        cline_retval = ''
        def handle_one_block(full_str: str, index_list: list, index_in_list: int, the_width: int) -> str:
            # content + '|'
            remaining_length = len(full_str) - index_list[index_in_list]
            assert remaining_length >= 0
            put_length = min(remaining_length, the_width)
            retval = full_str[index_list[index_in_list]: index_list[index_in_list] + put_length]
            index_list[index_in_list] += put_length
            return retval + ' ' * (the_width - put_length) + '|'
        for _ in range(rows_of_this_line):
            cline_retval += '|'
            for j in range(column_cnt + 1):
                if j == 0:
                    cline_retval += handle_one_block(row_name, remaining_index_start, 0, max_width)
                else:
                    cline_retval += handle_one_block(str(row_values[j - 1]), remaining_index_start, j, max_width)
            cline_retval += '\n'
        return cline_retval

    # Print row by row, but remember that some rows can be multiple rows due to limited screen width.
    retval += divide_line(column_cnt + 1, max_width)
    retval += content_line('', column_names, max_width)
    retval += divide_line(column_cnt + 1, max_width)
    for i in range(row_cnt):
        retval += content_line(row_names[i], per_row_values[i], max_width)
        retval += divide_line(column_cnt + 1, max_width)
    return retval





if __name__ == '__main__':
    column_names = ['reuse_ratio', 'unique_prefix_token_length', 'copy_pattern', 'cache-hierarchy']
    row_names = ['default', 'trace_cache_size', 'sharing_ratio', 'copy_patterns', 'cache-hierarchies']
    per_row_values = [['70%', '30,000', 'uniform', 'gpu+cpu+disk'],
                      ['70%', 'from 3,000 to 300,000', 'uniform', 'gpu+cpu+disk'],
                      ['from 60% to 90%', '30,000', 'uniform', 'gpu+cpu+disk'],
                      ['70%', '30,000', 'lastest_more_popular vary how skew', 'gpu+cpu+disk'],
                      ['70%', '30,000', 'uniform', 'gpu->+cpu->+disk']]
    width_of_screen = 180
    print(ascii_table(row_names, column_names, per_row_values, width_of_screen))

